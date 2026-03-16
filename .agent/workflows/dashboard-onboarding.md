---
description: Rapid Onboarding Workflow for new Dashboard Projects.
dashboard: true
version: 1.0.0
tags:
- dashboard
- onboarding
- standardized
---


# Dashboard Onboarding Workflow

**Version:** 1.0.0

This workflow guides the setup of a new analytical project within the Statistical Dashboard.

## Trigger Conditions
- A new analytical project is being initialized.
- A user needs to set up the dashboard for a new dataset or domain.
- Team onboarding requires a standardized project scaffold.

**Trigger Examples:**
- "Set up a new dashboard project for warehouse optimization."
- "Onboard the Q2 dataset into the statistical dashboard."

## Phases

### Phase 1: Project Creation
- **Goal**: Initialize a new analytical project with a unique identifier and domain.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-onboarding
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Navigate to the **⚙️ Project Center** and create the project scaffold.

### Phase 2: Data Ingestion
- **Goal**: Load and validate the dataset for analysis.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-data-health
- **Tools**: dashboard-importer
- **Actions**:
    - Upload dataset and verify "Data Loaded & Validated" status.

### Phase 3: Baseline Metrics
- **Goal**: Confirm basic statistical summaries and generate initial AI insights.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-analysis-routine
- **Tools**: statistical-optimizer
- **Actions**:
    - Verify counts and trigger AI insights.

### Phase 4: Customization
- **Goal**: Configure visualization types and layout elements.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: design-center-ui
- **Actions**:
    - Toggle visualization types in the **🛠️ Design Center**.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
