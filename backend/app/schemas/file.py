from datetime import datetime
from pydantic import BaseModel


class FileCreate(BaseModel):
    file_path: str
    file_name: str
    file_type: str = "deliverable"
    content: str | None = None


class FileUpdate(BaseModel):
    content: str | None = None
    file_name: str | None = None
    file_path: str | None = None


class FileResponse(BaseModel):
    id: int
    project_id: int
    file_path: str
    file_name: str
    file_type: str
    content: str | None = None
    file_size: int | None
    mime_type: str | None
    created_by: int
    updated_by: int | None = None
    created_at: datetime
    updated_at: datetime
    session_id: int | None
    version_label: str | None = None
    updated_by_name: str | None = None

    model_config = {"from_attributes": True}


class FileTreeItem(BaseModel):
    id: int
    file_path: str
    file_name: str
    file_type: str
    file_size: int | None
    updated_at: datetime
    version_label: str | None = None
    updated_by_name: str | None = None


class FileVersionResponse(BaseModel):
    id: int
    file_id: int
    version_label: str
    file_size: int | None
    updated_by: int
    updated_by_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
