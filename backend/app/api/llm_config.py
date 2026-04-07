from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.llm_config import LLMConfig
from app.schemas.llm import LLMConfigCreate, LLMConfigUpdate, LLMConfigResponse, LLMProviderInfo
from app.core.dependencies import get_current_user
from app.core.security import encrypt_api_key, decrypt_api_key
from app.core.exceptions import NotFoundError

router = APIRouter()

SUPPORTED_PROVIDERS = [
    LLMProviderInfo(
        id="anthropic",
        name="Anthropic",
        models=["claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251001", "claude-opus-4-6"],
    ),
    LLMProviderInfo(
        id="openai",
        name="OpenAI",
        models=["gpt-4o", "gpt-4o-mini", "o1-preview"],
    ),
    LLMProviderInfo(
        id="google",
        name="Google",
        models=["gemini-2.0-flash", "gemini-2.0-pro"],
    ),
    LLMProviderInfo(
        id="aion-u",
        name="AI:ON-U",
        models=["default"],
        requires_base_url=True,
    ),
]


@router.get("/providers", response_model=list[LLMProviderInfo])
async def list_providers():
    return SUPPORTED_PROVIDERS


@router.get("/configs", response_model=list[LLMConfigResponse])
async def list_configs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LLMConfig).where(LLMConfig.user_id == user.id)
    )
    configs = result.scalars().all()
    responses = []
    for c in configs:
        try:
            decrypted = decrypt_api_key(c.api_key_encrypted)
            hint = f"****{decrypted[-4:]}"
        except Exception:
            hint = "****"
        responses.append(LLMConfigResponse(
            id=c.id,
            provider=c.provider,
            model=c.model,
            base_url=c.base_url,
            is_default=c.is_default,
            created_at=c.created_at,
            api_key_hint=hint,
        ))
    return responses


@router.post("/configs", response_model=LLMConfigResponse)
async def create_config(
    req: LLMConfigCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if req.is_default:
        # Unset other defaults
        result = await db.execute(
            select(LLMConfig).where(LLMConfig.user_id == user.id, LLMConfig.is_default == True)
        )
        for existing in result.scalars().all():
            existing.is_default = False

    config = LLMConfig(
        user_id=user.id,
        provider=req.provider,
        api_key_encrypted=encrypt_api_key(req.api_key),
        model=req.model,
        base_url=req.base_url,
        is_default=req.is_default,
    )
    db.add(config)
    await db.flush()
    return LLMConfigResponse(
        id=config.id,
        provider=config.provider,
        model=config.model,
        base_url=config.base_url,
        is_default=config.is_default,
        created_at=config.created_at,
        api_key_hint=f"****{req.api_key[-4:]}",
    )


@router.put("/configs/{config_id}", response_model=LLMConfigResponse)
async def update_config(
    config_id: int,
    req: LLMConfigUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LLMConfig).where(LLMConfig.id == config_id, LLMConfig.user_id == user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise NotFoundError("LLM config not found")

    if req.provider is not None:
        config.provider = req.provider
    if req.model is not None:
        config.model = req.model
    if req.base_url is not None:
        config.base_url = req.base_url
    if req.api_key is not None:
        config.api_key_encrypted = encrypt_api_key(req.api_key)
    if req.is_default is not None:
        if req.is_default:
            others = await db.execute(
                select(LLMConfig).where(
                    LLMConfig.user_id == user.id,
                    LLMConfig.is_default == True,
                    LLMConfig.id != config_id,
                )
            )
            for other in others.scalars().all():
                other.is_default = False
        config.is_default = req.is_default

    await db.flush()

    try:
        decrypted = decrypt_api_key(config.api_key_encrypted)
        hint = f"****{decrypted[-4:]}"
    except Exception:
        hint = "****"

    return LLMConfigResponse(
        id=config.id,
        provider=config.provider,
        model=config.model,
        base_url=config.base_url,
        is_default=config.is_default,
        created_at=config.created_at,
        api_key_hint=hint,
    )


@router.delete("/configs/{config_id}")
async def delete_config(
    config_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LLMConfig).where(LLMConfig.id == config_id, LLMConfig.user_id == user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise NotFoundError("LLM config not found")
    await db.delete(config)
    await db.flush()
    return {"ok": True}
