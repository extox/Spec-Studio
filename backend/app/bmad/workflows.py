import os
from app.config import get_settings

settings = get_settings()

WORKFLOWS = {
    "create-brief": {
        "id": "create-brief",
        "name": "Create Project Brief",
        "persona": "analyst",
        "recommended_persona": "analyst",
        "description": "Brainstorm and create a comprehensive project brief through guided discovery.",
        "steps": [
            {"step": 1, "name": "Understand the Project Idea", "description": "Discuss the initial project idea. Discover context, inspiration, greenfield vs brownfield."},
            {"step": 2, "name": "Identify Target Users", "description": "Define primary and secondary user personas with demographics, pain points, and delights."},
            {"step": 3, "name": "Define Core Problem", "description": "Crystallize the core problem in one sentence. Explore why it matters and cost of status quo."},
            {"step": 4, "name": "Outline Key Features & Differentiator", "description": "List core capabilities and identify the ONE key differentiator."},
            {"step": 5, "name": "Generate Brief", "description": "Compile all discoveries into the product-brief template. Present for review."},
        ],
        "template": "product-brief",
        "supports_apc": True,
    },
    "create-prd": {
        "id": "create-prd",
        "name": "Create PRD",
        "persona": "pm",
        "description": "Create a comprehensive Product Requirements Document through 12-step systematic discovery.",
        "steps": [
            {"step": 1, "name": "Init — Input Discovery", "description": "Discover and load all available input documents. Classify greenfield vs brownfield."},
            {"step": 2, "name": "Discovery — Project Classification", "description": "Classify project type, domain, complexity, and key constraints."},
            {"step": 3, "name": "Vision — Product Vision", "description": "Discover product vision through conversation. NO content generation — pure discovery."},
            {"step": 4, "name": "Executive Summary", "description": "First content generation. Draft compelling executive summary from discovered insights."},
            {"step": 5, "name": "Success Criteria", "description": "Define user/business/technical success. Scope negotiation using MoSCoW (MVP/Growth/Vision)."},
            {"step": 6, "name": "User Journeys", "description": "Create narrative, story-based user journeys for all user types. Include emotional states."},
            {"step": 7, "name": "Domain Requirements", "description": "Optional: Domain-specific compliance, regulations, industry standards. Skip if not applicable."},
            {"step": 8, "name": "Innovation Patterns", "description": "Optional: Detect and explore innovation opportunities (AI/ML, novel patterns). Skip if straightforward."},
            {"step": 9, "name": "Scoping & Roadmap", "description": "Finalize MVP scope, create phased development roadmap, risk assessment with mitigation."},
            {"step": 10, "name": "Functional Requirements", "description": "The Capability Contract: 20-50 FRs organized by capability area with priorities."},
            {"step": 11, "name": "Non-Functional Requirements", "description": "Selective NFRs for relevant categories only (performance, security, scalability, etc.)."},
            {"step": 12, "name": "Complete — Polish & Finalize", "description": "Document optimization, consistency check, deduplication. Present validation options."},
        ],
        "template": "prd",
        "supports_apc": True,
    },
    "validate-prd": {
        "id": "validate-prd",
        "name": "Validate PRD",
        "persona": "pm",
        "description": "Systematic validation of an existing PRD with 13 quality checks.",
        "steps": [
            {"step": 1, "name": "Document Structure", "description": "Verify all required sections are present and properly ordered."},
            {"step": 2, "name": "Executive Summary Quality", "description": "Evaluate clarity, completeness, and compelling nature of the summary."},
            {"step": 3, "name": "Problem Statement Clarity", "description": "Check problem articulation, target audience definition, alternatives."},
            {"step": 4, "name": "Success Criteria Measurability", "description": "Verify all criteria are measurable with specific targets and timeframes."},
            {"step": 5, "name": "User Journey Completeness", "description": "Check all user types covered, happy paths and edge cases included."},
            {"step": 6, "name": "FR Coverage", "description": "Verify FRs cover all journeys, traceable to user needs, no duplicates."},
            {"step": 7, "name": "FR-NFR Alignment", "description": "Check NFRs support FRs, performance targets realistic, security appropriate."},
            {"step": 8, "name": "Scope Consistency", "description": "Verify MVP matches Must-Have priorities, phase boundaries clear."},
            {"step": 9, "name": "Technical Feasibility", "description": "Flag potentially infeasible FRs, hidden complexity, integration dependencies."},
            {"step": 10, "name": "Completeness Check", "description": "Find gaps in requirement chain, error scenarios, admin/ops requirements."},
            {"step": 11, "name": "Consistency Check", "description": "Verify consistent terminology, no contradictions, priorities aligned."},
            {"step": 12, "name": "Clarity & Ambiguity", "description": "Find vague terms, undefined acronyms, multi-interpretable requirements."},
            {"step": 13, "name": "Final Assessment", "description": "Overall quality score (1-10), critical issues, verdict: Ready/Needs Revision/Major Rework."},
        ],
        "template": None,
        "supports_apc": True,
    },
    "create-architecture": {
        "id": "create-architecture",
        "name": "Create Architecture",
        "persona": "architect",
        "description": "Design comprehensive system architecture with Architecture Decision Records (ADRs).",
        "steps": [
            {"step": 1, "name": "Init — Input Discovery", "description": "Load PRD, brief, UX spec. Identify constraints (team, timeline, infrastructure)."},
            {"step": 2, "name": "Context & Requirements Analysis", "description": "Categorize requirements by architectural impact. Identify quality attribute drivers."},
            {"step": 3, "name": "Starter Architecture Decisions", "description": "Choose architecture style (monolith/microservices/serverless), deployment model. Document as ADRs."},
            {"step": 4, "name": "Technical Decisions", "description": "Detailed technology choices: languages, frameworks, databases, auth, APIs. Document rationale for each."},
            {"step": 5, "name": "Architecture Patterns", "description": "Component diagram, data flow, database design, API design, integration patterns."},
            {"step": 6, "name": "Project Structure", "description": "Folder structure, module boundaries, naming conventions, configuration management."},
            {"step": 7, "name": "Validation", "description": "Cross-reference with PRD. Verify FR coverage, NFR achievability. Check for SPOFs and bottlenecks."},
            {"step": 8, "name": "Complete — Finalize", "description": "Compile architecture document. Generate summary diagrams. Present next steps."},
        ],
        "template": "architecture",
        "supports_apc": True,
    },
    "create-ux-design": {
        "id": "create-ux-design",
        "name": "Create UX Design",
        "persona": "ux-designer",
        "description": "Create comprehensive UX specification through 14-step user-centered design process.",
        "steps": [
            {"step": 1, "name": "Init — Input Discovery", "description": "Load PRD, brief, research. Identify design constraints and opportunities."},
            {"step": 2, "name": "User Research", "description": "Deep understanding of users, personas, mental models, and behavioral patterns."},
            {"step": 3, "name": "Information Architecture", "description": "Content structure, navigation hierarchy, sitemap, naming conventions."},
            {"step": 4, "name": "User Flows", "description": "Core task flows with entry points, key actions, decision points, error recovery."},
            {"step": 5, "name": "Wireframe Concepts", "description": "Low-fidelity layout explorations. Describe layouts in structured text."},
            {"step": 6, "name": "Interaction Patterns", "description": "Micro-interactions: forms, navigation transitions, drag-and-drop, keyboard shortcuts."},
            {"step": 7, "name": "Component Library", "description": "Reusable UI component specs with states, variants, and responsive behavior."},
            {"step": 8, "name": "Responsive Strategy", "description": "Breakpoints, device adaptation, mobile-first vs desktop-first decisions."},
            {"step": 9, "name": "Accessibility", "description": "WCAG 2.1 AA compliance: contrast, screen readers, keyboard navigation, focus management."},
            {"step": 10, "name": "Error Handling UX", "description": "Error states design, recovery flows, prevention strategies, graceful degradation."},
            {"step": 11, "name": "Empty & Loading States", "description": "First-run experience, no-data states, skeleton screens, optimistic updates."},
            {"step": 12, "name": "Content Strategy", "description": "Voice and tone, microcopy guidelines, terminology glossary, writing style."},
            {"step": 13, "name": "Validation", "description": "Cross-reference with PRD user journeys and FRs. Check UX consistency."},
            {"step": 14, "name": "Complete — Finalize", "description": "Compile UX specification. Create handoff notes. Present next steps."},
        ],
        "template": "ux-spec",
        "supports_apc": True,
    },
    "create-epics": {
        "id": "create-epics",
        "name": "Create Epics & Stories",
        "persona": "scrum-master",
        "description": "Break down PRD and architecture into implementation-ready epics with BDD stories.",
        "steps": [
            {"step": 1, "name": "Validate Prerequisites", "description": "Verify PRD and architecture exist. Build requirements inventory and FR coverage map."},
            {"step": 2, "name": "Design Epics", "description": "Group requirements into logical epics with IDs, priorities, dependencies, and complexity estimates."},
            {"step": 3, "name": "Create Stories with BDD", "description": "Break epics into stories with As a/I want/So that, Given/When/Then criteria, tasks, and story points."},
            {"step": 4, "name": "Final Validation", "description": "FR coverage check, dependency validation, estimation sanity, architecture alignment. Generate summary."},
        ],
        "template": "epic",
        "supports_apc": True,
    },
    "sprint-planning": {
        "id": "sprint-planning",
        "name": "Sprint Planning",
        "persona": "scrum-master",
        "description": "Plan sprints with intelligent status detection and story selection.",
        "steps": [
            {"step": 1, "name": "Parse Epics", "description": "Extract all work items from epic files. Build complete work item inventory."},
            {"step": 2, "name": "Build Sprint Status", "description": "Create sprint-status YAML structure with epic/story status hierarchy."},
            {"step": 3, "name": "Intelligent Status Detection", "description": "Apply smart rules to determine current status. Detect blockers and ready-for-dev stories."},
            {"step": 4, "name": "Generate Sprint Plan", "description": "Select stories by priority, dependencies, and capacity. Create sprint-status.yaml."},
            {"step": 5, "name": "Validate & Report", "description": "Verify sprint readiness, identify critical path, generate sprint report."},
        ],
        "template": None,
        "supports_apc": True,
    },
    "create-story": {
        "id": "create-story",
        "name": "Create Story",
        "persona": "scrum-master",
        "description": "Create implementation-ready user story with exhaustive artifact analysis and dev guardrails.",
        "steps": [
            {"step": 1, "name": "Discover — Find Next Story", "description": "Check sprint-status for next backlog story. Load epic context and confirm selection."},
            {"step": 2, "name": "Analyze — Artifact Analysis", "description": "Exhaustive analysis of PRD, architecture, UX spec, and epic. Extract all relevant context."},
            {"step": 3, "name": "Previous Intelligence", "description": "Review completed stories, established patterns, existing components, and tech debt."},
            {"step": 4, "name": "Research", "description": "Investigate technical specifics, best practices, library details. Validate assumptions."},
            {"step": 5, "name": "Create — Story File", "description": "Write comprehensive story with BDD criteria, tasks, dev notes, and references."},
            {"step": 6, "name": "Update Status", "description": "Update sprint-status.yaml. Mark story as ready-for-dev. Save deliverable."},
        ],
        "template": "story",
        "supports_apc": True,
    },
}


def get_workflow(workflow_id: str) -> dict | None:
    return WORKFLOWS.get(workflow_id)


def get_all_workflows() -> list[dict]:
    return list(WORKFLOWS.values())


def get_workflow_prompt(workflow_id: str) -> str:
    """Load workflow instructions from bmad_data/workflows/"""
    filename = f"{workflow_id}.md"
    path = os.path.join(settings.BMAD_DATA_PATH, "workflows", filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""
