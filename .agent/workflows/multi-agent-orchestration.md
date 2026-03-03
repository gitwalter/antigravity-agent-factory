---
## Overview

description: Workflow for designing, implementing, and deploying multi-agent AI systems. Covers topology selection, agent implemen...
---

# Multi Agent Orchestration

Workflow for designing, implementing, and deploying multi-agent AI systems. Covers topology selection, agent implementation, coordination patterns, and testing using LangGraph, CrewAI, or AutoGen.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** ai-agent-development, multi-agent-systems, python-multi-agent

## Trigger Conditions

This workflow is activated when:

- Multi-agent system design needed
- Agent coordination required
- Complex AI workflow needed
- Autonomous agent deployment

**Trigger Examples:**
- "Design a research agent team"
- "Create agents for code review"
- "Build a multi-agent customer service system"
- "Orchestrate agents for data analysis"

## Steps

### 0. Context Engineering (Memory MCP)
**MANDATORY**: Query the knowledge graph to understand existing agent topologies and coordination patterns before designing new systems.

```json
{ "query": "agent coordination patterns" }
```

### 1. Analyze Requirements
Determine the core goals and constraints of the multi-agent system.

### Select Topology

### Define Agent Specifications

### Implement Agents

### Implement Handoffs

### Implement Supervisor

### Unit Test Agents

### Integration Testing

### Evaluation

### Configure Production

### Deploy


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
