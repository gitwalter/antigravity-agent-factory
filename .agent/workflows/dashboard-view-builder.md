---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dashboard-view-builder. Standardized for IDX
  Visual Editor.
domain: universal
name: dashboard-view-builder
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Select domain and identify primary analytical objectives.
  agents:
  - python-ai-specialist
  goal: Identify core business questions and target analytical domains.
  name: Requirement Intake
  skills:
  - dashboard-view-builder
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Choose KPI widgets (Pareto, Heatmap, Time Series).
  - Arrange widgets for optimal data density.
  agents:
  - python-ai-specialist
  goal: Select appropriate KPI widgets and optimize visual layout.
  name: Widget & Layout Design
  skills:
  - dashboard-view-builder
  tools:
  - design-center-ui
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Verify statistical significance and add metadata annotations.
  agents:
  - workflow-quality-specialist
  goal: Ensure widgets support statistical significance and data accuracy.
  name: Statistical Verification
  skills:
  - dashboard-data-health
  tools:
  - statistical-validator
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Save as Situational Blueprint and set as default.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Save and publish the situational blueprint as the default view.
  name: Finalize & Publish
  skills:
  - committing-releases
  tools:
  - dashboard-publisher
tags: []
type: sequential
version: 1.0.0
---

# Dashboard View Builder Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for building and customizing dashboard views. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a new Situational Blueprint or layout.
- Need to optimize widget arrangement for specific data insights.
- User request: `/dashboard-view-builder`.

**Trigger Examples:**
- "Build a new view for the 'Real-time Monitoring' dashboard."
- "Customize the layout to prioritize Pareto charts."

## Phases

### 1. Requirement Intake
- **Goal**: Identify core business questions and target analytical domains.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Select domain and identify primary analytical objectives.

### 2. Widget & Layout Design
- **Goal**: Select appropriate KPI widgets and optimize visual layout.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: design-center-ui
- **Agents**: `python-ai-specialist`
- **Actions**:
- Choose KPI widgets (Pareto, Heatmap, Time Series).
- Arrange widgets for optimal data density.

### 3. Statistical Verification
- **Goal**: Ensure widgets support statistical significance and data accuracy.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: statistical-validator
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Verify statistical significance and add metadata annotations.

### 4. Finalize & Publish
- **Goal**: Save and publish the situational blueprint as the default view.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: dashboard-publisher
- **Agents**: `project-operations-specialist`
- **Actions**:
- Save as Situational Blueprint and set as default.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
