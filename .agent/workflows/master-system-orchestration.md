---
## Overview

description: Supreme command entity for strategic decomposition and multi-agent orchestration.
---

# Master System Orchestration (MSO)

The **Master System Orchestration** (MSO) is the top-level architectural commander. It exists to transform complex, multi-dimensional user objectives into a verifiable tree of execution, ensuring that all actions align with the system's foundational axioms and technical standards.

**Version:** 2.0.0
**Owner:** MasterSystemOrchestrator (MSO)
**Authority Tier:** Tier 0 (Strategic Command)

## Trigger Conditions

This workflow is activated when:
- A fundamental, multi-phase system change is requested.
- Multiple workflows need to be coordinated (e.g., Feature Dev + Agent Dev).
- A high-level, ambiguous objective requires strategic decomposition.
- System-wide structural or functional enrichment is required.

**Trigger Examples:**
- "Enrich the entire system's workflows and agents for better execution."
- "Design and implement a new microservices layer across the stack."
- "Perform a full repository audit and remediation cycle."

## Operational Philosophy

> "Complexity is managed through recursive decomposition and specialized delegation."

The MSO does not execute tactical work; it governs the **Strategy** and ensures the **Outcome**.

## Phases

### 1. Strategic Decomposition & Goal Rooting

Analyze the user's high-level request to identify the 'Root Goal' and its primary dependencies.

1.  **Lead Specialist**: `SystemArchitectSteward` (SAS)
2.  **Procedural Logic**:
    - Deconstruct the request into **Functional**, **Structural**, and **Factual** requirements.
    - Search the Knowledge Base (`.agent/knowledge/`) for existing patterns that match the objective.
    - Identity the "Critical Path" (the sequence of actions that must succeed for the goal to be met).
3.  **Axiom Gate**:
    - **Truth**: Are the requirements unambiguous?
    - **Beauty**: Is the proposed plan minimal and coherent?
4.  **Output**: `implementation_plan.md` (Architectural Blueprint).

### 2. Tactical Staffing & Dependency Binding

Map the decomposed goals to the most qualified Specialists in the `.agent/agents` registry.

1.  **Lead Specialist**: `MSO` (Self)
2.  **Procedural Logic**:
    - Consult `agent-staffing.json` to resolve roles (e.g., Architect, Engineer, Guardian).
    - **Delegation Logic**:
        - If the task requires architectural changes: Assign `SystemArchitectSteward`.
        - If the task requires LLM app implementation: Assign `CognitiveCycleEngineer`.
        - If the task requires structural repair: Assign `IntegrityGuardian`.
    - **Gap Detection**: If no agent matches the specialty, immediately trigger the `Agent Development` SOP.
3.  **Output**: Updated Task List in `task.md`.

### 3. Synchronized Execution Flows

Coordinate the specialists through their respective workflows (SOPs).

1.  **Lead Specialist**: Role-dependent (Project Manager mode).
2.  **Orchestration Rules**:
    - **Parallelism**: Execute `CognitiveCycleEngineer` and `TestConductor` tasks concurrently where possible.
    - **Handoffs**: Use `verified-communication` for data transfer between agents.
    - **State Maintenance**: Update `task.md` after every milestone.
3.  **Verification Gate**: Each phase must pass its specific validation suite (e.g., `pytest` for code, `link_checker` for docs).

### 4. Quality Governance & Final Convergence

Aggregate the outputs and verify the total system health.

1.  **Lead Specialist**: `CodeIntegrityGuardian`
2.  **Success Criteria**:
    - 100% pass rate in relevant regression suites.
    - All new links verified via `link_checker.py --deep`.
    - `walkthrough.md` provides proof of work with evidence (screenshots/logs).
3.  **Axiom Gate**:
    - **Love**: Does the result solve the user's *actual* problem with care?
    - **Truth**: Is the implementation accurate and fully documented?

## Decision Points

- **Insufficient Tools**: If needed skills don't exist, pivot to the **Skill Enrichment** workflow.
- **Architectural Shift**: If implementation reveals design flaws, SAS must update the `implementation_plan.md`.

## Fallback Procedures

1. **Stall Detection**: If a sub-agent hits `max_iterations`, the MSO intervenes to refine the prompt or re-task.
2. **Context Overload**: If context window limits are approached, the MSO performs a **Context Distillation**.
3. **User Clarification**: Pivot to `PLANNING` mode and ask for specific guidance if the objective is blocked.

## Related Documentation

- **Registry**: `d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge\agent-staffing.json`
- **SOP**: `Standard Feature Delivery Cycle` (SFDC)
- **SOP**: `Agent Development`


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
