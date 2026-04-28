# Design CI Pipeline Workflow

## Overview
Design a CI/CD pipeline grounded in the project's architecture and tech-stack.
The output is a vendor-neutral YAML that maps cleanly to GitHub Actions,
GitLab CI, or Jenkins.

The output file is saved under `construction-artifacts/ci-pipeline.yaml`.

## Step-by-Step Instructions

### Step 1: Load Inputs
**Goal:** Anchor the pipeline to real architecture.

- Load `planning-artifacts/architecture.md` and the `tech-stack` context file.
- Ask the user to confirm target environments (dev / staging / prod) and
  the deploy surface (container registry, serverless platform, etc.).
- List the architecture components that the pipeline must produce artifacts for.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Define Triggers
**Goal:** Decide when the pipeline runs.

- List triggers: push to main, pull-request open/update, tag, manual, schedule.
- For each trigger, specify which stages run (some triggers skip deploy).

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Stage Design
**Goal:** Define the stages and their contract.

- Stages: `build → lint → test → security-scan → package → deploy`.
- For each stage, state:
  - `success_criteria:` exit code 0 + any required artifact
  - `on_failure:` what happens if it fails (block merge, notify, etc.)
  - `artifacts:` what is emitted for downstream stages

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Quality Gates
**Goal:** Define the gating rules that hold quality at acceptable levels.

- Coverage thresholds (line, branch).
- Security scan policy (fail on HIGH/CRITICAL only).
- Manual approval points (usually prod deploy).
- Rollback triggers.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Save Pipeline
**Goal:** Produce and save the final ci-pipeline artifact.

- Use the `ci-pipeline` YAML template.
- Add `<!-- derived_from: ARCH#C-{n} -->` as a comment block above any stage
  specific to an architecture component.
- Wrap in `<!-- SAVE_FILE: construction-artifacts/ci-pipeline.yaml -->`
  and `<!-- END_FILE -->`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## Completion
After saving, suggest next steps:
- Hand off to **Create IaC** to pair the pipeline with infrastructure.
- Convert the vendor-neutral YAML to the actual CI vendor syntax.
