---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dashboard-data-health. Standardized for IDX
  Visual Editor.
domain: universal
name: dashboard-data-health
steps:
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Confirm presence of required columns and data types.
  agents:
  - workflow-quality-specialist
  goal: Ensure imported data adheres to required structural formats.
  name: Schema Validation
  skills:
  - dashboard-data-health
  tools:
  - schema-validator
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run null counts and duplicate entry checks.
  agents:
  - workflow-quality-specialist
  goal: Identify duplicate entries, spikes, or missing values in the dataset.
  name: Integrity & Anomaly Audit
  skills:
  - dashboard-data-health
  tools:
  - statistical-optimizer
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Flag significant deviations from the 7-day average.
  agents:
  - python-ai-specialist
  goal: Compare current metrics against historical averages to detect drifts.
  name: Historical Trend Analysis
  skills:
  - dashboard-analysis-routine
  tools:
  - trend-analyzer
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Update guides and re-ingest cleansed data.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Resolve schema drift or data quality issues and re-import data.
  name: Resolution & Re-ingestion
  skills:
  - dashboard-onboarding
  tools:
  - data-cleanser
tags: []
type: sequential
version: 2.0.0
---
# Data Health Audit Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for dashboard data health audits. Standardized for IDX Visual Editor.

## Trigger Conditions
- Data ingestion completed and requires validation.
- Anomaly detection alerts triggered.
- User request: `/dashboard-data-health`.

**Trigger Examples:**
- "Check the health of the incoming data stream."
- "Audit the data integrity for the sales dashboard."

## Phases

### 1. Schema Validation
- **Goal**: Ensure imported data adheres to required structural formats.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: schema-validator
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Confirm presence of required columns and data types.

### 2. Integrity & Anomaly Audit
- **Goal**: Identify duplicate entries, spikes, or missing values in the dataset.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: statistical-optimizer
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run null counts and duplicate entry checks.

### 3. Historical Trend Analysis
- **Goal**: Compare current metrics against historical averages to detect drifts.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-analysis-routine
- **Tools**: trend-analyzer
- **Agents**: `python-ai-specialist`
- **Actions**:
- Flag significant deviations from the 7-day average.

### 4. Resolution & Re-ingestion
- **Goal**: Resolve schema drift or data quality issues and re-import data.
- **Agents**: `project-operations-specialist`
- **Skills**: dashboard-onboarding
- **Tools**: data-cleanser
- **Agents**: `project-operations-specialist`
- **Actions**:
- Update guides and re-ingest cleansed data.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
