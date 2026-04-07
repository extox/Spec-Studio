from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.core.exceptions import NotFoundError, ConflictError, ForbiddenError


async def create_project(db: AsyncSession, user_id: int, name: str, description: str | None) -> Project:
    project = Project(name=name, description=description, created_by=user_id)
    db.add(project)
    await db.flush()

    member = ProjectMember(project_id=project.id, user_id=user_id, role="owner")
    db.add(member)
    await db.flush()
    return project


async def get_user_projects(db: AsyncSession, user_id: int) -> list[dict]:
    # Subquery: count all members per project
    member_count_sq = (
        select(ProjectMember.project_id, func.count(ProjectMember.id).label("member_count"))
        .group_by(ProjectMember.project_id)
        .subquery()
    )
    # Main query: projects where user is a member, with total member count and owner name
    result = await db.execute(
        select(Project, member_count_sq.c.member_count, User.display_name)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .outerjoin(member_count_sq, member_count_sq.c.project_id == Project.id)
        .outerjoin(User, User.id == Project.created_by)
        .where(ProjectMember.user_id == user_id)
        .group_by(Project.id, member_count_sq.c.member_count, User.display_name)
        .order_by(Project.updated_at.desc())
    )
    projects = []
    for row in result.all():
        project = row[0]
        project.member_count = row[1] or 1
        project.owner_name = row[2] or ""
        projects.append(project)
    return projects


async def get_project(db: AsyncSession, project_id: int) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project not found")
    return project


async def update_project(db: AsyncSession, project_id: int, **kwargs) -> Project:
    project = await get_project(db, project_id)
    for key, value in kwargs.items():
        if value is not None:
            setattr(project, key, value)
    await db.flush()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int):
    project = await get_project(db, project_id)
    await db.delete(project)
    await db.flush()


async def update_phase(db: AsyncSession, project_id: int, phase: str) -> Project:
    valid_phases = ["analysis", "planning", "solutioning", "implementation"]
    if phase not in valid_phases:
        raise ValueError(f"Invalid phase. Must be one of: {valid_phases}")
    return await update_project(db, project_id, phase=phase)


async def get_members(db: AsyncSession, project_id: int) -> list[dict]:
    result = await db.execute(
        select(ProjectMember, User)
        .join(User, User.id == ProjectMember.user_id)
        .where(ProjectMember.project_id == project_id)
    )
    members = []
    for row in result.all():
        member = row[0]
        user = row[1]
        members.append({
            "id": member.id,
            "user_id": member.user_id,
            "project_id": member.project_id,
            "role": member.role,
            "invited_at": member.invited_at,
            "display_name": user.display_name,
            "email": user.email,
        })
    return members


async def add_member(db: AsyncSession, project_id: int, email: str, role: str) -> dict:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User not found with this email")

    existing = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id,
        )
    )
    if existing.scalar_one_or_none():
        raise ConflictError("User is already a member")

    member = ProjectMember(project_id=project_id, user_id=user.id, role=role)
    db.add(member)
    await db.flush()
    return {
        "id": member.id,
        "user_id": user.id,
        "project_id": project_id,
        "role": role,
        "invited_at": member.invited_at,
        "display_name": user.display_name,
        "email": user.email,
    }


async def update_member_role(db: AsyncSession, project_id: int, user_id: int, role: str):
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise NotFoundError("Member not found")
    member.role = role
    await db.flush()


async def remove_member(db: AsyncSession, project_id: int, user_id: int):
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise NotFoundError("Member not found")
    if member.role == "owner":
        raise ForbiddenError("Cannot remove the project owner")
    await db.delete(member)
    await db.flush()
