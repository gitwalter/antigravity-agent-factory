---
name: dispatching-parallel-agents
description: "Use when facing 2+ independent tasks or failures that can be worked on without shared state or sequential dependencies."
type: skill
version: 1.0.0
category: execution
agents:
- master-system-orchestrator
- project-operations-specialist
- workflow-quality-specialist
---

# Dispatching Parallel Agents

## When to Use
- 3+ independent test file failures.
- Multiple broken subsystems (e.g., RAG vs. UI vs. API).
- No shared state or data dependencies between the tasks.

## Prerequisites
- Multiple independent failures identified.
- Context is clear for each failure.

## Process
The process involves identifying independent failures and dispatching specialists to handle them in parallel.

### The Pattern
1.  **Segment**: Group failures by problem domain (e.g., "RAG Pathing", "Plane Auth").
2.  **Tasking**: Create focused, self-contained prompts for each domain.
3.  **Dispatch**: Run agents concurrently using the `run` or `Task` primitive.
4.  **Integrate**:
    - Review summaries from all agents.
    - Check for file conflicts (unlikely if segmented properly).
    - Run the FULL test suite to confirm collective success.

## Best Practices
Adhere to these best practices to avoid race conditions and context pollution.

### Red Flags
- Dependencies between failures: Fix one, might fix the other? **Don't parallelize.**
- Exploratory debugging: Don't know what's broken yet? **Investigate first.**
- Shared state: Editing the same files? **Sequential only.**
