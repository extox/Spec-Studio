"""Context Expansion API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.project_file import ProjectFile
from app.schemas.context import ContextFileCreate, ContextFileUpdate, ContextCategoryInfo, ContextValidationResult
from app.schemas.file import FileResponse, FileTreeItem
from app.services.context_service import (
    CONTEXT_CATEGORIES, validate_yaml, validate_required_fields, get_category_from_path,
)
from app.services.context_templates import CONTEXT_TEMPLATES
from app.services.file_service import create_file, update_file, delete_file, get_file, get_file_with_editor
from app.core.dependencies import get_current_user, get_project_member

router = APIRouter()


@router.get("/categories", response_model=list[ContextCategoryInfo])
async def list_categories(
    project_id: int,
    member=Depends(get_project_member),
):
    return [ContextCategoryInfo(**{k: v for k, v in cat.items() if not k.startswith("_")}) for cat in CONTEXT_CATEGORIES.values() if not cat.get("_hidden")]


@router.get("/templates/{category}")
async def get_template(
    project_id: int,
    category: str,
    member=Depends(get_project_member),
):
    if category not in CONTEXT_TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template not found for category: {category}")
    return {"category": category, "content": CONTEXT_TEMPLATES[category]}


@router.get("", response_model=list[FileTreeItem])
async def list_context_files(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProjectFile)
        .where(ProjectFile.project_id == project_id, ProjectFile.file_type == "context")
        .order_by(ProjectFile.file_path)
    )
    files = result.scalars().all()

    # Get editor names
    from app.models.user import User as UserModel
    user_ids = {f.updated_by for f in files if f.updated_by}
    user_map = {}
    if user_ids:
        r = await db.execute(select(UserModel).where(UserModel.id.in_(user_ids)))
        user_map = {u.id: u.display_name for u in r.scalars().all()}

    # Get latest version labels
    from app.models.file_version import FileVersion
    from sqlalchemy import func
    file_ids = [f.id for f in files]
    version_map = {}
    if file_ids:
        sub = (
            select(FileVersion.file_id, func.max(FileVersion.version_label).label("latest"))
            .where(FileVersion.file_id.in_(file_ids))
            .group_by(FileVersion.file_id)
        )
        r2 = await db.execute(sub)
        version_map = {row[0]: row[1] for row in r2.all()}

    return [
        FileTreeItem(
            id=f.id,
            file_path=f.file_path,
            file_name=f.file_name,
            file_type=f.file_type,
            file_size=f.file_size,
            updated_at=f.updated_at,
            version_label=version_map.get(f.id),
            updated_by_name=user_map.get(f.updated_by) if f.updated_by else None,
        )
        for f in files
    ]


@router.post("", response_model=FileResponse)
async def create_context_file(
    project_id: int,
    req: ContextFileCreate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    if req.category not in CONTEXT_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Unknown category: {req.category}")

    # Validate YAML
    is_valid, parsed, errors = validate_yaml(req.content)
    if not is_valid:
        raise HTTPException(status_code=422, detail={"errors": errors, "warnings": []})

    # Check required fields (warnings only, don't block)
    warnings = validate_required_fields(req.category, parsed)

    # Build file path
    file_name = req.file_name if req.file_name.endswith((".yaml", ".yml")) else f"{req.file_name}.yaml"
    file_path = f"context/{req.category}/{file_name}"

    f = await create_file(
        db, project_id, user.id,
        file_path=file_path,
        file_name=file_name,
        file_type="context",
        content=req.content,
    )
    return f


@router.get("/{file_id}", response_model=FileResponse)
async def get_context_file(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    f, editor_name = await get_file_with_editor(db, project_id, file_id)
    if f.file_type != "context":
        raise HTTPException(status_code=404, detail="Not a context file")

    from app.models.file_version import FileVersion
    from sqlalchemy import func
    result = await db.execute(
        select(func.max(FileVersion.version_label)).where(FileVersion.file_id == file_id)
    )
    latest_version = result.scalar_one_or_none()

    return FileResponse(
        id=f.id,
        project_id=f.project_id,
        file_path=f.file_path,
        file_name=f.file_name,
        file_type=f.file_type,
        content=f.content,
        file_size=f.file_size,
        mime_type=f.mime_type,
        created_by=f.created_by,
        updated_by=f.updated_by,
        created_at=f.created_at,
        updated_at=f.updated_at,
        session_id=f.session_id,
        version_label=latest_version,
        updated_by_name=editor_name,
    )


@router.put("/{file_id}", response_model=FileResponse)
async def update_context_file(
    project_id: int,
    file_id: int,
    req: ContextFileUpdate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    # Validate YAML
    is_valid, parsed, errors = validate_yaml(req.content)
    if not is_valid:
        raise HTTPException(status_code=422, detail={"errors": errors, "warnings": []})

    kwargs: dict = {"content": req.content}
    if req.file_name:
        file_name = req.file_name if req.file_name.endswith((".yaml", ".yml")) else f"{req.file_name}.yaml"
        kwargs["file_name"] = file_name
        # Also update file_path
        f = await get_file(db, project_id, file_id)
        category = get_category_from_path(f.file_path) or "custom"
        kwargs["file_path"] = f"context/{category}/{file_name}"

    return await update_file(db, project_id, file_id, user_id=user.id, **kwargs)


@router.delete("/{file_id}")
async def delete_context_file(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    # Verify it's a context file
    f = await get_file(db, project_id, file_id)
    if f.file_type != "context":
        raise HTTPException(status_code=400, detail="Not a context file")
    await delete_file(db, project_id, file_id)
    return {"ok": True}


@router.post("/validate", response_model=ContextValidationResult)
async def validate_content(
    project_id: int,
    req: dict,
    member=Depends(get_project_member),
):
    content = req.get("content", "")
    category = req.get("category", "custom")

    is_valid, parsed, errors = validate_yaml(content)
    warnings = []
    if is_valid and parsed:
        warnings = validate_required_fields(category, parsed)

    return ContextValidationResult(valid=is_valid, errors=errors, warnings=warnings)


@router.post("/import-document")
async def import_document(
    project_id: int,
    category: str = "custom",
    custom_instruction: str = "",
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document, extract text, and use AI to structure it as YAML.

    Returns the extracted text and structured YAML for user review before saving.
    """
    if category not in CONTEXT_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Unknown category: {category}")

    # Read file
    content_bytes = await file.read()
    filename = file.filename or "document"
    mime_type = file.content_type or "application/octet-stream"

    # Extract text
    from app.services.document_parser import extract_text
    try:
        extracted = await extract_text(content_bytes, filename, mime_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not extracted.strip():
        raise HTTPException(status_code=400, detail="문서에서 텍스트를 추출할 수 없습니다.")

    # Get user's LLM config
    from app.models.llm_config import LLMConfig
    from app.models.project_member import ProjectMember as PM
    from app.core.security import decrypt_api_key

    # Try user's default config first
    result = await db.execute(
        select(LLMConfig).where(LLMConfig.user_id == user.id, LLMConfig.is_default == True).limit(1)
    )
    llm_config = result.scalar_one_or_none()

    # Fallback: project owner's config
    if not llm_config:
        owner_result = await db.execute(
            select(PM.user_id).where(PM.project_id == project_id, PM.role == "owner")
        )
        owner_id = owner_result.scalar_one_or_none()
        if owner_id and owner_id != user.id:
            result = await db.execute(
                select(LLMConfig).where(LLMConfig.user_id == owner_id, LLMConfig.is_default == True).limit(1)
            )
            llm_config = result.scalar_one_or_none()

    if not llm_config:
        raise HTTPException(status_code=400, detail="LLM API 설정이 필요합니다. 설정 페이지에서 API를 등록해주세요.")

    try:
        api_key = decrypt_api_key(llm_config.api_key_encrypted)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM API 키 복호화에 실패했습니다.")

    # AI structuring
    from app.services.ai_structurer import structure_document
    try:
        structured_yaml = await structure_document(
            document_text=extracted,
            category=category,
            provider=llm_config.provider,
            model=llm_config.model,
            api_key=api_key,
            base_url=llm_config.base_url,
            custom_instruction=custom_instruction or None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 구조화 중 오류: {str(e)}")

    # Validate the generated YAML
    is_valid, parsed, errors = validate_yaml(structured_yaml)
    warnings = []
    if is_valid and parsed:
        warnings = validate_required_fields(category, parsed)
    if not is_valid:
        warnings = errors + ["AI가 생성한 YAML이 유효하지 않습니다. 수동으로 수정해주세요."]

    # Build file_name
    file_name = file.filename or "imported"
    file_name = file_name.rsplit(".", 1)[0]  # Remove original extension

    return {
        "extracted_text": extracted[:5000] + ("..." if len(extracted) > 5000 else ""),
        "structured_yaml": structured_yaml,
        "category": category,
        "file_name": file_name,
        "warnings": warnings,
    }


@router.post("/import-save", response_model=FileResponse)
async def save_imported(
    project_id: int,
    req: ContextFileCreate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Save the AI-structured YAML (after user review/edit) as a context file."""
    if req.category not in CONTEXT_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Unknown category: {req.category}")

    # Validate YAML
    is_valid, parsed, errors = validate_yaml(req.content)
    if not is_valid:
        raise HTTPException(status_code=422, detail={"errors": errors, "warnings": []})

    file_name = req.file_name if req.file_name.endswith((".yaml", ".yml")) else f"{req.file_name}.yaml"
    file_path = f"context/{req.category}/{file_name}"

    f = await create_file(
        db, project_id, user.id,
        file_path=file_path,
        file_name=file_name,
        file_type="context",
        content=req.content,
    )
    return f


async def _get_llm_config_for_user(db: AsyncSession, user_id: int, project_id: int):
    """Get user's default LLM config, fallback to project owner's."""
    from app.models.llm_config import LLMConfig
    from app.models.project_member import ProjectMember as PM
    from app.core.security import decrypt_api_key

    result = await db.execute(select(LLMConfig).where(LLMConfig.user_id == user_id, LLMConfig.is_default == True).limit(1))
    llm_config = result.scalar_one_or_none()
    if not llm_config:
        owner_result = await db.execute(select(PM.user_id).where(PM.project_id == project_id, PM.role == "owner"))
        owner_id = owner_result.scalar_one_or_none()
        if owner_id and owner_id != user_id:
            result = await db.execute(select(LLMConfig).where(LLMConfig.user_id == owner_id, LLMConfig.is_default == True).limit(1))
            llm_config = result.scalar_one_or_none()
    if not llm_config:
        raise HTTPException(status_code=400, detail="LLM API 설정이 필요합니다. 설정 페이지에서 API를 등록해주세요.")
    try:
        api_key = decrypt_api_key(llm_config.api_key_encrypted)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM API 키 복호화에 실패했습니다.")
    return llm_config, api_key


@router.post("/review-architecture")
async def review_architecture_endpoint(
    project_id: int,
    req: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """AI multi-perspective architecture review."""
    yaml_content = req.get("yaml_content", "")
    custom_instruction = req.get("custom_instruction", "")

    if not yaml_content.strip():
        raise HTTPException(status_code=400, detail="아키텍처 YAML 내용이 비어있습니다.")

    llm_config, api_key = await _get_llm_config_for_user(db, user.id, project_id)

    from app.services.ai_reviewer import review_architecture
    try:
        review = await review_architecture(
            architecture_yaml=yaml_content,
            provider=llm_config.provider,
            model=llm_config.model,
            api_key=api_key,
            base_url=llm_config.base_url,
            custom_instruction=custom_instruction or None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 리뷰 중 오류: {str(e)}")

    return {"review": review}


@router.post("/generate-tobe")
async def generate_tobe_endpoint(
    project_id: int,
    req: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Generate To-Be architecture based on review."""
    asis_yaml = req.get("asis_yaml", "")
    review_result = req.get("review_result", "")
    custom_instruction = req.get("custom_instruction", "")

    if not asis_yaml.strip():
        raise HTTPException(status_code=400, detail="AS-IS 아키텍처 YAML이 비어있습니다.")
    if not review_result.strip():
        raise HTTPException(status_code=400, detail="리뷰 결과가 비어있습니다.")

    llm_config, api_key = await _get_llm_config_for_user(db, user.id, project_id)

    from app.services.ai_reviewer import generate_tobe_architecture
    try:
        tobe_yaml = await generate_tobe_architecture(
            asis_yaml=asis_yaml,
            review_result=review_result,
            provider=llm_config.provider,
            model=llm_config.model,
            api_key=api_key,
            base_url=llm_config.base_url,
            custom_instruction=custom_instruction or None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"To-Be 생성 중 오류: {str(e)}")

    # Validate
    is_valid, _, errors = validate_yaml(tobe_yaml)
    warnings = []
    if not is_valid:
        warnings = errors + ["생성된 YAML이 유효하지 않을 수 있습니다. 검토 후 수정해주세요."]

    return {"tobe_yaml": tobe_yaml, "warnings": warnings}


@router.post("/save-tobe", response_model=FileResponse)
async def save_tobe(
    project_id: int,
    req: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Save To-Be architecture as a separate context file."""
    content = req.get("content", "")
    file_name = req.get("file_name", "to-be-architecture")
    source_file = req.get("source_file", "")

    if not content.strip():
        raise HTTPException(status_code=400, detail="YAML 내용이 비어있습니다.")

    is_valid, _, errors = validate_yaml(content)
    if not is_valid:
        raise HTTPException(status_code=422, detail={"errors": errors, "warnings": []})

    if not file_name.endswith((".yaml", ".yml")):
        file_name = f"{file_name}.yaml"
    file_path = f"context/system-architecture/{file_name}"

    f = await create_file(
        db, project_id, user.id,
        file_path=file_path, file_name=file_name,
        file_type="context", content=content,
    )
    return f


@router.post("/upload", response_model=FileResponse)
async def upload_yaml(
    project_id: int,
    category: str = "custom",
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    if category not in CONTEXT_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Unknown category: {category}")

    content_bytes = await file.read()
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded YAML")

    is_valid, parsed, errors = validate_yaml(content)
    if not is_valid:
        raise HTTPException(status_code=422, detail={"errors": errors, "warnings": []})

    file_name = file.filename or "uploaded.yaml"
    if not file_name.endswith((".yaml", ".yml")):
        file_name = f"{file_name}.yaml"
    file_path = f"context/{category}/{file_name}"

    f = await create_file(
        db, project_id, user.id,
        file_path=file_path,
        file_name=file_name,
        file_type="context",
        content=content,
    )
    return f
