---
stepsCompleted: []
inputDocuments: []
workflowType: 'architecture'
project_name: '{{project_name}}'
user_name: '{{user_name}}'
date: '{{date}}'
---
# Architecture Decision Document - {{project_name}}

**Author:** {{user_name}}
**Date:** {{date}}
**Version:** 1.0
**Status:** Draft

<!--
Anchor Convention (for traceability):
- Architecture decisions: ADR-001, ADR-002, ...
- Components (in section 5.1): C-1, C-2, ... (use as section headings, e.g. "### C-1: API Gateway")
- When an ADR or component derives from PRD requirements, append a derived_from marker
  immediately after the heading, e.g.:
    ### C-1: API Gateway
    <!-- derived_from: PRD#FR-001, PRD#NFR-002 -->
- IDs once assigned MUST NOT be renumbered.
-->

---

## 1. Overview

### 1.1 Purpose

<!-- What problem does this architecture solve? -->

### 1.2 Scope

<!-- What is included and excluded from this architecture? -->

### 1.3 Context

<!-- High-level context: team, constraints, timeline -->

## 2. Architecture Drivers

### 2.1 Key Requirements

<!-- High-impact requirements that drive architecture decisions -->

| ID | Requirement | Impact Level |
|----|------------|-------------|
| | | High/Medium/Low |

### 2.2 Quality Attributes

| Attribute | Priority | Target |
|-----------|----------|--------|
| Performance | | |
| Scalability | | |
| Security | | |
| Maintainability | | |
| Reliability | | |

### 2.3 Constraints

<!-- Technical, business, regulatory constraints -->

## 3. Architecture Decisions (ADRs)

### ADR-001: Architecture Style

- **Context:** 
- **Decision:** 
- **Rationale:** 
- **Consequences:** 
- **Alternatives Considered:** 

### ADR-002: Deployment Model

- **Context:** 
- **Decision:** 
- **Rationale:** 
- **Consequences:** 
- **Alternatives Considered:** 

### ADR-003: {{Decision Title}}

- **Context:** 
- **Decision:** 
- **Rationale:** 
- **Consequences:** 
- **Alternatives Considered:** 

## 4. Technology Stack

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| Frontend | | | |
| Backend | | | |
| Database | | | |
| Authentication | | | |
| Hosting | | | |
| CI/CD | | | |

## 5. System Architecture

### 5.1 Components

<!-- List major components using stable anchor IDs (C-1, C-2, ...). -->
<!-- For each component, add a derived_from marker if it satisfies specific PRD requirements. -->

#### C-1: {{Component Name}}

<!-- derived_from: PRD#FR-001 -->

- **Responsibility:**
- **Tech:**
- **Interfaces:**

### 5.1.1 Component Diagram

<!-- Describe major components and their relationships -->

### 5.2 Data Flow

<!-- Request/response flow, event-driven patterns -->

### 5.3 Integration Points

<!-- External services, third-party APIs -->

## 6. Data Architecture

### 6.1 Entity Relationship Model

<!-- Key entities and relationships -->

### 6.2 Data Storage Strategy

<!-- Database selection, partitioning, caching -->

### 6.3 Data Flow Patterns

<!-- Read/write patterns, eventual consistency -->

## 7. API Design

### 7.1 API Style

<!-- REST, GraphQL, gRPC -->

### 7.2 Endpoint Structure

<!-- Key endpoints and their purpose -->

### 7.3 Authentication Flow

### 7.4 Error Handling

## 8. Project Structure

```
project-root/
├── ...
```

### 8.1 Module Boundaries

### 8.2 Naming Conventions

### 8.3 Configuration Management

## 9. Security Architecture

### 9.1 Authentication & Authorization

### 9.2 Data Protection

### 9.3 Security Patterns

## 10. Infrastructure & DevOps

### 10.1 Environments

| Environment | Purpose | Configuration |
|------------|---------|---------------|
| Development | | |
| Staging | | |
| Production | | |

### 10.2 Deployment Strategy

### 10.3 Monitoring & Observability

## 11. Validation

### 11.1 Requirements Coverage

<!-- Verify all FRs can be implemented -->

### 11.2 NFR Verification

<!-- Verify all NFRs are achievable -->

### 11.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | | | |
