---
stepsCompleted: []
inputDocuments: []
workflowType: 'epics'
project_name: '{{project_name}}'
---
# Epics & Stories - {{project_name}}

**Date:** {{date}}
**Status:** Draft

<!--
Anchor Convention (for traceability):
- Epics: E-001, E-002, ... (or E1, E2)
- Stories: S-001, S-002, ... or per-epic E1-S1, E1-S2
- Each Epic/Story should declare which FRs it covers via a derived_from marker
  placed under its heading:
    ## Epic 1: User Auth (E-001)
    <!-- derived_from: PRD#FR-001, PRD#FR-002, PRD#NFR-003 -->
-->

---

## Requirements Inventory

### Functional Requirements (from PRD)

| FR ID | Description | Priority | Epic Mapping |
|-------|------------|----------|-------------|
| | | | |

### Non-Functional Requirements

| NFR ID | Description | Category | Epic Mapping |
|--------|------------|----------|-------------|
| | | | |

### UX Design Requirements

| UX ID | Description | Epic Mapping |
|-------|------------|-------------|
| | | |

## FR Coverage Map

<!-- Track which FRs are covered by which epics/stories -->

| FR ID | Epic | Story | Status |
|-------|------|-------|--------|
| | | | Covered/Partial/Uncovered |

---

## Epic 1: {{Epic Title}} (E-001)

<!-- derived_from: PRD#FR-001 -->

**ID:** E-001
**Priority:** Must-Have
**Phase:** MVP
**Complexity:** S/M/L/XL
**Dependencies:** None

### Description

<!-- What this epic delivers and why -->

### Stories

#### Story 1.1: {{Story Title}}

**ID:** S-001
**Points:** 

**As a** {{user type}},
**I want** {{action}},
**So that** {{benefit}}.

**Acceptance Criteria:**

```gherkin
Given {{context}}
When {{action}}
Then {{expected result}}

Given {{context}}
When {{action}}
Then {{expected result}}
```

**Tasks:**

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
- [ ] Write tests

**Dev Notes:**
- Architecture pattern: 
- Related files: 
- References: 

---

#### Story 1.2: {{Story Title}}

**ID:** S-002
**Points:** 

**As a** {{user type}},
**I want** {{action}},
**So that** {{benefit}}.

**Acceptance Criteria:**

```gherkin
Given {{context}}
When {{action}}
Then {{expected result}}
```

**Tasks:**

- [ ] Task 1
- [ ] Task 2
- [ ] Write tests

**Dev Notes:**
- 

---

## Epic 2: {{Epic Title}}

**ID:** E-002
**Priority:** 
**Phase:** 
**Complexity:** 
**Dependencies:** E-001

### Description

### Stories

#### Story 2.1: {{Story Title}}

<!-- Repeat story structure -->

---

## Summary

| Metric | Value |
|--------|-------|
| Total Epics | |
| Total Stories | |
| Total Story Points | |
| Must-Have Points | |
| Should-Have Points | |
| Could-Have Points | |
