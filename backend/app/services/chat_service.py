from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.core.exceptions import NotFoundError


async def create_session(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    persona: str,
    workflow: str | None = None,
    title: str | None = None,
) -> ChatSession:
    session = ChatSession(
        project_id=project_id,
        persona=persona,
        workflow=workflow,
        workflow_step=1 if workflow else 0,
        title=title or f"Chat with {persona}",
        created_by=user_id,
    )
    db.add(session)
    await db.flush()
    return session


async def get_sessions(db: AsyncSession, project_id: int) -> list[dict]:
    result = await db.execute(
        select(ChatSession, func.count(ChatMessage.id).label("message_count"))
        .outerjoin(ChatMessage, ChatMessage.session_id == ChatSession.id)
        .where(ChatSession.project_id == project_id)
        .group_by(ChatSession.id)
        .order_by(ChatSession.updated_at.desc())
    )
    sessions = []
    for row in result.all():
        session = row[0]
        session.message_count = row[1]
        sessions.append(session)
    return sessions


async def get_session(db: AsyncSession, session_id: int) -> ChatSession:
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundError("Chat session not found")
    return session


async def get_session_messages(db: AsyncSession, session_id: int) -> list[ChatMessage]:
    """Get all messages for a session (used by LLM context builder)."""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    return list(result.scalars().all())


async def get_session_messages_paginated(
    db: AsyncSession,
    session_id: int,
    limit: int = 5,
    before_id: int | None = None,
) -> tuple[list[ChatMessage], int]:
    """Get messages with cursor-based pagination (newest first).

    Returns (messages_in_chronological_order, total_count).
    """
    # Total count
    count_result = await db.execute(
        select(func.count(ChatMessage.id))
        .where(ChatMessage.session_id == session_id)
    )
    total = count_result.scalar() or 0

    # Query with cursor
    query = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
    )
    if before_id:
        query = query.where(ChatMessage.id < before_id)

    query = query.order_by(ChatMessage.id.desc()).limit(limit)

    result = await db.execute(query)
    messages = list(result.scalars().all())
    messages.reverse()  # Return in chronological order

    return messages, total


async def add_message(
    db: AsyncSession,
    session_id: int,
    role: str,
    content: str,
    metadata_json: str | None = None,
) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata_json=metadata_json,
    )
    db.add(message)
    await db.flush()
    return message


async def delete_session(db: AsyncSession, session_id: int):
    session = await get_session(db, session_id)
    await db.delete(session)
    await db.flush()


async def update_workflow_step(db: AsyncSession, session_id: int, step: int):
    session = await get_session(db, session_id)
    session.workflow_step = step
    await db.flush()
    return session
