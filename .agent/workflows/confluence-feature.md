---
agents:
- system-architecture-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for confluence-feature. Standardized for IDX Visual
  Editor.
domain: universal
name: confluence-feature
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Fetch Confluence page and clarify requirements.
  agents:
  - system-architecture-specialist
  goal: Fetch documentation from Confluence and analyze features for technical gaps.
  name: Requirement Extraction & Analysis
  skills:
  - confluence-feature
  - reviewing-requirements
  tools:
  - confluence-mcp
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Initialize implementation plans.
  agents:
  - system-architecture-specialist
  goal: Create technical blueprints and implementation plans based on Confluence specs.
  name: Design & Blueprinting
  skills:
  - designing-ai-systems
  - confluence-feature
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Implement production code and verify with tests.
  agents:
  - project-operations-specialist
  goal: Implement the feature and verify correctness through testing-agents.
  name: Execution & implementation
  skills:
  - confluence-feature
  - developing-ai-agents
  tools:
  - write_to_file
  - pytest-cli
- actions:
  - '**Agents**: `knowledge-operations-specialist`'
  - '**Actions**:'
  - Update Confluence page and finalize closure.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - knowledge-operations-specialist
  goal: Update Confluence with implementation details and close the feature loop.
  name: Documentation Loop-back
  skills:
  - generating-documentation
  - confluence-feature
  tools:
  - confluence-mcp
tags: []
type: sequential
version: 2.0.0
---
# Confluence Feature

**Version:** 1.0.0

## Overview
Antigravity workflow for confluence-feature. Standardized for IDX Visual Editor.

## Trigger Conditions
- New feature documentation or specification available on Confluence.
- Need to sync project state with Confluence pages.
- User request: `/confluence-feature`.

**Trigger Examples:**
- "Implement the feature described in the Confluence page 'User Auth'."
- "Analyze the specs from the Confluence document 'Dashboard API'."

## Phases

### 1. Requirement Extraction & Analysis
- **Goal**: Fetch documentation from Confluence and analyze features for technical gaps.
- **Agents**: `system-architecture-specialist`
- **Skills**: confluence-feature, reviewing-requirements
- **Tools**: confluence-mcp, mcp_memory_search_nodes
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Fetch Confluence page and clarify requirements.

### 2. Design & Blueprinting
- **Goal**: Create technical blueprints and implementation plans based on Confluence specs.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, confluence-feature
- **Tools**: write_to_file
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Initialize implementation plans.

### 3. Execution & implementation
- **Goal**: Implement the feature and verify correctness through testing-agents.
- **Agents**: `project-operations-specialist`
- **Skills**: confluence-feature, developing-ai-agents
- **Tools**: write_to_file, pytest-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Implement production code and verify with tests.

### 4. Documentation Loop-back
- **Goal**: Update Confluence with implementation details and close the feature loop.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation, confluence-feature
- **Tools**: confluence-mcp
- **Agents**: `knowledge-operations-specialist`
- **Actions**:
- Update Confluence page and finalize closure.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
