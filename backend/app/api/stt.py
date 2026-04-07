import httpx
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.llm_config import LLMConfig
from app.core.dependencies import get_current_user
from app.core.security import decrypt_api_key

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Convert audio to text using the user's configured LLM provider.

    - AI:ON-U (Dify): Uses Dify audio-to-text API
    - OpenAI: Uses Whisper API
    - Others: Falls back to OpenAI Whisper if available
    """
    result = await db.execute(
        select(LLMConfig).where(
            LLMConfig.user_id == user.id,
            LLMConfig.is_default == True,
        )
    )
    llm_config = result.scalar_one_or_none()
    if not llm_config:
        return {"text": "", "error": "No LLM configuration found."}

    try:
        api_key = decrypt_api_key(llm_config.api_key_encrypted)
    except Exception:
        return {"text": "", "error": "Failed to decrypt API key."}

    audio_data = await file.read()

    if llm_config.provider == "aion-u":
        return await _transcribe_dify(api_key, llm_config.base_url, audio_data, file.filename or "audio.webm")
    elif llm_config.provider == "openai":
        return await _transcribe_openai(api_key, audio_data, file.filename or "audio.webm")
    else:
        return {"text": "", "error": f"STT not supported for provider: {llm_config.provider}"}


async def _transcribe_dify(api_key: str, base_url: str | None, audio_data: bytes, filename: str) -> dict:
    """Use Dify audio-to-text API."""
    if not base_url:
        return {"text": "", "error": "Base URL required for AI:ON-U STT."}

    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1"):
        normalized = normalized[:-3]
    url = f"{normalized}/v1/audio-to-text"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            files = {"file": (filename, audio_data, "audio/webm")}
            data = {"user": "web-bmad-user"}
            headers = {"Authorization": f"Bearer {api_key}"}
            response = await client.post(url, files=files, data=data, headers=headers)
            if response.status_code != 200:
                return {"text": "", "error": f"Dify STT error ({response.status_code}): {response.text}"}
            result = response.json()
            return {"text": result.get("text", "")}
        except Exception as e:
            return {"text": "", "error": f"Dify STT failed: {str(e)}"}


async def _transcribe_openai(api_key: str, audio_data: bytes, filename: str) -> dict:
    """Use OpenAI Whisper API."""
    url = "https://api.openai.com/v1/audio/transcriptions"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            files = {"file": (filename, audio_data, "audio/webm")}
            data = {"model": "whisper-1", "language": "ko"}
            headers = {"Authorization": f"Bearer {api_key}"}
            response = await client.post(url, files=files, data=data, headers=headers)
            if response.status_code != 200:
                return {"text": "", "error": f"OpenAI STT error ({response.status_code}): {response.text}"}
            result = response.json()
            return {"text": result.get("text", "")}
        except Exception as e:
            return {"text": "", "error": f"OpenAI STT failed: {str(e)}"}
