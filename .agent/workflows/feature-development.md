---
## Overview

description: Comprehensive workflow for developing new features from specifications through to completion.
---

# Standard Feature Delivery Cycle (SFDC)

The **Standard Feature Delivery Cycle** (SFDC) is the primary engine for turning requirements into production-ready code. It orchestrates a multi-agent team to ensure technical excellence, alignment with user needs, and long-term maintainability.

**Version:** 1.2.0
**Owner:** CognitiveCycleEngineer (CCE)
**Team Agents**: `SystemArchitectSteward`, `CodeIntegrityGuardian`, `TestConductor`

## Trigger Conditions

This workflow is activated when:
- A new feature specification is provided.
- A GitHub issue or ticket is assigned for implementation.
- User requests "implement feature", "develop functionality", or "new module".

**Trigger Examples:**
- "Implement the user authentication feature from CONF-123"
- "Develop the payment processing module"
- "Build the dashboard feature according to the new spec"

## Phases

### 0. Context Engineering (Memory-First)
Before writing any requirements, query the factory's memory to establish the structural topography and check for existing schemas.
- **Lead Agent**: `RequirementsArchitect`
- **Skill**: `managing-memory-bank`
- **Action**: Execute `mcp_memory_search_nodes` (Tier 0) to check for relevant patterns or past architectural decisions.
- **Fallback (MANDATORY)**: If the Tier 0 query returns zero results or outdated info, you MUST immediately pause the SFDC workflow and execute the "Zero-Context Fallback" (Ask the user, verify truth, delete old nodes, propose new Tier 4 memory). Never proceed without building verified truth coordinates.

### 1. Requirements Harvesting
Extract and formalize the core requirements and success criteria.
- **Lead Agent**: `RequirementsArchitect`
- **Output**: Formal requirements document (usually in `brain/`).

### 2. Architectural Design
Design the system structure, data models, and API interfaces.
- **Lead Agent**: `SystemArchitectSteward`
- **Skill**: `designing-ai-systems`, `designing-apis`
- **Output**: `implementation_plan.md`

### 3. TDD Implementation (Red Phase)
Define the tests before writing a single line of production code.
- **Lead Agent**: `TestConductor`
- **Skill**: `testing-frontend` / `testing-spring-apps` / `agent-testing`
- **Action**: Write failing tests that represent the requirements.

### 4. Core Implementation (Green Phase)
Implement the minimal code required to make the tests pass.
- **Lead Agent**: `CognitiveCycleEngineer`
- **Skill**: Relevant feature-specific skill (e.g., `developing-nextjs`, `developing-fastapi`)
- **Action**: Iterative coding until all tests are green.

### 5. Integrity & Quality Gate
Perform code review, security audit, and documentation generation.
- **Lead Agent**: `CodeIntegrityGuardian`
- **Skill**: `clean-code-review`, `securing-ai-systems`
- **Action**: Verify adherence to SOLID principles and Axiom Zero.

### 6. Documentation
Generate README updates, changelogs, and the final walkthrough.
- **Lead Agent**: `DocumentationSteward`
- **Skill**: `documentation-generation`
- **Output**: `walkthrough.md`

### 7. Memory Induction & Closure
Analyze the session for significant, reusable patterns and propose them for permanent storage.
- **Lead Agent**: `CognitiveCycleEngineer`
- **Skill**: `managing-plane-tasks`, `managing-memory-bank`
- **Action**: Extract architectural decisions or new methodologies. Store them as an `architectural_decisions` array on the Plane task closure. This acts as the Tier 4 Memory Proposal, awaiting User Approval to become Permanent Semantic Memory.

## Decision Points

- **Architectural Shift**: If implementation reveals design flaws, pivot back to Phase 2.
- **Test Failure**: Stay in Phase 4 until all tests pass; do not proceed to review without green tests.

## Fallback Procedures

1. **Backlog Refinement**: If requirements are too ambiguous, trigger the `backlog-refinement` workflow.
2. **Manual Intervention**: If automated review fails three times, notify the user for strategic guidance.


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
