"""LLM-based rule: detect contradictory or inconsistent terminology across artifacts.

Cheap one-shot call. Off by default if no LLM config is available.
"""

from __future__ import annotations

import json

from sqlalchemy import select

from app.llm.provider import non_stream_chat
from app.models.project_file import ProjectFile
from app.services.traceability_service import detect_file_prefix
from app.services.validation.base import IssueDraft, Rule, RuleContext


PROMPT = """\
You are a spec-consistency reviewer. Compare the following PRD and Architecture
documents. Find places where terminology, concepts, or constraints CONTRADICT
each other — same word used differently, mismatched assumptions, or conflicting
numbers.

## PRD
```
{prd}
```

## Architecture
```
{arch}
```

Return ONLY a JSON array. Each entry:
{{
  "anchor": "FR-001",                // PRD anchor when applicable, else null
  "related_anchor": "C-1",           // Architecture anchor when applicable, else null
  "message": "FR-001 says 'real-time' but C-1 uses batch ingestion (max 5min)",
  "confidence": 0.8
}}

Maximum 10 items. Skip items below confidence 0.6. If nothing is wrong, return [].
"""


async def _check(ctx: RuleContext) -> list[IssueDraft]:
    if ctx.llm is None:
        return []

    db = ctx.db
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == ctx.project_id)
    )
    files = list(result.scalars().all())

    prd = next((f for f in files if detect_file_prefix(f.file_name) == "PRD"), None)
    arch = next((f for f in files if detect_file_prefix(f.file_name) == "ARCH"), None)
    if not prd or not arch or not prd.content or not arch.content:
        return []

    provider, model, api_key, base_url = ctx.llm

    prompt = PROMPT.format(prd=prd.content[:20_000], arch=arch.content[:20_000])
    try:
        raw = await non_stream_chat(
            provider=provider, model=model, api_key=api_key,
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
        items = json.loads(raw)
    except Exception:
        return []
    if not isinstance(items, list):
        return []

    issues: list[IssueDraft] = []
    for item in items[:10]:
        try:
            message = str(item.get("message", "")).strip()
            confidence = float(item.get("confidence", 0.0))
            anchor = item.get("anchor") or None
            related_anchor = item.get("related_anchor") or None
        except (TypeError, ValueError):
            continue
        if confidence < 0.6 or not message:
            continue
        issues.append(
            IssueDraft(
                rule_id="contradictory_terms",
                severity="info",
                message=message,
                file_id=prd.id,
                anchor=anchor,
                related_file_id=arch.id,
                related_anchor=related_anchor,
                confidence=confidence,
            )
        )
    return issues


RULE = Rule(
    id="contradictory_terms",
    severity="info",
    description="LLM-based: find contradictions between PRD and Architecture.",
    is_llm=True,
    check=_check,
    tags=["consistency", "llm"],
)
