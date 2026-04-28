"""Intelligent project context builder for LLM prompts.

Builds project context by prioritizing files relevant to the current
persona/workflow, and includes full content within a token budget.
Context expansion files (file_type='context') are always included first.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.project_file import ProjectFile

# Approximate: 1 token ~ 4 chars for Korean/English mixed text
MAX_CONTEXT_CHARS = 60_000  # ~15k tokens budget (increased for context expansion)
CONTEXT_EXPANSION_BUDGET = 20_000  # Separate budget for context files

# Which artifacts each workflow needs most
WORKFLOW_PRIORITY = {
    "create-brief": [],  # Starting point -- no prior artifacts needed
    "create-prd": ["product-brief"],
    "validate-prd": ["PRD", "product-brief"],
    "create-architecture": ["PRD", "product-brief", "ux-spec"],
    "create-ux-design": ["PRD", "product-brief"],
    "create-epics": ["PRD", "architecture", "ux-spec"],
    "sprint-planning": ["epics", "sprint-status", "PRD"],
    "create-story": ["epics", "sprint-status", "PRD", "architecture", "ux-spec"],
    "goal-backward-analysis": ["PRD", "product-brief"],
    "generate-code-skeleton": ["story", "architecture", "PRD"],
    "create-test-plan": ["story", "PRD", "ux-spec"],
    "design-ci-pipeline": ["architecture", "PRD"],
    "create-iac": ["architecture", "PRD"],
}

# File name patterns for matching priority keywords
FILE_KEYWORD_MAP = {
    "product-brief": ["product-brief", "brief"],
    "PRD": ["prd"],
    "architecture": ["architecture", "arch"],
    "ux-spec": ["ux-spec", "ux"],
    "epics": ["epics", "epic"],
    "story": ["story"],
    "sprint-status": ["sprint-status", "sprint"],
    "project-context": ["project-context"],
}


def _match_priority(file_name: str, keywords: list[str]) -> bool:
    name_lower = file_name.lower()
    return any(kw in name_lower for kw in keywords)


def _get_file_priority(file_name: str, workflow_id: str | None) -> int:
    """Lower number = higher priority. 0 = most important."""
    if not workflow_id:
        return 50

    priority_list = WORKFLOW_PRIORITY.get(workflow_id, [])
    for i, artifact_key in enumerate(priority_list):
        keywords = FILE_KEYWORD_MAP.get(artifact_key, [artifact_key.lower()])
        if _match_priority(file_name, keywords):
            return i
    return 100  # Non-priority files


def _build_context_expansion_section(context_files: list[ProjectFile]) -> str | None:
    """Format context expansion files as a structured section for LLM."""
    if not context_files:
        return None

    parts = []
    chars_used = 0

    # Group by category (extracted from file_path: context/{category}/...)
    by_category: dict[str, list[ProjectFile]] = {}
    for f in context_files:
        path_parts = f.file_path.split("/")
        category = path_parts[1] if len(path_parts) >= 2 else "custom"
        by_category.setdefault(category, []).append(f)

    for category, files in by_category.items():
        for f in files:
            if not f.content:
                continue
            header = f"### [{category}] {f.file_name}\n```yaml\n"
            footer = "\n```"
            available = CONTEXT_EXPANSION_BUDGET - chars_used - len(header) - len(footer) - 10

            if available <= 200:
                break

            if len(f.content) <= available:
                parts.append(f"{header}{f.content}{footer}")
                chars_used += len(header) + len(f.content) + len(footer)
            else:
                truncated = f.content[:available - 50]
                parts.append(f"{header}{truncated}\n... (truncated, {len(f.content)} chars total){footer}")
                chars_used += len(header) + available
                break

    if not parts:
        return None

    return "## Project Context (\ucee8\ud14d\uc2a4\ud2b8 \ud655\uc7a5)\n\n" + "\n\n".join(parts)


async def build_project_context(
    db: AsyncSession,
    project_id: int,
    workflow_id: str | None = None,
    max_chars: int = MAX_CONTEXT_CHARS,
) -> str | None:
    """Build project context string with intelligent file prioritization.

    Context expansion files (file_type='context') are included first with their own budget.
    Then deliverable/other files are included with the remaining budget.
    """
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = result.scalars().all()

    if not files:
        return None

    # Separate context expansion files from other files
    context_files = [f for f in files if f.file_type == "context" and f.content]
    other_files = [(f, f.content) for f in files if f.file_type != "context" and f.content]

    if not context_files and not other_files:
        return None

    sections = []
    chars_used = 0

    # 1. Build context expansion section (separate budget)
    context_section = _build_context_expansion_section(context_files)
    if context_section:
        sections.append(context_section)
        chars_used += len(context_section)

    # 2. Build deliverable section with remaining budget
    remaining_budget = max_chars - chars_used

    if other_files and remaining_budget > 200:
        # Sort by priority (lower = more important)
        other_files.sort(key=lambda x: _get_file_priority(x[0].file_name, workflow_id))

        artifact_parts = []
        artifact_chars = 0

        for f, content in other_files:
            header = f"### {f.file_path}\n"
            available = remaining_budget - artifact_chars - len(header) - 10

            if available <= 200:
                break

            if len(content) <= available:
                artifact_parts.append(f"{header}{content}")
                artifact_chars += len(header) + len(content)
            else:
                truncated = content[:available - 50]
                artifact_parts.append(f"{header}{truncated}\n\n... (truncated, {len(content)} chars total)")
                artifact_chars += len(header) + available
                break

        if artifact_parts:
            sections.append("\n\n---\n\n".join(artifact_parts))

    return "\n\n---\n\n".join(sections) if sections else None
