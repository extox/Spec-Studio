"""Recent activity feed aggregated from project files, chat messages, and members."""

from datetime import timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, union_all, literal, func


def _utc_iso(dt) -> str:
    """Convert naive datetime (assumed UTC from SQLite) to UTC ISO string."""
    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.project_file import ProjectFile
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.file_version import FileVersion
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/recent")
async def get_recent_activities(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, le=50),
):
    """Get recent activities across all projects the user is a member of."""

    # Get user's project IDs
    member_result = await db.execute(
        select(ProjectMember.project_id).where(ProjectMember.user_id == user.id)
    )
    project_ids = [row[0] for row in member_result.all()]

    if not project_ids:
        return []

    # Preload project names
    proj_result = await db.execute(
        select(Project.id, Project.name).where(Project.id.in_(project_ids))
    )
    project_names = {row[0]: row[1] for row in proj_result.all()}

    # Preload user names
    user_result = await db.execute(select(User.id, User.display_name))
    user_names = {row[0]: row[1] for row in user_result.all()}

    activities = []

    # 1. File versions (artifact created/updated)
    fv_result = await db.execute(
        select(FileVersion, ProjectFile.project_id, ProjectFile.file_name, ProjectFile.file_path)
        .join(ProjectFile, ProjectFile.id == FileVersion.file_id)
        .where(ProjectFile.project_id.in_(project_ids))
        .order_by(FileVersion.created_at.desc())
        .limit(limit)
    )
    for row in fv_result.all():
        fv, proj_id, file_name, file_path = row
        # Check if this is the first version (created) or subsequent (updated)
        count_result = await db.execute(
            select(func.count(FileVersion.id))
            .where(FileVersion.file_id == fv.file_id, FileVersion.id <= fv.id)
        )
        version_count = count_result.scalar() or 1
        action = "artifact_created" if version_count == 1 else "artifact_updated"

        activities.append({
            "type": action,
            "project_id": proj_id,
            "project_name": project_names.get(proj_id, ""),
            "user_name": user_names.get(fv.updated_by, ""),
            "detail": file_name,
            "detail_path": file_path,
            "timestamp": _utc_iso(fv.created_at),
        })

    # 2. Chat messages (recent chat activity — group by session, last message)
    # Get latest message per session
    session_result = await db.execute(
        select(
            ChatSession.id,
            ChatSession.project_id,
            ChatSession.title,
            ChatSession.persona,
            func.max(ChatMessage.created_at).label("last_msg_at"),
        )
        .join(ChatMessage, ChatMessage.session_id == ChatSession.id)
        .where(ChatSession.project_id.in_(project_ids))
        .group_by(ChatSession.id)
        .order_by(func.max(ChatMessage.created_at).desc())
        .limit(limit)
    )
    for row in session_result.all():
        sess_id, proj_id, title, persona, last_at = row
        # Get the last message author
        last_msg_result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == sess_id, ChatMessage.role == "user")
            .order_by(ChatMessage.created_at.desc())
            .limit(1)
        )
        last_msg = last_msg_result.scalar_one_or_none()
        msg_user = ""
        if last_msg and last_msg.metadata_json:
            import json
            try:
                meta = json.loads(last_msg.metadata_json)
                msg_user = meta.get("display_name", "")
            except Exception:
                pass

        activities.append({
            "type": "chat_activity",
            "project_id": proj_id,
            "project_name": project_names.get(proj_id, ""),
            "user_name": msg_user,
            "detail": title or f"Chat with {persona}",
            "detail_path": f"/projects/{proj_id}/chat/{sess_id}",
            "timestamp": _utc_iso(last_at),
        })

    # 3. Members added
    member_activity_result = await db.execute(
        select(ProjectMember, User.display_name)
        .join(User, User.id == ProjectMember.user_id)
        .where(ProjectMember.project_id.in_(project_ids))
        .order_by(ProjectMember.invited_at.desc())
        .limit(limit)
    )
    for row in member_activity_result.all():
        pm, display_name = row
        activities.append({
            "type": "member_added",
            "project_id": pm.project_id,
            "project_name": project_names.get(pm.project_id, ""),
            "user_name": display_name,
            "detail": display_name,
            "detail_path": "",
            "timestamp": _utc_iso(pm.invited_at),
        })

    # 4. Project created
    for proj_id in project_ids:
        proj_result2 = await db.execute(
            select(Project, User.display_name)
            .outerjoin(User, User.id == Project.created_by)
            .where(Project.id == proj_id)
        )
        row = proj_result2.one_or_none()
        if row:
            proj, creator_name = row
            activities.append({
                "type": "project_created",
                "project_id": proj.id,
                "project_name": proj.name,
                "user_name": creator_name or "",
                "detail": proj.name,
                "detail_path": f"/projects/{proj.id}",
                "timestamp": _utc_iso(proj.created_at),
            })

    # 5. Activity logs (project updates, phase changes, deletions, etc.)
    from app.models.activity_log import ActivityLog
    log_result = await db.execute(
        select(ActivityLog, User.display_name)
        .outerjoin(User, User.id == ActivityLog.user_id)
        .where(ActivityLog.project_id.in_(project_ids))
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
    )
    for row in log_result.all():
        log, user_name = row
        activities.append({
            "type": log.action,
            "project_id": log.project_id,
            "project_name": project_names.get(log.project_id, ""),
            "user_name": user_name or "",
            "detail": log.detail or "",
            "detail_path": f"/projects/{log.project_id}/settings" if log.action in ("project_updated", "phase_changed") else f"/projects/{log.project_id}",
            "timestamp": _utc_iso(log.created_at),
        })

    # Sort all by timestamp descending
    activities.sort(key=lambda a: a["timestamp"], reverse=True)

    return activities[:limit]
