"""Rule: every UX User Flow (UF-) should derive from at least one PRD User Journey (UJ-)."""

from sqlalchemy import select

from app.models.project_file import ProjectFile
from app.models.traceability_link import TraceabilityLink
from app.services.traceability_service import detect_file_prefix, extract_anchors
from app.services.validation.base import IssueDraft, Rule, RuleContext


async def _check(ctx: RuleContext) -> list[IssueDraft]:
    db = ctx.db

    files_result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == ctx.project_id)
    )
    files = list(files_result.scalars().all())

    ux_files = [f for f in files if detect_file_prefix(f.file_name) == "UX"]
    prd_file_ids = {f.id for f in files if detect_file_prefix(f.file_name) == "PRD"}
    if not ux_files or not prd_file_ids:
        return []

    links_result = await db.execute(
        select(TraceabilityLink).where(TraceabilityLink.project_id == ctx.project_id)
    )
    links = list(links_result.scalars().all())

    issues: list[IssueDraft] = []
    for ux in ux_files:
        ux_links = [l for l in links if l.source_file_id == ux.id]
        for anchor in extract_anchors(ux):
            if not anchor.startswith("UF-"):
                continue
            # Does this anchor have a derived_from that targets PRD UJ-?
            has_uj = any(
                l.source_anchor == anchor
                and l.target_file_id in prd_file_ids
                and l.target_anchor.startswith("UJ-")
                for l in ux_links
            )
            if not has_uj:
                issues.append(
                    IssueDraft(
                        rule_id="ux_flow_aligned_with_journey",
                        severity="warning",
                        message=f"User flow `{anchor}` is not linked to any PRD User Journey (UJ-).",
                        file_id=ux.id,
                        anchor=anchor,
                        suggestion=(
                            "Add a `<!-- derived_from: PRD#UJ-XXX -->` marker under the flow heading."
                        ),
                    )
                )
    return issues


RULE = Rule(
    id="ux_flow_aligned_with_journey",
    severity="warning",
    description="Every UX User Flow should derive from at least one PRD User Journey.",
    is_llm=False,
    check=_check,
    tags=["coverage", "ux", "prd"],
)
