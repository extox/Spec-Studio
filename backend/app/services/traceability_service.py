"""Traceability service: anchor extraction, link parsing, LLM-based link suggestion.

Anchors are stable IDs embedded in artifacts (FR-001, NFR-002, ADR-001, C-1, UF-001,
CMP-001, UJ-001, E-001, S-001, E1-S3, ...).

Source of truth for links:
1. **Explicit** — `<!-- derived_from: PRD#FR-001, ARCH#C-1 -->` HTML comments placed
   immediately after a heading. Re-extracted on every file save (origin='explicit').
2. **Suggested** — produced by an LLM call comparing anchors across artifacts
   (origin='suggested', has confidence < 1.0).
3. **Manual** — created by the user via UI (origin='manual').
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_file import ProjectFile
from app.models.traceability_link import TraceabilityLink


# --- File-type mapping --------------------------------------------------------

# Map filename keywords to a "type prefix" used in derived_from markers.
# The same mapping resolves derived_from prefix back to a file in the project.
FILE_TYPE_PREFIXES: dict[str, list[str]] = {
    "PRD": ["prd"],
    "BRIEF": ["product-brief", "brief"],
    "ARCH": ["architecture", "arch"],
    "UX": ["ux-spec", "ux"],
    "EPIC": ["epics", "epic"],
    "STORY": ["story"],
    "SPRINT": ["sprint-status", "sprint"],
}


def detect_file_prefix(file_name: str) -> str | None:
    """Return the canonical type prefix (PRD, ARCH, ...) for a given file name.

    Story files use dynamic naming (E1-S3-user-login.md) — those resolve to STORY.
    Returns None if no known artifact type is detected.
    """
    name = file_name.lower()
    # Story dynamic naming: E{n}-S{n}-... takes precedence over generic 'epic'/'sprint'.
    if re.match(r"^e\d+-s\d+", name):
        return "STORY"
    for prefix, keywords in FILE_TYPE_PREFIXES.items():
        for kw in keywords:
            if kw in name:
                return prefix
    return None


# --- Anchor extraction --------------------------------------------------------

# Top-level anchor regex. Matches FR-001, FR-1, NFR-12, ADR-001, C-1, UF-001,
# CMP-002, UJ-001, E-001, S-001, and the composite story anchor E1-S3.
ANCHOR_RE = re.compile(
    r"\b(?:E\d+-S\d+|(?:FR|NFR|UJ|ADR|UF|CMP|C|E|S)-\d+)\b"
)

# Match a derived_from marker. Inside, items are comma-separated PREFIX#ANCHOR.
DERIVED_FROM_RE = re.compile(
    r"<!--\s*derived_from\s*:\s*(.+?)\s*-->",
    re.IGNORECASE,
)

# Each item inside a derived_from marker: PREFIX#ANCHOR (case-insensitive prefix).
DERIVED_ITEM_RE = re.compile(
    r"\b([A-Z]+)\s*#\s*(E\d+-S\d+|(?:FR|NFR|UJ|ADR|UF|CMP|C|E|S)-\d+)\b",
    re.IGNORECASE,
)


@dataclass
class Anchor:
    """A stable anchor ID found in a file."""

    file_id: int
    file_name: str
    file_path: str
    file_prefix: str | None  # PRD / ARCH / UX / ...
    anchor: str  # FR-001 / C-1 / E1-S3 / ...


@dataclass
class ExplicitLink:
    """A link declared via a derived_from marker."""

    source_file_id: int
    source_anchor: str
    target_prefix: str  # PRD / ARCH / ...
    target_anchor: str
    rationale: str | None = None


# Per-file-type whitelist of anchor prefixes that the file is allowed to OWN.
# Anchors of any other prefix found in the file's body are treated as references
# to other artifacts, NOT as anchors owned by this file.
#
# Rationale: BMad artifacts routinely quote anchors that belong to upstream
# documents (e.g. epics.md tabulates every PRD FR; architecture.md lists which
# FRs each component addresses). Without this whitelist, those quotes get
# mis-attributed and explode the anchor count.
#
# Anchor prefix derivation:
#   - "E1-S1" form → prefix "E_S" (composite story id)
#   - "FR-001" form → prefix "FR"
#
# Note on EPIC: EPIC files (epics.md) only own their Epic-level IDs (E-001).
# Composite story IDs (E1-S1) are owned EXCLUSIVELY by STORY files, even
# though epics.md routinely lists those IDs inline under each Epic. Without
# this restriction, the same `E1-S1` anchor would appear as both an EPIC node
# and a STORY node in the traceability graph, which is confusing — there's no
# such thing as an "EPIC#E1-S1" entity; only "STORY#E1-S1".
OWNED_PREFIXES_BY_FILE_TYPE: dict[str, set[str]] = {
    "PRD": {"FR", "NFR", "UJ"},
    "BRIEF": {"FR", "NFR", "UJ"},
    "ARCH": {"C", "ADR", "CMP"},
    "EPIC": {"E", "S"},
    "STORY": {"E_S", "S"},
    "UX": {"UF", "UJ"},
    "SPRINT": set(),
}


def _anchor_owner_prefix(anchor: str) -> str:
    """Classify an anchor token into a coarse 'owner prefix' bucket."""
    if re.match(r"^E\d+-S\d+$", anchor):
        return "E_S"
    m = re.match(r"^([A-Z]+)-\d+$", anchor)
    return m.group(1) if m else ""


def extract_anchors(file: ProjectFile) -> list[str]:
    """Return the de-duplicated list of anchor IDs **owned by** this file.

    A file's *own* anchors must satisfy two conditions:
    1. The anchor's prefix is in this file type's OWNED_PREFIXES whitelist.
       This filters out cases like an EPIC file tabulating every PRD FR — the
       FRs there belong to the PRD, not the EPIC.
    2. The anchor doesn't appear inside a region we know is for external
       references: YAML frontmatter, HTML comments, or `PREFIX#ANCHOR` patterns.

    We strip the external-reference regions by masking with whitespace,
    preserving offsets so other code that uses anchor positions
    (extract_explicit_links etc.) is unaffected.
    """
    if not file.content:
        return []

    # STORY files own exactly ONE anchor: their storyId, taken from the
    # filename (E{n}-S{n}-slug.md). Anything else in the body — "Related
    # Stories: E1-S2, E2-S1", example anchors in comments, etc. — is a
    # reference to other artifacts, never an anchor owned by this file.
    if detect_file_prefix(file.file_name) == "STORY":
        m = re.match(r"^(E\d+-S\d+)", file.file_name)
        return [m.group(1)] if m else []

    content = file.content

    # 1) Mask YAML frontmatter at the top of the file ("---\n...\n---\n").
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            end += 4  # include closing "---"
            content = (" " * end) + content[end:]

    # 2) Mask ALL HTML comments — derived_from markers AND documentation
    # comments that contain example anchors in prose. extract_explicit_links()
    # runs against the raw content, so legitimate derived_from references are
    # still parsed correctly there.
    content = re.sub(
        r"<!--.*?-->",
        lambda m: " " * len(m.group(0)),
        content,
        flags=re.DOTALL,
    )

    # 3) Mask PREFIX#ANCHOR references that survive elsewhere (body prose).
    content = re.sub(
        r"\b[A-Z]+\s*#\s*(?:E\d+-S\d+|(?:FR|NFR|UJ|ADR|UF|CMP|C|E|S)-\d+)\b",
        lambda m: " " * len(m.group(0)),
        content,
    )

    file_type = detect_file_prefix(file.file_name)
    # Unknown file type → fall back to legacy "accept all" behavior so we
    # don't silently drop anchors from artifacts we don't classify.
    owned = OWNED_PREFIXES_BY_FILE_TYPE.get(file_type) if file_type else None

    seen: set[str] = set()
    ordered: list[str] = []
    for match in ANCHOR_RE.findall(content):
        if match in seen:
            continue
        if owned is not None and _anchor_owner_prefix(match) not in owned:
            continue
        seen.add(match)
        ordered.append(match)
    return ordered


def extract_explicit_links(file: ProjectFile) -> list[ExplicitLink]:
    """Parse `<!-- derived_from: PREFIX#ANCHOR, ... -->` markers in the file.

    Each marker is attributed to the most recent preceding anchor in the file:
    the anchor that the marker is declaring its derivation for.

    A marker without a preceding anchor (e.g. one in the file header) is attached
    to the file itself — represented by source_anchor='__file__'.
    """
    if not file.content:
        return []

    content = file.content
    file_type = detect_file_prefix(file.file_name)

    # STORY files own exactly ONE anchor: their storyId from the filename.
    # Every derived_from marker in the file MUST be attributed to that storyId,
    # never to incidental raw anchors that appear in body prose
    # (e.g. "Related Stories: E1-S2" or comment examples).
    forced_source: str | None = None
    if file_type == "STORY":
        m = re.match(r"^(E\d+-S\d+)", file.file_name)
        forced_source = m.group(1) if m else "__file__"

    # For non-STORY files, build anchor_positions on a *masked* copy of the
    # content so that anchors inside frontmatter, HTML comments, or
    # `PREFIX#ANCHOR` references are NOT eligible to become a source_anchor.
    if forced_source is None:
        masked = content
        if masked.startswith("---"):
            end = masked.find("\n---", 3)
            if end != -1:
                end += 4
                masked = (" " * end) + masked[end:]
        masked = re.sub(
            r"<!--.*?-->",
            lambda m: " " * len(m.group(0)),
            masked,
            flags=re.DOTALL,
        )
        masked = re.sub(
            r"\b[A-Z]+\s*#\s*(?:E\d+-S\d+|(?:FR|NFR|UJ|ADR|UF|CMP|C|E|S)-\d+)\b",
            lambda m: " " * len(m.group(0)),
            masked,
        )
        anchor_positions: list[tuple[int, str]] = [
            (m.start(), m.group(0)) for m in ANCHOR_RE.finditer(masked)
        ]
        # Filter to only anchors actually OWNED by this file type.
        owned = OWNED_PREFIXES_BY_FILE_TYPE.get(file_type) if file_type else None
        if owned is not None:
            anchor_positions = [
                (pos, a) for pos, a in anchor_positions
                if _anchor_owner_prefix(a) in owned
            ]
    else:
        anchor_positions = []

    out: list[ExplicitLink] = []
    # Markers must be parsed from the RAW content (not masked) — otherwise
    # comment masking would erase derived_from markers themselves.
    for marker in DERIVED_FROM_RE.finditer(content):
        marker_pos = marker.start()
        if forced_source is not None:
            source_anchor = forced_source
        else:
            source_anchor = "__file__"
            for pos, anchor in anchor_positions:
                if pos < marker_pos:
                    source_anchor = anchor
                else:
                    break
        # Parse items inside the marker.
        for item in DERIVED_ITEM_RE.finditer(marker.group(1)):
            prefix = item.group(1).upper()
            anchor = item.group(2)
            # Skip self-references (a derived_from marker pointing to its own anchor).
            if anchor == source_anchor and file_type == prefix:
                continue
            out.append(
                ExplicitLink(
                    source_file_id=file.id,
                    source_anchor=source_anchor,
                    target_prefix=prefix,
                    target_anchor=anchor,
                )
            )
    return out


# --- Project-wide indexing ---------------------------------------------------

@dataclass
class ProjectIndex:
    """In-memory map of all anchors in a project, keyed by (prefix, anchor)."""

    files_by_prefix: dict[str, list[ProjectFile]] = field(default_factory=dict)
    anchor_to_file: dict[tuple[str, str], int] = field(default_factory=dict)

    def add_file(self, file: ProjectFile) -> None:
        prefix = detect_file_prefix(file.file_name)
        if not prefix:
            return
        self.files_by_prefix.setdefault(prefix, []).append(file)
        for anchor in extract_anchors(file):
            self.anchor_to_file.setdefault((prefix, anchor), file.id)

    def resolve(self, prefix: str, anchor: str) -> int | None:
        """Resolve a (prefix, anchor) pair to a file_id if known."""
        return self.anchor_to_file.get((prefix, anchor))


async def build_project_index(db: AsyncSession, project_id: int) -> ProjectIndex:
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    index = ProjectIndex()
    for f in result.scalars().all():
        if f.content:
            index.add_file(f)
    return index


# --- Link materialization ----------------------------------------------------

async def rebuild_explicit_links_for_file(
    db: AsyncSession,
    project_id: int,
    file_id: int,
) -> int:
    """Re-extract derived_from links for a single file.

    Removes prior explicit links sourced from this file, parses the file's
    content, resolves PREFIX#ANCHOR targets to existing file_ids, and inserts
    new TraceabilityLink rows. Returns the number of inserted links.

    Unresolved targets (target file not yet present) are silently skipped —
    they will be picked up on the next rebuild after the missing file is added.
    """
    file = await db.get(ProjectFile, file_id)
    if not file or file.project_id != project_id or not file.content:
        return 0

    # Remove existing explicit links from this source.
    await db.execute(
        delete(TraceabilityLink).where(
            TraceabilityLink.source_file_id == file_id,
            TraceabilityLink.origin == "explicit",
        )
    )

    explicit = extract_explicit_links(file)
    if not explicit:
        await db.flush()
        return 0

    index = await build_project_index(db, project_id)

    inserted = 0
    seen: set[tuple[int, str, int, str, str]] = set()
    for link in explicit:
        target_id = index.resolve(link.target_prefix, link.target_anchor)
        if not target_id:
            continue
        key = (file_id, link.source_anchor, target_id, link.target_anchor, "derived_from")
        if key in seen:
            continue
        seen.add(key)
        db.add(
            TraceabilityLink(
                project_id=project_id,
                source_file_id=file_id,
                source_anchor=link.source_anchor,
                target_file_id=target_id,
                target_anchor=link.target_anchor,
                relation="derived_from",
                origin="explicit",
                confidence=1.0,
                rationale=link.rationale,
            )
        )
        inserted += 1
    await db.flush()
    return inserted


async def rebuild_all_explicit_links(db: AsyncSession, project_id: int) -> int:
    """Re-extract derived_from links across all files in the project."""
    await db.execute(
        delete(TraceabilityLink).where(
            TraceabilityLink.project_id == project_id,
            TraceabilityLink.origin == "explicit",
        )
    )
    files_result = await db.execute(
        select(ProjectFile.id).where(ProjectFile.project_id == project_id)
    )
    file_ids = [row[0] for row in files_result.all()]

    total = 0
    for fid in file_ids:
        total += await rebuild_explicit_links_for_file(db, project_id, fid)
    return total


# --- Query helpers -----------------------------------------------------------

async def get_graph(db: AsyncSession, project_id: int) -> dict:
    """Return a graph payload for visualization.

    Nodes include EVERY anchor extracted from project files — even those that
    are not part of any traceability link (orphans). Orphans appear as isolated
    boxes in the canvas, which is itself a useful visual signal.
    Edges are TraceabilityLink rows.
    """
    files_result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = {f.id: f for f in files_result.scalars().all()}

    links_result = await db.execute(
        select(TraceabilityLink).where(TraceabilityLink.project_id == project_id)
    )
    links = list(links_result.scalars().all())

    nodes: dict[str, dict] = {}

    def node_id(file_id: int, anchor: str) -> str:
        return f"{file_id}:{anchor}"

    def add_node(file_id: int, anchor: str) -> None:
        nid = node_id(file_id, anchor)
        if nid in nodes:
            return
        f = files.get(file_id)
        prefix = detect_file_prefix(f.file_name) if f else None
        nodes[nid] = {
            "id": nid,
            "anchor": anchor,
            "file_id": file_id,
            "file_name": f.file_name if f else None,
            "file_path": f.file_path if f else None,
            "prefix": prefix,
        }

    # Pass 1 — seed nodes from every anchor we can extract, so orphans get a node.
    for f in files.values():
        if not f.content:
            continue
        if not detect_file_prefix(f.file_name):
            continue
        for anchor in extract_anchors(f):
            add_node(f.id, anchor)

    # Pass 2 — edges (also ensures any anchor that appears only on the link
    # side, but somehow not in extraction, still gets a node).
    edges = []
    for link in links:
        add_node(link.source_file_id, link.source_anchor)
        add_node(link.target_file_id, link.target_anchor)
        edges.append(
            {
                "id": link.id,
                "source": node_id(link.source_file_id, link.source_anchor),
                "target": node_id(link.target_file_id, link.target_anchor),
                "relation": link.relation,
                "origin": link.origin,
                "confidence": link.confidence,
                "rationale": link.rationale,
            }
        )

    return {"nodes": list(nodes.values()), "edges": edges}


async def get_trace_for_anchor(
    db: AsyncSession,
    project_id: int,
    file_id: int,
    anchor: str,
    direction: str = "both",
    max_depth: int = 5,
) -> dict:
    """Walk the link graph from a given (file_id, anchor) up/down to max_depth.

    direction: 'upstream' (follow source -> target), 'downstream', or 'both'.
    """
    links_result = await db.execute(
        select(TraceabilityLink).where(TraceabilityLink.project_id == project_id)
    )
    links = list(links_result.scalars().all())

    upstream: list[dict] = []
    downstream: list[dict] = []

    if direction in ("upstream", "both"):
        frontier = [(file_id, anchor, 0)]
        seen: set[tuple[int, str]] = {(file_id, anchor)}
        while frontier:
            f_id, anc, depth = frontier.pop()
            if depth >= max_depth:
                continue
            for link in links:
                if link.source_file_id == f_id and link.source_anchor == anc:
                    key = (link.target_file_id, link.target_anchor)
                    if key in seen:
                        continue
                    seen.add(key)
                    upstream.append(
                        {
                            "from": {"file_id": f_id, "anchor": anc},
                            "to": {"file_id": link.target_file_id, "anchor": link.target_anchor},
                            "relation": link.relation,
                            "origin": link.origin,
                            "depth": depth + 1,
                        }
                    )
                    frontier.append((link.target_file_id, link.target_anchor, depth + 1))

    if direction in ("downstream", "both"):
        frontier = [(file_id, anchor, 0)]
        seen = {(file_id, anchor)}
        while frontier:
            f_id, anc, depth = frontier.pop()
            if depth >= max_depth:
                continue
            for link in links:
                if link.target_file_id == f_id and link.target_anchor == anc:
                    key = (link.source_file_id, link.source_anchor)
                    if key in seen:
                        continue
                    seen.add(key)
                    downstream.append(
                        {
                            "from": {"file_id": link.source_file_id, "anchor": link.source_anchor},
                            "to": {"file_id": f_id, "anchor": anc},
                            "relation": link.relation,
                            "origin": link.origin,
                            "depth": depth + 1,
                        }
                    )
                    frontier.append((link.source_file_id, link.source_anchor, depth + 1))

    return {
        "anchor": anchor,
        "file_id": file_id,
        "upstream": upstream,
        "downstream": downstream,
    }


# --- LLM-based suggestion ---------------------------------------------------

SUGGEST_PROMPT = """\
You are a software-engineering traceability analyst.

You are given:
1. A "source" artifact (e.g. an Architecture document) with anchored items.
2. A list of "target" anchors from upstream artifacts (PRD, UX Spec, Brief, etc.).

Your task: for each anchor in the SOURCE, decide which TARGET anchors it most
likely derives from. Only suggest a link when there is clear evidence in the
source content. Do NOT invent connections.

## Source artifact
File: {source_file_name}
Type prefix: {source_prefix}

```
{source_content}
```

## Target anchors available
{target_lines}

## Output format
Return ONLY a JSON array (no prose). Each element:
{{
  "source_anchor": "C-1",
  "target_prefix": "PRD",
  "target_anchor": "FR-001",
  "rationale": "C-1 implements user authentication described in FR-001",
  "confidence": 0.85
}}

Confidence is 0.0-1.0. Skip suggestions below 0.5.
Return [] if nothing is clear.
"""


async def _get_user_llm_config(db: AsyncSession, project_id: int, user_id: int):
    """Resolve an LLM config to use, preferring the requester's default,
    then the project owner's default. Returns (provider, model, api_key, base_url)
    or None if no config exists.
    """
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


async def suggest_links_for_file(
    db: AsyncSession,
    project_id: int,
    file_id: int,
    user_id: int,
    min_confidence: float = 0.5,
) -> int:
    """LLM-based link suggestion for a single file.

    Replaces this file's existing suggested links (origin='suggested').
    Returns the number of newly inserted suggestions.
    Silently no-ops when no LLM config is available.
    """
    import json

    from app.llm.provider import non_stream_chat

    file = await db.get(ProjectFile, file_id)
    if not file or file.project_id != project_id or not file.content:
        return 0

    source_prefix = detect_file_prefix(file.file_name)
    if not source_prefix:
        return 0
    source_anchors = extract_anchors(file)
    if not source_anchors:
        return 0

    # Build the catalog of target anchors (everything from artifact types upstream
    # of the source — for PRD we include nothing, for ARCH we include PRD, etc.).
    upstream_map = {
        "PRD": ["BRIEF"],
        "UX": ["PRD", "BRIEF"],
        "ARCH": ["PRD", "UX", "BRIEF"],
        "EPIC": ["PRD", "ARCH", "UX"],
        "STORY": ["EPIC", "PRD", "ARCH", "UX"],
    }
    upstream_prefixes = upstream_map.get(source_prefix, [])
    if not upstream_prefixes:
        return 0

    index = await build_project_index(db, project_id)
    target_lines: list[str] = []
    valid_targets: set[tuple[str, str]] = set()
    for prefix in upstream_prefixes:
        files_of_prefix = index.files_by_prefix.get(prefix, [])
        for f in files_of_prefix:
            for anchor in extract_anchors(f):
                target_lines.append(f"- {prefix}#{anchor}  ({f.file_name})")
                valid_targets.add((prefix, anchor))

    if not target_lines:
        return 0

    cfg = await _get_user_llm_config(db, project_id, user_id)
    if not cfg:
        return 0
    provider, model, api_key, base_url = cfg

    # Cap source content to keep prompt size manageable.
    source_content = file.content
    if len(source_content) > 30_000:
        source_content = source_content[:30_000] + "\n... (truncated)"

    prompt = SUGGEST_PROMPT.format(
        source_file_name=file.file_name,
        source_prefix=source_prefix,
        source_content=source_content,
        target_lines="\n".join(target_lines[:200]),
    )

    try:
        raw = await non_stream_chat(
            provider=provider,
            model=model,
            api_key=api_key,
            messages=[
                {"role": "system", "content": "Output ONLY a valid JSON array. No prose."},
                {"role": "user", "content": prompt},
            ],
            base_url=base_url,
        )
    except Exception:
        return 0

    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    elif raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    try:
        suggestions = json.loads(raw)
    except Exception:
        return 0
    if not isinstance(suggestions, list):
        return 0

    # Replace prior suggested links from this source.
    await db.execute(
        delete(TraceabilityLink).where(
            TraceabilityLink.source_file_id == file_id,
            TraceabilityLink.origin == "suggested",
        )
    )

    inserted = 0
    seen: set[tuple[str, int, str]] = set()
    for s in suggestions:
        try:
            src_anchor = str(s["source_anchor"]).strip()
            tgt_prefix = str(s["target_prefix"]).strip().upper()
            tgt_anchor = str(s["target_anchor"]).strip()
            confidence = float(s.get("confidence", 0.0))
            rationale = str(s.get("rationale", "")).strip() or None
        except (KeyError, TypeError, ValueError):
            continue
        if confidence < min_confidence:
            continue
        if src_anchor not in source_anchors:
            continue
        if (tgt_prefix, tgt_anchor) not in valid_targets:
            continue
        target_id = index.resolve(tgt_prefix, tgt_anchor)
        if not target_id:
            continue
        key = (src_anchor, target_id, tgt_anchor)
        if key in seen:
            continue
        seen.add(key)
        db.add(
            TraceabilityLink(
                project_id=project_id,
                source_file_id=file_id,
                source_anchor=src_anchor,
                target_file_id=target_id,
                target_anchor=tgt_anchor,
                relation="derived_from",
                origin="suggested",
                confidence=confidence,
                rationale=rationale,
            )
        )
        inserted += 1

    await db.flush()
    return inserted


def extract_anchor_snippet(content: str, anchor: str, max_chars: int = 1500) -> dict:
    """Locate an anchor inside a markdown document and return a readable snippet.

    Resolution order:
    1. Heading line containing the anchor → return the section up to the next
       same-or-higher-level heading.
    2. Table row containing the anchor → return the table header (if found) +
       the matching row.
    3. Any line containing the anchor → return ±a few lines of context.

    Returns: {kind: 'heading'|'table'|'text'|'none', heading: str|None, snippet: str}
    """
    if not content or not anchor:
        return {"kind": "none", "heading": None, "snippet": ""}

    # Skip YAML frontmatter so anchors that appear there (e.g. storyId in a
    # story file) don't shadow the body.
    body_start = 0
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            body_start = end + 4
    body_text = content[body_start:]

    pat = re.compile(rf"\b{re.escape(anchor)}\b")
    lines = body_text.splitlines()

    # Story-style early path: storyIds (E1-S1 / S-014) typically live in
    # frontmatter, never in headings, so headings/tables/text passes would
    # otherwise miss them or return a shallow metadata line. Show the whole
    # first H1 section as the story body.
    if re.match(r"^(E\d+-S\d+|S-\d+)$", anchor):
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                heading_text = stripped.lstrip("#").strip()
                body_lines: list[str] = []
                for j in range(i + 1, len(lines)):
                    nxt = lines[j].lstrip()
                    if nxt.startswith("# ") and not nxt.startswith("## "):
                        break
                    body_lines.append(lines[j])
                snippet = "\n".join(body_lines).strip()
                if len(snippet) > max_chars:
                    snippet = snippet[:max_chars] + "\n... (truncated)"
                return {"kind": "heading", "heading": heading_text, "snippet": snippet}

    # Pass 1 — heading
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith("#"):
            continue
        if not pat.search(line):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        heading_text = stripped.lstrip("#").strip()
        body: list[str] = []
        for j in range(i + 1, len(lines)):
            nxt = lines[j].lstrip()
            if nxt.startswith("#"):
                nxt_level = len(nxt) - len(nxt.lstrip("#"))
                if nxt_level <= level:
                    break
            body.append(lines[j])
        snippet = "\n".join(body).strip()
        if len(snippet) > max_chars:
            snippet = snippet[:max_chars] + "\n... (truncated)"
        return {"kind": "heading", "heading": heading_text, "snippet": snippet}

    # Pass 2 — table row
    for i, line in enumerate(lines):
        if "|" not in line or not pat.search(line):
            continue
        # Walk upward through the contiguous table block to find header.
        header_idx = i
        while header_idx > 0 and lines[header_idx - 1].lstrip().startswith("|"):
            header_idx -= 1
        chunk: list[str] = []
        if header_idx < i:
            chunk.append(lines[header_idx])
            if header_idx + 1 < len(lines) and "---" in lines[header_idx + 1]:
                chunk.append(lines[header_idx + 1])
        chunk.append(line)
        snippet = "\n".join(chunk).strip()
        if len(snippet) > max_chars:
            snippet = snippet[:max_chars] + "\n... (truncated)"
        return {"kind": "table", "heading": None, "snippet": snippet}

    # Pass 3 — any free-text mention
    for i, line in enumerate(lines):
        if pat.search(line):
            start = max(0, i - 2)
            end = min(len(lines), i + 5)
            snippet = "\n".join(lines[start:end]).strip()
            if len(snippet) > max_chars:
                snippet = snippet[:max_chars] + "\n... (truncated)"
            return {"kind": "text", "heading": None, "snippet": snippet}

    return {"kind": "none", "heading": None, "snippet": ""}


async def get_orphan_anchors(db: AsyncSession, project_id: int) -> list[dict]:
    """Anchors that are referenced by no downstream artifact and reference no upstream.

    Useful to surface uncovered FRs (no Story derives from them) or orphan ADRs.
    """
    index = await build_project_index(db, project_id)
    links_result = await db.execute(
        select(TraceabilityLink.source_file_id, TraceabilityLink.source_anchor,
               TraceabilityLink.target_file_id, TraceabilityLink.target_anchor)
        .where(TraceabilityLink.project_id == project_id)
    )
    sources: set[tuple[int, str]] = set()
    targets: set[tuple[int, str]] = set()
    for row in links_result.all():
        sources.add((row[0], row[1]))
        targets.add((row[2], row[3]))

    orphans = []
    for (prefix, anchor), file_id in index.anchor_to_file.items():
        if (file_id, anchor) not in sources and (file_id, anchor) not in targets:
            orphans.append({"file_id": file_id, "anchor": anchor, "prefix": prefix})
    return orphans
