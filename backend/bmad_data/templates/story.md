---
storyId: '{{story_id}}'
epicId: '{{epic_id}}'
status: 'backlog'
points: 0
---
# Story: {{story_title}}

**ID:** {{story_id}}
**Epic:** {{epic_id}} - {{epic_title}}
**Points:** {{points}}
**Status:** {{status}}

---

## Story

**As a** {{user_type}},
**I want** {{action}},
**So that** {{benefit}}.

## Acceptance Criteria

```gherkin
Scenario: {{scenario_name}}
  Given {{context}}
  When {{action}}
  Then {{expected_result}}

Scenario: {{scenario_name_2}}
  Given {{context}}
  When {{action}}
  Then {{expected_result}}

Scenario: Error - {{error_scenario}}
  Given {{context}}
  When {{action}}
  Then {{error_result}}
```

## Tasks / Subtasks

- [ ] 1. {{task_1}}
  - [ ] 1.1 {{subtask}}
  - [ ] 1.2 {{subtask}}
- [ ] 2. {{task_2}}
- [ ] 3. {{task_3}}
- [ ] 4. Write unit tests
- [ ] 5. Write integration tests
- [ ] 6. Update documentation

## Dev Notes

### Architecture Patterns

<!-- Specific architecture patterns to follow for this story -->

### Project Structure

<!-- Files and modules that will be created or modified -->

```
src/
├── ...
```

### References

- PRD: {{fr_ids}}
- Architecture: {{adr_ids}}
- UX Spec: {{ux_section}}
- Related Stories: {{related_story_ids}}

### Technical Guidance

<!-- Specific technical notes, gotchas, or recommendations -->

---

## Dev Agent Record

<!-- Filled during implementation -->

| Field | Value |
|-------|-------|
| Model Used | |
| Start Time | |
| End Time | |
| Tasks Completed | /{{total_tasks}} |
| Tests Passing | |

### Debug Log

<!-- Notable issues encountered during implementation -->

### Completion Notes

<!-- Summary of what was implemented and any deviations from plan -->

### Files Modified

| File | Action | Description |
|------|--------|-------------|
| | Created/Modified/Deleted | |
