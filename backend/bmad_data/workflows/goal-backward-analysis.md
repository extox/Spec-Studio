# Goal-Backward Analysis Workflow

## Overview
Take a single high-level goal and decompose it into the verifiable preconditions
that must be true for the goal to be achieved. Then map those preconditions to
existing PRD anchors (FR-001, NFR-001, ...) or surface them as gaps to add.

The output is a **delta-document**: a short note describing which FRs to add
or amend in the PRD, with stable anchor IDs ready to be merged.

This workflow is the entry point for traceability — every downstream artifact
will eventually trace back to one of the FRs produced here.

## Step-by-Step Instructions

### Step 1: State the Goal
**Goal:** Force the user to commit to ONE concrete, measurable goal.

- Ask: "What is the single goal you want this analysis to serve?"
- Reject vague goals like "make it better" — push for measurable outcome.
- Restate the goal back to the user in one sentence and confirm.
- **Do NOT generate content yet** — only capture the goal verbatim.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Surface Assumptions
**Goal:** Make the implicit assumptions inside the goal explicit.

- Ask: "What must be true about users, market, tech, operations, or compliance
  for this goal to even be reachable?"
- List 3–7 assumptions. For each, mark whether it is verified or unverified.
- Flag any assumption the user cannot defend — those become risks.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Decompose into Preconditions
**Goal:** Recursively expand the goal into a tree of verifiable preconditions.

- Ask repeatedly: "For X to be true, what must first be true?"
- Stop expanding a branch when the leaf is automatically verifiable —
  i.e., a test, a metric, or a directly observable behavior.
- Render the result as an indented list (Markdown bullet tree) so the
  hierarchy is visible.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Map Preconditions to FRs
**Goal:** Connect each leaf precondition to a PRD anchor.

- Load the existing PRD (file `planning-artifacts/PRD.md`) if available.
- For each leaf precondition, attempt to match it to an existing FR-### or
  NFR-### in the PRD. Cite the matched anchor (e.g. `→ PRD#FR-014`).
- Where no existing FR matches, propose a NEW anchor:
  - Use the next available number in the FR sequence.
  - Write a one-line FR statement.
- Group the result as a table: precondition | anchor | status (existing/new).

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Detect Gaps
**Goal:** Surface preconditions that have no FR coverage.

- List every precondition whose status is "new" — these are spec gaps.
- For each gap, briefly explain why it matters and what risks it carries
  if left uncovered.
- Ask the user which gaps to merge into the PRD now and which to defer.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: Inject into PRD
**Goal:** Produce the delta-document the user can merge into the PRD.

- Compose a markdown delta with two sections:
  - **New FRs to add:** stable anchor + statement + suggested priority.
  - **Existing FRs to amend:** the existing anchor + the proposed change.
- Place a `<!-- derived_from: ... -->` marker after each new FR to record
  the originating goal/precondition for traceability.
- If the user approves direct merge, output the updated PRD wrapped in
  `<!-- SAVE_FILE: planning-artifacts/PRD.md --> ... <!-- END_FILE -->`
  with all anchors preserved.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## Completion
Suggest next steps after the analysis:
- Run **Validate PRD** to verify consistency after the merge.
- Move to **Create Architecture** to design components for the new FRs.
- Re-run the analysis with a different goal to broaden coverage.
