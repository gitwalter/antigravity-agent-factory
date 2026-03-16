---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for dashboard-analysis-routine. Standardized for
  IDX Visual Editor.
domain: universal
name: dashboard-analysis-routine
steps:
- actions:
  - Check for NULLs or outliers in the **Explorer** view.
  - Verify data types (ensure dates are parsed correctly).
  agents:
  - '@Architect'
  goal: ''
  name: Data Cleaning & Inspection
  skills: []
  tools: []
- actions:
  - "Based on the **\U0001F4DA KPI Dictionary**, identify which metric you are optimizing\
    \ (e.g., UPH or Accuracy)."
  agents:
  - '@Architect'
  goal: ''
  name: Hypothesis Definition
  skills: []
  tools: []
- actions:
  - Generate a **Heatmap** to identify spatial or categorical clusters.
  - Run a **Regression** to find correlations between independent variables (e.g.,
    Temperature vs. Process Time).
  agents:
  - '@Architect'
  goal: ''
  name: Visual Discovery
  skills: []
  tools: []
- actions:
  - "Use the **\U0001F52C Statistical Primer** to choose the right test (t-test, Z-score)."
  - Confirm if the findings are statistically significant.
  agents:
  - '@Architect'
  goal: ''
  name: Significance Testing
  skills: []
  tools: []
- actions:
  - "Use the **\U0001F916 AI Workspace** to generate a final executive summary."
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: AI Commentary
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Statistical Analysis Routine

**Version:** 1.0.0

## Overview
Antigravity workflow for statistical analysis routines. Standardized for IDX Visual Editor.

## Trigger Conditions
- Need for statistical validation of experimental data.
- Periodic data analysis for performance optimization.
- User request: `/dashboard-analysis-routine`.

**Trigger Examples:**
- "Analyze the performance data for the last week."
- "Run a significance test on the A/B experiment results."

## Phases

### 1. Data Cleaning & Inspection
- **Agents**: `@Architect`
- Check for NULLs or outliers in the **Explorer** view.
- Verify data types (ensure dates are parsed correctly).

### 2. Hypothesis Definition
- **Agents**: `@Architect`
- Based on the **📚 KPI Dictionary**, identify which metric you are optimizing (e.g., UPH or Accuracy).

### 3. Visual Discovery
- **Agents**: `@Architect`
- Generate a **Heatmap** to identify spatial or categorical clusters.
- Run a **Regression** to find correlations between independent variables (e.g., Temperature vs. Process Time).

### 4. Significance Testing
- **Agents**: `@Architect`
- Use the **🔬 Statistical Primer** to choose the right test (t-test, Z-score).
- Confirm if the findings are statistically significant.

### 5. AI Commentary
- **Agents**: `@Architect`
- Use the **🤖 AI Workspace** to generate a final executive summary.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
