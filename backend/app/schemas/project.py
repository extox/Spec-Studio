from datetime import datetime, timezone
from pydantic import BaseModel, model_validator


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class PhaseUpdate(BaseModel):
    phase: str  # analysis/planning/solutioning/implementation


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    phase: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    member_count: int | None = None
    owner_name: str | None = None

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def ensure_utc(self):
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=timezone.utc)
        return self


class MemberCreate(BaseModel):
    email: str
    role: str = "member"


class MemberUpdate(BaseModel):
    role: str


class MemberResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    role: str
    invited_at: datetime
    display_name: str | None = None
    email: str | None = None

    model_config = {"from_attributes": True}
