---
storyId: '{{story_id}}'
workflowType: 'code-skeleton'
date: '{{date}}'
---
# Code Skeleton — {{story_title}}

<!-- derived_from: STORY#{{story_id}} -->

**Story:** {{story_id}} — {{story_title}}
**Date:** {{date}}
**Status:** Draft

<!--
This is a scaffold, not an implementation.
- Signatures only, no function bodies.
- Every function must contain TODO(<story-id>:<scenario>) markers.
- Add derived_from markers linking files to architecture components.
-->

---

## 1. Affected File Tree

```
<!-- Mark each entry NEW / MODIFIED / TOUCH -->
project-root/
├── src/
│   ├── {{module_1}}.{{ext}}           # NEW — {{one-line purpose}}
│   ├── {{module_2}}.{{ext}}           # MODIFIED — {{one-line purpose}}
│   └── ...
└── tests/
    └── {{test_module}}.{{ext}}        # NEW — {{one-line purpose}}
```

## 2. Module Signatures

### {{file_path}}

<!-- derived_from: ARCH#C-{{n}} -->

```{{lang}}
// Purpose: {{short description}}

function {{fn_name}}({{arg}}: {{type}}): {{return_type}}
  // TODO({{story_id}}:SC1): {{what this does — ties to BDD scenario}}
  throw new NotImplementedError()

class {{class_name}}:
  // Purpose: {{short description}}

  method {{method_name}}({{arg}}: {{type}}): {{return_type}}
    // TODO({{story_id}}:SC2): {{what this does}}
    throw new NotImplementedError()
```

### {{file_path_2}}

<!-- Repeat for each new/modified file -->

## 3. BDD Scenario → Signature Map

| Scenario ID | Scenario | Signature that covers it |
|-------------|----------|--------------------------|
| {{story_id}}-SC1 | {{scenario name}} | `{{file}}::{{fn}}` |
| {{story_id}}-SC2 | {{scenario name}} | `{{file}}::{{fn}}` |

## 4. Out-of-Scope Notes

<!-- Anything the developer should NOT do in this skeleton, and why -->

- 

## 5. Next Steps

- [ ] Hand off to QA (Quinn) for the test plan.
- [ ] Implement TODOs in scenario-priority order.
- [ ] Run tests after each TODO is resolved.
