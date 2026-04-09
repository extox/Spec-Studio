import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse as FR
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.schemas.chat import ChatSessionCreate, ChatSessionResponse, ChatSessionDetail, ChatMessageResponse, ChatMessagePage
from app.services.chat_service import (
    create_session, get_sessions, get_session, get_session_messages,
    get_session_messages_paginated, delete_session,
)
from app.core.dependencies import get_current_user, get_project_member

router = APIRouter()


@router.get("/sessions", response_model=list[ChatSessionResponse])
async def list_sessions(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_sessions(db, project_id)


@router.post("/sessions", response_model=ChatSessionResponse)
async def create(
    project_id: int,
    req: ChatSessionCreate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await create_session(db, project_id, user.id, req.persona, req.workflow, req.title)


@router.get("/sessions/{session_id}", response_model=ChatSessionDetail)
async def get_detail(
    project_id: int,
    session_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    session = await get_session(db, session_id)
    messages = await get_session_messages(db, session_id)
    return ChatSessionDetail(
        session=ChatSessionResponse.model_validate(session),
        messages=[ChatMessageResponse.model_validate(m) for m in messages],
    )


@router.get("/sessions/{session_id}/messages", response_model=ChatMessagePage)
async def get_messages_paginated(
    project_id: int,
    session_id: int,
    limit: int = 5,
    before_id: int | None = None,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Get messages with cursor-based pagination. Returns newest messages first."""
    messages, total = await get_session_messages_paginated(db, session_id, limit, before_id)
    msg_responses = [ChatMessageResponse.model_validate(m) for m in messages]
    oldest_id = messages[0].id if messages else None
    # has_more = there are messages older than what we returned
    has_more = oldest_id is not None and total > 0 and await _has_older_messages(db, session_id, oldest_id)
    return ChatMessagePage(messages=msg_responses, total=total, has_more=has_more)


async def _has_older_messages(db: AsyncSession, session_id: int, oldest_id: int) -> bool:
    from app.models.chat_message import ChatMessage as CM
    result = await db.execute(
        select(func.count(CM.id)).where(CM.session_id == session_id, CM.id < oldest_id)
    )
    return (result.scalar() or 0) > 0


@router.delete("/sessions/{session_id}")
async def delete(
    project_id: int,
    session_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    await delete_session(db, session_id)
    return {"ok": True}


@router.post("/upload-image")
async def upload_chat_image(
    project_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Upload an image for use in chat messages.

    For AI:ON-U provider, also uploads to the provider's API and returns the file_id.
    """
    from app.config import get_settings
    from app.models.llm_config import LLMConfig
    settings = get_settings()

    ext = os.path.splitext(file.filename or "image.png")[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Unsupported image format")

    content = await file.read()

    # Save locally
    upload_dir = os.path.join(settings.UPLOAD_PATH, "chat-images", str(project_id))
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    local_url = f"/api/projects/{project_id}/chat/images/{filename}"

    # Try uploading to AI:ON-U if that's the user's provider
    provider_file_id = None
    try:
        llm_result = await db.execute(
            select(LLMConfig).where(LLMConfig.user_id == user.id, LLMConfig.is_default == True).limit(1)
        )
        llm_config = llm_result.scalar_one_or_none()
        if llm_config and llm_config.provider == "aion-u" and llm_config.base_url:
            from app.core.security import decrypt_api_key
            from app.llm.provider import upload_file_to_aion_u
            api_key = decrypt_api_key(llm_config.api_key_encrypted)
            result = await upload_file_to_aion_u(
                api_key=api_key,
                base_url=llm_config.base_url,
                file_content=content,
                filename=file.filename or filename,
            )
            provider_file_id = result.get("id")
    except Exception as e:
        # Non-critical: local upload succeeded, provider upload failed
        import traceback
        traceback.print_exc()

    return {
        "url": local_url,
        "filename": filename,
        "provider_file_id": provider_file_id,
    }


@router.get("/images/{filename}")
async def serve_chat_image(project_id: int, filename: str):
    """Serve uploaded chat images."""
    from app.config import get_settings
    settings = get_settings()
    filepath = os.path.join(settings.UPLOAD_PATH, "chat-images", str(project_id), filename)
    if not os.path.exists(filepath):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Image not found")
    return FR(filepath)
