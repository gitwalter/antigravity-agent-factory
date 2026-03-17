---
agents:
- workflow-quality-specialist
- python-ai-specialist (mapped to SAP Specialist)
- python-ai-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for rap-development. Standardized for IDX Visual
  Editor.
domain: universal
name: rap-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist` (mapped to SAP Specialist)'
  - '**Actions**:'
  - Create the database table for persistent storage.
  - Define the CDS Interface View (`R_ProductTP`) and Projection View (`C_ProductTP`).
  agents:
  - python-ai-specialist (mapped to SAP Specialist)
  goal: Define the core data structure and relationships in the ABAP layer.
  name: Data Modeling (CDS)
  skills:
  - developing-rap-objects
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create the Behavior Definition (`BDEF`).
  - Implement the Behavior Pool (Local Types) for actions, validations, and determinations.
  agents:
  - python-ai-specialist
  goal: Define business logic, CRUD capabilities, and custom actions.
  name: Behavior Definition & Implementation
  skills:
  - developing-rap-objects
  tools:
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Define the Service Definition (`SRV`).
  - Create the Service Binding (UI or Web API).
  agents:
  - python-ai-specialist
  goal: Expose the BO as a consumable OData service for Fiori or external consumption.
  name: Service Exposure
  skills:
  - designing-apis
  tools:
  - replace_file_content
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Add UI Annotations via Metadata Extension (`MDE`) or directly in the CDS.
  agents:
  - python-ai-specialist
  goal: Provide a consumption layer with Fiori Elements annotations.
  name: UI & Orchestration
  skills:
  - developing-fiori-apps
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Run ABAP Unit tests and verify authorization objects.
  - Trigger quality gate before transport.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Ensure quality via ABAP Unit and move to production via transports.
  name: Verification & Deployment
  skills:
  - verifying-artifact-structures
  - committing-releases
  tools:
  - run_tests.py (simulated ABAP unit)
tags: []
type: sequential
version: 2.0.0
---
# RESTful ABAP Programming (RAP) Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP RESTful ABAP Programming (RAP) model development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for building modern, OData-based SAP applications on S/4HANA.
- Need to implement business objects with persistent memory and transactional logic.
- User request: `/rap-development`.

**Trigger Examples:**
- "Develop a RAP-based business object for managing 'Product Categories'."
- "Implement custom actions and validations for the 'Sales Order' RAP application."

## Phases

### 1. Data Modeling (CDS)
- **Goal**: Define the core data structure and relationships in the ABAP layer.
- **Agents**: `python-ai-specialist (mapped to SAP Specialist)`
- **Skills**: developing-rap-objects, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist` (mapped to SAP Specialist)
- **Actions**:
- Create the database table for persistent storage.
- Define the CDS Interface View (`R_ProductTP`) and Projection View (`C_ProductTP`).

### 2. Behavior Definition & Implementation
- **Goal**: Define business logic, CRUD capabilities, and custom actions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create the Behavior Definition (`BDEF`).
- Implement the Behavior Pool (Local Types) for actions, validations, and determinations.

### 3. Service Exposure
- **Goal**: Expose the BO as a consumable OData service for Fiori or external consumption.
- **Agents**: `python-ai-specialist`
- **Skills**: designing-apis
- **Tools**: replace_file_content
- **Agents**: `python-ai-specialist`
- **Actions**:
- Define the Service Definition (`SRV`).
- Create the Service Binding (UI or Web API).

### 4. UI & Orchestration
- **Goal**: Provide a consumption layer with Fiori Elements annotations.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Add UI Annotations via Metadata Extension (`MDE`) or directly in the CDS.

### 5. Verification & Deployment
- **Goal**: Ensure quality via ABAP Unit and move to production via transports.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, committing-releases
- **Tools**: run_tests.py (simulated ABAP unit)
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Run ABAP Unit tests and verify authorization objects.
- Trigger quality gate before transport.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
