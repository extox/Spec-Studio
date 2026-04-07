from datetime import timezone as tz
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, PhaseUpdate
from app.services.project_service import (
    create_project, get_user_projects, get_project,
    update_project, delete_project, update_phase,
)
from app.core.dependencies import get_current_user, get_project_member, require_project_admin
from app.services.activity_service import log_activity
from app.api.members import router as members_router
from app.api.files import router as files_router
from app.api.chat import router as chat_router
from app.api.context import router as context_router

router = APIRouter()
router.include_router(members_router, prefix="/{project_id}/members", tags=["members"])
router.include_router(files_router, prefix="/{project_id}/files", tags=["files"])
router.include_router(chat_router, prefix="/{project_id}/chat", tags=["chat"])
router.include_router(context_router, prefix="/{project_id}/context", tags=["context"])


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_user_projects(db, user.id)


@router.get("/all")
async def list_all_projects(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=12, le=50),
    search: str = Query(default=""),
    sort: str = Query(default="updated_at"),  # name, updated_at, created_at
    order: str = Query(default="desc"),  # asc, desc
    filter: str = Query(default="all"),  # all, member, owned
):
    """List all projects with pagination, search, sorting, and filter."""
    # Base query with owner name
    query = (
        select(
            Project,
            User.display_name.label("owner_name"),
            func.count(ProjectMember.id).label("member_count"),
        )
        .outerjoin(User, User.id == Project.created_by)
        .outerjoin(ProjectMember, ProjectMember.project_id == Project.id)
        .group_by(Project.id, User.display_name)
    )

    # Filter
    if filter == "member":
        member_sq = select(ProjectMember.project_id).where(ProjectMember.user_id == user.id)
        query = query.where(Project.id.in_(member_sq))
    elif filter == "owned":
        query = query.where(Project.created_by == user.id)

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Project.name.ilike(search_term),
                Project.description.ilike(search_term),
                User.display_name.ilike(search_term),
            )
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Sort
    sort_col = getattr(Project, sort, Project.updated_at)
    if order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    # Paginate
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)

    # Check which projects the user is a member of
    my_projects_result = await db.execute(
        select(ProjectMember.project_id).where(ProjectMember.user_id == user.id)
    )
    my_project_ids = set(row[0] for row in my_projects_result.all())

    projects = []
    for row in result.all():
        project = row[0]
        projects.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "phase": project.phase,
            "created_by": project.created_by,
            "created_at": project.created_at.replace(tzinfo=tz.utc).isoformat() if project.created_at else "",
            "updated_at": project.updated_at.replace(tzinfo=tz.utc).isoformat() if project.updated_at else "",
            "owner_name": row[1] or "",
            "member_count": row[2] or 0,
            "is_member": project.id in my_project_ids,
        })

    return {
        "projects": projects,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
    }


@router.post("", response_model=ProjectResponse)
async def create(
    req: ProjectCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await create_project(db, user.id, req.name, req.description)
    await log_activity(db, project.id, user.id, "project_created", req.name)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_project(db, project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update(
    project_id: int,
    req: ProjectUpdate,
    user: User = Depends(get_current_user),
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    changes = []
    if req.name:
        changes.append(f"이름: {req.name}")
    if req.description is not None:
        changes.append("설명 변경")
    result = await update_project(db, project_id, name=req.name, description=req.description)
    if changes:
        await log_activity(db, project_id, user.id, "project_updated", ", ".join(changes))
    return result


@router.delete("/{project_id}")
async def delete(
    project_id: int,
    user: User = Depends(get_current_user),
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    project = await get_project(db, project_id)
    project_name = project.name
    await log_activity(db, project_id, user.id, "project_deleted", project_name)
    await delete_project(db, project_id)
    return {"ok": True}


@router.put("/{project_id}/phase", response_model=ProjectResponse)
async def change_phase(
    project_id: int,
    req: PhaseUpdate,
    user: User = Depends(get_current_user),
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await update_phase(db, project_id, req.phase)
    await log_activity(db, project_id, user.id, "phase_changed", req.phase)
    return result
