"""Rule: every PRD FR must be covered by at least one Story.

An FR is "covered" when at least one TraceabilityLink connects it (as target)
to a Story file (as source).
"""

from sqlalchemy import select

from app.models.project_file import ProjectFile
from app.models.traceability_link import TraceabilityLink
from app.services.traceability_service import (
    detect_file_prefix,
    extract_anchors,
)
from app.services.validation.base import IssueDraft, Rule, RuleContext


async def _check(ctx: RuleContext) -> list[IssueDraft]:
    db = ctx.db

    files_result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == ctx.project_id)
    )
    files = list(files_result.scalars().all())

    prd_files = [f for f in files if detect_file_prefix(f.file_name) == "PRD"]
    if not prd_files:
        return []

    story_files = [f for f in files if detect_file_prefix(f.file_name) == "STORY"]
    story_file_ids = {f.id for f in story_files}

    # Count FR anchors that would need to be covered. Used both for the
    # "no story file at all" summary issue and as an early exit.
    fr_anchors: list[tuple[ProjectFile, str]] = []
    for prd in prd_files:
        for anchor in extract_anchors(prd):
            if anchor.startswith("FR-"):
                fr_anchors.append((prd, anchor))

    # Special case: PRD has FRs but the project has zero Story files.
    # Surface this as a single, explicit "no Story files exist" issue on the
    # first PRD so users understand they must run Create Story separately —
    # rather than drowning them in N identical "FR-xxx not covered" errors.
    if fr_anchors and not story_files:
        return [
            IssueDraft(
                rule_id="fr_covered_by_story",
                severity="error",
                message=(
                    f"No Story files found in `implementation-artifacts/` "
                    f"(PRD has {len(fr_anchors)} FR(s) needing coverage). "
                    "Stories described inside `epic.md` do NOT count — each "
                    "story must live in its own file like "
                    "`implementation-artifacts/E{n}-S{n}-{slug}.md`."
                ),
                file_id=prd_files[0].id,
                anchor=None,
                suggestion=(
                    "Run the Create Story workflow for each story listed in "
                    "epic.md to generate the per-story files (with "
                    "`derived_from: PRD#FR-xxx` markers). Create Epics & "
                    "Stories alone only outlines stories inside epic.md."
                ),
            )
        ]

    links_result = await db.execute(
        select(TraceabilityLink).where(TraceabilityLink.project_id == ctx.project_id)
    )
    links = list(links_result.scalars().all())

    # Set of (target_file_id, target_anchor) covered by any Story.
    covered: set[tuple[int, str]] = set()
    for l in links:
        if l.source_file_id in story_file_ids:
            covered.add((l.target_file_id, l.target_anchor))

    issues: list[IssueDraft] = []
    for prd, anchor in fr_anchors:
        if (prd.id, anchor) in covered:
            continue
        issues.append(
            IssueDraft(
                rule_id="fr_covered_by_story",
                severity="error",
                message=f"FR `{anchor}` in PRD has no Story covering it.",
                file_id=prd.id,
                anchor=anchor,
                suggestion=(
                    "Create a Story whose `derived_from` marker references "
                    f"`PRD#{anchor}`, or mark the FR as deferred."
                ),
            )
        )
    return issues


RULE = Rule(
    id="fr_covered_by_story",
    severity="error",
    description="Every PRD FR must be covered by at least one Story.",
    is_llm=False,
    check=_check,
    tags=["coverage", "prd", "story"],
)
