"""Validation API — run engine, list issues, update issue status, fetch latest run."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_project_member
from app.database import get_db
from app.models.user import User
from app.models.validation import ValidationIssue, ValidationRun
from app.services.traceability_service import build_project_index
from app.services.validation.registry import all_rules
from app.services.validation_service import (
    get_issue_counts_by_file,
    get_latest_run,
    run_validation,
)

router = APIRouter()


def _run_to_dict(r: ValidationRun, total_anchors: int | None = None) -> dict:
    return {
        "id": r.id,
        "scope": r.scope,
        "file_id": r.file_id,
        "triggered_by": r.triggered_by,
        "status": r.status,
        "duration_ms": r.duration_ms,
        "rules_executed": r.rules_executed,
        "issues_open": r.issues_open,
        "issues_resolved": r.issues_resolved,
        "health_score": r.health_score,
        "total_anchors": total_anchors,
        "created_at": r.created_at,
    }


def _issue_to_dict(i: ValidationIssue) -> dict:
    return {
        "id": i.id,
        "rule_id": i.rule_id,
        "severity": i.severity,
        "file_id": i.file_id,
        "anchor": i.anchor,
        "related_file_id": i.related_file_id,
        "related_anchor": i.related_anchor,
        "message": i.message,
        "suggestion": i.suggestion,
        "status": i.status,
        "confidence": i.confidence,
        "created_at": i.created_at,
        "resolved_at": i.resolved_at,
    }


@router.get("/rules")
async def list_rules(
    project_id: int,
    member=Depends(get_project_member),
):
    return [
        {
            "id": r.id,
            "severity": r.severity,
            "description": r.description,
            "is_llm": r.is_llm,
            "tags": r.tags,
            "enabled": r.enabled,
        }
        for r in all_rules()
    ]


@router.post("")
async def run(
    project_id: int,
    scope: str = Query(default="all", pattern="^(all|file|cross-doc)$"),
    file_id: int | None = Query(default=None),
    include_llm: bool = Query(default=True),
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    r = await run_validation(
        db,
        project_id=project_id,
        user_id=user.id,
        scope=scope,
        file_id=file_id,
        triggered_by="manual",
        include_llm_rules=include_llm,
    )
    await db.commit()
    index = await build_project_index(db, project_id)
    return _run_to_dict(r, total_anchors=len(index.anchor_to_file))


@router.get("/runs/latest")
async def latest_run(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    r = await get_latest_run(db, project_id)
    if not r:
        return None
    index = await build_project_index(db, project_id)
    return _run_to_dict(r, total_anchors=len(index.anchor_to_file))


@router.get("/issues")
async def list_issues(
    project_id: int,
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    file_id: int | None = Query(default=None),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    q = select(ValidationIssue).where(ValidationIssue.project_id == project_id)
    if status and status != "all":
        q = q.where(ValidationIssue.status == status)
    if severity:
        q = q.where(ValidationIssue.severity == severity)
    if file_id is not None:
        q = q.where(ValidationIssue.file_id == file_id)
    q = q.order_by(ValidationIssue.severity, ValidationIssue.id)
    result = await db.execute(q)
    return [_issue_to_dict(i) for i in result.scalars().all()]


@router.get("/issues/counts")
async def issue_counts(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    """Return per-status counts of user dispositions (label-only, not engine state)."""
    q = (
        select(ValidationIssue.status, func.count(ValidationIssue.id))
        .where(ValidationIssue.project_id == project_id)
        .group_by(ValidationIssue.status)
    )
    result = await db.execute(q)
    counts = {"open": 0, "acknowledged": 0, "resolved": 0, "suppressed": 0}
    for status_val, n in result.all():
        if status_val in counts:
            counts[status_val] = n
    return counts


@router.get("/issues/by-file")
async def issues_by_file(
    project_id: int,
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    return await get_issue_counts_by_file(db, project_id)


@router.patch("/issues/{issue_id}")
async def update_issue(
    project_id: int,
    issue_id: int,
    payload: dict,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    new_status = payload.get("status")
    if new_status not in ("open", "acknowledged", "resolved", "suppressed"):
        raise HTTPException(status_code=400, detail="invalid status")
    result = await db.execute(
        select(ValidationIssue).where(
            ValidationIssue.id == issue_id,
            ValidationIssue.project_id == project_id,
        )
    )
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.status = new_status
    if new_status in ("resolved", "suppressed"):
        issue.resolved_at = datetime.now(timezone.utc)
    elif new_status == "open":
        issue.resolved_at = None
    await db.commit()
    return _issue_to_dict(issue)
