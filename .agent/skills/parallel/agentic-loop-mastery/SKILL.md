---
description: Tactical Blueprint for stateful AI agents and multi-agent systems. Focuses
  on LangGraph orchestration, state persistence, and procedural loop logic.
name: agentic-loop-mastery
type: skill
---
# Capability Manifest: Agentic Loop Mastery

This blueprint provides the **procedural truth** for engineering resilient, stateful AI agents using LangGraph and LangChain 1.x.

## When to Use

This skill should be used when completing tasks related to agentic loop mastery.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Designing an Authoritative "State"
1.  **Strict Typing**: Every state field must be typed via `TypedDict` or `Pydantic`.
2.  **Reducer Awareness**: Use `Annotated` with reducers (e.g., `add_messages`) for fields that accumulate data over time.
3.  **Audit Logging**: Include an `interaction_log` list in the state to record reasoning steps that are *not* part of the message history.

### Procedure 2: The Multi-Agent Orchestration (Supervisor Pattern)
1.  **The Supervisor Node**: A central node that decides which specialist to call based on the `agent-staffing.json` mission.
2.  **Hand-off Logic**: Use `conditional_edges` to route the state to specialists. Specialists update the state and route back to the Supervisor.
3.  **Result Aggregation**: The Supervisor reviews the specialist outputs and decides if the goal is reached or if further delegation is required.

### Procedure 3: Human-in-the-Loop (HITL) Gating
1.  **Interrupt Gate**: Use `interrupt_before=["tool_execution_node"]` for high-risk tools (e.g., file deletion, payments).
2.  **Approval State**: Add an `is_approved` boolean to the state.
3.  **Resumption Logic**: The graph pauses execution; once the user provides a "go-ahead," the state is updated and the node is re-triggered.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **State Drift** | Node functions modifying state outside of the return statement. | Run an "Immutability Audit"; ensure all nodes are pure functions that return state updates; use `copy.deepcopy` if necessary. |
| **Loop Stalling** | Agent repeating the same tool call with same result. | Trigger the "Anti-Loop" gate: detect duplicate `tool_calls` in history; force a "Strategy Shift" node that requires a new plan. |
| **Persistence Sync Error** | SQLite/Postgres connection failure. | Implement a "Persistence Fallback" to in-memory `Checkpointer`; notify the system orchestrator for a "Health Restart." |

## Idiomatic Code Patterns (The Gold Standard)

### The "Supervisor" Decision Node
```python
def supervisor_node(state: AgentState):
    prompt = f"Objective: {state['objective']}. Specialists available: {get_staffing_registry()}."
    # Use .with_structured_output to force a valid 'next_agent' decision
    decision = llm.with_structured_output(SupervisionSchema).invoke(prompt)
    return {"messages": [SystemMessage(content=f"Delegating to {decision.next_agent}")], "current_specialist": decision.next_agent}
```

### The "Safe-Fail" Termination
```python
def final_verification(state: AgentState):
    if state["iteration_count"] > 10:
        return {"messages": [AIMessage(content="CRITICAL: Goal unreached within safety limit. Terminating chain.")]}
    # ... regular verification logic
```

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Visualize SOP | `app.get_graph().print_ascii()` |
| Time Travel | `app.get_state_history(thread_id)` |
| Monitor State | `LangSmith` (inspect 'checkpoint' metadata) |

## Best Practices
Before finalizing an agentic loop:
- [ ] State Schema is strictly typed and reducer-enabled.
- [ ] `max_iterations` counter is implemented in the state.
- [ ] HITL gates are active for destructive tools.
- [ ] Persistence checkpointer is configured and verified.
