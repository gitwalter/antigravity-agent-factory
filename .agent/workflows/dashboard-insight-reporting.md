---
description: Automated Insight Reporting Workflow
dashboard: true
version: 1.0.0
tags:
- dashboard
- insight
- reporting
- standardized
---


# Insight Reporting Workflow

**Version:** 1.0.0

Standardized process for generating and distributing analytical reports.

## Trigger Conditions
- A periodic report cycle is due (weekly, monthly).
- A stakeholder requests an ad-hoc analytical summary.
- A significant trend or anomaly is detected that needs documentation.

**Trigger Examples:**
- "Generate a weekly insight report for the dashboard."
- "Create an executive summary of the last 30 days."

## Phases

### Phase 1: Context & Metric Selection
- **Goal**: Select report timeframe and lead metrics for analysis.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-insight-reporting
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify lead metrics and period context.

### Phase 2: AI Synthesis & Trend Analysis
- **Goal**: Use AI to synthesize trends and generate executive takeaways.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-insight-reporting
- **Tools**: ai-workspace-ui
- **Actions**:
    - Trigger AI analysis and generate takeaways.

### Phase 3: Visual Export & Formatting
- **Goal**: Compile visualizations into formatted PDF reports.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation
- **Tools**: pdf-generator
- **Actions**:
    - Compile charts with captions and dates into PDF.

### Phase 4: Distribution & Archiving
- **Goal**: Distribute report to stakeholders and archive historical state.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: knowledge-bridge-ui
- **Actions**:
    - Post to Knowledge Bridge and archive JSON records.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
