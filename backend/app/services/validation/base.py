"""Base classes for validation rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class IssueDraft:
    """A finding produced by a rule. Persisted as ValidationIssue rows."""

    rule_id: str
    severity: str  # error | warning | info
    message: str
    file_id: int | None = None
    anchor: str | None = None
    related_file_id: int | None = None
    related_anchor: str | None = None
    suggestion: str | None = None
    confidence: float = 1.0

    def fingerprint(self) -> str:
        """Stable identity used to detect resolved/duplicate issues across runs."""
        return "|".join(
            [
                self.rule_id,
                str(self.file_id or ""),
                self.anchor or "",
                str(self.related_file_id or ""),
                self.related_anchor or "",
            ]
        )


@dataclass
class RuleContext:
    """Everything a rule needs: DB session + project id + the LLM config tuple."""

    db: AsyncSession
    project_id: int
    user_id: int
    llm: tuple[str, str, str, str | None] | None = None  # (provider, model, api_key, base_url)


@dataclass
class Rule:
    id: str
    severity: str  # default severity for issues this rule produces
    description: str
    is_llm: bool
    check: Callable[[RuleContext], Awaitable[list[IssueDraft]]]
    enabled: bool = True
    tags: list[str] = field(default_factory=list)
