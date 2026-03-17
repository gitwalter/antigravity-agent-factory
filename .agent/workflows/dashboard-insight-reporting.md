---
agents:
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for dashboard-insight-reporting. Standardized for
  IDX Visual Editor.
domain: universal
name: dashboard-insight-reporting
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Identify lead metrics and period context.
  agents:
  - python-ai-specialist
  goal: Select report timeframe and lead metrics for analysis.
  name: Context & Metric Selection
  skills:
  - dashboard-insight-reporting
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Trigger AI analysis and generate takeaways.
  agents:
  - python-ai-specialist
  goal: Use AI to synthesize trends and generate executive takeaways.
  name: AI Synthesis & Trend Analysis
  skills:
  - dashboard-insight-reporting
  tools:
  - ai-workspace-ui
- actions:
  - '**Agents**: `knowledge-operations-specialist`'
  - '**Actions**:'
  - Compile charts with captions and dates into PDF.
  agents:
  - knowledge-operations-specialist
  goal: Compile visualizations into formatted PDF reports.
  name: Visual Export & Formatting
  skills:
  - generating-documentation
  tools:
  - pdf-generator
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Post to Knowledge Bridge and archive JSON records.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Distribute report to stakeholders and archive historical state.
  name: Distribution & Archiving
  skills:
  - committing-releases
  tools:
  - knowledge-bridge-ui
tags: []
type: sequential
version: 2.0.0
---
# Insight Reporting Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for dashboard insight reporting. Standardized for IDX Visual Editor.

## Trigger Conditions
- Periodic reporting cycle reached.
- Need for AI-assisted synthesis of business trends.
- User request: `/dashboard-insight-reporting`.

**Trigger Examples:**
- "Generate an insight report for the Q1 performance."
- "Summarize the key trends from the latest dashboard data."

## Phases

### 1. Context & Metric Selection
- **Goal**: Select report timeframe and lead metrics for analysis.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-insight-reporting
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Identify lead metrics and period context.

### 2. AI Synthesis & Trend Analysis
- **Goal**: Use AI to synthesize trends and generate executive takeaways.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-insight-reporting
- **Tools**: ai-workspace-ui
- **Agents**: `python-ai-specialist`
- **Actions**:
- Trigger AI analysis and generate takeaways.

### 3. Visual Export & Formatting
- **Goal**: Compile visualizations into formatted PDF reports.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation
- **Tools**: pdf-generator
- **Agents**: `knowledge-operations-specialist`
- **Actions**:
- Compile charts with captions and dates into PDF.

### 4. Distribution & Archiving
- **Goal**: Distribute report to stakeholders and archive historical state.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: knowledge-bridge-ui
- **Agents**: `project-operations-specialist`
- **Actions**:
- Post to Knowledge Bridge and archive JSON records.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
