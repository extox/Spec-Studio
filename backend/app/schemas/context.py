from pydantic import BaseModel


class ContextFileCreate(BaseModel):
    category: str
    file_name: str
    content: str


class ContextFileUpdate(BaseModel):
    content: str
    file_name: str | None = None


class ContextCategoryInfo(BaseModel):
    id: str
    name: str
    name_en: str
    description: str
    icon: str


class ContextValidationResult(BaseModel):
    valid: bool
    errors: list[str]
    warnings: list[str]


class DocumentImportRequest(BaseModel):
    category: str
    file_name: str
    custom_instruction: str | None = None


class DocumentImportResponse(BaseModel):
    extracted_text: str
    structured_yaml: str
    category: str
    file_name: str
    warnings: list[str]
