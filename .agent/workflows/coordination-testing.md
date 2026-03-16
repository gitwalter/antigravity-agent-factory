---
agents:
- system-architecture-specialist
- workflow-quality-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for coordination-testing. Standardized for IDX Visual
  Editor.
domain: universal
name: coordination-testing
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Identify handoff points and shared resource locks.
  agents:
  - system-architecture-specialist
  goal: Map all agent handoff points and resource dependencies in the multi-agent
    system.
  name: Coordination Point Identification
  skills:
  - testing-agents
  - designing-ai-systems
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Design test cases for successful handoffs and conflict resolution.
  agents:
  - workflow-quality-specialist
  goal: Design positive and negative test scenarios for coordination flows.
  name: Scenario Design & Mocking
  skills:
  - testing-agents
  - testing-agents
  tools:
  - write_to_file
  - pytest-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run flow tests and verify result aggregation.
  agents:
  - workflow-quality-specialist
  goal: Run coordination tests and logging-and-monitoring for race conditions or deadlocks.
  name: Execution & Deadlock Detection
  skills:
  - testing-agents
  tools:
  - python-interpreter
  - shell-execute
- actions:
  - '**Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Generate coordination quality report and recommendations.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - system-architecture-specialist
  - knowledge-operations-specialist
  goal: Analyze coordination quality metrics and propose flow optimizations.
  name: Analysis & Optimization
  skills:
  - generating-documentation
  - testing-agents
  tools:
  - python-interpreter
tags: []
type: sequential
version: 1.0.0
---

# Coordination Testing

**Version:** 1.0.0

## Overview
Antigravity workflow for coordination-testing in multi-agent systems. Standardized for IDX Visual Editor.

## Trigger Conditions
- New multi-agent collaboration patterns implemented.
- Detection of race conditions, deadlocks, or handoff failures in the system.
- User request: `/coordination-testing`.

**Trigger Examples:**
- "Test the coordination between @Architect and @Bug-Hunter."
- "Validate the handoff points in the release workflow."

## Phases

### 1. Coordination Point Identification
- **Goal**: Map all agent handoff points and resource dependencies in the multi-agent system.
- **Agents**: `system-architecture-specialist`
- **Skills**: testing-agents, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Identify handoff points and shared resource locks.

### 2. Scenario Design & Mocking
- **Goal**: Design positive and negative test scenarios for coordination flows.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, testing-agents
- **Tools**: write_to_file, pytest-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Design test cases for successful handoffs and conflict resolution.

### 3. Execution & Deadlock Detection
- **Goal**: Run coordination tests and logging-and-monitoring for race conditions or deadlocks.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: python-interpreter, shell-execute
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run flow tests and verify result aggregation.

### 4. Analysis & Optimization
- **Goal**: Analyze coordination quality metrics and propose flow optimizations.
- **Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, testing-agents
- **Tools**: python-interpreter
- **Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Generate coordination quality report and recommendations.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
