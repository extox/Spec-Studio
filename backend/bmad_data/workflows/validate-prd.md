# Validate PRD Workflow (13 Validation Checks)

## Overview
Systematically validate an existing PRD for completeness, consistency, and quality. Each check produces a pass/fail/warning result with specific feedback.

## Prerequisites
- An existing PRD document must be loaded

## Validation Checks

### Check 1: Document Structure
- Verify all required sections are present
- Check section ordering is logical
- Validate frontmatter/metadata is complete
- **Result:** List of missing or misplaced sections

### Check 2: Executive Summary Quality
- Is it clear and compelling?
- Does it accurately summarize the full document?
- Can someone understand the product from this alone?
- **Result:** Pass/Fail with specific improvement suggestions

### Check 3: Problem Statement Clarity
- Is the problem clearly articulated?
- Is the target audience defined?
- Are current alternatives mentioned?
- **Result:** Pass/Fail with clarity score

### Check 4: Success Criteria Measurability
- Are all success criteria measurable?
- Do they have specific targets/thresholds?
- Are timeframes defined?
- **Result:** List of unmeasurable criteria

### Check 5: User Journey Completeness
- Are all user types covered?
- Do journeys cover happy path AND edge cases?
- Are emotional states and pain points captured?
- **Result:** Coverage matrix

### Check 6: Functional Requirements Coverage
- Do FRs cover all user journey touchpoints?
- Is every FR traceable to a user need?
- Are FRs specific enough for implementation?
- No duplicate or contradictory requirements?
- **Result:** Coverage gaps and conflicts

### Check 7: FR-NFR Alignment
- Do NFRs support the FR requirements?
- Are performance targets realistic given the FRs?
- Are security requirements appropriate for the data handled?
- **Result:** Alignment matrix

### Check 8: Scope Consistency
- Does MVP scope match Must-Have priorities?
- Are phase boundaries clear?
- Are Won't-Have items truly excluded?
- **Result:** Scope conflict list

### Check 9: Technical Feasibility
- Are there FRs that may be technically infeasible?
- Are integration dependencies identified?
- Are there hidden complexity traps?
- **Result:** Risk-flagged requirements

### Check 10: Completeness Check
- Are there gaps in the requirement chain?
- Are error/failure scenarios covered?
- Are admin/ops requirements included?
- **Result:** Gap analysis

### Check 11: Consistency Check
- Terminology used consistently throughout?
- No contradictory statements between sections?
- Priorities consistent across all sections?
- **Result:** Inconsistency list

### Check 12: Clarity & Ambiguity
- Are there vague terms (e.g., "fast", "easy", "good")?
- Are all acronyms defined?
- Could any requirement be interpreted multiple ways?
- **Result:** Ambiguity list with suggested rewrites

### Check 13: Final Assessment
- Generate overall quality score (1-10)
- Summarize critical issues vs nice-to-have improvements
- Prioritize recommended changes
- Provide final verdict: Ready for Architecture / Needs Revision / Major Rework
- **Result:** Summary report with actionable recommendations

## Output Format
Present results as a validation report with:
- Overall score and verdict
- Section-by-section results
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)
