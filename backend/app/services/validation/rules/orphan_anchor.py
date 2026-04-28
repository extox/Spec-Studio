"""Rule: anchors that are referenced by no traceability link in either direction."""

from app.services.traceability_service import get_orphan_anchors
from app.services.validation.base import IssueDraft, Rule, RuleContext


async def _check(ctx: RuleContext) -> list[IssueDraft]:
    orphans = await get_orphan_anchors(ctx.db, ctx.project_id)
    issues: list[IssueDraft] = []
    for o in orphans:
        # Skip benign anchors that are not interesting orphans.
        if o["prefix"] in ("BRIEF", "SPRINT"):
            continue
        issues.append(
            IssueDraft(
                rule_id="orphan_anchor",
                severity="info",
                message=f"Anchor `{o['prefix']}#{o['anchor']}` is not connected to any other artifact.",
                file_id=o["file_id"],
                anchor=o["anchor"],
                suggestion=(
                    "Add a derived_from marker linking this anchor to upstream/downstream "
                    "artifacts, or remove it if it is no longer needed."
                ),
            )
        )
    return issues


RULE = Rule(
    id="orphan_anchor",
    severity="info",
    description="Surface anchors that are not part of any traceability chain.",
    is_llm=False,
    check=_check,
    tags=["traceability"],
)
