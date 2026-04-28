"""Story Execution Board API — kanban over Story files (replaces Bolt feature)."""

import traceback

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_project_member
from app.database import get_db
from app.models.user import User
from app.services.story_board_service import (
    COLUMNS,
    get_board,
    update_story_status,
)
from app.services.story_generator_service import (
    generate_all_missing_stories,
    list_epics_with_story_counts,
)

router = APIRouter()


class StatusUpdate(BaseModel):
    status: str


@router.get("")
async def board(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_project_member),
):
    return await get_board(db, project_id)


@router.get("/statuses")
async def statuses(
    project_id: int,
    _user: User = Depends(get_project_member),
):
    return {"statuses": list(COLUMNS)}


@router.patch("/{story_id}/status")
async def patch_status(
    project_id: int,
    story_id: str,
    payload: StatusUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_project_member),
):
    try:
        return await update_story_status(
            db, project_id, story_id, payload.status, user_id=user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/epics")
async def list_epics(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_project_member),
):
    """Return Epic summary so the UI can offer per-Epic generation."""
    try:
        return await list_epics_with_story_counts(db, project_id)
    except Exception as e:
        traceback.print_exc()
        return {"epics": [], "error": f"server error: {e}"}


@router.post("/generate-all")
async def generate_all(
    project_id: int,
    limit: int = Query(
        3,
        ge=1,
        le=20,
        description="Max stories to generate in this call. The frontend loops "
        "with small batches so a single LLM call cannot exceed common HTTP "
        "proxy timeouts (Next.js dev server, nginx, etc.)",
    ),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_project_member),
):
    """Bulk-generate Story files for every Story in epics.md that lacks one.

    Returns at most `limit` newly created stories per call. The frontend keeps
    re-calling until the response reports nothing left to create.
    """
    try:
        return await generate_all_missing_stories(
            db, project_id, user.id, max_stories=limit
        )
    except Exception as e:
        traceback.print_exc()
        return {
            "created": [],
            "skipped": [],
            "failed": [],
            "error": f"server error: {e}",
        }


@router.post("/generate-epic/{epic_num}")
async def generate_for_epic(
    project_id: int,
    epic_num: int,
    limit: int = Query(3, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_project_member),
):
    """Generate Story files only for the given Epic — useful when full bulk
    generation is too long or rate-limited. Same client-side batching loop
    semantics as `/generate-all`.
    """
    try:
        return await generate_all_missing_stories(
            db, project_id, user.id, epic_num=epic_num, max_stories=limit
        )
    except Exception as e:
        traceback.print_exc()
        return {
            "created": [],
            "skipped": [],
            "failed": [],
            "error": f"server error: {e}",
        }
