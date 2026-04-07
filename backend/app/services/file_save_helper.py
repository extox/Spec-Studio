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

    return saved
