"""Traceability API — anchor extraction, link rebuild, graph, trace."""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_project_member
from app.database import get_db, async_session
from app.models.project_file import ProjectFile
from app.models.traceability_link import TraceabilityLink
from app.models.user import User
from app.services.traceability_service import (
    build_project_index,
    detect_file_prefix,
    extract_anchor_snippet,
    extract_anchors,
    get_graph,
    get_orphan_anchors,
    get_trace_for_anchor,
    rebuild_all_explicit_links,
    rebuild_explicit_links_for_file,
    suggest_links_for_file,
)

router = APIRouter()


# --- Anchors -----------------------------------------------------------------

@router.get("/anchors")
async def list_anchors(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """List every (file, anchor) pair detected in the project."""
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    out = []
    for f in result.scalars().all():
        prefix = detect_file_prefix(f.file_name)
        if not prefix or not f.content:
            continue
        for anchor in extract_anchors(f):
            out.append(
                {
                    "file_id": f.id,
                    "file_name": f.file_name,
                    "file_path": f.file_path,
                    "prefix": prefix,
                    "anchor": anchor,
                }
            )
    return out


# --- Rebuild explicit links --------------------------------------------------

@router.post("/rebuild")
async def rebuild(
    project_id: int,
    file_id: int | None = Query(default=None, description="If set, rebuild only this file"),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    if file_id is not None:
        count = await rebuild_explicit_links_for_file(db, project_id, file_id)
    else:
        count = await rebuild_all_explicit_links(db, project_id)
    await db.commit()
    return {"ok": True, "links_inserted": count, "scope": "file" if file_id else "all"}


# --- LLM-based suggestion ----------------------------------------------------

@router.post("/suggest")
async def suggest(
    project_id: int,
    file_id: int = Query(..., description="Source file to suggest links for"),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    count = await suggest_links_for_file(
        db, project_id, file_id, user.id, min_confidence=min_confidence
    )
    await db.commit()
    return {"ok": True, "links_inserted": count}


# --- Graph -------------------------------------------------------------------

@router.get("/graph")
async def graph(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_graph(db, project_id)


# --- Trace -------------------------------------------------------------------

@router.get("/trace")
async def trace(
    project_id: int,
    file_id: int = Query(...),
    anchor: str = Query(...),
    direction: str = Query("both", pattern="^(upstream|downstream|both)$"),
    max_depth: int = Query(5, ge=1, le=10),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_trace_for_anchor(
        db, project_id, file_id, anchor, direction=direction, max_depth=max_depth
    )


# --- Anchor content ----------------------------------------------------------

@router.get("/anchor-content")
async def anchor_content(
    project_id: int,
    file_id: int = Query(...),
    anchor: str = Query(...),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Return a readable snippet for a (file_id, anchor) pair.

    Tries heading section first, then table row, then ±a few lines of context.
    """
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )
    f = result.scalar_one_or_none()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    snip = extract_anchor_snippet(f.content or "", anchor)
    return {
        "file_id": f.id,
        "file_name": f.file_name,
        "file_path": f.file_path,
        "prefix": detect_file_prefix(f.file_name),
        "anchor": anchor,
        **snip,
    }


# --- Orphans -----------------------------------------------------------------

@router.get("/orphans")
async def orphans(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_orphan_anchors(db, project_id)


# --- Manual link CRUD --------------------------------------------------------

@router.get("/links")
async def list_links(
    project_id: int,
    file_id: int | None = Query(default=None),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    q = select(TraceabilityLink).where(TraceabilityLink.project_id == project_id)
    if file_id is not None:
        from sqlalchemy import or_
        q = q.where(
            or_(
                TraceabilityLink.source_file_id == file_id,
                TraceabilityLink.target_file_id == file_id,
            )
        )
    result = await db.execute(q)
    links = list(result.scalars().all())
    return [
        {
            "id": l.id,
            "source_file_id": l.source_file_id,
            "source_anchor": l.source_anchor,
            "target_file_id": l.target_file_id,
            "target_anchor": l.target_anchor,
            "relation": l.relation,
            "origin": l.origin,
            "confidence": l.confidence,
            "rationale": l.rationale,
            "created_at": l.created_at,
        }
        for l in links
    ]


@router.post("/links")
async def create_link(
    project_id: int,
    payload: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Create a manual traceability link."""
    required = ("source_file_id", "source_anchor", "target_file_id", "target_anchor")
    if any(payload.get(k) in (None, "") for k in required):
        raise HTTPException(status_code=400, detail=f"Missing required fields: {required}")

    # Validate that both files belong to this project.
    files_q = await db.execute(
        select(ProjectFile.id, ProjectFile.project_id).where(
            ProjectFile.id.in_([payload["source_file_id"], payload["target_file_id"]])
        )
    )
    rows = files_q.all()
    if len(rows) != 2 or any(r[1] != project_id for r in rows):
        raise HTTPException(status_code=400, detail="Files do not belong to this project")

    link = TraceabilityLink(
        project_id=project_id,
        source_file_id=payload["source_file_id"],
        source_anchor=payload["source_anchor"],
        target_file_id=payload["target_file_id"],
        target_anchor=payload["target_anchor"],
        relation=payload.get("relation", "derived_from"),
        origin="manual",
        confidence=1.0,
        rationale=payload.get("rationale"),
        created_by_persona=payload.get("created_by_persona"),
    )
    db.add(link)
    await db.flush()
    await db.commit()
    return {"id": link.id, "ok": True}


@router.delete("/links/{link_id}")
async def delete_link(
    project_id: int,
    link_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TraceabilityLink).where(
            TraceabilityLink.id == link_id,
            TraceabilityLink.project_id == project_id,
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    await db.execute(delete(TraceabilityLink).where(TraceabilityLink.id == link_id))
    await db.commit()
    return {"ok": True}


# --- Background hook used by websocket file save -----------------------------

async def background_rebuild_after_save(project_id: int, file_id: int) -> None:
    """Background entry-point used by the chat WebSocket when a SAVE_FILE marker
    completes. Runs in its own DB session so the calling request can return."""
    async with async_session() as db:
        try:
            await rebuild_explicit_links_for_file(db, project_id, file_id)
            await db.commit()
        except Exception:
            await db.rollback()
