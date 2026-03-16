---
description: End-to-end workflow for developing RESTful ABAP Programming Model (RAP)
  business objects in SAP S/4HANA. Covers CDS m...
version: 1.0.0
tags:
- rap
- development
- standardized
---


# Rap Development

End-to-end workflow for developing RESTful ABAP Programming Model (RAP) business objects in SAP S/4HANA. Covers CDS modeling, behavior definition, implementation, Fiori Elements UI, and deployment.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** sap-rap, sap-abap

## Trigger Conditions

This workflow is activated when:

- New RAP business object required
- CRUD operations needed for SAP data
- Fiori Elements app development
- ABAP Cloud development

**Trigger Examples:**
- "Create a RAP BO for purchase orders"
- "Develop Fiori app for inventory management"
- "Build managed BO with draft handling"
- "Implement custom RAP action"

## Steps

## Phases

### Phase 1: Data Modeling (CDS)
- **Goal**: Define the core data structure and relationships in the ABAP layer.
- **Agents**: `python-ai-specialist` (mapped to SAP Specialist)
- **Skills**: developing-rap-objects, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Create the database table for persistent storage.
    - Define the CDS Interface View (`R_ProductTP`) and Projection View (`C_ProductTP`).

### Phase 2: Behavior Definition & Implementation
- **Goal**: Define business logic, CRUD capabilities, and custom actions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: write_to_file
- **Actions**:
    - Create the Behavior Definition (`BDEF`).
    - Implement the Behavior Pool (Local Types) for actions, validations, and determinations.

### Phase 3: Service Exposure
- **Goal**: Expose the BO as a consumable OData service for Fiori or external consumption.
- **Agents**: `python-ai-specialist`
- **Skills**: designing-apis
- **Tools**: replace_file_content
- **Actions**:
    - Define the Service Definition (`SRV`).
    - Create the Service Binding (UI or Web API).

### Phase 4: UI & Orchestration
- **Goal**: Provide a consumption layer with Fiori Elements annotations.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: write_to_file
- **Actions**:
    - Add UI Annotations via Metadata Extension (`MDE`) or directly in the CDS.

### Phase 5: Verification & Deployment
- **Goal**: Ensure quality via ABAP Unit and move to production via transports.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, committing-releases
- **Tools**: run_tests.py (simulated ABAP unit)
- **Actions**:
    - Run ABAP Unit tests and verify authorization objects.
    - Trigger quality gate before transport.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
