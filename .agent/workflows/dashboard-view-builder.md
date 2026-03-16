---
description: Custom Dashboard View Builder Workflow
dashboard: true
version: 1.0.0
tags:
- dashboard
- view
- builder
- standardized
---


# Dashboard View Builder Workflow

**Version:** 1.0.0

Standardized process for creating and optimizing dashboard views.

## Trigger Conditions
- A user needs a custom dashboard view for a specific domain.
- An existing view requires optimization or redesign.
- New widget types or KPIs need visual integration.

**Trigger Examples:**
- "Build a custom view for downtime root-cause analysis."
- "Optimize the warehouse operations dashboard layout."

## Phases

### Phase 1: Requirement Intake
- **Goal**: Identify core business questions and target analytical domains.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Select domain and identify primary analytical objectives.

### Phase 2: Widget & Layout Design
- **Goal**: Select appropriate KPI widgets and optimize visual layout.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-view-builder
- **Tools**: design-center-ui
- **Actions**:
    - Choose KPI widgets (Pareto, Heatmap, Time Series).
    - Arrange widgets for optimal data density.

### Phase 3: Statistical Verification
- **Goal**: Ensure widgets support statistical significance and data accuracy.
- **Agents**: `workflow-quality-specialist`
- **Skills**: dashboard-data-health
- **Tools**: statistical-validator
- **Actions**:
    - Verify statistical significance and add metadata annotations.

### Phase 4: Finalize & Publish
- **Goal**: Save and publish the situational blueprint as the default view.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: dashboard-publisher
- **Actions**:
    - Save as Situational Blueprint and set as default.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
