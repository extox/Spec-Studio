import os
from app.config import get_settings

settings = get_settings()

TEMPLATES = {
    "product-brief": {
        "id": "product-brief",
        "name": "Product Brief",
        "file_name": "product-brief.md",
        "phase": "analysis",
        "description": "Flexible 1-2 page brief capturing problem, solution, users, and vision.",
    },
    "prd": {
        "id": "prd",
        "name": "Product Requirements Document",
        "file_name": "prd.md",
        "phase": "planning",
        "description": "Comprehensive PRD with executive summary, user journeys, FRs, NFRs, and roadmap.",
    },
    "architecture": {
        "id": "architecture",
        "name": "Architecture Document",
        "file_name": "architecture.md",
        "phase": "solutioning",
        "description": "Architecture decisions document with ADRs, tech stack, data model, and API design.",
    },
    "epic": {
        "id": "epic",
        "name": "Epics & Stories",
        "file_name": "epic.md",
        "phase": "implementation",
        "description": "Epic breakdown with requirements inventory, FR coverage map, and BDD stories.",
    },
    "story": {
        "id": "story",
        "name": "User Story",
        "file_name": "story.md",
        "phase": "implementation",
        "description": "Detailed story with BDD acceptance criteria, tasks, dev notes, and references.",
    },
    "ux-spec": {
        "id": "ux-spec",
        "name": "UX Specification",
        "file_name": "ux-spec.md",
        "phase": "planning",
        "description": "Comprehensive UX spec with user research, flows, wireframes, and accessibility.",
    },
    "project-context": {
        "id": "project-context",
        "name": "Project Context",
        "file_name": "project-context.md",
        "phase": "cross-cutting",
        "description": "AI implementation rules: tech stack, conventions, and project structure.",
    },
    "sprint-status": {
        "id": "sprint-status",
        "name": "Sprint Status",
        "file_name": "sprint-status.md",
        "phase": "implementation",
        "description": "YAML-based sprint tracking with epic/story status state machine.",
    },
}


def get_template(template_id: str) -> dict | None:
    return TEMPLATES.get(template_id)


def get_all_templates() -> list[dict]:
    return list(TEMPLATES.values())


def get_template_content(template_id: str) -> str:
    """Load template content from bmad_data/templates/"""
    template = TEMPLATES.get(template_id)
    if not template:
        return ""
    path = os.path.join(settings.BMAD_DATA_PATH, "templates", template["file_name"])
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""
