---
## Overview

description: Rapid Exploratory Data Analysis (EDA) of local or uploaded datasets.
---

# Exploratory Data Analysis (EDA)

This workflow guides the process of exploring a dataset, identifying patterns, and generating initial insights using the Antigravity Stats Dashboard.

**Version:** 1.0.0
**Owner:** DataScientist
**Skill Set:** `eda`, `data-visualization`

## Trigger Conditions

This workflow is activated when:
- A new dataset is uploaded for initial exploration.
- Correlation analysis is required for hypothesis generation.
- Data quality needs a visual check.

**Trigger Examples:**
- "Run an EDA on the newly uploaded sales data."
- "Explore the correlations in the customer churn dataset."

// turbo-all

## Phases

### 1. Upload Dataset
- Navigate to the **Data Manager** tab in the dashboard.
- Select or create a project.
- Upload your CSV/Excel file.
- Click "Process & Save".

### 2. Structural Inspection
- Go to the **Dashboard** tab.
- Select your project and dataset.
- Inspect the column types and first 10 rows.
- Check the Metrics (Total Rows, Columns).

### 3. Visual Exploration
- Use the **VizManager** tools to generate plots.
- Identify correlations or outliers.

### 4. Summarization
- provide a markdown summary of the data insights found.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
