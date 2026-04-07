# Sprint Planning Workflow (5 Steps)

## Overview
Plan sprints by parsing epic files, building status tracking, and creating an actionable sprint plan with intelligent status detection.

## Prerequisites
- Epic documents with stories (required)
- Architecture document (recommended)

## Step-by-Step Instructions

### Step 1: Parse Epics
**Goal:** Extract all work items from epic files.

- Load all epic documents from the project
- Extract:
  - All epics with their metadata
  - All stories within each epic
  - Story point estimates
  - Dependencies between stories
  - Current status of each item (if previously tracked)
- Build a complete work item inventory

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Build Sprint Status Structure
**Goal:** Create the sprint status YAML structure.

- Organize work items into sprint-status format:
  ```yaml
  development_status:
    epic-id:
      status: backlog|in-progress|done
      stories:
        story-id:
          status: backlog|ready-for-dev|in-progress|review|done
      retrospective:
        status: optional|done
  ```
- Apply status hierarchy rules:
  - Epic is "in-progress" if any story is in-progress
  - Epic is "done" if all stories are done
  - Otherwise epic is "backlog"

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Intelligent Status Detection
**Goal:** Apply smart rules to determine current status.

- Check for existing sprint-status.yaml
- If exists, preserve existing statuses
- Apply detection rules:
  - Stories with completed tasks → "in-progress" or "review"
  - Stories with no started tasks → "backlog"
  - Stories with all tasks done → "done"
- Detect blockers and flag them
- Identify ready-for-dev stories (all dependencies met)

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Generate Sprint Plan
**Goal:** Create the sprint plan with story selection.

- Recommend stories for the next sprint based on:
  - Priority (Must-Have first)
  - Dependencies (prerequisite stories first)
  - Story points capacity
  - Team capability alignment
- Sprint plan includes:
  - Sprint goal
  - Selected stories with point total
  - Dependency order for implementation
  - Risk items and mitigation
- Generate sprint-status.yaml

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Validate & Report
**Goal:** Verify sprint readiness and generate report.

- Validate:
  - Sprint point total is within capacity
  - No unresolved dependencies
  - All selected stories are "ready-for-dev"
  - Critical path is identified
- Generate sprint report:
  - Sprint overview
  - Story list with assignments
  - Definition of done criteria
  - Sprint timeline
- Present recommendations:
  - **Create Story** — Detail a specific story
  - **Correct Course** — Adjust sprint if needed
  - **Start Development** — Begin implementation

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue
