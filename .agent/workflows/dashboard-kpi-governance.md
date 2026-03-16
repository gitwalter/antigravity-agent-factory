---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dashboard-kpi-governance. Standardized for IDX
  Visual Editor.
domain: universal
name: dashboard-kpi-governance
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Document formula and business rationale.
  agents:
  - python-ai-specialist
  goal: Define business value and mathematical formula for the new KPI.
  name: Metric Definition
  skills:
  - dashboard-kpi-governance
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Add KPI to `GuidanceCenter` dictionary.
  agents:
  - python-ai-specialist
  goal: Integrate KPI into the system dictionary and provide visualization targets.
  name: Implementation & Dictionary Update
  skills:
  - dashboard-kpi-governance
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Confirm logic and visual clarity in the dictionary.
  agents:
  - workflow-quality-specialist
  goal: Test KPI logic against golden datasets for accuracy.
  name: Logical Verification
  skills:
  - verifying-artifact-structures
  tools:
  - statistical-validator
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Align with Analyst/Manager personas and update status.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Obtain sign-off from relevant personas and promote to standard.
  name: Stakeholder Governance
  skills:
  - committing-releases
  tools:
  - safety-gate
tags: []
type: sequential
version: 1.0.0
---

# KPI Governance Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for dashboard-kpi-governance. Standardized for IDX Visual Editor.

## Trigger Conditions
- New KPI requirement identified by stakeholders.
- Need for periodic metric audit or logic update.
- User request: `/dashboard-kpi-governance`.

**Trigger Examples:**
- "Define a new KPI for measuring agent latency."
- "Audit the business logic for the 'Conversion Rate' metric."

## Phases

### 1. Metric Definition
- **Goal**: Define business value and mathematical formula for the new KPI.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-kpi-governance
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Document formula and business rationale.

### 2. Implementation & Dictionary Update
- **Goal**: Integrate KPI into the system dictionary and provide visualization targets.
- **Agents**: `python-ai-specialist`
- **Skills**: dashboard-kpi-governance
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Add KPI to `GuidanceCenter` dictionary.

### 3. Logical Verification
- **Goal**: Test KPI logic against golden datasets for accuracy.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: statistical-validator
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Confirm logic and visual clarity in the dictionary.

### 4. Stakeholder Governance
- **Goal**: Obtain sign-off from relevant personas and promote to standard.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: safety-gate
- **Agents**: `project-operations-specialist`
- **Actions**:
- Align with Analyst/Manager personas and update status.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
