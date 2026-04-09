"""Admin back office API endpoints."""

from datetime import timezone as tz
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.login_history import LoginHistory
from app.models.llm_config import LLMConfig
from app.core.dependencies import require_admin
from app.core.security import hash_password, decrypt_api_key

router = APIRouter()


# --- Login History ---
@router.get("/login-history")
async def list_login_history(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, le=100),
):
    count_result = await db.execute(select(func.count(LoginHistory.id)))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(LoginHistory, User.email, User.display_name)
        .outerjoin(User, User.id == LoginHistory.user_id)
        .order_by(LoginHistory.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    items = []
    for row in result.all():
        h, email, name = row
        items.append({
            "id": h.id,
            "user_id": h.user_id,
            "email": email or "",
            "display_name": name or "",
            "ip_address": h.ip_address or "",
            "user_agent": h.user_agent or "",
            "created_at": h.created_at.replace(tzinfo=tz.utc).isoformat() if h.created_at else "",
        })

    return {"items": items, "total": total, "page": page, "per_page": per_page}


@router.get("/login-stats")
async def login_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    days: int = Query(default=14, le=90),
):
    """Login statistics for chart: daily login counts for last N days."""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)

    result = await db.execute(
        select(
            func.date(LoginHistory.created_at).label("day"),
            func.count(LoginHistory.id).label("count"),
        )
        .where(LoginHistory.created_at >= start)
        .group_by(func.date(LoginHistory.created_at))
        .order_by(func.date(LoginHistory.created_at))
    )

    stats = {}
    for row in result.all():
        stats[str(row[0])] = row[1]

    # Fill missing days with 0
    chart_data = []
    for i in range(days):
        day = (start + timedelta(days=i + 1)).strftime("%Y-%m-%d")
        chart_data.append({"date": day, "count": stats.get(day, 0)})

    # Total and unique users
    total_result = await db.execute(
        select(func.count(LoginHistory.id)).where(LoginHistory.created_at >= start)
    )
    unique_result = await db.execute(
        select(func.count(func.distinct(LoginHistory.user_id))).where(LoginHistory.created_at >= start)
    )

    return {
        "chart": chart_data,
        "total_logins": total_result.scalar() or 0,
        "unique_users": unique_result.scalar() or 0,
        "days": days,
    }


# --- User Management ---
@router.get("/users")
async def list_users(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    search: str = Query(default=""),
):
    query = select(User).order_by(User.created_at.desc())
    if search:
        query = query.where(
            User.email.ilike(f"%{search}%") | User.display_name.ilike(f"%{search}%")
        )
    result = await db.execute(query)
    users = []
    for u in result.scalars().all():
        users.append({
            "id": u.id,
            "email": u.email,
            "display_name": u.display_name,
            "is_admin": u.is_admin,
            "created_at": u.created_at.replace(tzinfo=tz.utc).isoformat() if u.created_at else "",
        })
    return users


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("User not found")

    if "display_name" in req and req["display_name"]:
        user.display_name = req["display_name"]
    if "is_admin" in req:
        user.is_admin = bool(req["is_admin"])
    if "password" in req and req["password"]:
        user.hashed_password = hash_password(req["password"])
    await db.flush()
    return {"ok": True}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    if user_id == admin.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("User not found")
    await db.delete(user)
    await db.flush()
    return {"ok": True}


# --- Project Management ---
@router.get("/projects")
async def list_all_projects(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project, User.display_name, func.count(ProjectMember.id))
        .outerjoin(User, User.id == Project.created_by)
        .outerjoin(ProjectMember, ProjectMember.project_id == Project.id)
        .group_by(Project.id, User.display_name)
        .order_by(Project.updated_at.desc())
    )
    projects = []
    for row in result.all():
        p, owner, mc = row
        projects.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "phase": p.phase,
            "owner_name": owner or "",
            "member_count": mc or 0,
            "created_at": p.created_at.replace(tzinfo=tz.utc).isoformat() if p.created_at else "",
            "updated_at": p.updated_at.replace(tzinfo=tz.utc).isoformat() if p.updated_at else "",
        })
    return projects


@router.delete("/projects/{project_id}")
async def delete_project_admin(
    project_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Project not found")
    await db.delete(project)
    await db.flush()
    return {"ok": True}


@router.put("/projects/{project_id}/phase")
async def update_project_phase(
    project_id: int,
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Project not found")
    phase = req.get("phase", "")
    valid = ["analysis", "planning", "solutioning", "implementation"]
    if phase not in valid:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid phase. Must be one of: {valid}")
    project.phase = phase
    await db.flush()
    return {"ok": True}


@router.get("/projects/{project_id}/members")
async def list_project_members(
    project_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProjectMember, User.display_name, User.email)
        .join(User, User.id == ProjectMember.user_id)
        .where(ProjectMember.project_id == project_id)
        .order_by(ProjectMember.invited_at)
    )
    members = []
    for row in result.all():
        pm, name, email = row
        members.append({
            "id": pm.id,
            "user_id": pm.user_id,
            "display_name": name or "",
            "email": email or "",
            "role": pm.role,
            "invited_at": pm.invited_at.replace(tzinfo=tz.utc).isoformat() if pm.invited_at else "",
        })
    return members


@router.post("/projects/{project_id}/members")
async def add_project_member(
    project_id: int,
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    email = req.get("email", "").strip()
    role = req.get("role", "member")
    if not email:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email required")

    user_result = await db.execute(select(User).where(User.email == email))
    user = user_result.scalar_one_or_none()
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("User not found")

    existing = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id,
        )
    )
    if existing.scalar_one_or_none():
        from app.core.exceptions import ConflictError
        raise ConflictError("Already a member")

    member = ProjectMember(project_id=project_id, user_id=user.id, role=role)
    db.add(member)
    await db.flush()
    return {"ok": True}


@router.put("/projects/{project_id}/members/{member_id}")
async def update_member_role(
    project_id: int,
    member_id: int,
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ProjectMember).where(ProjectMember.id == member_id))
    pm = result.scalar_one_or_none()
    if not pm:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Member not found")
    pm.role = req.get("role", pm.role)
    await db.flush()
    return {"ok": True}


@router.delete("/projects/{project_id}/members/{member_id}")
async def remove_project_member(
    project_id: int,
    member_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ProjectMember).where(ProjectMember.id == member_id))
    pm = result.scalar_one_or_none()
    if not pm:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Member not found")
    await db.delete(pm)
    await db.flush()
    return {"ok": True}


# --- LLM Config Management ---
@router.get("/llm-configs")
async def list_llm_configs(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LLMConfig, User.display_name, User.email)
        .outerjoin(User, User.id == LLMConfig.user_id)
        .order_by(LLMConfig.created_at.desc())
    )
    configs = []
    for row in result.all():
        c, name, email = row
        configs.append({
            "id": c.id,
            "user_id": c.user_id,
            "user_name": name or "",
            "user_email": email or "",
            "provider": c.provider,
            "model": c.model,
            "base_url": c.base_url,
            "is_default": c.is_default,
            "created_at": c.created_at.replace(tzinfo=tz.utc).isoformat() if c.created_at else "",
        })
    return configs


@router.delete("/llm-configs/{config_id}")
async def delete_llm_config(
    config_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(LLMConfig).where(LLMConfig.id == config_id))
    config = result.scalar_one_or_none()
    if not config:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("LLM config not found")
    await db.delete(config)
    await db.flush()
    return {"ok": True}


# --- AI Translation ---
@router.post("/translate")
async def translate_content(
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Translate Korean content to English using admin's LLM."""
    content = req.get("content", "")
    if not content:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Content required")

    # Get admin's default LLM config
    llm_config = await db.execute(
        select(LLMConfig).where(
            LLMConfig.user_id == admin.id,
            LLMConfig.is_default == True,
        ).limit(1)
    )
    config = llm_config.scalar_one_or_none()
    if not config:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No default LLM configuration. Please configure one in Settings.")

    try:
        api_key = decrypt_api_key(config.api_key_encrypted)
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to decrypt API key")

    from app.llm.provider import stream_chat

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional translator. Translate the following Korean Markdown content to English. "
                "Preserve ALL Markdown formatting exactly (headings, tables, lists, bold, links, images, code blocks). "
                "Do NOT add, remove, or modify any structural elements. "
                "Only translate the text content. Output ONLY the translated Markdown, no explanations."
            ),
        },
        {"role": "user", "content": content},
    ]

    result = ""
    async for chunk in stream_chat(
        provider=config.provider,
        model=config.model,
        api_key=api_key,
        messages=messages,
        base_url=config.base_url,
    ):
        result += chunk

    return {"translated": result}


@router.post("/translate-short")
async def translate_short(
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Translate short Korean text (title, group name) to English."""
    text = req.get("text", "").strip()
    if not text:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Text required")

    llm_config = await db.execute(
        select(LLMConfig).where(LLMConfig.user_id == admin.id, LLMConfig.is_default == True).limit(1)
    )
    config = llm_config.scalar_one_or_none()
    if not config:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No default LLM configuration")

    try:
        api_key = decrypt_api_key(config.api_key_encrypted)
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to decrypt API key")

    from app.llm.provider import stream_chat

    messages = [
        {"role": "system", "content": "Translate the following Korean text to English. Output ONLY the translated text, nothing else. Keep it concise."},
        {"role": "user", "content": text},
    ]

    result = ""
    async for chunk in stream_chat(
        provider=config.provider, model=config.model,
        api_key=api_key, messages=messages, base_url=config.base_url,
    ):
        result += chunk

    return {"translated": result.strip()}
