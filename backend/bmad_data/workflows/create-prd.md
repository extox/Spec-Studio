# Create PRD Workflow (12 Steps)

## Overview
Guide creation of a comprehensive Product Requirements Document through systematic discovery and documentation. Each step builds on previous discoveries. Never skip steps — optional steps may be bypassed only when clearly irrelevant.

## Step-by-Step Instructions

### Step 1: Init — Input Discovery
**Goal:** Discover and load all available input documents.

- Search for existing project artifacts:
  - Project briefs, brainstorming outputs, research documents
  - Any uploaded files or existing deliverables
- Classify: greenfield (new project) vs brownfield (existing system)
- Load the PRD template for structured output
- Summarize what inputs are available
- **Do NOT generate content yet**

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Discovery — Project Classification
**Goal:** Classify the project to guide the PRD structure.

- Determine project type (web app, mobile, API, platform, etc.)
- Identify domain (fintech, healthcare, e-commerce, etc.)
- Assess complexity level (simple, moderate, complex, enterprise)
- Identify key constraints (budget, timeline, technology, regulatory)
- This classification drives which optional sections are needed

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Vision — Product Vision Discovery
**Goal:** Discover the product vision through natural conversation.

- **CRITICAL: NO content generation in this step** — pure discovery
- Explore through conversation:
  - What is the product's north star?
  - What does the world look like when this succeeds?
  - What's the 1-year vision? 3-year vision?
  - What is the core differentiator?
- Capture key phrases and insights for later use
- Validate understanding with the user

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Executive Summary
**Goal:** Draft the executive summary from discovered insights.

- First content generation step — synthesize discoveries from steps 1-3
- Write a compelling 3-5 paragraph executive summary covering:
  - What the product is
  - Why it matters
  - Who it's for
  - What makes it different
- Present for user review and refinement

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Success Criteria
**Goal:** Define measurable success criteria and negotiate scope.

- Define three categories of success:
  - **User Success** — What does the user achieve? (task completion, satisfaction)
  - **Business Success** — What business outcomes? (revenue, adoption, retention)
  - **Technical Success** — What technical goals? (performance, reliability, scale)
- Scope negotiation using MoSCoW framework:
  - **MVP** — Minimum viable product (Must-Have only)
  - **Growth** — MVP + Should-Have
  - **Vision** — Full feature set
- Agree on which scope tier to target

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: User Journeys
**Goal:** Create narrative, story-based user journeys.

- For each user type/persona identified:
  - Write a narrative journey (not just steps — tell a STORY)
  - Cover: discovery, onboarding, core usage, edge cases, return usage
  - Highlight pain points and delight moments
  - Include emotional state at each stage
- These journeys drive functional requirements

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 7: Domain — Domain-Specific Requirements (Optional)
**Goal:** Capture domain-specific compliance and constraints.

- Skip if the project has no special domain requirements
- If applicable, document:
  - Regulatory compliance (GDPR, HIPAA, PCI-DSS, etc.)
  - Industry standards and certifications
  - Legal constraints
  - Domain-specific terminology and conventions
  - Integration requirements with domain systems

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 8: Innovation — Innovation Patterns (Optional)
**Goal:** Detect and explore innovation opportunities.

- Skip if the project is straightforward
- If applicable, explore:
  - AI/ML integration opportunities
  - Novel interaction patterns
  - Platform/ecosystem play
  - Data network effects
  - Emerging technology applications

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 9: Scoping — MVP Strategy & Roadmap
**Goal:** Define MVP scope, phased development, and risk assessment.

- Finalize MVP feature set based on success criteria
- Create phased development roadmap:
  - Phase 1 (MVP): Must-have features
  - Phase 2 (Growth): Should-have features
  - Phase 3 (Vision): Could-have features
- Risk assessment:
  - Technical risks
  - Market risks
  - Resource risks
  - Mitigation strategies for each

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 10: Functional Requirements — The Capability Contract
**Goal:** Define 20-50 functional requirements organized by capability area.

- This is the CORE of the PRD — the contract between product and engineering
- Organize by capability area (e.g., Authentication, User Management, Core Features)
- For each FR:
  - Unique ID (FR-XXX)
  - Description
  - Priority (Must/Should/Could/Won't)
  - Acceptance criteria (high-level)
- Ensure complete coverage of user journeys
- Cross-reference with success criteria

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 11: Non-Functional Requirements
**Goal:** Define selective NFRs for relevant categories only.

- Only include categories that matter for this project:
  - Performance (response times, throughput, concurrency)
  - Security (authentication, authorization, data protection)
  - Scalability (growth targets, infrastructure)
  - Reliability (uptime, disaster recovery)
  - Accessibility (WCAG level, assistive technology)
  - Internationalization (languages, locales, RTL)
  - Monitoring & Observability (logging, metrics, alerting)
- Skip irrelevant categories

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 12: Complete — Polish & Finalize
**Goal:** Polish the document and present completion options.

- Document optimization:
  - Check for internal consistency
  - Remove duplicate content
  - Reconcile any brainstorming notes with final content
  - Ensure all cross-references are valid
- Update document status to complete
- Present options:
  - **Validate PRD** — Run systematic validation checks
  - **Create Architecture** — Move to Winston for technical design
  - **Create UX Design** — Move to Sally for UX specification
  - **Edit PRD** — Make targeted changes
- Save final deliverable

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## A/P/C Menu Pattern

Every step offers three options:
- **[A] Advanced Elicitation** — Activate deeper critique methods:
  - Socratic questioning (challenge every assumption)
  - First-principles thinking (break down to fundamentals)
  - Pre-mortem analysis (imagine failure and work backward)
  - Red team review (adversarial critique)
- **[P] Party Mode** — Multi-agent collaborative discussion:
  - Bring in 2-3 relevant personas for diverse perspectives
  - Each persona contributes from their expertise
  - Synthesize insights from the discussion
- **[C] Continue** — Save current progress and proceed to the next step
