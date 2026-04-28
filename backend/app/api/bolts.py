"""Bolt API — kanban CRUD + lifecycle actions + plan-from-sprint."""

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_project_member
from app.database import get_db
from app.models.bolt import Bolt, BoltActivity
from app.models.user import User
from app.services.bolt_service import (
    approve_bolt,
    block_bolt,
    complete_bolt,
    get_velocity,
    log_activity,
    plan_bolts_from_sprint,
    start_bolt,
    unblock_bolt,
)

router = APIRouter()


def _bolt_to_dict(b: Bolt) -> dict:
    return {
        "id": b.id,
        "project_id": b.project_id,
        "sprint_id": b.sprint_id,
        "bolt_number": b.bolt_number,
        "title": b.title,
        "story_anchor": b.story_anchor,
        "persona_id": b.persona_id,
        "workflow_id": b.workflow_id,
        "status": b.status,
        "started_at": b.started_at,
        "completed_at": b.completed_at,
        "approved_at": b.approved_at,
        "approved_by": b.approved_by,
        "estimated_minutes": b.estimated_minutes,
        "approval_required": b.approval_required,
        "blocker_reason": b.blocker_reason,
        "notes": b.notes,
        "created_at": b.created_at,
        "updated_at": b.updated_at,
    }


# --- Listing -----------------------------------------------------------------

@router.get("")
async def list_bolts(
    project_id: int,
    status: str | None = Query(default=None),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    q = select(Bolt).where(Bolt.project_id == project_id).order_by(Bolt.bolt_number)
    if status:
        q = q.where(Bolt.status == status)
    result = await db.execute(q)
    return [_bolt_to_dict(b) for b in result.scalars().all()]


@router.get("/velocity")
async def velocity(
    project_id: int,
    days: int = Query(default=7, ge=1, le=90),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_velocity(db, project_id, days=days)


# --- Manual create -----------------------------------------------------------

@router.post("")
async def create_bolt(
    project_id: int,
    payload: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    title = (payload.get("title") or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    # Next bolt_number
    from sqlalchemy import func
    max_result = await db.execute(
        select(func.max(Bolt.bolt_number)).where(Bolt.project_id == project_id)
    )
    next_number = (max_result.scalar_one_or_none() or 0) + 1

    bolt = Bolt(
        project_id=project_id,
        sprint_id=payload.get("sprint_id"),
        bolt_number=next_number,
        title=title[:200],
        story_anchor=payload.get("story_anchor"),
        persona_id=payload.get("persona_id") or "developer",
        workflow_id=payload.get("workflow_id"),
        status="todo",
        estimated_minutes=int(payload.get("estimated_minutes", 60)),
        approval_required=bool(payload.get("approval_required", True)),
        created_by=user.id,
    )
    db.add(bolt)
    await db.flush()
    await log_activity(db, bolt.id, "checkpoint", {"event": "manual_create"}, user.id)
    await db.commit()
    return _bolt_to_dict(bolt)


# --- Plan from sprint --------------------------------------------------------

@router.post("/plan-from-sprint")
async def plan_from_sprint(
    project_id: int,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolts = await plan_bolts_from_sprint(db, project_id, user.id)
    await db.commit()
    return {"created": len(bolts), "bolts": [_bolt_to_dict(b) for b in bolts]}


# --- Single-bolt operations --------------------------------------------------

async def _get_or_404(db: AsyncSession, project_id: int, bolt_id: int) -> Bolt:
    result = await db.execute(
        select(Bolt).where(Bolt.id == bolt_id, Bolt.project_id == project_id)
    )
    bolt = result.scalar_one_or_none()
    if not bolt:
        raise HTTPException(status_code=404, detail="Bolt not found")
    return bolt


@router.get("/{bolt_id}")
async def get_bolt(
    project_id: int,
    bolt_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolt = await _get_or_404(db, project_id, bolt_id)
    return _bolt_to_dict(bolt)


@router.get("/{bolt_id}/activities")
async def list_activities(
    project_id: int,
    bolt_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    await _get_or_404(db, project_id, bolt_id)
    result = await db.execute(
        select(BoltActivity).where(BoltActivity.bolt_id == bolt_id)
        .order_by(desc(BoltActivity.created_at))
    )
    return [
        {
            "id": a.id,
            "event_type": a.event_type,
            "payload": json.loads(a.payload) if a.payload else None,
            "actor_user_id": a.actor_user_id,
            "created_at": a.created_at,
        }
        for a in result.scalars().all()
    ]


@router.post("/{bolt_id}/start")
async def start(
    project_id: int,
    bolt_id: int,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolt = await _get_or_404(db, project_id, bolt_id)
    # Enforce single active bolt per project.
    active = await db.execute(
        select(Bolt).where(
            Bolt.project_id == project_id,
            Bolt.status == "in_bolt",
            Bolt.id != bolt_id,
        ).limit(1)
    )
    if active.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Another bolt is already in progress. Complete or block it first.",
        )
    try:
        await start_bolt(db, bolt, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return _bolt_to_dict(bolt)


@router.post("/{bolt_id}/complete")
async def complete(
    project_id: int,
    bolt_id: int,
    payload: dict | None = None,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolt = await _get_or_404(db, project_id, bolt_id)
    notes = (payload or {}).get("notes")
    try:
        await complete_bolt(db, bolt, user.id, notes=notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return _bolt_to_dict(bolt)


@router.post("/{bolt_id}/approve")
async def approve(
    project_id: int,
    bolt_id: int,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolt = await _get_or_404(db, project_id, bolt_id)
    try:
        await approve_bolt(db, bolt, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return _bolt_to_dict(bolt)


@router.post("/{bolt_id}/block")
async def block(
    project_id: int,
    bolt_id: int,
    payload: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    reason = (payload.get("reason") or "").strip()
    if not reason:
        raise HTTPException(status_code=400, detail="reason is required")
    bolt = await _get_or_404(db, project_id, bolt_id)
    try:
        await block_bolt(db, bolt, user.id, reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return _bolt_to_dict(bolt)


@router.post("/{bolt_id}/unblock")
async def unblock(
    project_id: int,
    bolt_id: int,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    bolt = await _get_or_404(db, project_id, bolt_id)
    try:
        await unblock_bolt(db, bolt, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return _bolt_to_dict(bolt)


@router.delete("/{bolt_id}")
async def delete_bolt(
    project_id: int,
    bolt_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    await _get_or_404(db, project_id, bolt_id)
    await db.execute(delete(Bolt).where(Bolt.id == bolt_id))
    await db.commit()
    return {"ok": True}
