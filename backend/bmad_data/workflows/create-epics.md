# Create Epics and Stories Workflow (4 Steps)

## Overview
Break down the PRD and architecture into implementation-ready epics with stories. Every epic must trace to requirements, and every story must be detailed enough for a developer to implement.

## Prerequisites
- PRD document (required)
- Architecture document (required)
- UX specification (recommended)

## Step-by-Step Instructions

### Step 1: Validate Prerequisites
**Goal:** Ensure all necessary inputs exist and are aligned.

- Verify PRD exists and is complete
- Verify Architecture document exists
- Load UX specification if available
- Create Requirements Inventory:
  - List all Functional Requirements (FRs)
  - List all Non-Functional Requirements (NFRs)
  - List additional requirements from architecture
  - List UX design requirements
- Build FR Coverage Map (to track which FRs are covered by epics)
- Flag any misalignments between artifacts

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Design Epics
**Goal:** Identify and outline major epics from requirements.

- Group related requirements into logical epics
- For each epic define:
  - Epic ID (E-XXX)
  - Title and description
  - Business value and justification
  - Requirements covered (FR IDs)
  - Dependencies on other epics
  - Estimated complexity (S/M/L/XL)
  - Priority and suggested phase (MVP/Growth/Vision)
- Ensure every FR is mapped to at least one epic
- Order epics by dependency and priority

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Create Stories with BDD Acceptance Criteria
**Goal:** Break each epic into implementable stories.

- For each story within an epic:
  - Story ID (S-XXX)
  - User story format: "As a [user], I want [action], so that [benefit]"
  - BDD Acceptance Criteria:
    - Given [context]
    - When [action]
    - Then [expected result]
  - Technical tasks (as checkboxes)
  - Story points estimate (Fibonacci: 1, 2, 3, 5, 8, 13)
  - Dev notes (architecture patterns, references)
- Stories should be:
  - Independent (can be developed in isolation where possible)
  - Negotiable (details can be discussed)
  - Valuable (delivers user or business value)
  - Estimable (clear enough to size)
  - Small (completable in one sprint)
  - Testable (clear acceptance criteria)

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Final Validation
**Goal:** Verify completeness and readiness.

- FR Coverage check: Every FR mapped to at least one story
- Dependency validation: No circular dependencies
- Estimation sanity check: No stories > 13 points
- Architecture alignment: Stories reference correct patterns
- Generate summary:
  - Total epics and stories
  - Story point distribution
  - Critical path
  - Recommended sprint order
- Save epic documents as deliverables
- Suggest next steps:
  - **Sprint Planning** — Plan first sprint with Bob
  - **Implementation Readiness** — Full cross-artifact check
  - **Review with PM** — Validate with John

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue
