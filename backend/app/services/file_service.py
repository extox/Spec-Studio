import io
import os
import zipfile
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.project_file import ProjectFile
from app.models.file_version import FileVersion
from app.models.user import User
from app.core.exceptions import NotFoundError, ConflictError
from app.config import get_settings

settings = get_settings()


from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


def _make_version_label() -> str:
    """Generate version label as YYMMDD_HHMMSS in KST."""
    now = datetime.now(KST)
    return now.strftime("%y%m%d_%H%M%S")


async def get_project_files(db: AsyncSession, project_id: int) -> list[ProjectFile]:
    result = await db.execute(
        select(ProjectFile)
        .where(ProjectFile.project_id == project_id)
        .order_by(ProjectFile.file_path)
    )
    return list(result.scalars().all())


async def get_file(db: AsyncSession, project_id: int, file_id: int) -> ProjectFile:
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )
    file = result.scalar_one_or_none()
    if not file:
        raise NotFoundError("File not found")
    return file


async def get_file_with_editor(db: AsyncSession, project_id: int, file_id: int) -> tuple[ProjectFile, str | None]:
    """Get file with editor's display name."""
    result = await db.execute(
        select(ProjectFile, User.display_name)
        .outerjoin(User, User.id == ProjectFile.updated_by)
        .where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )
    row = result.one_or_none()
    if not row:
        raise NotFoundError("File not found")
    return row[0], row[1]


async def create_file(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    file_path: str,
    file_name: str,
    file_type: str = "deliverable",
    content: str | None = None,
    session_id: int | None = None,
) -> ProjectFile:
    existing = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.file_path == file_path,
        )
    )
    if existing.scalar_one_or_none():
        raise ConflictError(f"File already exists at path: {file_path}")

    version_label = _make_version_label()
    file = ProjectFile(
        project_id=project_id,
        file_path=file_path,
        file_name=file_name,
        file_type=file_type,
        content=content,
        file_size=len(content.encode()) if content else 0,
        mime_type="text/yaml" if file_type == "context" else ("text/markdown" if file_type == "deliverable" else None),
        created_by=user_id,
        updated_by=user_id,
        session_id=session_id,
    )
    db.add(file)
    await db.flush()
    await db.refresh(file)

    # Create initial version
    version = FileVersion(
        file_id=file.id,
        version_label=version_label,
        content=content,
        file_size=len(content.encode()) if content else 0,
        updated_by=user_id,
    )
    db.add(version)
    await db.flush()
    return file


async def update_file(db: AsyncSession, project_id: int, file_id: int, user_id: int | None = None, **kwargs) -> ProjectFile:
    file = await get_file(db, project_id, file_id)

    # Save current state as version before updating
    if "content" in kwargs and kwargs["content"] is not None and file.content != kwargs["content"]:
        version_label = _make_version_label()
        version = FileVersion(
            file_id=file.id,
            version_label=version_label,
            content=kwargs["content"],
            file_size=len(kwargs["content"].encode()),
            updated_by=user_id or file.created_by,
        )
        db.add(version)

    for key, value in kwargs.items():
        if value is not None:
            setattr(file, key, value)
    if "content" in kwargs and kwargs["content"] is not None:
        file.file_size = len(kwargs["content"].encode())
    if user_id:
        file.updated_by = user_id
    await db.flush()
    await db.refresh(file)
    return file


async def delete_file(db: AsyncSession, project_id: int, file_id: int):
    file = await get_file(db, project_id, file_id)
    # If it's an uploaded file, delete the physical file
    if file.file_type == "uploaded" and file.file_path:
        physical_path = os.path.join(settings.UPLOAD_PATH, str(project_id), file.file_name)
        if os.path.exists(physical_path):
            os.remove(physical_path)
    await db.delete(file)
    await db.flush()


async def save_uploaded_file(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    file_name: str,
    file_content: bytes,
    mime_type: str,
) -> ProjectFile:
    upload_dir = os.path.join(settings.UPLOAD_PATH, str(project_id))
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"uploads/{file_name}"
    physical_path = os.path.join(upload_dir, file_name)

    with open(physical_path, "wb") as f:
        f.write(file_content)

    file = ProjectFile(
        project_id=project_id,
        file_path=file_path,
        file_name=file_name,
        file_type="uploaded",
        file_size=len(file_content),
        mime_type=mime_type,
        created_by=user_id,
        updated_by=user_id,
    )
    db.add(file)
    await db.flush()
    return file


async def create_zip(db: AsyncSession, project_id: int) -> bytes:
    files = await get_project_files(db, project_id)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            if file.content:
                zf.writestr(file.file_path, file.content)
            elif file.file_type == "uploaded":
                physical_path = os.path.join(
                    settings.UPLOAD_PATH, str(project_id), file.file_name
                )
                if os.path.exists(physical_path):
                    zf.write(physical_path, file.file_path)
    buffer.seek(0)
    return buffer.getvalue()


# --- Version functions ---

async def get_file_versions(db: AsyncSession, file_id: int) -> list[dict]:
    """Get all versions for a file with editor names."""
    result = await db.execute(
        select(FileVersion, User.display_name)
        .outerjoin(User, User.id == FileVersion.updated_by)
        .where(FileVersion.file_id == file_id)
        .order_by(FileVersion.created_at.desc())
    )
    versions = []
    for row in result.all():
        v = row[0]
        versions.append({
            "id": v.id,
            "file_id": v.file_id,
            "version_label": v.version_label,
            "file_size": v.file_size,
            "updated_by": v.updated_by,
            "updated_by_name": row[1],
            "created_at": v.created_at,
        })
    return versions


async def get_version(db: AsyncSession, version_id: int) -> FileVersion:
    result = await db.execute(
        select(FileVersion).where(FileVersion.id == version_id)
    )
    version = result.scalar_one_or_none()
    if not version:
        raise NotFoundError("Version not found")
    return version


async def restore_version(db: AsyncSession, project_id: int, file_id: int, version_id: int, user_id: int) -> ProjectFile:
    """Restore a file to a previous version. Creates a new version with current timestamp."""
    file = await get_file(db, project_id, file_id)
    version = await get_version(db, version_id)

    if version.file_id != file_id:
        raise NotFoundError("Version does not belong to this file")

    # Create new version with restored content
    new_label = _make_version_label()
    new_version = FileVersion(
        file_id=file.id,
        version_label=new_label,
        content=version.content,
        file_size=version.file_size,
        updated_by=user_id,
    )
    db.add(new_version)

    # Update file to restored content
    file.content = version.content
    file.file_size = version.file_size
    file.updated_by = user_id
    await db.flush()
    await db.refresh(file)
    return file
