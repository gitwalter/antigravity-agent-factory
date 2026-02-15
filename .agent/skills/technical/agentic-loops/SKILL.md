---
description: Procedural implementation of ReAct, Reflection, Planning, and Iterative
  Refinement patterns.
name: agentic-loops
owner: CognitiveCycleEngineer
tier: Tactical Capability
type: skill
---

# Agentic Loops (Tactical Blueprint)

The **Agentic Loops** skill provides the procedural 'how-to' for implementing autonomous reasoning cycles. It is designed for use by **Operational Intelligence** agents to navigate complex, non-linear tactical objectives with high reliability.

## When to Use

This skill should be used when completing tasks related to agentic loops.

## Process

Follow these procedures to implement the capability:

### 1. The ReAct Core (Reason → Act → Observe)
The foundational pattern for any autonomous agent.

- **Reasoning Phase**: The agent must state its current understanding, its intent, and the reasoning behind its tool choice.
- **Action Phase**: Precise execution of a single tool call.
- **Observation Phase**: Objective recording of the tool's output without immediate interpretation.
- **Loop Termination**: The cycle ends only when the goal is met or a `max_iterations` fail-safe is triggered.

### 2. Multi-Dimensional Thinking (Sequential Thinking)
For complex problem solving, integrate the `sequential-thinking` MCP tool directly into the loop.

```python
# Sequential Thinking Integration Pattern
async def complex_problem_solver(objective: str):
    thinking_process = await call_tool("sequential-thinking", {
        "thought": f"Decomposing the objective: {objective}",
        "thoughtNumber": 1,
        "totalThoughts": 5,
        "nextThoughtNeeded": True
    })
    # Use output to drive the next ReAct iteration
```

### 3. Reflective Quality Gates
Implement a secondary reflection pass to evaluate and correct the agent's own output.

- **Reflection Prompting**: "Evaluate your last 3 actions against the Root Goal. Did you advance the strategy or are you stalling? If stalling, propose a radical change in approach."
- **Self-Correction Logic**: Inhibit tool execution if the reflection score is below a predefined threshold (e.g., 0.8 consistency).

## Process

| Objective | Preferred Sequence |
| :--- | :--- |
| **Code Refactoring** | `view_file` → `codebase_search` → `sequential-thinking` → `replace_file_content` → `pytest` |
| **Structural Audit** | `list_dir` → `find_by_name` → `grep_search` → `link_checker` |
| **New Feature Dev** | `read_url_content` (Specs) → `implementation_plan` (Doc) → `task_boundary` → `write_to_file` |

## Best Practices

1.  **Strict State Management**: Always update `task.md` or a state registry between major loop transitions to prevent context fragmentation.
2.  **Explicit Tool Intent**: The agent *must* declare its intent *before* calling a tool (e.g., "I will now list the directory to verify the path exists").
3.  **Fail-State Awareness**: Explicitly handle common errors (e.g., `FileNotFoundError`, `API Timeout`) with retry-backoff or human-in-the-loop (HITL) triggers.

## Anti-Patterns

- **Hallucinated Tool Args**: Calling tools with parameters that don't exist in the definition.
- **Reaching 'Max Iterations' without Observation**: Continuously reasoning without taking actions or observing results.
- **Ambiguous Reasoning**: Providing generic "I will do X" without explaining *why* X is the correct next step.

## Related Entities

- **Specialist**: `CognitiveCycleEngineer` (Primary User)
- **Knowledge**: `agentic-loop-patterns.json`
- **Workflow**: `Standard Feature Delivery Cycle` (SFDC)


## Prerequisites

- Access to relevant project documentation
- Environmental awareness of the target stack


## Best Practices

- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Document complex logic for future maintenance
