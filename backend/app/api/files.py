from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.file import FileCreate, FileUpdate, FileResponse, FileTreeItem, FileVersionResponse
from app.services.file_service import (
    get_project_files, get_file, get_file_with_editor, create_file, update_file,
    delete_file, save_uploaded_file, create_zip,
    get_file_versions, restore_version,
)
from app.services.samples import SAMPLE_CATALOG, SAMPLE_FILES_MAP
from app.core.dependencies import get_current_user, get_project_member

router = APIRouter()


@router.get("", response_model=list[FileTreeItem])
async def list_files(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    files = await get_project_files(db, project_id)
    # Batch fetch editor names
    from sqlalchemy import select
    from app.models.user import User as UserModel
    user_ids = {f.updated_by for f in files if f.updated_by}
    user_map = {}
    if user_ids:
        result = await db.execute(select(UserModel).where(UserModel.id.in_(user_ids)))
        user_map = {u.id: u.display_name for u in result.scalars().all()}

    # Get latest version labels
    from app.models.file_version import FileVersion
    file_ids = [f.id for f in files]
    version_map = {}
    if file_ids:
        from sqlalchemy import func
        sub = (
            select(FileVersion.file_id, func.max(FileVersion.version_label).label("latest"))
            .where(FileVersion.file_id.in_(file_ids))
            .group_by(FileVersion.file_id)
        )
        result = await db.execute(sub)
        version_map = {row[0]: row[1] for row in result.all()}

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


@router.get("/download-all")
async def download_all(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    zip_bytes = await create_zip(db, project_id)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=project-{project_id}.zip"},
    )


@router.get("/sample-catalog")
async def get_sample_catalog(
    project_id: int,
    member=Depends(get_project_member),
):
    return SAMPLE_CATALOG


@router.get("/{file_id}", response_model=FileResponse)
async def get_one(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    f, editor_name = await get_file_with_editor(db, project_id, file_id)

    # Get latest version label
    from app.models.file_version import FileVersion
    from sqlalchemy import select, func
    result = await db.execute(
        select(func.max(FileVersion.version_label))
        .where(FileVersion.file_id == file_id)
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


@router.post("", response_model=FileResponse)
async def create(
    project_id: int,
    req: FileCreate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await create_file(
        db, project_id, user.id,
        req.file_path, req.file_name, req.file_type, req.content,
    )


@router.put("/rename-directory")
async def rename_directory(
    project_id: int,
    req: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Rename a directory by updating file_path of all files in it."""
    old_dir = req.get("old_dir", "")
    new_dir = req.get("new_dir", "")
    if not old_dir or not new_dir:
        raise HTTPException(status_code=400, detail="old_dir and new_dir required")

    files = await get_project_files(db, project_id)
    updated = 0
    for f in files:
        if f.file_path.startswith(old_dir + "/") or f.file_path == old_dir:
            new_path = new_dir + f.file_path[len(old_dir):]
            f.file_path = new_path
            f.updated_by = user.id
            updated += 1
    if updated == 0:
        raise HTTPException(status_code=404, detail="No files found in directory")
    await db.flush()
    return {"ok": True, "updated": updated}


@router.delete("/{file_id}")
async def delete(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    await delete_file(db, project_id, file_id)
    return {"ok": True}


@router.put("/{file_id}", response_model=FileResponse)
async def update(
    project_id: int,
    file_id: int,
    req: FileUpdate,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await update_file(db, project_id, file_id, user_id=user.id, content=req.content, file_name=req.file_name, file_path=req.file_path)


@router.post("/load-samples", response_model=list[FileResponse])
async def load_samples(
    project_id: int,
    req: dict | None = None,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    existing = await get_project_files(db, project_id)
    if existing:
        raise HTTPException(status_code=400, detail="Project already has files")

    sample_id = (req or {}).get("sample_id", "taskflow")
    sample_fn = SAMPLE_FILES_MAP.get(sample_id)
    if not sample_fn:
        raise HTTPException(status_code=400, detail=f"Unknown sample: {sample_id}")

    created = []
    for sample in sample_fn():
        # Files placed under context/ are context-expansion YAML; everything
        # else is a deliverable. Optional `file_type` override on the sample
        # entry takes precedence when present.
        path = sample["file_path"]
        ftype = sample.get("file_type") or (
            "context" if path.startswith("context/") else "deliverable"
        )
        f = await create_file(
            db, project_id, user.id,
            path, sample["file_name"],
            ftype, sample["content"],
        )
        created.append(f)
    return created


@router.post("/upload", response_model=FileResponse)
async def upload(
    project_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    return await save_uploaded_file(
        db, project_id, user.id, file.filename, content, file.content_type or "application/octet-stream",
    )


@router.get("/{file_id}/download")
async def download(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    f = await get_file(db, project_id, file_id)
    if f.content:
        return Response(
            content=f.content.encode(),
            media_type=f.mime_type or "text/plain",
            headers={"Content-Disposition": f"attachment; filename={f.file_name}"},
        )
    import os
    from app.config import get_settings
    settings = get_settings()
    physical_path = os.path.join(settings.UPLOAD_PATH, str(project_id), f.file_name)
    if os.path.exists(physical_path):
        with open(physical_path, "rb") as fh:
            data = fh.read()
        return Response(
            content=data,
            media_type=f.mime_type or "application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={f.file_name}"},
        )
    from app.core.exceptions import NotFoundError
    raise NotFoundError("Physical file not found")


# --- Version endpoints ---

@router.get("/{file_id}/versions", response_model=list[FileVersionResponse])
async def list_versions(
    project_id: int,
    file_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    await get_file(db, project_id, file_id)  # verify access
    return await get_file_versions(db, file_id)


@router.get("/{file_id}/versions/{version_id}")
async def get_version_content(
    project_id: int,
    file_id: int,
    version_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    from app.services.file_service import get_version
    await get_file(db, project_id, file_id)  # verify access
    v = await get_version(db, version_id)
    if v.file_id != file_id:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Version does not belong to this file")
    return {"id": v.id, "version_label": v.version_label, "content": v.content}


@router.post("/{file_id}/versions/{version_id}/restore", response_model=FileResponse)
async def restore(
    project_id: int,
    file_id: int,
    version_id: int,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await restore_version(db, project_id, file_id, version_id, user.id)
