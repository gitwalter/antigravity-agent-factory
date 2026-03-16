---
description: Dashboard Data Health & Integrity Audit
dashboard: true
version: 1.0.0
tags:
- dashboard
- data
- health
- standardized
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

## Phases

### Phase 1: Schema Validation
- **Goal**: Ensure imported data adheres to required structural formats.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: schema-validator
- **Actions**:
    - Confirm presence of required columns and data types.

### Phase 2: Integrity & Anomaly Audit
- **Goal**: Identify duplicate entries, spikes, or missing values in the dataset.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: statistical-optimizer
- **Actions**:
    - Run null counts and duplicate entry checks.

### Phase 3: Historical Trend Analysis
- **Goal**: Compare current metrics against historical averages to detect drifts.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-analysis-routine
- **Tools**: trend-analyzer
- **Actions**:
    - Flag significant deviations from the 7-day average.

### Phase 4: Resolution & Re-ingestion
- **Goal**: Resolve schema drift or data quality issues and re-import data.
- **Agents**: `project-operations-specialist`
- **Skills**: dashboard-onboarding
- **Tools**: data-cleanser
- **Actions**:
    - Update guides and re-ingest cleansed data.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
