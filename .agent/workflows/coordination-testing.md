---
description: Multi-agent coordination testing-agents and validation workflow. Covers handoff
  verification, conflict resolution, result ag...
version: 1.0.0
tags:
- coordination
- testing-agents
- standardized
---


# Coordination Testing

Multi-agent coordination testing-agents and validation workflow. Covers handoff verification, conflict resolution, result aggregation, and end-to-end coordination quality.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** multi-agent-systems, crewai, langgraph

## Trigger Conditions

This workflow is activated when:

- Multi-agent system needs validation
- Coordination bugs suspected
- Pre-release coordination check
- New handoff logic added

**Trigger Examples:**
- "Test multi-agent coordination"
- "Validate agent handoffs"
- "Run coordination tests"
- "Check for deadlocks in agent flow"

## Phases

### Phase 1: Coordination Point Identification
- **Goal**: Map all agent handoff points and resource dependencies in the multi-agent system.
- **Agents**: `system-architecture-specialist`
- **Skills**: testing-agents, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify handoff points and shared resource locks.

### Phase 2: Scenario Design & Mocking
- **Goal**: Design positive and negative test scenarios for coordination flows.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, testing-agents
- **Tools**: write_to_file, pytest-cli
- **Actions**:
    - Design test cases for successful handoffs and conflict resolution.

### Phase 3: Execution & Deadlock Detection
- **Goal**: Run coordination tests and logging-and-monitoring for race conditions or deadlocks.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: python-interpreter, shell-execute
- **Actions**:
    - Run flow tests and verify result aggregation.

### Phase 4: Analysis & Optimization
- **Goal**: Analyze coordination quality metrics and propose flow optimizations.
- **Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, testing-agents
- **Tools**: python-interpreter
- **Actions**:
    - Generate coordination quality report and recommendations.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
