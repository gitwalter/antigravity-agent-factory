---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for sd-development. Standardized for IDX Visual
  Editor.
domain: universal
name: sd-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Map requirements to core SD tables (`VBAK`, `VBAP`, `VBRK`, `VBRP`).
  agents:
  - python-ai-specialist
  goal: Identify sales document types and pricing rules.
  name: Sales Process Analysis
  skills:
  - guiding-s4-processes
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Search for Condition Techniques or User Exits (`MV45AFZZ`).
  agents:
  - python-ai-specialist
  goal: Define custom pricing requirements or processing logic.
  name: Pricing & Logic Design
  skills:
  - guiding-s4-processes
  - designing-apis
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement custom logic via ABAP or RAP.
  agents:
  - python-ai-specialist
  goal: Build sales enhancements or RAP BOs for sales.
  name: Implementation (RAP or Classic)
  skills:
  - guiding-s4-processes
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test end-to-end sales scenarios.
  agents:
  - workflow-quality-specialist
  goal: Ensure sales cycle flows correctly to delivery and billing.
  name: Integration Verification
  skills:
  - verifying-artifact-structures
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Update design documents and release transport.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  - knowledge-operations-specialist
  goal: Formally deploy and document sales changes.
  name: Release & Documentation
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
tags: []
type: sequential
version: 2.0.0
---
# SAP Sales and Distribution (SD) Development

**Version:** 1.0.0

## Overview
Antigravity workflow for developing and enhancing SAP Sales and Distribution (SD) processes. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for implementing custom sales processes or pricing logic in SAP.
- Need to enhance core SD functionalities (Sales Orders, Billing, etc.).
- User request: `/sd-development`.

**Trigger Examples:**
- "Develop a custom pricing routine for 'Volume-Based Discounts' in SD."
- "Implement an enhancement for sales order creation in the S/4HANA system."

## Phases

### 1. Sales Process Analysis
- **Goal**: Identify sales document types and pricing rules.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Map requirements to core SD tables (`VBAK`, `VBAP`, `VBRK`, `VBRP`).

### 2. Pricing & Logic Design
- **Goal**: Define custom pricing requirements or processing logic.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Search for Condition Techniques or User Exits (`MV45AFZZ`).

### 3. Implementation (RAP or Classic)
- **Goal**: Build sales enhancements or RAP BOs for sales.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement custom logic via ABAP or RAP.

### 4. Integration Verification
- **Goal**: Ensure sales cycle flows correctly to delivery and billing.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test end-to-end sales scenarios.

### 5. Release & Documentation
- **Goal**: Formally deploy and document sales changes.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Update design documents and release transport.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
