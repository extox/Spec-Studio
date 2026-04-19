# Create Story Workflow (6 Steps)

## Overview
Create a comprehensive, implementation-ready user story by exhaustively analyzing all project artifacts and producing a detailed story file with BDD acceptance criteria and dev guardrails.

## Prerequisites
- Epic documents (required)
- Sprint status (recommended)
- PRD, Architecture, UX spec (recommended)

## Step-by-Step Instructions

### Step 1: Discover — Find Next Story
**Goal:** Identify the next story to detail.

- Check sprint-status.yaml for next backlog story
- If no sprint status, ask user which story to create
- Load the story's epic context:
  - Epic description and goals
  - Story's position in the epic
  - Related stories and dependencies
- Confirm story selection with user

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Analyze — Exhaustive Artifact Analysis
**Goal:** Gather all relevant context from project artifacts.

- Deep analysis of all related artifacts:
  - **PRD:** Relevant functional requirements, NFRs, user journeys
  - **Architecture:** Relevant patterns, data models, API designs
  - **UX Spec:** Relevant screens, interactions, components
  - **Epic:** Story context, acceptance criteria outline
- Extract:
  - All relevant requirements (by ID)
  - Technical constraints and patterns to follow
  - UX requirements and interaction details
  - Edge cases and error scenarios

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Previous Intelligence
**Goal:** Learn from previous stories and implementation.

- Review completed stories in the same epic:
  - Patterns established
  - Lessons learned
  - Reusable components created
- Check for architectural decisions that affect this story
- Identify what already exists vs what needs to be built
- Note any technical debt or constraints from previous work

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Research
**Goal:** Investigate technical specifics and best practices.

- Research specific technical aspects needed:
  - Library or framework specifics
  - API integration details
  - Best practices for the patterns involved
- Validate assumptions against current technology state
- Document any technical risks or uncertainties

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Create — Comprehensive Story File
**Goal:** Write the complete story document.

- Story file structure:
  - **Story:** As a [user], I want [action], so that [benefit]
  - **Acceptance Criteria (BDD):**
    - Given [context] / When [action] / Then [result]
    - Cover happy path, edge cases, error cases
  - **Tasks/Subtasks:** Numbered checkbox list
    - Each task is a concrete, implementable unit
    - Tasks ordered by logical implementation sequence
    - Include test tasks for each feature task
  - **Dev Notes:**
    - Architecture patterns to follow
    - Project structure references
    - Related files and modules
    - Specific technical guidance
  - **References:**
    - PRD requirement IDs
    - Architecture decision IDs
    - UX spec section references
- Present for review and refinement

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: Update Status
**Goal:** Update sprint tracking and finalize.

- Update sprint-status.yaml:
  - Mark story as "ready-for-dev"
- Save story as project deliverable using the filename format:
  `implementation-artifacts/E{epicNum}-S{storyNum}-{story-slug}.md`
  (e.g., `implementation-artifacts/E1-S3-user-login.md`).
  Each story MUST have a unique filename — NEVER save as `story.md`.
- Present summary:
  - Story overview
  - Task count and complexity
  - Dependencies and prerequisites
  - Recommended implementation order
- Suggest next steps:
  - **Create another story** — Continue with next backlog item
  - **Sprint Planning** — Review sprint plan
  - **Back to Epics** — Review epic progress

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue
