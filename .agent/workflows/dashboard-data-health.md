---
description: Dashboard Data Health & Integrity Audit
dashboard: true
version: 1.0.0
---

# Data Health Audit Workflow

**Version:** 1.0.0

Routine for ensuring data integrity and schema compliance for the Statistical Dashboard.

## Trigger Conditions
- A new dataset is imported or refreshed.
- A scheduled data quality check is triggered.
- Anomalies or missing values are reported in dashboard metrics.

**Trigger Examples:**
- "Run a data health check on the latest import."
- "Audit the dashboard data for integrity issues."

## Steps

### 1. Schema Validation
- Use the **📦 Data Manager** to run a schema check.
- Confirm all required columns (e.g., `Timestamp`, `Metric_Value`) are present.

### 2. Integrity Check
- Identify duplicate entries or suspicious spikes.
- Run a "Null Count" to find data gaps.

### 3. Historical Consistency
- Compare current row count against the 7-day average.
- Flag significant deviations (±20%).

### 4. Resolution
- Update the **Data Import Guide** if schema drift is detected.
- Re-ingest cleansed data if necessary.


## Trigger Examples
- "Execute this workflow."
