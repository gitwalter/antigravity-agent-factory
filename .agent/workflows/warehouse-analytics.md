---
## Overview

description: Specialized workflow for analyzing Amazon-scale fulfillment KPIs.
---

# Warehouse Analytics

This workflow guides the process of analyzing large-scale fulfillment operations to identify bottlenecks and optimize storage and outbound performance.

**Version:** 1.0.0
**Owner:** OperationalAnalyst
**Skill Set:** `warehouse-analytics`, `statistics-analysis`

## Trigger Conditions

This workflow is activated when:
- Weekly operational performance needs review.
- Significant delays in Dock-to-Stock (D2S) are reported.
- Cube-out efficiency drops below threshold.

**Trigger Examples:**
- "Analyze last week's fulfillment performance for Warehouse DXB1."
- "Identify bottlenecks in the packing and loading process."

## Steps

1.  **Project Initialization**: Create a new project in the Statistical Dashboard named "Warehouse Intelligence [Location ID]".
2.  **Data Ingestion**:
    - Download and populate the [Inbound Log Template](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/projects/statistical_dashboards/data/templates/warehouse/inbound_log.csv).
    - Download and populate the [Inventory Snapshot Template](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/projects/statistical_dashboards/data/templates/warehouse/inventory_snapshot.csv).
    - Download and populate the [Outbound Fulfillment Template](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/projects/statistical_dashboards/data/templates/warehouse/outbound_fulfillment.csv).
3.  **Upload to Dashboard**: Use the **Data Manager** tab in the Streamlit app to upload these files to your project.
4.  **Analyze Storing Performance**:
    - Navigate to **Warehousing Intel**.
    - Verify "Dock-to-Stock" (D2S) metrics.
    - Analyze bottleneck between 'Unloading' and 'Storing'.
5.  **Analyze Fulfillment (Packing & Loading)**:
    - Review the "Pick-Pack-Load" cycle times.
    - Check for "Cube-Out" efficiency (Box volume vs Item volume).
    - Monitor carrier turnaround times.
6.  **AI Insights**: Generate automated insights to identify the day's primary operational bottleneck.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
