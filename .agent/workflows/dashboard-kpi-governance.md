---
description: KPI Definition & Governance Process
dashboard: true
version: 1.0.0
tags:
- dashboard
- kpi
- governance
- standardized
---


# KPI Governance Workflow

**Version:** 1.0.0

Systematic routine for introducing, auditing, and publishing new KPIs.

## Trigger Conditions
- A new KPI is proposed for the dashboard.
- An existing KPI needs recalibration or audit.
- Stakeholders request alignment on metric definitions.

**Trigger Examples:**
- "Define and publish a new UPH metric."
- "Audit the accuracy of the current KPI dictionary."

## Phases

### Phase 1: Metric Definition
- **Goal**: Define business value and mathematical formula for the new KPI.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-kpi-governance
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Document formula and business rationale.

### Phase 2: Implementation & Dictionary Update
- **Goal**: Integrate KPI into the system dictionary and provide visualization targets.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-kpi-governance
- **Tools**: write_to_file
- **Actions**:
    - Add KPI to `GuidanceCenter` dictionary.

### Phase 3: Logical Verification
- **Goal**: Test KPI logic against golden datasets for accuracy.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: statistical-validator
- **Actions**:
    - Confirm logic and visual clarity in the dictionary.

### Phase 4: Stakeholder Governance
- **Goal**: Obtain sign-off from relevant personas and promote to standard.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: safety-gate
- **Actions**:
    - Align with Analyst/Manager personas and update status.


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
