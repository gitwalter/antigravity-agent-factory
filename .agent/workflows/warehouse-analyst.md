---
## Overview

description: Process Optimization & Industrial Engineering Workflow
---

# Industrial Analyst Optimization Guide

Deep-dive analytical routine for improving building-level performance.

**Version:** 1.0.0
**Owner:** OperationalAnalyst
**Skill Set:** `industrial-analysis`, `optimization`

## Trigger Conditions

This workflow is activated when:
- Fulfillment density exceeds 85%.
- Throughput bottlenecks are identified at the station level.

**Trigger Examples:**
- "Conduct a density analysis for the main fulfillment hall."
- "Optimize SKU placement based on pick speed correlation."

## 1. Density Analysis
- **Bin Flow**: Generate the **Bin Density Heatmap**.
- **Congestion Check**: Identify "High-Traffic" aisles where multiple picks/stows occur simultaneously.
- **Constraint**: If Density > 85%, stowing UPH usually drops due to lack of space.

## 2. Height vs. Speed Correlation
- Run **Correlation Analysis** between `Shelf_Level` (A, B, C, D) and `Stow_UPH`.
- **Insight**: Typically, levels C/D (ground/eye level) are 30% faster than A/E.
- **Optimization**: Reserve "Fast-Moving SKUs" for level B/C/D.

## 3. Predictive Labor Modeling
- Use the **Regression Analysis** tool to forecast next-week volume based on historical ASN trends.
- Suggest labor headcount adjustments to the Ops Manager based on predicted cube-out volume.

## 4. Inventory Accuracy
- Verify **ICA (Inventory Count Accuracy)** via cycle count logs vs. system state.
- Target zero variance for high-value SKUs.


## Trigger Conditions

- User request
- Manual activation


## Phases

1. Initial Analysis
2. Implementation
3. Verification


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
