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
    "developer": {
        "id": "developer",
        "name": "Developer (Dex)",
        "description": "Senior Software Developer who turns user stories into clean, well-structured scaffolds. Pragmatic, opinionated, ships fast.",
        "phase": "construction",
        "avatar": "💻",
        "workflows": ["generate-code-skeleton"],
        "capabilities": [
            {"code": "GS", "name": "Generate Code Skeleton", "description": "Story → directory tree + function signatures with TODO markers"},
            {"code": "IG", "name": "Implementation Guide", "description": "Step-by-step implementation instructions"},
            {"code": "PR", "name": "Plan Refactor", "description": "Outline a behavior-preserving refactor"},
        ],
    },
    "qa-engineer": {
        "id": "qa-engineer",
        "name": "QA Engineer (Quinn)",
        "description": "QA Engineer who turns BDD criteria into a defensible test matrix. Adversarial, risk-weighted, matrix-driven.",
        "phase": "construction",
        "avatar": "🧪",
        "workflows": ["create-test-plan"],
        "capabilities": [
            {"code": "TP", "name": "Test Plan", "description": "Convert a story's BDD into a complete test matrix"},
            {"code": "RA", "name": "Risk Analysis", "description": "Identify high-risk paths that need extra coverage"},
            {"code": "TF", "name": "Test Fixtures", "description": "Design fixture/seed data for repeatable tests"},
        ],
    },
    "devops-engineer": {
        "id": "devops-engineer",
        "name": "DevOps Engineer (Ollie)",
        "description": "DevOps Engineer who designs the path from commit to production. Pipeline-first, secret-conscious, vendor-neutral by default.",
        "phase": "construction",
        "avatar": "⚙️",
        "workflows": ["design-ci-pipeline", "create-iac"],
        "capabilities": [
            {"code": "CI", "name": "CI Pipeline", "description": "Design a CI/CD pipeline from architecture inputs"},
            {"code": "IA", "name": "IaC Design", "description": "Cloud-vendor-friendly IaC sketch in YAML"},
            {"code": "RB", "name": "Runbook", "description": "Operational runbook for a component"},
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
        "developer": "developer.md",
        "qa-engineer": "qa-engineer.md",
        "devops-engineer": "devops-engineer.md",
    }
    filename = file_map.get(persona_id)
    if not filename:
        return ""
    path = os.path.join(settings.BMAD_DATA_PATH, "personas", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
