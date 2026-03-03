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

### 1. Requirements Harvesting & Issue Instantiation
Extract and formalize the core requirements and success criteria. All feature work MUST be tracked in Plane.
- **Lead Agent**: `RequirementsArchitect`
- **Skill**: `managing-plane-tasks`
- **Action**: Ensure a Plane issue exists detailing the requirements and acceptance criteria. If one does not exist, use `.agent/skills/routing/managing-plane-tasks/scripts/create_task.py` to create it immediately. Record the Issue ID in your context.
- **Output**: Formal Plane issue and local requirements document (usually in `brain/`).

### 2. Architectural Design & Plan Deployment
Design the system structure, data models, and API interfaces.
- **Lead Agent**: `SystemArchitectSteward`
- **Skill**: `designing-ai-systems`, `designing-apis`
- **Output**: `implementation_plan.md` in the active factory iteration folder.
- **Mandatory PMS Sync**: Immediately after generating the `implementation_plan.md`, the AI Agent MUST post this full plan as a comment (or issue update) to the active Plane issue. Plane acts as the primary AI planning tool and provides maximum transparency to human managers.

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
- **Action**: Extract architectural decisions or new methodologies into a localized `solution.json` payload. Run `.agent/skills/routing/managing-plane-tasks/scripts/post_solution.py` to securely store these insights in the Plane issue and mark it as 'Done'. This acts as the Tier 4 Memory Proposal, awaiting User Approval to become Permanent Semantic Memory.

## Mandatory: Continuous PMS Documentation
Workflows are **PMS-driven**. Throughout all phases (1-7):
- Agents MUST document their ongoing solution steps, test results, and architectural choices directly into the Plane issue.
- Do not wait until Phase 7 to update Plane. Use `mcp_plane_create_work_item_comment` or equivalent tools to log audit trails incrementally as major milestones are hit during Design, Implementation, and Quality Gates.

## Decision Points

- **Architectural Shift**: If implementation reveals design flaws, pivot back to Phase 2.
- **Test Failure**: Stay in Phase 4 until all tests pass; do not proceed to review without green tests.

## Fallback Procedures

1. **Backlog Refinement**: If requirements are too ambiguous, trigger the `backlog-refinement` workflow.
2. **Manual Intervention**: If automated review fails three times, notify the user for strategic guidance.


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
