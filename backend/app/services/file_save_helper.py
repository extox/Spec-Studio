"""Unified helper for saving/updating project files from chat.

All chat-originated file saves go through this helper to ensure:
- Version history is created
- updated_by is tracked
- Consistent broadcast of deliverable_created events
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.project_file import ProjectFile
from app.services.file_service import create_file, update_file
from app.services.websocket_service import manager


async def save_or_update_file(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    file_path: str,
    file_name: str,
    content: str,
    session_id: int | None = None,
    broadcast_session_id: int | None = None,
) -> ProjectFile:
    """Create or update a file, with version tracking.

    Returns the saved ProjectFile.
    """
    # Check if file exists
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.file_path == file_path,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        saved = await update_file(
            db, project_id, existing.id,
            user_id=user_id,
            content=content,
        )
        if session_id:
            saved.session_id = session_id
            await db.flush()
            await db.refresh(saved)
    else:
        saved = await create_file(
            db, project_id, user_id,
            file_path, file_name,
            file_type="deliverable",
            content=content,
            session_id=session_id,
        )

    await db.commit()

    # Broadcast event
    if broadcast_session_id:
        await manager.broadcast_all(broadcast_session_id, {
            "type": "deliverable_created",
            "file": {
                "id": saved.id,
                "file_path": saved.file_path,
                "file_name": saved.file_name,
            },
        })

    # Fire-and-forget traceability rebuild for this file. Uses its own DB session
    # so it cannot interfere with the request lifecycle. Failures are swallowed —
    # traceability is auxiliary, never blocks a save.
    try:
        import asyncio
        from app.api.traceability import background_rebuild_after_save
        asyncio.create_task(
            background_rebuild_after_save(saved.project_id, saved.id)
        )
    except Exception:
        pass

    # Fire-and-forget bolt-activity capture: if a Bolt is currently `in_bolt`
    # for this project, append a `file_saved` activity to it.
    try:
        import asyncio
        from app.database import async_session
        from app.services.bolt_service import get_active_bolt_for_project, log_activity

        async def _capture():
            async with async_session() as bdb:
                try:
                    active = await get_active_bolt_for_project(bdb, saved.project_id)
                    if active:
                        await log_activity(
                            bdb, active.id, "file_saved",
                            {"file_id": saved.id, "file_path": saved.file_path},
                            user_id,
                        )
                        await bdb.commit()
                except Exception:
                    await bdb.rollback()

        asyncio.create_task(_capture())
    except Exception:
        pass

    # Fire-and-forget validation re-run (rule-based only, no LLM rules).
    try:
        import asyncio
        from app.services.validation_service import background_run_after_save
        asyncio.create_task(
            background_run_after_save(saved.project_id, saved.id)
        )
    except Exception:
        pass

    return saved
