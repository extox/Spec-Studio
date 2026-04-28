"""Bulk Story generator — fills missing Story files in one LLM pass per story.

Reads `planning-artifacts/epics.md` (or any planning-artifacts file with
`workflowType: 'epics'` / Epic+Story headings), parses the Epic→Story tree,
diffs against existing `implementation-artifacts/E*-S*-*.md` files, and asks
the LLM to draft a full Story body for each missing one. New files are created
through `file_service.create_file` so version history is recorded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_file import ProjectFile
from app.services import file_service


EPIC_HEADING_RE = re.compile(
    r"^##\s+Epic\s+(\d+)\s*[:.\-]?\s*(.*?)\s*(?:\(E[\-_]?(\d+)\))?\s*$",
    re.MULTILINE | re.IGNORECASE,
)
# Captures the exact epic anchor token (e.g., "E-001") that appears in body —
# used to format `EPIC#E-001` in the Story's derived_from marker so the
# Epic ↔ Story parent link materializes in the traceability graph.
EPIC_ANCHOR_IN_BODY_RE = re.compile(
    r"^##\s+Epic\s+(\d+).*?\(\s*(E[\-_]\d+)\s*\)",
    re.MULTILINE | re.IGNORECASE,
)
STORY_HEADING_RE = re.compile(
    r"^####\s+Story\s+(\d+)\.(\d+)\s*[:.\-]?\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
EXPLICIT_STORY_ID_RE = re.compile(r"\bE(\d+)\s*[-_]\s*S(\d+)\b", re.IGNORECASE)
EXISTING_STORY_PATH_RE = re.compile(
    r"implementation-artifacts/E(\d+)-S(\d+)[\-_].*\.md$", re.IGNORECASE
)


@dataclass
class StorySpec:
    epic_num: int
    epic_title: str
    story_num: int
    story_title: str
    raw_block: str

    @property
    def story_id(self) -> str:
        return f"E{self.epic_num}-S{self.story_num}"

    def slug(self) -> str:
        s = re.sub(r"[^A-Za-z0-9가-힣]+", "-", self.story_title.strip().lower())
        s = re.sub(r"-+", "-", s).strip("-")
        return s or "story"

    def file_path(self) -> str:
        return f"implementation-artifacts/{self.story_id}-{self.slug()}.md"


GENERATE_STORY_PROMPT = """You are a senior agile coach writing a single user story file in BMad-Method format.

# Story Identity
- ID: {story_id}
- Epic: E{epic_num} - {epic_title}
- Story Title: {story_title}

# Source Block (from epics.md)
{story_block}

# Cross-Document Context
## PRD
{prd}

## Architecture
{architecture}

## UX Spec
{ux_spec}

# Parent Epic Anchor (REQUIRED — always include in derived_from)
This story belongs to: EPIC#{parent_epic_anchor}
Always include `EPIC#{parent_epic_anchor}` in the `<!-- derived_from: ... -->` marker.

# Available Upstream Anchors (CRITICAL — also pick at least one PRD anchor and one ARCH anchor)
You MUST link this story to its parent Epic AND to at least one PRD requirement
AND one Architecture component using the `<!-- derived_from: ... -->` marker.
Pick from THIS LIST ONLY — do not invent IDs.

{anchor_inventory}

If none of the listed PRD/ARCH anchors clearly fit, pick the closest match by topic.
Never leave the marker as a literal placeholder.

# Output Format
Return ONLY the markdown body — no code fences, no preamble. Follow this template exactly:

# Story: {story_title}

<!-- derived_from: EPIC#{parent_epic_anchor}, PRD#<a real FR or NFR id from the inventory>, ARCH#<a real C or ADR id from the inventory> -->

**ID:** {story_id}
**Epic:** E{epic_num} - {epic_title}
**Points:** <integer estimate, default 5>
**Status:** backlog

---

## Story

**As a** <user type>,
**I want** <action>,
**So that** <benefit>.

## Acceptance Criteria

```gherkin
Scenario: <happy path>
  Given <context>
  When <action>
  Then <expected>

Scenario: <edge case>
  Given <context>
  When <action>
  Then <expected>

Scenario: Error - <error scenario>
  Given <context>
  When <action>
  Then <error result>
```

## Tasks / Subtasks

- [ ] 1. <task>
  - [ ] 1.1 <subtask>
- [ ] 2. <task>
- [ ] 3. Write unit tests
- [ ] 4. Write integration tests
- [ ] 5. Update documentation

## Dev Notes

### Architecture Patterns

<patterns derived from Architecture doc>

### Project Structure

```
src/
├── ...
```

### References

- PRD: <relevant FR/NFR ids>
- Architecture: <relevant ADR ids>
- UX Spec: <relevant section>
- Related Stories: <ids if any>

### Technical Guidance

<concrete implementation hints, libraries, gotchas>

---

## Dev Agent Record

| Field | Value |
|-------|-------|
| Model Used | |
| Start Time | |
| End Time | |
| Tasks Completed | / |
| Tests Passing | |

### Debug Log

### Completion Notes

### Files Modified

| File | Action | Description |
|------|--------|-------------|
| | | |

# Rules
- Fill EVERY placeholder concretely using the source block + cross-document context. No `<...>` left.
- Acceptance Criteria must include at least one happy path AND one error scenario.
- Tasks must be implementation-orderable (smallest concrete steps).
- If information is missing, infer reasonably and stay consistent with PRD/Architecture.
- Output the markdown body only.
"""


def _parse_epic_blocks(content: str) -> list[tuple[int, str, str]]:
    """Split epics.md content into (epic_num, epic_title, block_text) tuples."""
    if not content:
        return []
    matches = list(EPIC_HEADING_RE.finditer(content))
    if not matches:
        return []
    out: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        epic_num = int(m.group(3) or m.group(1))
        epic_title = (m.group(2) or "").strip() or f"Epic {epic_num}"
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end]
        out.append((epic_num, epic_title, block))
    return out


def _parse_stories_in_epic(
    epic_num: int, epic_title: str, block: str
) -> list[StorySpec]:
    out: list[StorySpec] = []
    headings = list(STORY_HEADING_RE.finditer(block))
    for i, m in enumerate(headings):
        epic_idx = int(m.group(1))
        story_idx = int(m.group(2))
        title = m.group(3).strip()
        # Use epic_num from outer scope; if heading numbering disagrees, prefer epic_num.
        start = m.start()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(block)
        raw = block[start:end].strip()
        # Story number = the second heading number (e.g. "Story 1.3" → 3).
        out.append(
            StorySpec(
                epic_num=epic_num if epic_idx != epic_num else epic_idx,
                epic_title=epic_title,
                story_num=story_idx,
                story_title=title,
                raw_block=raw,
            )
        )
    return out


def parse_story_specs(epics_content: str) -> list[StorySpec]:
    """Public entrypoint: extract every StorySpec declared inside epics.md."""
    specs: list[StorySpec] = []
    for epic_num, epic_title, block in _parse_epic_blocks(epics_content):
        specs.extend(_parse_stories_in_epic(epic_num, epic_title, block))
    return specs


def parse_epic_anchor_map(epics_content: str) -> dict[int, str]:
    """Map `epic_num` (1, 2, ...) → exact anchor token in epics.md (`E-001`).

    The Story's `derived_from` marker must use the EXACT anchor string the
    EPIC file owns, otherwise `index.resolve("EPIC", anchor)` returns None
    and the link is silently dropped.
    """
    out: dict[int, str] = {}
    if not epics_content:
        return out
    for m in EPIC_ANCHOR_IN_BODY_RE.finditer(epics_content):
        try:
            out[int(m.group(1))] = m.group(2).upper().replace("_", "-")
        except (TypeError, ValueError):
            continue
    return out


async def _load_planning_files(
    db: AsyncSession, project_id: int
) -> dict[str, ProjectFile]:
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = list(result.scalars().all())
    out: dict[str, ProjectFile] = {}
    for f in files:
        out[f.file_path] = f
    return out


def _find_first(files: dict[str, ProjectFile], *keywords: str) -> ProjectFile | None:
    """Return the first file whose path contains any of the keywords (case-insensitive)."""
    for path, f in files.items():
        lower = path.lower()
        if any(k in lower for k in keywords):
            return f
    return None


def _existing_story_keys(files: Iterable[ProjectFile]) -> set[str]:
    out: set[str] = set()
    for f in files:
        m = EXISTING_STORY_PATH_RE.search(f.file_path or "")
        if m:
            out.add(f"E{int(m.group(1))}-S{int(m.group(2))}")
    return out


async def _get_user_llm_config(
    db: AsyncSession, project_id: int, user_id: int
):
    """Same fallback chain as bolt_service: user default → project owner default."""
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


VALID_DERIVED_FROM_RE = re.compile(
    r"<!--\s*derived_from\s*:\s*"
    r"(?:[A-Z]+\s*#\s*[A-Z][A-Z0-9_\-]*?-\d+(?:\s*,\s*[A-Z]+\s*#\s*[A-Z][A-Z0-9_\-]*?-\d+)*|"
    r"[A-Z]+\s*#\s*E\d+-S\d+(?:\s*,\s*[A-Z]+\s*#\s*[A-Z][A-Z0-9_\-]*?-\d+)*)"
    r"\s*-->",
    re.IGNORECASE,
)
PLACEHOLDER_DERIVED_RE = re.compile(
    r"<!--\s*derived_from\s*:[^>]*?(?:#FR-\.\.\.|#\.\.\.|#<[^>]*>|#XXX|#YYY)[^>]*?-->",
    re.IGNORECASE,
)


def _ensure_derived_from(
    body: str,
    prd_anchors: list[str],
    arch_anchors: list[str],
    epic_anchor: str | None = None,
) -> str:
    """Make sure the story body declares its parent links.

    A Story is linked to upstream artifacts ONLY through `<!-- derived_from -->`
    markers. The marker MUST resolve to anchors owned by upstream files:
    - EPIC#<E-001>  — the parent epic (mandatory if available — drives the
      Epic ↔ Story tree visualization)
    - PRD#<FR-...>  — the requirement this story implements
    - ARCH#<C-...>  — the component/ADR this story builds against

    Strategy:
    - Strip placeholder-only markers like `PRD#FR-...`.
    - If a fully-valid marker already exists AND it includes an EPIC reference,
      keep the body untouched. Otherwise we add our own marker so the graph at
      least gets one EPIC link.
    """
    cleaned = PLACEHOLDER_DERIVED_RE.sub("", body)

    needs_inject = True
    for m in VALID_DERIVED_FROM_RE.finditer(cleaned):
        marker_text = m.group(0)
        if epic_anchor is None or "EPIC#" in marker_text.upper():
            needs_inject = False
            break

    if not needs_inject:
        return cleaned

    parts: list[str] = []
    if epic_anchor:
        parts.append(f"EPIC#{epic_anchor}")
    if prd_anchors:
        parts.append(f"PRD#{prd_anchors[0]}")
    if arch_anchors:
        parts.append(f"ARCH#{arch_anchors[0]}")
    if not parts:
        return cleaned  # nothing to point at

    marker = f"<!-- derived_from: {', '.join(parts)} -->"

    # Insert after the first H1 line if present, otherwise at the very top.
    lines = cleaned.split("\n")
    inserted = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("# ") and not line.lstrip().startswith("## "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, marker)
            inserted = True
            break
    if not inserted:
        lines = [marker, ""] + lines
    return "\n".join(lines)


def _strip_code_fence(s: str) -> str:
    s = s.strip()
    if s.startswith("```markdown"):
        s = s[len("```markdown"):].lstrip("\n")
    elif s.startswith("```md"):
        s = s[len("```md"):].lstrip("\n")
    elif s.startswith("```"):
        s = s[3:].lstrip("\n")
    if s.endswith("```"):
        s = s[:-3].rstrip()
    return s.strip()


async def list_epics_with_story_counts(
    db: AsyncSession, project_id: int
) -> dict:
    """Return Epic summary with story counts so the UI can offer per-Epic generation.

    Shape: { epics: [{ epic_num, epic_title, total, missing }], error?: str }
    """
    files_by_path = await _load_planning_files(db, project_id)
    epics_file = _find_first(
        files_by_path, "planning-artifacts/epics.md", "/epic.md", "/epics.md"
    )
    if not epics_file or not epics_file.content:
        return {"epics": [], "error": "epics.md not found"}

    specs = parse_story_specs(epics_file.content)
    if not specs:
        return {"epics": [], "error": "no stories detected in epics.md"}

    existing = _existing_story_keys(files_by_path.values())
    by_epic: dict[int, dict] = {}
    for s in specs:
        slot = by_epic.setdefault(
            s.epic_num,
            {"epic_num": s.epic_num, "epic_title": s.epic_title, "total": 0, "missing": 0},
        )
        slot["total"] += 1
        if s.story_id not in existing:
            slot["missing"] += 1
    return {"epics": [by_epic[k] for k in sorted(by_epic)]}


async def generate_all_missing_stories(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    epic_num: int | None = None,
    max_stories: int | None = None,
) -> dict:
    """Generate Story files for every Story in epics.md that doesn't yet have a file.

    If `epic_num` is given, only that Epic's missing stories are generated.
    If `max_stories` is given, generation stops after that many created stories
    (handy when the LLM is rate-limited; the user can re-click to continue).

    Returns: { created: [...], skipped: [...], failed: [...], error?: str }.
    """
    from app.llm.provider import non_stream_chat

    files_by_path = await _load_planning_files(db, project_id)
    if not files_by_path:
        return {"created": [], "skipped": [], "failed": [], "error": "no project files"}

    epics_file = _find_first(
        files_by_path, "planning-artifacts/epics.md", "/epic.md", "/epics.md"
    )
    if not epics_file or not epics_file.content:
        return {
            "created": [],
            "skipped": [],
            "failed": [],
            "error": "epics.md not found in planning-artifacts",
        }

    specs = parse_story_specs(epics_file.content)
    epic_anchor_map = parse_epic_anchor_map(epics_file.content)
    if epic_num is not None:
        specs = [s for s in specs if s.epic_num == epic_num]
    if not specs:
        return {
            "created": [],
            "skipped": [],
            "failed": [],
            "error": (
                f"no stories detected for Epic {epic_num}"
                if epic_num is not None
                else "no stories detected in epics.md"
            ),
        }

    existing_keys = _existing_story_keys(files_by_path.values())

    cfg = await _get_user_llm_config(db, project_id, user_id)
    if not cfg:
        return {
            "created": [],
            "skipped": [],
            "failed": [],
            "error": "no LLM config available",
        }
    provider, model, api_key, base_url = cfg

    prd_file = _find_first(files_by_path, "/prd.md", "planning-artifacts/prd")
    arch_file = _find_first(
        files_by_path, "/architecture.md", "solutioning-artifacts/architecture"
    )
    ux_file = _find_first(
        files_by_path, "/ux-spec.md", "solutioning-artifacts/ux-spec", "ux_spec.md"
    )
    prd_text = (prd_file.content or "")[:8000] if prd_file else "(not provided)"
    arch_text = (arch_file.content or "")[:8000] if arch_file else "(not provided)"
    ux_text = (ux_file.content or "")[:5000] if ux_file else "(not provided)"

    # Build the upstream anchor inventory so the LLM picks real IDs for the
    # `<!-- derived_from: EPIC#..., PRD#..., ARCH#... -->` marker that drives
    # traceability.
    from app.services.traceability_service import (
        extract_anchors,
        rebuild_explicit_links_for_file,
    )

    prd_anchors = extract_anchors(prd_file) if prd_file else []
    arch_anchors = extract_anchors(arch_file) if arch_file else []
    ux_anchors = extract_anchors(ux_file) if ux_file else []
    inv_lines: list[str] = []
    if epic_anchor_map:
        inv_lines.append("EPIC anchors (parent — use the one matching this story's epic_num):")
        for num in sorted(epic_anchor_map):
            inv_lines.append(f"- EPIC#{epic_anchor_map[num]}  (Epic {num})")
    if prd_anchors:
        inv_lines.append("PRD anchors:")
        inv_lines.extend(f"- PRD#{a}" for a in prd_anchors[:80])
    if arch_anchors:
        inv_lines.append("ARCH anchors:")
        inv_lines.extend(f"- ARCH#{a}" for a in arch_anchors[:80])
    if ux_anchors:
        inv_lines.append("UX anchors:")
        inv_lines.extend(f"- UX#{a}" for a in ux_anchors[:40])
    anchor_inventory = (
        "\n".join(inv_lines) if inv_lines else "(no upstream anchors detected)"
    )

    created: list[dict] = []
    skipped: list[dict] = []
    failed: list[dict] = []

    for spec in specs:
        if max_stories is not None and len(created) >= max_stories:
            skipped.append(
                {"story_id": spec.story_id, "reason": "max_stories reached"}
            )
            continue
        if spec.story_id in existing_keys:
            skipped.append({"story_id": spec.story_id, "reason": "already exists"})
            continue

        parent_epic_anchor = epic_anchor_map.get(
            spec.epic_num, f"E-{spec.epic_num:03d}"
        )
        prompt = GENERATE_STORY_PROMPT.format(
            story_id=spec.story_id,
            epic_num=spec.epic_num,
            epic_title=spec.epic_title,
            story_title=spec.story_title,
            story_block=spec.raw_block[:4000],
            prd=prd_text,
            architecture=arch_text,
            ux_spec=ux_text,
            anchor_inventory=anchor_inventory,
            parent_epic_anchor=parent_epic_anchor,
        )

        try:
            raw = await non_stream_chat(
                provider=provider,
                model=model,
                api_key=api_key,
                messages=[
                    {
                        "role": "system",
                        "content": "Output ONLY the markdown body — no code fences, no preamble.",
                    },
                    {"role": "user", "content": prompt},
                ],
                base_url=base_url,
            )
        except Exception as e:
            failed.append({"story_id": spec.story_id, "reason": f"llm error: {e}"})
            continue

        body = _strip_code_fence(raw or "")
        if not body or "**Status:**" not in body:
            failed.append(
                {"story_id": spec.story_id, "reason": "empty or malformed LLM output"}
            )
            continue

        # Safety net: if the LLM forgot/mangled the derived_from marker, inject
        # one using the inventory so the story is at least linked to its
        # parent EPIC, one PRD anchor, and one ARCH anchor. Without the EPIC
        # link the story shows up disconnected from its parent epic in the
        # traceability graph (filename E1-S1 alone is not enough — links are
        # driven only by explicit `<!-- derived_from -->` markers).
        # Pass the resolvable epic anchor (None if epics.md doesn't declare
        # this epic_num explicitly) so we never inject an unresolvable target.
        body = _ensure_derived_from(
            body,
            prd_anchors,
            arch_anchors,
            epic_anchor=epic_anchor_map.get(spec.epic_num),
        )

        path = spec.file_path()
        if path in files_by_path:
            skipped.append({"story_id": spec.story_id, "reason": "path collision"})
            continue

        try:
            saved = await file_service.create_file(
                db,
                project_id=project_id,
                user_id=user_id,
                file_path=path,
                file_name=path.rsplit("/", 1)[-1],
                file_type="deliverable",
                content=body,
            )
            files_by_path[path] = saved
            existing_keys.add(spec.story_id)
            created.append(
                {
                    "story_id": spec.story_id,
                    "file_path": path,
                    "file_id": saved.id,
                    "title": spec.story_title,
                }
            )
        except Exception as e:
            failed.append(
                {"story_id": spec.story_id, "reason": f"save error: {e}"}
            )

    # NOTE: do NOT call db.commit() here — FastAPI's get_db() dependency
    # commits at the end of the request. Calling commit twice can leave the
    # session in an unexpected state on some SQLAlchemy versions.

    # Materialize traceability links from the `<!-- derived_from: ... -->`
    # markers inserted into each new story file. Without this, the stories
    # appear as orphaned nodes in the traceability graph because the
    # extract→TraceabilityLink pipeline only runs through file_save_helper,
    # which we bypassed in favor of file_service.create_file.
    rebuilt = 0
    for c in created:
        try:
            rebuilt += await rebuild_explicit_links_for_file(
                db, project_id, c["file_id"]
            )
        except Exception:
            # Traceability is auxiliary — never let a rebuild failure mask
            # a successful story generation.
            pass

    return {
        "created": created,
        "skipped": skipped,
        "failed": failed,
        "links_rebuilt": rebuilt,
    }
