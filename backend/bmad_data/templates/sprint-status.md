---
workflowType: 'sprint-status'
project_name: '{{project_name}}'
date: '{{date}}'
---
# Sprint Status - {{project_name}}

## Status Definitions

### Epic Status
- **backlog** — Not yet started
- **in-progress** — At least one story is in progress
- **done** — All stories completed

### Story Status
- **backlog** — Not yet started
- **ready-for-dev** — Detailed, estimated, and ready for implementation
- **in-progress** — Currently being implemented
- **review** — Implementation complete, awaiting review
- **done** — Reviewed and accepted

### Retrospective Status
- **optional** — Not yet planned
- **done** — Completed

## Development Status

```yaml
development_status:
  # Epic E-001: {{epic_title}}
  e-001:
    status: backlog
    stories:
      s-001:
        status: backlog
      s-002:
        status: backlog
    retrospective:
      status: optional

  # Epic E-002: {{epic_title}}
  e-002:
    status: backlog
    stories:
      s-003:
        status: backlog
    retrospective:
      status: optional
```

## Sprint Summary

| Metric | Value |
|--------|-------|
| Current Sprint | |
| Sprint Goal | |
| Total Points | |
| Completed Points | |
| In Progress Points | |
| Remaining Points | |

## Blockers

| Story | Blocker | Status |
|-------|---------|--------|
| | | |
