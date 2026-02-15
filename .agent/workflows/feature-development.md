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

### 1. Requirements Harvesting
Extract and formalize the core requirements and success criteria.
- **Lead Agent**: `RequirementsArchitect`
- **Output**: Formal requirements document (usually in `brain/`).

### 2. Architectural Design
Design the system structure, data models, and API interfaces.
- **Lead Agent**: `SystemArchitectSteward`
- **Skill**: `ai-system-design`, `api-design`
- **Output**: `implementation_plan.md`

### 3. TDD Implementation (Red Phase)
Define the tests before writing a single line of production code.
- **Lead Agent**: `TestConductor`
- **Skill**: `frontend-testing` / `spring-testing` / `agent-testing`
- **Action**: Write failing tests that represent the requirements.

### 4. Core Implementation (Green Phase)
Implement the minimal code required to make the tests pass.
- **Lead Agent**: `CognitiveCycleEngineer`
- **Skill**: Relevant feature-specific skill (e.g., `nextjs-development`, `fastapi-development`)
- **Action**: Iterative coding until all tests are green.

### 5. Integrity & Quality Gate
Perform code review, security audit, and documentation generation.
- **Lead Agent**: `CodeIntegrityGuardian`
- **Skill**: `clean-code-review`, `ai-security`
- **Action**: Verify adherence to SOLID principles and Axiom Zero.

### 6. Documentation & Closure
Generate README updates, changelogs, and the final walkthrough.
- **Lead Agent**: `DocumentationSteward`
- **Skill**: `documentation-generation`
- **Output**: `walkthrough.md`

## Decision Points

- **Architectural Shift**: If implementation reveals design flaws, pivot back to Phase 2.
- **Test Failure**: Stay in Phase 4 until all tests pass; do not proceed to review without green tests.

## Fallback Procedures

1. **Backlog Refinement**: If requirements are too ambiguous, trigger the `backlog-refinement` workflow.
2. **Manual Intervention**: If automated review fails three times, notify the user for strategic guidance.


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
