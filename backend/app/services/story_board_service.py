"""Story Execution Board — kanban over Story files (BMad-aligned, body-centric).

Source of truth = the body header line `**Status:** {value}`. This matches every
other BMad artifact template (architecture/prd/epic/ux-spec/test-plan all use
`**Status:** Draft` in body, no frontmatter status). Story files no longer
carry a YAML frontmatter — the body header block (ID/Epic/Points/Status) is
the canonical metadata.

Moving a card on the board patches that single `**Status:**` line in place,
preserving every other byte of the file. The patched file is saved through
`file_service.update_file` which records a new file version automatically.
"""

from __future__ import annotations

import re
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_file import ProjectFile
from app.services import file_service

# Board column keys (UI/i18n side). NOT the values written to files.
COLUMNS: list[str] = ["todo", "in_progress", "review", "done", "blocked"]
DEFAULT_COLUMN = "todo"

# Column ↔ BMad body-status value.
COLUMN_TO_FILE: dict[str, str] = {
    "todo": "backlog",
    "in_progress": "in-progress",
    "review": "review",
    "done": "done",
    "blocked": "blocked",
}
# Multiple legacy values can map to the same column on read.
FILE_TO_COLUMN: dict[str, str] = {
    "backlog": "todo",
    "ready-for-dev": "todo",
    "ready_for_dev": "todo",
    "todo": "todo",
    "draft": "todo",
    "in-progress": "in_progress",
    "in_progress": "in_progress",
    "wip": "in_progress",
    "review": "review",
    "in-review": "review",
    "done": "done",
    "completed": "done",
    "blocked": "blocked",
}

STORY_PATH_RE = re.compile(
    r"implementation-artifacts/E(\d+)-S(\d+)[\-_].*\.md$", re.IGNORECASE
)
STORY_ID_RE = re.compile(r"E(\d+)-S(\d+)", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)

# Body header lines — `**Key:** value`
HEADER_LINE_RE = re.compile(
    r"^[ \t]*\*\*([A-Za-z][\w \-]*?):\*\*[ \t]+(.+?)[ \t]*$",
    re.MULTILINE,
)
STATUS_LABEL_RE = re.compile(
    r"(^[ \t]*\*\*Status:\*\*[ \t]+)([A-Za-z_\-][\w\-]*)([ \t]*)$",
    re.MULTILINE | re.IGNORECASE,
)


def _normalize_column(value: str | None) -> str:
    if not value:
        return DEFAULT_COLUMN
    v = value.strip().lower().replace("-", "_")
    return v if v in COLUMNS else DEFAULT_COLUMN


def _file_status_to_column(file_status: str | None) -> str:
    if not file_status:
        return DEFAULT_COLUMN
    return FILE_TO_COLUMN.get(file_status.strip().lower(), DEFAULT_COLUMN)


def _column_to_file_status(column: str) -> str:
    return COLUMN_TO_FILE.get(column, "backlog")


def _extract_header_block(content: str) -> dict[str, str]:
    """Pull `**Key:** value` pairs from the body. Read-only.

    Stops at the first `---`/section heading after the headers begin. Returns
    a flat dict keyed by lowercased label (e.g., {'id': 'E1-S1', 'status': ...}).
    """
    if not content:
        return {}
    out: dict[str, str] = {}
    for m in HEADER_LINE_RE.finditer(content):
        key = m.group(1).strip().lower().replace(" ", "_")
        val = m.group(2).strip()
        out.setdefault(key, val)
    return out


def _story_id_from_path(path: str) -> str | None:
    name = path.rsplit("/", 1)[-1]
    m = STORY_ID_RE.search(name)
    return f"E{int(m.group(1))}-S{int(m.group(2))}" if m else None


def _title_from(content: str, fallback: str) -> str:
    m = H1_RE.search(content or "")
    if m:
        # Strip any leading "Story:" prefix the template inserts.
        title = m.group(1).strip()
        return re.sub(r"^Story:\s*", "", title, flags=re.IGNORECASE) or title
    return fallback


def _is_story_path(path: str | None) -> bool:
    return bool(path and STORY_PATH_RE.search(path))


async def _load_story_files(db: AsyncSession, project_id: int) -> list[ProjectFile]:
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = result.scalars().all()
    return [f for f in files if _is_story_path(f.file_path)]


def _summarize(file: ProjectFile) -> dict:
    headers = _extract_header_block(file.content or "")
    story_id = _story_id_from_path(file.file_path) or file.file_name
    file_status = headers.get("status")
    column = _file_status_to_column(file_status)
    return {
        "id": file.id,
        "story_id": story_id,
        "file_path": file.file_path,
        "file_name": file.file_name,
        "title": _title_from(file.content or "", story_id),
        "status": column,
        "file_status": file_status,
        "epic": headers.get("epic"),
        "estimate": headers.get("points") or headers.get("estimate"),
        "owner": headers.get("owner") or headers.get("assignee"),
        "updated_at": file.updated_at,
    }


async def get_board(db: AsyncSession, project_id: int) -> dict:
    files = await _load_story_files(db, project_id)
    cards = [_summarize(f) for f in files]
    cards.sort(key=lambda c: (c["story_id"] or ""))

    by_status: dict[str, list[dict]] = {s: [] for s in COLUMNS}
    for c in cards:
        by_status.setdefault(c["status"], []).append(c)

    columns = [{"status": s, "items": by_status.get(s, [])} for s in COLUMNS]
    return {"columns": columns, "total": len(cards)}


def _patch_status(content: str, new_value: str) -> str | None:
    """Replace ONLY the body `**Status:** ...` line. Returns None if absent."""
    if not content:
        return None
    new_content, count = STATUS_LABEL_RE.subn(
        lambda mm: f"{mm.group(1)}{new_value}{mm.group(3)}",
        content,
        count=1,
    )
    return new_content if count else None


async def update_story_status(
    db: AsyncSession,
    project_id: int,
    story_id: str,
    new_column: str,
    user_id: int | None = None,
) -> dict:
    """Patch the Story file's body **Status:** line and create a new version."""
    new_column = _normalize_column(new_column)
    new_file_value = _column_to_file_status(new_column)

    files = await _load_story_files(db, project_id)
    target: ProjectFile | None = None
    for f in files:
        if _story_id_from_path(f.file_path) == story_id:
            target = f
            break
    if not target:
        raise ValueError(f"Story not found: {story_id}")

    new_content = _patch_status(target.content or "", new_file_value)
    if new_content is None:
        raise ValueError(
            f"Story {story_id} has no `**Status:**` line in its body; cannot patch"
        )
    if new_content == target.content:
        return _summarize(target)

    updated = await file_service.update_file(
        db, project_id, target.id, user_id=user_id, content=new_content
    )
    return _summarize(updated)


def allowed_statuses() -> Iterable[str]:
    return COLUMNS
