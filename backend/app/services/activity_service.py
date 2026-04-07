from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity_log import ActivityLog


async def log_activity(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    action: str,
    detail: str | None = None,
):
    """Record a project activity."""
    log = ActivityLog(
        project_id=project_id,
        user_id=user_id,
        action=action,
        detail=detail,
    )
    db.add(log)
    await db.flush()
    return log
