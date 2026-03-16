---
agents:
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dashboard-onboarding. Standardized for IDX Visual
  Editor.
domain: universal
name: dashboard-onboarding
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - "Navigate to the **\u2699\uFE0F Project Center** and create the project scaffold."
  agents:
  - python-ai-specialist
  goal: Initialize a new analytical project with a unique identifier and domain.
  name: Project Creation
  skills:
  - dashboard-onboarding
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Upload dataset and verify "Data Loaded & Validated" status.
  agents:
  - python-ai-specialist
  goal: Load and validate the dataset for analysis.
  name: Data Ingestion
  skills:
  - dashboard-data-health
  tools:
  - dashboard-importer
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Verify counts and trigger AI insights.
  agents:
  - python-ai-specialist
  goal: Confirm basic statistical summaries and generate initial AI insights.
  name: Baseline Metrics
  skills:
  - dashboard-analysis-routine
  tools:
  - statistical-optimizer
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - "Toggle visualization types in the **\U0001F6E0\uFE0F Design Center**."
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - python-ai-specialist
  goal: Configure visualization types and layout elements.
  name: Customization
  skills:
  - dashboard-view-builder
  tools:
  - design-center-ui
tags: []
type: sequential
version: 1.0.0
---

# Dashboard Onboarding Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for dashboard-onboarding. Standardized for IDX Visual Editor.

## Trigger Conditions
- New analytical project initiated.
- Dataset ready for initial ingestion and analysis.
- User request: `/dashboard-onboarding`.

**Trigger Examples:**
- "Onboard the new 'Sales 2024' dataset."
- "Initialize a dashboard for the 'Marketing Optimization' project."

## Phases

### 1. Project Creation
- **Goal**: Initialize a new analytical project with a unique identifier and domain.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-onboarding
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Navigate to the **⚙️ Project Center** and create the project scaffold.

### 2. Data Ingestion
- **Goal**: Load and validate the dataset for analysis.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-data-health
- **Tools**: dashboard-importer
- **Agents**: `python-ai-specialist`
- **Actions**:
- Upload dataset and verify "Data Loaded & Validated" status.

### 3. Baseline Metrics
- **Goal**: Confirm basic statistical summaries and generate initial AI insights.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-analysis-routine
- **Tools**: statistical-optimizer
- **Agents**: `python-ai-specialist`
- **Actions**:
- Verify counts and trigger AI insights.

### 4. Customization
- **Goal**: Configure visualization types and layout elements.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: design-center-ui
- **Agents**: `python-ai-specialist`
- **Actions**:
- Toggle visualization types in the **🛠️ Design Center**.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
