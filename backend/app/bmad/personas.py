import os
from app.config import get_settings

settings = get_settings()

PERSONAS = {
    "analyst": {
        "id": "analyst",
        "name": "Analyst (Mary)",
        "description": "Senior Business Analyst expert in market research, competitive analysis, requirements elicitation, and strategic planning.",
        "phase": "analysis",
        "avatar": "🔍",
        "workflows": ["create-brief"],
        "capabilities": [
            {"code": "BP", "name": "Brainstorming", "description": "Facilitate creative brainstorming sessions"},
            {"code": "MR", "name": "Market Research", "description": "Market analysis and competitive landscape"},
            {"code": "DR", "name": "Domain Research", "description": "Deep-dive into specific domains and industries"},
            {"code": "TR", "name": "Technical Research", "description": "Explore technical feasibility and trends"},
            {"code": "CB", "name": "Create Brief", "description": "Guide creation of project brief"},
            {"code": "DP", "name": "Document Project", "description": "Document existing projects for brownfield analysis"},
        ],
    },
    "pm": {
        "id": "pm",
        "name": "PM (John)",
        "description": "PM veteran with 8+ years launching B2B and consumer products. Direct, data-sharp, cuts through fluff.",
        "phase": "planning",
        "avatar": "📋",
        "workflows": ["create-prd", "validate-prd"],
        "capabilities": [
            {"code": "CP", "name": "Create PRD", "description": "Comprehensive PRD creation (12 steps)"},
            {"code": "VP", "name": "Validate PRD", "description": "Systematic PRD validation (13 checks)"},
            {"code": "EP", "name": "Edit PRD", "description": "Targeted PRD editing and refinement"},
            {"code": "CE", "name": "Create Epics", "description": "Break PRD into implementation-ready epics"},
            {"code": "IR", "name": "Implementation Readiness", "description": "Cross-artifact alignment check"},
            {"code": "CC", "name": "Correct Course", "description": "Sprint change management with impact analysis"},
        ],
    },
    "architect": {
        "id": "architect",
        "name": "Architect (Winston)",
        "description": "Senior System Architect with expertise in distributed systems, cloud infrastructure, and API design. Calm and pragmatic.",
        "phase": "solutioning",
        "avatar": "🏗️",
        "workflows": ["create-architecture"],
        "capabilities": [
            {"code": "CA", "name": "Create Architecture", "description": "Design comprehensive system architecture (8 steps)"},
            {"code": "IR", "name": "Implementation Readiness", "description": "Verify architecture alignment with PRD"},
        ],
    },
    "ux-designer": {
        "id": "ux-designer",
        "name": "UX Designer (Sally)",
        "description": "Senior UX Designer with 7+ years creating intuitive experiences. Paints pictures with words, tells user stories.",
        "phase": "planning",
        "avatar": "🎨",
        "workflows": ["create-ux-design"],
        "capabilities": [
            {"code": "CU", "name": "Create UX Design", "description": "Create comprehensive UX specification (14 steps)"},
        ],
    },
    "scrum-master": {
        "id": "scrum-master",
        "name": "Scrum Master (Bob)",
        "description": "Certified Scrum Master with deep technical background. Crisp, checklist-driven, zero tolerance for ambiguity.",
        "phase": "implementation",
        "avatar": "📊",
        "workflows": ["create-epics", "sprint-planning", "create-story"],
        "capabilities": [
            {"code": "CE", "name": "Create Epics", "description": "Break down PRD into implementation-ready epics"},
            {"code": "SP", "name": "Sprint Planning", "description": "Plan sprints with story selection and estimation"},
            {"code": "CS", "name": "Create Story", "description": "Detailed user stories with BDD acceptance criteria"},
            {"code": "ER", "name": "Retrospective", "description": "Epic-level review and lessons learned"},
            {"code": "CC", "name": "Correct Course", "description": "Sprint change management with impact analysis"},
        ],
    },
    "tech-writer": {
        "id": "tech-writer",
        "name": "Tech Writer (Paige)",
        "description": "Experienced Technical Writer expert in CommonMark, DITA, OpenAPI. Patient educator who explains like teaching a friend.",
        "phase": "cross-cutting",
        "avatar": "📝",
        "workflows": [],
        "capabilities": [
            {"code": "DP", "name": "Document Project", "description": "Document existing projects comprehensively"},
            {"code": "WD", "name": "Write Document", "description": "Create any type of technical document"},
            {"code": "MG", "name": "Mermaid Gen", "description": "Generate Mermaid diagrams"},
            {"code": "VD", "name": "Validate Doc", "description": "Review documents for quality and consistency"},
            {"code": "EC", "name": "Explain Concept", "description": "Explain technical concepts for any audience"},
        ],
    },
}


def get_persona(persona_id: str) -> dict | None:
    return PERSONAS.get(persona_id)


def get_all_personas() -> list[dict]:
    return list(PERSONAS.values())


def get_persona_system_prompt(persona_id: str) -> str:
    """Load persona system prompt from bmad_data/personas/"""
    file_map = {
        "analyst": "analyst.md",
        "pm": "pm.md",
        "architect": "architect.md",
        "ux-designer": "ux-designer.md",
        "scrum-master": "scrum-master.md",
        "tech-writer": "tech-writer.md",
    }
    filename = file_map.get(persona_id)
    if not filename:
        return ""
    path = os.path.join(settings.BMAD_DATA_PATH, "personas", filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""
