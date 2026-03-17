---
agents:
- workflow-quality-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for agent-1-bridge. Standardized for IDX Visual
  Editor.
domain: universal
name: agent-1-bridge
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Ingest data and perform analysis in Advanced Analytics.
  agents:
  - project-operations-specialist
  goal: Ingest operational data and perform statistical analysis for intelligence
    generation.
  name: Data Ingestion & Analysis
  skills:
  - dashboard-onboarding
  - analysis-routine
  tools:
  - statistical-dashboard
  - python-interpreter
- actions:
  - '**Agents**: `knowledge-operations-specialist`'
  - '**Actions**:'
  - Sync data artifacts to Memory and verify ingestion.
  agents:
  - knowledge-operations-specialist
  goal: Serialize analysis results and synchronize with the Memory MCP knowledge graph.
  name: Knowledge Serialization & Sync
  skills:
  - repository-maintenance
  - agent-1-bridge
  tools:
  - mcp_memory_add_observations
  - mcp_memory_create_entities
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Post analysis report to Plane issue (e.g., AGENT-1).
  agents:
  - project-operations-specialist
  goal: Synchronize analysis results with Plane issues for product management visibility.
  name: Plane Reporting (Bridge Implementation)
  skills:
  - managing-plane-tasks
  - agent-1-bridge
  tools:
  - scripts/pms/manager.py
- actions:
  - '**Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Verify Memory observations and Plane board reflections.
  - Manual update of Plane issues if the bridge script fails.
  - Direct JSON ingestion into Memory if the serialization step hangs.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - knowledge-operations-specialist
  goal: Conduct final verification of knowledge integrity and Plane status synchronization.
  name: Verification & Loop Closure
  skills:
  - generating-documentation
  - verifying-artifact-structures
  tools:
  - mcp_memory_search_nodes
  - plane-mcp
tags: []
type: sequential
version: 2.0.0
---
# Statistical Dashboard & Knowledge Bridge Synchronization

**Version:** 1.1.0

## Overview
This workflow governs the synchronization between statistical dashboards and the Memory MCP knowledge graph, ensuring that operational data is translated into verifiable intelligence and reported to Plane.

## Trigger Conditions
- New statistical analysis report generated.
- Request to synchronize dashboard data with Plane.

**Trigger Examples:**
- "Sync the latest analysis results to Plane."
- "Serialize the dashboard data for Memory ingestion."

## Phases

### 1. Data Ingestion & Analysis
- **Goal**: Ingest operational data and perform statistical analysis for intelligence generation.
- **Agents**: `project-operations-specialist`
- **Skills**: dashboard-onboarding, analysis-routine
- **Tools**: statistical-dashboard, python-interpreter
- **Actions**:
- Ingest data and perform analysis in Advanced Analytics.

### 2. Knowledge Serialization & Sync
- **Goal**: Serialize analysis results and synchronize with the Memory MCP knowledge graph.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: repository-maintenance, agent-1-bridge
- **Tools**: mcp_memory_add_observations, mcp_memory_create_entities
- **Actions**:
- Sync data artifacts to Memory and verify ingestion.

### 3. Plane Reporting (Bridge Implementation)
- **Goal**: Synchronize analysis results with Plane issues for product management visibility.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, agent-1-bridge
- **Tools**: scripts/pms/manager.py
- **Actions**:
- Post analysis report to Plane issue (e.g., AGENT-1).

### 4. Verification & Loop Closure
- **Goal**: Conduct final verification of knowledge integrity and Plane status synchronization.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, verifying-artifact-structures
- **Tools**: mcp_memory_search_nodes, plane-mcp
- **Actions**:
- Verify Memory observations and Plane board reflections.
- Manual update of Plane issues if the bridge script fails.
- Direct JSON ingestion into Memory if the serialization step hangs.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
