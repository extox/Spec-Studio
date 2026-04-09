from datetime import datetime
from pydantic import BaseModel


class LLMConfigCreate(BaseModel):
    provider: str
    api_key: str
    model: str
    base_url: str | None = None
    is_default: bool = False


class LLMConfigUpdate(BaseModel):
    provider: str | None = None
    api_key: str | None = None
    model: str | None = None
    base_url: str | None = None
    is_default: bool | None = None


class LLMConfigResponse(BaseModel):
    id: int
    provider: str
    model: str
    base_url: str | None = None
    is_default: bool
    created_at: datetime
    api_key_hint: str | None = None  # last 4 chars
    api_key_decrypted: str | None = None  # full key for editing

    model_config = {"from_attributes": True}


class LLMProviderInfo(BaseModel):
    id: str
    name: str
    models: list[str]
    requires_base_url: bool = False
