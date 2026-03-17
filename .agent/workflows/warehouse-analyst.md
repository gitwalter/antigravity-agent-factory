---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for warehouse-analyst. Standardized for IDX Visual
  Editor.
domain: universal
name: warehouse-analyst
steps:
- actions:
  - '**Bin Flow**: Generate the **Bin Density Heatmap**.'
  - '**Congestion Check**: Identify "High-Traffic" aisles where multiple picks/stows
    occur simultaneously.'
  - '**Constraint**: If Density > 85%, stowing UPH usually drops due to lack of space.'
  agents:
  - '@Architect'
  goal: ''
  name: Density Analysis
  skills: []
  tools: []
- actions:
  - Run **Correlation Analysis** between `Shelf_Level` (A, B, C, D) and `Stow_UPH`.
  - '**Insight**: Typically, levels C/D (ground/eye level) are 30% faster than A/E.'
  - '**Optimization**: Reserve "Fast-Moving SKUs" for level B/C/D.'
  agents:
  - '@Architect'
  goal: ''
  name: Height vs. Speed Correlation
  skills: []
  tools: []
- actions:
  - Use the **Regression Analysis** tool to forecast next-week volume based on historical
    ASN trends.
  - Suggest labor headcount adjustments to the Ops Manager based on predicted cube-out
    volume.
  agents:
  - '@Architect'
  goal: ''
  name: Predictive Labor Modeling
  skills: []
  tools: []
- actions:
  - Verify **ICA (Inventory Count Accuracy)** via cycle count logs vs. system state.
  - Target zero variance for high-value SKUs.
  - User request
  - Manual activation
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
  name: Inventory Accuracy
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Industrial Analyst Optimization Guide

**Version:** 1.0.0

## Overview
Antigravity workflow for warehouse data analysis, labor modeling, and operational optimization. Standardized for IDX Visual Editor.

## Trigger Conditions
- Periodic review of warehouse density and operational efficiency (UPH).
- Need to forecast labor requirements based on historical volume trends.
- User request: `/warehouse-analyst`.

**Trigger Examples:**
- "Perform a density analysis for the 'Zone A' warehouse area."
- "Execute the analyst guide to forecast labor headcount for the upcoming peak season."

## Phases

### 1. Density Analysis
- **Agents**: `@Architect`
- **Bin Flow**: Generate the **Bin Density Heatmap**.
- **Congestion Check**: Identify "High-Traffic" aisles where multiple picks/stows occur simultaneously.
- **Constraint**: If Density > 85%, stowing UPH usually drops due to lack of space.

### 2. Height vs. Speed Correlation
- **Agents**: `@Architect`
- Run **Correlation Analysis** between `Shelf_Level` (A, B, C, D) and `Stow_UPH`.
- **Insight**: Typically, levels C/D (ground/eye level) are 30% faster than A/E.
- **Optimization**: Reserve "Fast-Moving SKUs" for level B/C/D.

### 3. Predictive Labor Modeling
- **Agents**: `@Architect`
- Use the **Regression Analysis** tool to forecast next-week volume based on historical ASN trends.
- Suggest labor headcount adjustments to the Ops Manager based on predicted cube-out volume.

### 4. Inventory Accuracy
- **Agents**: `@Architect`
- Verify **ICA (Inventory Count Accuracy)** via cycle count logs vs. system state.
- Target zero variance for high-value SKUs.
- User request
- Manual activation
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
