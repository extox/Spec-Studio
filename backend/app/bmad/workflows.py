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
    "goal-backward-analysis": {
        "id": "goal-backward-analysis",
        "name": "Goal-Backward Analysis",
        "persona": "analyst",
        "recommended_persona": "analyst",
        "description": "Decompose a goal into the verifiable preconditions that must be true for it to be achieved, then map those preconditions to PRD requirements (existing or new).",
        "steps": [
            {"step": 1, "name": "State the Goal", "description": "Have the user state ONE concrete goal. Refuse vague goals — push for measurable outcome."},
            {"step": 2, "name": "Surface Assumptions", "description": "List the unspoken assumptions baked into the goal. What must be true about users, market, tech, ops?"},
            {"step": 3, "name": "Decompose into Preconditions", "description": "Recursively ask: 'For this to be true, what must first be true?' until each leaf is automatically verifiable (testable, measurable, observable)."},
            {"step": 4, "name": "Map to FRs", "description": "Match each verifiable precondition to an existing FR/NFR anchor (PRD#FR-001) or propose a NEW FR with a fresh anchor ID."},
            {"step": 5, "name": "Detect Gaps", "description": "List preconditions that have no FR coverage. These are gaps in the spec."},
            {"step": 6, "name": "Inject into PRD", "description": "Produce a delta-document that the user can merge into PRD: new FRs to add, existing FRs to amend. Use SAVE_FILE markers if the user approves direct merge."},
        ],
        "template": None,
        "supports_apc": True,
    },
    "generate-code-skeleton": {
        "id": "generate-code-skeleton",
        "name": "Generate Code Skeleton",
        "persona": "developer",
        "recommended_persona": "developer",
        "description": "Turn a story (E#-S#) into a directory tree + function signatures + TODO markers. No business logic — just the scaffold a developer can extend.",
        "steps": [
            {"step": 1, "name": "Load Story", "description": "Confirm the story ID (E#-S#). Load the story file, the architecture, and the tech-stack context."},
            {"step": 2, "name": "Plan File Tree", "description": "Propose the directory tree affected by this story. Each entry: path, purpose."},
            {"step": 3, "name": "Define Modules", "description": "For each new file, define functions/classes with signatures (types only, no body)."},
            {"step": 4, "name": "Decompose TODOs", "description": "Inside each function, add TODO comments tagged with the BDD scenario id they cover."},
            {"step": 5, "name": "Save Skeleton", "description": "Compose the code-skeleton template, add derived_from markers, and save with the SAVE_FILE marker."},
        ],
        "template": "code-skeleton",
        "supports_apc": True,
    },
    "create-test-plan": {
        "id": "create-test-plan",
        "name": "Create Test Plan",
        "persona": "qa-engineer",
        "recommended_persona": "qa-engineer",
        "description": "Convert a story's BDD acceptance criteria into a complete test matrix with unit/integration/E2E classification, edge cases, and fixtures.",
        "steps": [
            {"step": 1, "name": "Load Story BDD", "description": "Load the story file. Extract every Given/When/Then scenario."},
            {"step": 2, "name": "Classify Tests", "description": "For each scenario, decide unit / integration / e2e and justify."},
            {"step": 3, "name": "Add Negative Cases", "description": "For every happy path, add at least one negative/error path test."},
            {"step": 4, "name": "Design Fixtures", "description": "List the fixtures, seed data, and mocks required."},
            {"step": 5, "name": "Identify Risks", "description": "Call out untested risk areas and flaky-test risks."},
            {"step": 6, "name": "Save Test Plan", "description": "Compose the test-plan template and save with SAVE_FILE marker."},
        ],
        "template": "test-plan",
        "supports_apc": True,
    },
    "design-ci-pipeline": {
        "id": "design-ci-pipeline",
        "name": "Design CI Pipeline",
        "persona": "devops-engineer",
        "recommended_persona": "devops-engineer",
        "description": "Design a CI/CD pipeline derived from architecture + tech-stack inputs. Vendor-neutral YAML; trivially mappable to GitHub Actions / GitLab / Jenkins.",
        "steps": [
            {"step": 1, "name": "Load Inputs", "description": "Load architecture document and tech-stack context. Confirm target environments (dev/staging/prod)."},
            {"step": 2, "name": "Define Triggers", "description": "Decide what events trigger the pipeline (push, PR, tag, schedule)."},
            {"step": 3, "name": "Stage Design", "description": "Define stages: build → test → quality gate → deploy. For each, success criteria and failure behavior."},
            {"step": 4, "name": "Quality Gates", "description": "Define gating policy (coverage thresholds, security scans, manual approvals)."},
            {"step": 5, "name": "Save Pipeline", "description": "Save the ci-pipeline.yaml with derived_from markers tying stages to architecture components."},
        ],
        "template": "ci-pipeline",
        "supports_apc": True,
    },
    "create-iac": {
        "id": "create-iac",
        "name": "Create IaC",
        "persona": "devops-engineer",
        "recommended_persona": "devops-engineer",
        "description": "Generate a vendor-neutral IaC sketch (resources, dependencies, environments) that maps cleanly to Terraform/CDK/Bicep.",
        "steps": [
            {"step": 1, "name": "Load Architecture", "description": "Load architecture, identify deployable components, confirm cloud target (AWS/GCP/Azure/on-prem)."},
            {"step": 2, "name": "Resource Inventory", "description": "List every resource needed (compute, storage, network, secret, identity)."},
            {"step": 3, "name": "Dependencies", "description": "Map resource dependencies (which resource depends on which)."},
            {"step": 4, "name": "Network Topology", "description": "Define VPC/subnet/security group structure."},
            {"step": 5, "name": "Secrets & Config", "description": "List secrets and config values per environment. Use placeholders, NEVER plaintext."},
            {"step": 6, "name": "Save IaC", "description": "Save iac.yaml with derived_from markers tying resources back to architecture components."},
        ],
        "template": "iac",
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
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
