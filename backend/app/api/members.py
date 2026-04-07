from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.project import MemberCreate, MemberUpdate, MemberResponse
from app.services.project_service import get_members, add_member, update_member_role, remove_member
from app.core.dependencies import get_project_member, require_project_admin

router = APIRouter()


@router.get("", response_model=list[MemberResponse])
async def list_members(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_members(db, project_id)


@router.post("", response_model=MemberResponse)
async def invite_member(
    project_id: int,
    req: MemberCreate,
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    return await add_member(db, project_id, req.email, req.role)


@router.put("/{user_id}")
async def update_role(
    project_id: int,
    user_id: int,
    req: MemberUpdate,
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    await update_member_role(db, project_id, user_id, req.role)
    return {"ok": True}


@router.delete("/{user_id}")
async def remove(
    project_id: int,
    user_id: int,
    member=Depends(require_project_admin),
    db: AsyncSession = Depends(get_db),
):
    await remove_member(db, project_id, user_id)
    return {"ok": True}
