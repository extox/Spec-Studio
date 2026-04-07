from datetime import datetime
from pydantic import BaseModel


class ChatSessionCreate(BaseModel):
    persona: str
    workflow: str | None = None
    title: str | None = None


class ChatSessionResponse(BaseModel):
    id: int
    project_id: int
    persona: str
    workflow: str | None
    workflow_step: int
    title: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    message_count: int | None = None

    model_config = {"from_attributes": True}


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    metadata_json: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionDetail(BaseModel):
    session: ChatSessionResponse
    messages: list[ChatMessageResponse]


class ChatMessagePage(BaseModel):
    messages: list[ChatMessageResponse]
    total: int
    has_more: bool
