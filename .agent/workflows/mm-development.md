---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for mm-development. Standardized for IDX Visual
  Editor.
domain: universal
name: mm-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Map requirements to core MM tables (`EKKO`, `EKPO`, `MKPF`, `MSEG`).
  agents:
  - python-ai-specialist
  goal: Identify the correct SAP tables and fields for procurement and inventory.
  name: Requirement & Data Mapping
  skills:
  - guiding-s4-processes
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Identify enhancement points or BAPIs.
  - Create technical design.
  agents:
  - python-ai-specialist
  goal: Select the enhancement technique (BAdI, Exit, RAP) and define logic.
  name: Technical Design & Enhancement
  skills:
  - guiding-s4-processes
  - designing-apis
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement custom logic and report/BO logic.
  agents:
  - python-ai-specialist
  goal: Build the MM solution using ABAP Cloud or Classic ABAP.
  name: Development & Implementation
  skills:
  - guiding-s4-processes
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test goods movements and procurement cycles.
  agents:
  - workflow-quality-specialist
  goal: Validate the procurement cycle and inventory movements.
  name: Verification & Integration Testing
  skills:
  - verifying-artifact-structures
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Update specifications and release transport.
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
  goal: Formally release the change and update technical documentation.
  name: Transport & Documentation
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
tags: []
type: sequential
version: 2.0.0
---
# Materials Management (MM) Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP Materials Management (MM) development in S/4HANA. Standardized for IDX Visual Editor.

## Trigger Conditions
- Business requirement for procurement process enhancements or inventory management tools.
- Need to implement SAP BAdIs, Exits, or BAPIs in the MM module.
- User request: `/mm-development`.

**Trigger Examples:**
- "Implement a custom check for purchase order releases in company code 1000."
- "Develop a report for monitoring inventory stock levels across multiple warehouses."

## Phases

### 1. Requirement & Data Mapping
- **Goal**: Identify the correct SAP tables and fields for procurement and inventory.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Map requirements to core MM tables (`EKKO`, `EKPO`, `MKPF`, `MSEG`).

### 2. Technical Design & Enhancement
- **Goal**: Select the enhancement technique (BAdI, Exit, RAP) and define logic.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Identify enhancement points or BAPIs.
- Create technical design.

### 3. Development & Implementation
- **Goal**: Build the MM solution using ABAP Cloud or Classic ABAP.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement custom logic and report/BO logic.

### 4. Verification & Integration Testing
- **Goal**: Validate the procurement cycle and inventory movements.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test goods movements and procurement cycles.

### 5. Transport & Documentation
- **Goal**: Formally release the change and update technical documentation.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Update specifications and release transport.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
