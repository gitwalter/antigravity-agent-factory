---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for eda. Standardized for IDX Visual Editor.
domain: universal
name: eda
steps:
- actions:
  - Navigate to the **Data Manager** tab in the dashboard.
  - Select or create a project.
  - Upload your CSV/Excel file.
  - Click "Process & Save".
  agents:
  - '@Architect'
  goal: ''
  name: Upload Dataset
  skills: []
  tools: []
- actions:
  - Go to the **Dashboard** tab.
  - Select your project and dataset.
  - Inspect the column types and first 10 rows.
  - Check the Metrics (Total Rows, Columns).
  agents:
  - '@Architect'
  goal: ''
  name: Structural Inspection
  skills: []
  tools: []
- actions:
  - Use the **VizManager** tools to generate plots.
  - Identify correlations or outliers.
  agents:
  - '@Architect'
  goal: ''
  name: Visual Exploration
  skills: []
  tools: []
- actions:
  - provide a markdown summary of the data insights found.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: Summarization
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Exploratory Data Analysis (EDA)

**Version:** 1.0.0

## Overview
Antigravity workflow for exploratory data analysis. Standardized for IDX Visual Editor.

## Trigger Conditions
- New dataset uploaded and requiring initial analysis.
- Need to identify patterns, correlations, or outliers in data.
- User request: `/eda`.

**Trigger Examples:**
- "Run an EDA on the newly uploaded sales data."
- "Explore the correlations in the customer behavior dataset."

## Phases

### 1. Upload Dataset
- **Agents**: `@Architect`
- Navigate to the **Data Manager** tab in the dashboard.
- Select or create a project.
- Upload your CSV/Excel file.
- Click "Process & Save".

### 2. Structural Inspection
- **Agents**: `@Architect`
- Go to the **Dashboard** tab.
- Select your project and dataset.
- Inspect the column types and first 10 rows.
- Check the Metrics (Total Rows, Columns).

### 3. Visual Exploration
- **Agents**: `@Architect`
- Use the **VizManager** tools to generate plots.
- Identify correlations or outliers.

### 4. Summarization
- **Agents**: `@Architect`
- provide a markdown summary of the data insights found.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
