---
version: 2.0.0
description: Standardized factory workflow.
tags:
- agent
- '1'
- bridge
- standardized
---
# Statistical Dashboard & Knowledge Bridge Synchronization

**Version:** 1.0.0

## Overview
This workflow defines the standard operating procedure for synchronizing statistical analysis results with the Factory's Knowledge Graph and reporting back to the Project Management System (Plane).

## Trigger Conditions
- **Trigger Examples:**
    - "Sync the latest analysis for AGENT-1 to memory."
    - "Update the Plane issue with the new statistical insights."

## Phases

### Phase 1: Data Ingestion & Analysis
- **Goal**: Ingest operational data and perform statistical analysis for intelligence generation.
- **Agents**: `project-operations-specialist`
- **Skills**: dashboard-onboarding, analysis-routine
- **Tools**: statistical-dashboard, python-interpreter
- **Actions**:
    - Ingest data and perform analysis in Advanced Analytics.

### Phase 2: Knowledge Serialization & Sync
- **Goal**: Serialize analysis results and synchronize with the Memory MCP knowledge graph.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: repository-maintenance, agent-1-bridge
- **Tools**: mcp_memory_add_observations, mcp_memory_create_entities
- **Actions**:
    - Sync data artifacts to Memory and verify ingestion.

### Phase 3: Plane Reporting (Bridge Implementation)
- **Goal**: Synchronize analysis results with Plane issues for product management visibility.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, agent-1-bridge
- **Tools**: scripts/pms/manager.py
- **Actions**:
    - Post analysis report to Plane issue (e.g., AGENT-1).

### Phase 4: Verification & Loop Closure
- **Goal**: Conduct final verification of knowledge integrity and Plane status synchronization.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, verifying-artifact-structures
- **Tools**: mcp_memory_search_nodes, plane-mcp
- **Actions**:
    - Verify Memory observations and Plane board reflections.

## Fallback Procedures
- Manual update of Plane issues if the bridge script fails.
- Direct JSON ingestion into Memory if the serialization step hangs.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
