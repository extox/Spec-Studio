---
stepsCompleted: []
inputDocuments: []
workflowType: 'ux-design'
project_name: '{{project_name}}'
user_name: '{{user_name}}'
date: '{{date}}'
---
# UX Specification - {{project_name}}

**Author:** {{user_name}}
**Date:** {{date}}
**Version:** 1.0
**Status:** Draft

<!--
Anchor Convention (for traceability):
- User flows: UF-001, UF-002, ... (use as flow section headings)
- UI components: CMP-001, CMP-002, ...
- When a flow or component derives from PRD user journeys or requirements, add a marker:
    ### UF-001: Onboarding
    <!-- derived_from: PRD#UJ-001, PRD#FR-002 -->
-->

---

## 1. User Research

### 1.1 User Personas

#### Persona 1: {{persona_name}}

| Attribute | Details |
|-----------|---------|
| Role | |
| Age Range | |
| Tech Proficiency | |
| Goals | |
| Frustrations | |
| Context of Use | |

### 1.2 Mental Models

<!-- How do users think about this problem space? -->

## 2. Information Architecture

### 2.1 Sitemap

<!-- Hierarchical content structure -->

### 2.2 Navigation Structure

<!-- Primary, secondary, and utility navigation -->

## 3. User Flows

### UF-001: {{Flow Name}}

<!-- derived_from: PRD#UJ-001 -->
<!-- Entry → Key Actions → Completion -->
<!-- Include decision points and error paths -->

## 4. Wireframes

### 4.1 {{Screen Name}}

**Purpose:** 
**Context:** When does the user see this?

**Layout:**
<!-- Describe the layout structure -->

**Content Hierarchy:**
1. Primary: 
2. Secondary: 
3. Actions: 

## 5. Interaction Patterns

### 5.1 Form Interactions

### 5.2 Navigation Transitions

### 5.3 Data Loading Patterns

### 5.4 Micro-interactions

## 6. Component Specifications

### CMP-001: {{Component Name}}

<!-- derived_from: UX#UF-001 -->

**Purpose:** 
**States:** Default, Hover, Active, Disabled, Loading, Error
**Variants:** 
**Responsive:** 

## 7. Responsive Strategy

| Breakpoint | Width | Adaptation |
|-----------|-------|------------|
| Mobile | < 768px | |
| Tablet | 768-1024px | |
| Desktop | > 1024px | |

## 8. Accessibility

### 8.1 Target Level: WCAG 2.1 AA

### 8.2 Key Requirements

- Color contrast: 
- Keyboard navigation: 
- Screen reader: 
- Focus management: 

## 9. Error Handling UX

### 9.1 Validation Errors

### 9.2 System Errors

### 9.3 Network Errors

## 10. Empty & Loading States

### 10.1 First-Time Experience

### 10.2 Empty Data States

### 10.3 Loading Patterns

## 11. Content Strategy

### 11.1 Voice & Tone

### 11.2 Microcopy Guidelines

### 11.3 Terminology

| Term | Usage |
|------|-------|
| | |

## 12. Handoff Notes

<!-- Notes for architecture and development teams -->
