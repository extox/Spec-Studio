"""Guide pages API - public read, admin write."""

import os
import uuid
from datetime import timezone as tz

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.guide import GuidePage
from app.core.dependencies import get_current_user, require_admin
from app.config import get_settings

settings = get_settings()
GUIDE_UPLOAD_DIR = os.path.join(settings.UPLOAD_PATH, "guide")

router = APIRouter()


# --- Public endpoints ---

@router.get("/pages")
async def list_pages(db: AsyncSession = Depends(get_db)):
    """List all published guide pages (for viewer)."""
    result = await db.execute(
        select(GuidePage)
        .where(GuidePage.is_published == True)
        .order_by(GuidePage.sort_order, GuidePage.id)
    )
    pages = []
    for p in result.scalars().all():
        pages.append({
            "id": p.id,
            "slug": p.slug,
            "title": p.title,
            "title_en": p.title_en or p.title,
            "group_name": p.group_name,
            "group_name_en": p.group_name_en or p.group_name,
            "sort_order": p.sort_order,
        })
    return pages


@router.get("/pages/{slug}")
async def get_page(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a single guide page content."""
    result = await db.execute(select(GuidePage).where(GuidePage.slug == slug))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {
        "id": page.id,
        "slug": page.slug,
        "title": page.title,
        "group_name": page.group_name,
        "content_ko": page.content_ko,
        "content_en": page.content_en,
        "sort_order": page.sort_order,
        "is_published": page.is_published,
        "updated_at": page.updated_at.replace(tzinfo=tz.utc).isoformat() if page.updated_at else "",
    }


# --- Admin endpoints ---

@router.get("/admin/pages")
async def admin_list_pages(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all guide pages including unpublished (for admin)."""
    result = await db.execute(
        select(GuidePage).order_by(GuidePage.sort_order, GuidePage.id)
    )
    pages = []
    for p in result.scalars().all():
        pages.append({
            "id": p.id,
            "slug": p.slug,
            "title": p.title,
            "title_en": p.title_en or "",
            "group_name": p.group_name,
            "group_name_en": p.group_name_en or "",
            "content_ko": p.content_ko or "",
            "content_en": p.content_en or "",
            "sort_order": p.sort_order,
            "is_published": p.is_published,
            "updated_at": p.updated_at.replace(tzinfo=tz.utc).isoformat() if p.updated_at else "",
        })
    return pages


@router.post("/admin/pages")
async def create_page(
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new guide page."""
    slug = req.get("slug", "").strip()
    title = req.get("title", "").strip()
    if not slug or not title:
        raise HTTPException(status_code=400, detail="slug and title required")

    existing = await db.execute(select(GuidePage).where(GuidePage.slug == slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Slug already exists")

    page = GuidePage(
        slug=slug,
        title=title,
        title_en=req.get("title_en", ""),
        group_name=req.get("group_name", ""),
        group_name_en=req.get("group_name_en", ""),
        content_ko=req.get("content_ko", ""),
        content_en=req.get("content_en", ""),
        sort_order=req.get("sort_order", 0),
        is_published=req.get("is_published", True),
        updated_by=admin.id,
    )
    db.add(page)
    await db.flush()
    return {"ok": True, "id": page.id}


@router.put("/admin/pages/{page_id}")
async def update_page(
    page_id: int,
    req: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a guide page."""
    result = await db.execute(select(GuidePage).where(GuidePage.id == page_id))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    if "title" in req:
        page.title = req["title"]
    if "title_en" in req:
        page.title_en = req["title_en"]
    if "group_name" in req:
        page.group_name = req["group_name"]
    if "group_name_en" in req:
        page.group_name_en = req["group_name_en"]
    if "content_ko" in req:
        page.content_ko = req["content_ko"]
    if "content_en" in req:
        page.content_en = req["content_en"]
    if "sort_order" in req:
        page.sort_order = req["sort_order"]
    if "is_published" in req:
        page.is_published = req["is_published"]
    if "slug" in req:
        page.slug = req["slug"]
    page.updated_by = admin.id
    await db.flush()
    return {"ok": True}


@router.post("/admin/pages/{page_id}/duplicate")
async def duplicate_page(
    page_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Duplicate a guide page as unpublished draft."""
    result = await db.execute(select(GuidePage).where(GuidePage.id == page_id))
    original = result.scalar_one_or_none()
    if not original:
        raise HTTPException(status_code=404, detail="Page not found")

    # Generate unique slug
    base_slug = f"{original.slug}-copy"
    slug = base_slug
    counter = 1
    while True:
        existing = await db.execute(select(GuidePage).where(GuidePage.slug == slug))
        if not existing.scalar_one_or_none():
            break
        counter += 1
        slug = f"{base_slug}-{counter}"

    copy = GuidePage(
        slug=slug,
        title=f"{original.title} (복제)",
        group_name=original.group_name,
        content_ko=original.content_ko,
        content_en=original.content_en,
        sort_order=original.sort_order + 1,
        is_published=False,
        updated_by=admin.id,
    )
    db.add(copy)
    await db.flush()
    return {"ok": True, "id": copy.id, "slug": slug}


@router.delete("/admin/pages/{page_id}")
async def delete_page(
    page_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(GuidePage).where(GuidePage.id == page_id))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    await db.delete(page)
    await db.flush()
    return {"ok": True}


# --- Image upload ---

@router.post("/admin/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    admin: User = Depends(require_admin),
):
    """Upload an image for guide pages. Returns the URL."""
    os.makedirs(GUIDE_UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename or "image.png")[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        raise HTTPException(status_code=400, detail="Unsupported image format")

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(GUIDE_UPLOAD_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    url = f"/api/guide/images/{filename}"
    return {"url": url, "filename": filename}


@router.post("/admin/seed-defaults")
async def seed_default_pages(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Seed default guide pages into DB if they don't exist."""
    from app.services.guide_defaults import DEFAULT_GUIDE_PAGES

    created = 0
    for page_data in DEFAULT_GUIDE_PAGES:
        existing = await db.execute(
            select(GuidePage).where(GuidePage.slug == page_data["slug"])
        )
        if existing.scalar_one_or_none():
            continue

        page = GuidePage(
            slug=page_data["slug"],
            title=page_data["title"],
            group_name=page_data.get("group_name", ""),
            content_ko=page_data.get("content_ko", ""),
            content_en=page_data.get("content_en", ""),
            sort_order=page_data.get("sort_order", 0),
            is_published=True,
            updated_by=admin.id,
        )
        db.add(page)
        created += 1

    await db.flush()
    return {"ok": True, "created": created}


@router.get("/images/{filename}")
async def serve_image(filename: str):
    """Serve uploaded guide images."""
    filepath = os.path.join(GUIDE_UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Image not found")

    from fastapi.responses import FileResponse as FR
    return FR(filepath)
