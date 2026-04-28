"""Rule: each PRD NFR should be referenced by at least one Architecture component or ADR."""

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

    prd_files = [f for f in files if detect_file_prefix(f.file_name) == "PRD"]
    arch_file_ids = {f.id for f in files if detect_file_prefix(f.file_name) == "ARCH"}
    if not prd_files or not arch_file_ids:
        return []

    links_result = await db.execute(
        select(TraceabilityLink).where(TraceabilityLink.project_id == ctx.project_id)
    )
    links = list(links_result.scalars().all())

    referenced: set[tuple[int, str]] = set()
    for l in links:
        if l.source_file_id in arch_file_ids:
            referenced.add((l.target_file_id, l.target_anchor))

    issues: list[IssueDraft] = []
    for prd in prd_files:
        for anchor in extract_anchors(prd):
            if not anchor.startswith("NFR-"):
                continue
            if (prd.id, anchor) in referenced:
                continue
            issues.append(
                IssueDraft(
                    rule_id="nfr_referenced_in_architecture",
                    severity="warning",
                    message=f"NFR `{anchor}` is not referenced from the Architecture.",
                    file_id=prd.id,
                    anchor=anchor,
                    suggestion=(
                        "Add a `<!-- derived_from: PRD#" + anchor + " -->` marker under the "
                        "Architecture component or ADR that satisfies it."
                    ),
                )
            )
    return issues


RULE = Rule(
    id="nfr_referenced_in_architecture",
    severity="warning",
    description="Each PRD NFR should be referenced by an Architecture component or ADR.",
    is_llm=False,
    check=_check,
    tags=["coverage", "prd", "architecture"],
)
