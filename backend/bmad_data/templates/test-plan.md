---
storyId: '{{story_id}}'
workflowType: 'test-plan'
date: '{{date}}'
---
# Test Plan — {{story_title}}

<!-- derived_from: STORY#{{story_id}} -->

**Story:** {{story_id}} — {{story_title}}
**Date:** {{date}}
**Status:** Draft

---

## 1. Scenario Inventory

| Scenario ID | BDD Summary | Source (story line) |
|-------------|-------------|---------------------|
| {{story_id}}-SC1 | Given ... When ... Then ... | Story §3 |
| {{story_id}}-SC2 | Given ... When ... Then ... | Story §3 |

## 2. Test Matrix

| Test ID | Scenario | Level | Rationale | Input | Expected |
|---------|----------|-------|-----------|-------|----------|
| T-001 | {{story_id}}-SC1 | unit | no I/O | {{input}} | {{expected}} |
| T-002 | {{story_id}}-SC1-NEG1 | unit | negative | {{bad input}} | error X |
| T-003 | {{story_id}}-SC2 | integration | touches DB | {{input}} | {{expected}} |
| T-004 | {{story_id}}-SC2-NEG1 | integration | permission denied | {{input}} | 403 |

Level legend: `unit` (pure logic, no I/O), `integration` (crosses a boundary),
`e2e` (full stack, user-facing).

## 3. Fixtures & Seed Data

| Name | Shape | Purpose | Scope |
|------|-------|---------|-------|
| {{fixture_name}} | `{...}` | {{what it's for}} | per-test / per-suite |

## 4. Mocks & Stubs

| Interface | Strategy | Reset Point |
|-----------|----------|-------------|
| {{interface}} | stub / fake / mock | per-test / per-suite |

## 5. Risk & Coverage Notes

### Untested Risks
<!-- What is NOT being tested here, and why -->
- 

### Flaky Test Risks
<!-- Timing, concurrency, external service risks -->
- 

### Follow-up Tests
<!-- Tests to add later and the trigger for adding them -->
- 

## 6. Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| {{test_runner}} | Unit + integration | |
| {{e2e_tool}} | E2E | Runs only in CI |

## 7. Next Steps

- [ ] Developer (Dex) wires the fixtures into the skeleton.
- [ ] QA reviews test results after each BDD scenario is implemented.
