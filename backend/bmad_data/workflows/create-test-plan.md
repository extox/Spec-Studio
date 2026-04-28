# Create Test Plan Workflow

## Overview
Convert a story's BDD acceptance criteria into a complete, defensible test plan:
a matrix of tests classified by level (unit/integration/e2e), with negative cases,
fixtures, and an explicit risk note.

The output file is saved under `construction-artifacts/E{epicNum}-S{storyNum}-test-plan.md`.

## Step-by-Step Instructions

### Step 1: Load Story BDD
**Goal:** Extract every Given/When/Then from the story.

- Load the story file from `implementation-artifacts/`.
- List every scenario. Give each a scenario-id like `E1-S3-SC1`.
- Confirm you captured them all before moving on.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Classify Tests
**Goal:** Decide the test level for each scenario.

- For each scenario, choose `unit` / `integration` / `e2e`.
- Justify the choice in one short phrase (e.g. "no I/O → unit").
- Prefer lower levels when the same confidence is achievable.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Add Negative Cases
**Goal:** Defend against hostile inputs and error paths.

- For every happy-path scenario, add at least one negative-path test:
  invalid input, missing field, timeout, permission denied, race, etc.
- Give each its own scenario-id (e.g. `E1-S3-SC1-NEG1`).

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Design Fixtures
**Goal:** List the test data and mocks needed.

- Fixtures table: `name | shape | purpose | scope (per-test / per-suite)`.
- Mocks table: `interface | strategy (stub/fake/mock) | reset point`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Identify Risks
**Goal:** Surface what is NOT being tested.

- Flag known flaky-test risks (time, concurrency, network).
- Flag untested risk areas and why (cost, infra not available, etc.).
- Propose follow-up tests to add later with clear triggers.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: Save Test Plan
**Goal:** Produce and save the final test-plan artifact.

- Use the `test-plan` template structure.
- Add `<!-- derived_from: STORY#E{n}-S{n} -->` near the top.
- Wrap in `<!-- SAVE_FILE: construction-artifacts/E{n}-S{n}-test-plan.md -->`
  and `<!-- END_FILE -->`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## Completion
After saving, suggest next steps:
- Hand off to **Generate Code Skeleton** with Dex (Developer) if not done yet.
- Run the plan against the implementation as it progresses.
