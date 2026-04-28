"""Bolt service — sprint → bolts decomposition + state transitions + activity log.

Bolt lifecycle:
    todo  ──start──▶  in_bolt  ──complete──▶  awaiting_approval ──approve──▶  done
                          │                                                    ▲
                          └────────────────block────────────────▶ blocked ─────┘
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bolt import Bolt, BoltActivity
from app.models.project_file import ProjectFile


# --- Activity log ------------------------------------------------------------

async def log_activity(
    db: AsyncSession,
    bolt_id: int,
    event_type: str,
    payload: dict | None = None,
    actor_user_id: int | None = None,
) -> BoltActivity:
    activity = BoltActivity(
        bolt_id=bolt_id,
        event_type=event_type,
        payload=json.dumps(payload, ensure_ascii=False) if payload is not None else None,
        actor_user_id=actor_user_id,
    )
    db.add(activity)
    await db.flush()
    return activity


# --- State transitions -------------------------------------------------------

async def start_bolt(db: AsyncSession, bolt: Bolt, user_id: int) -> Bolt:
    if bolt.status not in ("todo", "blocked"):
        raise ValueError(f"Cannot start bolt in status '{bolt.status}'")
    bolt.status = "in_bolt"
    bolt.started_at = datetime.now(timezone.utc)
    bolt.blocker_reason = None
    await db.flush()
    await log_activity(db, bolt.id, "status_change", {"to": "in_bolt"}, user_id)
    return bolt


async def complete_bolt(db: AsyncSession, bolt: Bolt, user_id: int, notes: str | None = None) -> Bolt:
    if bolt.status != "in_bolt":
        raise ValueError(f"Cannot complete bolt in status '{bolt.status}'")
    bolt.status = "awaiting_approval" if bolt.approval_required else "done"
    bolt.completed_at = datetime.now(timezone.utc)
    if notes:
        bolt.notes = notes
    await db.flush()
    await log_activity(
        db, bolt.id, "status_change", {"to": bolt.status, "notes": notes}, user_id
    )
    return bolt


async def approve_bolt(db: AsyncSession, bolt: Bolt, user_id: int) -> Bolt:
    if bolt.status != "awaiting_approval":
        raise ValueError(f"Cannot approve bolt in status '{bolt.status}'")
    bolt.status = "done"
    bolt.approved_by = user_id
    bolt.approved_at = datetime.now(timezone.utc)
    await db.flush()
    await log_activity(db, bolt.id, "approval", {"approved_by": user_id}, user_id)
    return bolt


async def block_bolt(db: AsyncSession, bolt: Bolt, user_id: int, reason: str) -> Bolt:
    if bolt.status not in ("todo", "in_bolt"):
        raise ValueError(f"Cannot block bolt in status '{bolt.status}'")
    bolt.status = "blocked"
    bolt.blocker_reason = reason
    await db.flush()
    await log_activity(db, bolt.id, "status_change", {"to": "blocked", "reason": reason}, user_id)
    return bolt


async def unblock_bolt(db: AsyncSession, bolt: Bolt, user_id: int) -> Bolt:
    if bolt.status != "blocked":
        raise ValueError(f"Cannot unblock bolt in status '{bolt.status}'")
    bolt.status = "todo"
    bolt.blocker_reason = None
    await db.flush()
    await log_activity(db, bolt.id, "status_change", {"to": "todo"}, user_id)
    return bolt


# --- Active-bolt lookup (used by chat to attach activities) ------------------

async def get_active_bolt_for_project(db: AsyncSession, project_id: int) -> Bolt | None:
    """Return the single Bolt currently in `in_bolt` status, or None.

    There should be at most one active bolt per project at a time.
    """
    result = await db.execute(
        select(Bolt).where(
            Bolt.project_id == project_id,
            Bolt.status == "in_bolt",
        ).limit(1)
    )
    return result.scalar_one_or_none()


# --- Sprint → Bolts decomposition --------------------------------------------

PLAN_BOLTS_PROMPT = """\
You are a Scrum facilitator decomposing a Sprint plan into "Bolts" — short,
intense work cycles 1–3 hours long. Each Bolt focuses on ONE story (or a small
slice of a story) and produces ONE concrete deliverable.

## Sprint plan
```
{sprint_content}
```

## Available stories (with anchors)
{story_lines}

## Task
Produce a JSON array of bolts. Each bolt:
{{
  "title": "E1-S3 — login form scaffolding",
  "story_anchor": "E1-S3",
  "persona_id": "developer",       // developer | qa-engineer | devops-engineer | scrum-master
  "workflow_id": "generate-code-skeleton",  // exact workflow id; null if none
  "estimated_minutes": 90,         // 30..180
  "approval_required": true
}}

Rules:
- Cover ONLY stories that appear in the Sprint plan as ready-for-dev or in-progress.
- For each ready story, propose ONE bolt for code skeleton AND ONE bolt for test plan.
- Estimate honestly — small stories get 30-60 minutes; large get 120-180.
- Output ONLY the JSON array. No prose.
"""


async def _get_sprint_status_file(db: AsyncSession, project_id: int) -> ProjectFile | None:
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.file_path.like("%sprint-status%"),
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def _list_story_files(db: AsyncSession, project_id: int) -> list[ProjectFile]:
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.file_path.like("implementation-artifacts/E%-S%"),
        )
    )
    return list(result.scalars().all())


async def _get_user_llm_config(db: AsyncSession, project_id: int, user_id: int):
    """Same fallback chain as traceability_service: user default → project owner default."""
    from app.models.llm_config import LLMConfig
    from app.models.project_member import ProjectMember
    from app.core.security import decrypt_api_key

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


async def plan_bolts_from_sprint(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> list[Bolt]:
    """Use the LLM to break the current sprint into Bolts and persist them.

    Returns the list of newly created Bolts. If no sprint file exists or the
    LLM call fails, returns []. Existing `todo`/`blocked` bolts are NOT
    deleted — newly planned bolts are appended.
    """
    from app.llm.provider import non_stream_chat

    sprint_file = await _get_sprint_status_file(db, project_id)
    if not sprint_file or not sprint_file.content:
        return []

    story_files = await _list_story_files(db, project_id)
    if not story_files:
        return []
    story_lines = "\n".join(
        f"- {f.file_name}" for f in story_files if f.content
    )

    cfg = await _get_user_llm_config(db, project_id, user_id)
    if not cfg:
        return []
    provider, model, api_key, base_url = cfg

    sprint_content = sprint_file.content[:20_000]
    prompt = PLAN_BOLTS_PROMPT.format(
        sprint_content=sprint_content,
        story_lines=story_lines,
    )

    try:
        raw = await non_stream_chat(
            provider=provider,
            model=model,
            api_key=api_key,
            messages=[
                {"role": "system", "content": "Output ONLY a valid JSON array."},
                {"role": "user", "content": prompt},
            ],
            base_url=base_url,
        )
    except Exception:
        return []

    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    elif raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    try:
        proposals = json.loads(raw)
    except Exception:
        return []
    if not isinstance(proposals, list):
        return []

    # Resolve next bolt_number for this project.
    max_result = await db.execute(
        select(func.max(Bolt.bolt_number)).where(Bolt.project_id == project_id)
    )
    next_number = (max_result.scalar_one_or_none() or 0) + 1

    created: list[Bolt] = []
    valid_personas = {"developer", "qa-engineer", "devops-engineer", "scrum-master", "architect"}
    for p in proposals:
        try:
            title = str(p["title"])[:200]
            story_anchor = (str(p.get("story_anchor")) if p.get("story_anchor") else None)
            persona_id = str(p.get("persona_id", "developer"))
            if persona_id not in valid_personas:
                persona_id = "developer"
            workflow_id = (str(p.get("workflow_id")) if p.get("workflow_id") else None)
            est_min = int(p.get("estimated_minutes", 60))
            est_min = max(15, min(240, est_min))
            approval_required = bool(p.get("approval_required", True))
        except (KeyError, TypeError, ValueError):
            continue

        bolt = Bolt(
            project_id=project_id,
            sprint_id=sprint_file.file_name,
            bolt_number=next_number,
            title=title,
            story_anchor=story_anchor,
            persona_id=persona_id,
            workflow_id=workflow_id,
            status="todo",
            estimated_minutes=est_min,
            approval_required=approval_required,
            created_by=user_id,
        )
        db.add(bolt)
        await db.flush()
        await log_activity(db, bolt.id, "checkpoint", {"event": "planned", "source": "sprint"}, user_id)
        created.append(bolt)
        next_number += 1

    return created


# --- Velocity / metrics ------------------------------------------------------

async def get_velocity(db: AsyncSession, project_id: int, days: int = 7) -> dict:
    """Return per-day count of bolts completed within `days`."""
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    result = await db.execute(
        select(Bolt).where(
            Bolt.project_id == project_id,
            Bolt.status == "done",
            Bolt.completed_at >= cutoff,
        )
    )
    bolts = list(result.scalars().all())
    by_day: dict[str, int] = {}
    for b in bolts:
        if not b.completed_at:
            continue
        key = b.completed_at.strftime("%Y-%m-%d")
        by_day[key] = by_day.get(key, 0) + 1
    return {"days": by_day, "total_completed": len(bolts)}
