"""Rule: total story points should not exceed the parent epic's estimate.

Heuristic check — parses Story-level "Points: <n>" fields and compares against
Epic-level "Complexity"/"Points" fields if present. If the per-epic sum exceeds
twice the epic's stated complexity (T-shirt sizes converted to a numeric upper bound),
flag a warning.
"""

import re

from sqlalchemy import select

from app.models.project_file import ProjectFile
from app.services.traceability_service import detect_file_prefix
from app.services.validation.base import IssueDraft, Rule, RuleContext


_POINTS_RE = re.compile(r"\*\*Points:\*\*\s*([0-9]+)", re.IGNORECASE)
_EPIC_HEADING_RE = re.compile(r"^##\s+Epic\s+(\d+):", re.MULTILINE | re.IGNORECASE)
_COMPLEXITY_RE = re.compile(r"\*\*Complexity:\*\*\s*([SMLX]+)", re.IGNORECASE)

# T-shirt size → soft upper bound on story points.
SIZE_CAP = {"S": 8, "M": 21, "L": 55, "XL": 144}


async def _check(ctx: RuleContext) -> list[IssueDraft]:
    db = ctx.db
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == ctx.project_id)
    )
    files = list(result.scalars().all())

    epics_files = [f for f in files if detect_file_prefix(f.file_name) == "EPIC" and f.content]
    story_files = [f for f in files if detect_file_prefix(f.file_name) == "STORY" and f.content]
    if not epics_files:
        return []

    issues: list[IssueDraft] = []

    # Sum story points by epic_number from story file names: E{n}-S{n}-...
    points_by_epic: dict[int, int] = {}
    for s in story_files:
        m = re.match(r"^[Ee](\d+)-[Ss]\d+", s.file_name)
        if not m:
            continue
        epic_num = int(m.group(1))
        pts_match = _POINTS_RE.search(s.content or "")
        if pts_match:
            try:
                points_by_epic[epic_num] = points_by_epic.get(epic_num, 0) + int(pts_match.group(1))
            except ValueError:
                continue

    # Read epic complexity caps from the epics document.
    for ef in epics_files:
        content = ef.content or ""
        # Iterate epics by heading.
        for m in _EPIC_HEADING_RE.finditer(content):
            epic_num = int(m.group(1))
            tail = content[m.end(): m.end() + 1000]
            comp_match = _COMPLEXITY_RE.search(tail)
            if not comp_match:
                continue
            cap = SIZE_CAP.get(comp_match.group(1).upper())
            if not cap:
                continue
            actual = points_by_epic.get(epic_num, 0)
            if actual > cap * 2:  # 2x over T-shirt cap → warn
                issues.append(
                    IssueDraft(
                        rule_id="estimation_sanity",
                        severity="info",
                        message=(
                            f"Epic E-{epic_num:03d} stories sum to {actual} points, "
                            f"more than 2x the {comp_match.group(1).upper()} complexity cap (~{cap})."
                        ),
                        file_id=ef.id,
                        anchor=f"E-{epic_num:03d}",
                        suggestion="Consider splitting the epic or revising story estimates.",
                    )
                )
    return issues


RULE = Rule(
    id="estimation_sanity",
    severity="info",
    description="Sum of story points per epic should not vastly exceed its complexity cap.",
    is_llm=False,
    check=_check,
    tags=["estimation", "epic", "story"],
)
