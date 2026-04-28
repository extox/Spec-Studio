"""Rule registry — central catalog of validation rules."""

from __future__ import annotations

from app.services.validation.base import Rule
from app.services.validation.rules import (
    contradictory_terms,
    estimation_sanity,
    fr_covered_by_story,
    nfr_referenced_in_architecture,
    orphan_anchor,
    ux_flow_aligned_with_journey,
)


_REGISTRY: list[Rule] = [
    fr_covered_by_story.RULE,
    nfr_referenced_in_architecture.RULE,
    ux_flow_aligned_with_journey.RULE,
    orphan_anchor.RULE,
    estimation_sanity.RULE,
    contradictory_terms.RULE,
]


def all_rules(include_llm: bool = True) -> list[Rule]:
    return [r for r in _REGISTRY if r.enabled and (include_llm or not r.is_llm)]


def get_rule(rule_id: str) -> Rule | None:
    for r in _REGISTRY:
        if r.id == rule_id:
            return r
    return None
