# Generate Code Skeleton Workflow

## Overview
Translate ONE story (E#-S#) into a concrete directory tree and function-signature
scaffold. The output is a developer-ready structure — **no business logic**, only
the shape: files, signatures, and TODO markers tagged with the BDD scenario they
implement.

The output file is saved under `construction-artifacts/E{epicNum}-S{storyNum}-skeleton.md`.

## Step-by-Step Instructions

### Step 1: Load Story
**Goal:** Anchor the work to a specific story.

- Ask the user: "Which story should we scaffold? (E#-S# or story title)"
- Load the corresponding story file from `implementation-artifacts/`.
- Load the architecture document and the `tech-stack` context file if present.
- Confirm the story anchor (e.g. `E1-S3`) before producing any content.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Plan File Tree
**Goal:** Decide which files are created or touched by this story.

- Produce a directory tree block. Mark each entry as NEW, MODIFIED, or TOUCH.
- For every entry, write a one-line purpose statement.
- Do NOT list files outside this story's scope.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Define Modules
**Goal:** Define the functions/classes each file exposes, signatures only.

- For each NEW or MODIFIED file, list function/class signatures.
- Include parameter names, types (or type hints), and return types.
- DO NOT write function bodies — leave `pass` / `throw NotImplementedError` / `// TODO`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Decompose TODOs
**Goal:** Tie every signature to a BDD scenario.

- Inside each function body, add `TODO(E#-S#:<scenario-id>): <what this step does>`.
- Cover EVERY Given/When/Then scenario from the story at least once.
- Flag any scenario that cannot fit in this scope — those become spec gaps.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Save Skeleton
**Goal:** Produce and save the final code-skeleton artifact.

- Use the `code-skeleton` template structure.
- Add `<!-- derived_from: STORY#E{n}-S{n}, ARCH#C-{n} -->` near the top so
  downstream traceability works.
- Wrap the full document in `<!-- SAVE_FILE: construction-artifacts/E{n}-S{n}-skeleton.md -->`
  and `<!-- END_FILE -->`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## Completion
After saving, suggest next steps:
- Hand off to **Create Test Plan** with Quinn (QA).
- Implement the TODOs in order of BDD scenario priority.
