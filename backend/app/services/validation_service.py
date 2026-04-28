"""Validation service — orchestrate rules, persist runs/issues, diff vs. prior."""

from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.validation import ValidationIssue, ValidationRun
from app.services.traceability_service import build_project_index
from app.services.validation.base import IssueDraft, RuleContext
from app.services.validation.registry import all_rules


def _compute_health_score(
    open_issues: list[ValidationIssue], total_anchors: int
) -> float:
    """Coverage-based health score in [0, 100].

    Score = 100 × (1 − affected_anchors / total_anchors), where
      affected_anchors = unique error anchors
                       + 0.5 × unique warning anchors
                       + 0.25 × unique info anchors

    Why a denominator: a pure subtractive penalty (e.g. error×15) collapses to
    0 once the project has more than a handful of issues, so users can never
    see partial progress. By dividing affected anchors by the total number of
    anchors that *exist* in the project, the score becomes a coverage ratio
    that scales naturally with project size and converges back to 100 as the
    user resolves issues.
    """
    if total_anchors <= 0:
        return 100.0
    by_sev: dict[str, set[str]] = {"error": set(), "warning": set(), "info": set()}
    for i in open_issues:
        anchor = i.anchor or f"_no_anchor_{i.id}"
        if i.severity in by_sev:
            by_sev[i.severity].add(anchor)
    weighted = (
        len(by_sev["error"])
        + 0.5 * len(by_sev["warning"])
        + 0.25 * len(by_sev["info"])
    )
    coverage = max(0.0, 1.0 - weighted / float(total_anchors))
    return round(coverage * 100.0, 1)


async def _resolve_llm(db: AsyncSession, project_id: int, user_id: int):
    """Reuse the same fallback chain as other services."""
    from app.core.security import decrypt_api_key
    from app.models.llm_config import LLMConfig
    from app.models.project_member import ProjectMember

    result = await db.execute(
        select(LLMConfig).where(
            LLMConfig.user_id == user_id, LLMConfig.is_default == True
        ).limit(1)
    )
    cfg = result.scalar_one_or_none()
    if not cfg:
        owner_result = await db.execute(
            select(ProjectMember.user_id).where(
                ProjectMember.project_id == project_id,
                ProjectMember.role == "owner",
            )
        )
        owner_id = owner_result.scalar_one_or_none()
        if owner_id and owner_id != user_id:
            result = await db.execute(
                select(LLMConfig).where(
                    LLMConfig.user_id == owner_id, LLMConfig.is_default == True
                ).limit(1)
            )
            cfg = result.scalar_one_or_none()
    if not cfg:
        return None
    try:
        api_key = decrypt_api_key(cfg.api_key_encrypted)
    except Exception:
        return None
    return cfg.provider, cfg.model, api_key, cfg.base_url


async def run_validation(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    scope: str = "all",
    file_id: int | None = None,
    triggered_by: str = "manual",
    include_llm_rules: bool = True,
) -> ValidationRun:
    """Execute the rule registry and persist the run + new issues.

    Diff strategy:
    - For each rule, compute new fingerprints.
    - Existing OPEN issues with the same fingerprint stay open (their run_id is
      not changed — the original run_id is preserved as the discovery point).
    - Existing OPEN issues whose fingerprints disappear are marked `resolved`
      with `resolved_at = now`.
    - Brand-new fingerprints become new ValidationIssue rows attached to this run.
    """
    started = time.monotonic()
    llm = await _resolve_llm(db, project_id, user_id) if include_llm_rules else None

    ctx = RuleContext(db=db, project_id=project_id, user_id=user_id, llm=llm)

    rules = all_rules(include_llm=include_llm_rules)

    # Run rules sequentially (LLM rules can be slow; keep DB session sane).
    drafts: list[IssueDraft] = []
    for rule in rules:
        try:
            rule_drafts = await rule.check(ctx)
        except Exception:
            continue
        for d in rule_drafts:
            if not d.severity:
                d.severity = rule.severity
            drafts.append(d)

    new_fingerprints = {d.fingerprint(): d for d in drafts}

    # Load existing OPEN issues for this project.
    existing_result = await db.execute(
        select(ValidationIssue).where(
            ValidationIssue.project_id == project_id,
            ValidationIssue.status == "open",
        )
    )
    existing = list(existing_result.scalars().all())

    # Resolve issues that no longer appear.
    resolved_count = 0
    keep_fingerprints: set[str] = set()
    for issue in existing:
        if issue.fingerprint in new_fingerprints:
            keep_fingerprints.add(issue.fingerprint)
        else:
            issue.status = "resolved"
            issue.resolved_at = datetime.now(timezone.utc)
            resolved_count += 1

    # Create the run row first so we can attach new issues to it.
    run = ValidationRun(
        project_id=project_id,
        scope=scope,
        file_id=file_id,
        triggered_by=triggered_by,
        status="completed",
        rules_executed=len(rules),
        duration_ms=int((time.monotonic() - started) * 1000),
        issues_open=0,         # filled in below
        issues_resolved=resolved_count,
        health_score=100.0,    # filled in below
    )
    db.add(run)
    await db.flush()

    # Insert new issues.
    inserted = 0
    for fp, d in new_fingerprints.items():
        if fp in keep_fingerprints:
            continue
        db.add(
            ValidationIssue(
                project_id=project_id,
                run_id=run.id,
                rule_id=d.rule_id,
                severity=d.severity,
                file_id=d.file_id,
                anchor=d.anchor,
                related_file_id=d.related_file_id,
                related_anchor=d.related_anchor,
                message=d.message,
                suggestion=d.suggestion,
                status="open",
                fingerprint=fp,
                confidence=d.confidence,
            )
        )
        inserted += 1

    await db.flush()

    # Compute open issues + health score.
    open_result = await db.execute(
        select(ValidationIssue).where(
            ValidationIssue.project_id == project_id,
            ValidationIssue.status == "open",
        )
    )
    open_issues = list(open_result.scalars().all())
    run.issues_open = len(open_issues)

    # Project-wide anchor count is the denominator of the coverage score.
    project_index = await build_project_index(db, project_id)
    total_anchors = len(project_index.anchor_to_file)
    run.health_score = _compute_health_score(open_issues, total_anchors)

    await db.flush()
    return run


async def background_run_after_save(project_id: int, file_id: int) -> None:
    """Background entry point used by the chat WebSocket file-save flow."""
    from app.database import async_session

    async with async_session() as db:
        try:
            # System user_id=0 → no LLM lookup; rule-based only.
            await run_validation(
                db,
                project_id=project_id,
                user_id=0,
                scope="file",
                file_id=file_id,
                triggered_by="auto-on-save",
                include_llm_rules=False,
            )
            await db.commit()
        except Exception:
            await db.rollback()


# --- Read helpers used by the API -------------------------------------------

async def get_latest_run(db: AsyncSession, project_id: int) -> ValidationRun | None:
    # Tie-break on id so back-to-back runs (same created_at second) still resolve
    # deterministically to the most recently inserted row.
    result = await db.execute(
        select(ValidationRun)
        .where(ValidationRun.project_id == project_id)
        .order_by(ValidationRun.created_at.desc(), ValidationRun.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_issue_counts_by_file(db: AsyncSession, project_id: int) -> dict[int, dict]:
    """Per-file open-issue count, grouped by severity. Used for FileTree badges."""
    result = await db.execute(
        select(ValidationIssue).where(
            ValidationIssue.project_id == project_id,
            ValidationIssue.status == "open",
        )
    )
    out: dict[int, dict] = {}
    for issue in result.scalars().all():
        if issue.file_id is None:
            continue
        bucket = out.setdefault(issue.file_id, {"error": 0, "warning": 0, "info": 0})
        bucket[issue.severity] = bucket.get(issue.severity, 0) + 1
    return out
