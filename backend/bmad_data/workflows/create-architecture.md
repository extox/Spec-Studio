# Create Architecture Workflow (8 Steps)

## Overview
Design a comprehensive system architecture based on PRD and project requirements. Every decision must be justified with rationale and documented trade-offs.

## Prerequisites
- PRD document should exist (strongly recommended)
- Project brief or equivalent context

## Step-by-Step Instructions

### Step 1: Init — Input Discovery & Context Loading
**Goal:** Gather all available context before making any decisions.

- Load and review available artifacts:
  - PRD (functional and non-functional requirements)
  - Project brief
  - UX specifications (if available)
  - Any existing technical documentation
- Identify constraints:
  - Team size and expertise
  - Timeline and budget
  - Existing infrastructure or technology commitments
  - Compliance and regulatory requirements
- Summarize the architectural challenge

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Context & Requirements Analysis
**Goal:** Deeply analyze requirements to inform architecture decisions.

- Categorize requirements by architectural impact:
  - High-impact (drives major architecture decisions)
  - Medium-impact (influences component design)
  - Low-impact (implementation detail)
- Identify architectural drivers:
  - Quality attributes (performance, scalability, security, etc.)
  - Key functional requirements with system-wide impact
  - Integration requirements
- Map constraints to architectural trade-offs

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Starter Architecture Decisions
**Goal:** Establish the high-level architecture direction.

- Choose architectural style:
  - Monolith, modular monolith, microservices, serverless, hybrid
  - Justify the choice based on requirements and constraints
- Define deployment model:
  - Cloud provider, on-premise, hybrid
  - Containerization strategy
- Identify major system components at a high level
- Document as Architecture Decision Records (ADRs)

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Technical Decisions Documentation
**Goal:** Make and document detailed technology choices.

For each technology choice, document:
- **Context:** Why is this decision needed?
- **Decision:** What was chosen?
- **Rationale:** Why this over alternatives?
- **Consequences:** What are the trade-offs?
- **Alternatives Considered:** What else was evaluated?

Key decisions to make:
- Programming languages and frameworks
- Database(s) and data storage strategy
- Authentication and authorization approach
- API design style (REST, GraphQL, gRPC)
- Message queuing and event handling
- Caching strategy
- CI/CD and deployment tools

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Architecture Patterns
**Goal:** Define system patterns, data flow, and integration.

- System component diagram:
  - Major components and their responsibilities
  - Communication patterns between components
  - Data flow (request/response, event-driven, batch)
- Database design:
  - Entity relationships (high-level)
  - Data partitioning strategy
  - Read/write patterns
- API design:
  - Endpoint structure
  - Authentication flow
  - Error handling patterns
- Integration patterns:
  - External service integration
  - Third-party API consumption

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: Project Structure
**Goal:** Define folder structure and module organization.

- Define the project directory structure
- Module boundaries and dependencies
- Package/module naming conventions
- Configuration management approach
- Environment management (dev, staging, prod)
- Coding standards and patterns to follow

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 7: Validation
**Goal:** Cross-reference architecture with PRD requirements.

- Verify every FR can be implemented with the chosen architecture
- Verify NFRs are achievable:
  - Performance targets
  - Scalability requirements
  - Security requirements
- Check for:
  - Single points of failure
  - Scalability bottlenecks
  - Security vulnerabilities in the design
  - Operational complexity concerns
- Document any PRD requirements that need revision based on technical reality

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 8: Complete — Document Finalization
**Goal:** Finalize the architecture document.

- Compile all decisions into the architecture template
- Generate summary diagrams (described in text/Mermaid)
- Present the complete architecture document
- Suggest next steps:
  - **Implementation Readiness Check** — Full cross-artifact alignment
  - **Create Epics** — Move to Bob (Scrum Master) for work breakdown
  - **Edit Architecture** — Refine specific sections
- Save final deliverable

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue
