---
description: End-to-end workflow for developing RESTful ABAP Programming Model (RAP) business objects in SAP S/4HANA. Covers CDS m...
version: 1.0.0
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

### 1. Data Modeling (CDS)
- **Goal**: Define the core data structure and relationships.
- **Action 1**: Create the database table for persistent storage.
- **Action 2**: Define the CDS Interface View (`R_ProductTP`) and Projection View (`C_ProductTP`).
- **Tool**: Use `mcp_memory_search_nodes` to find reusable CDS patterns.

### 2. Behavior Definition & Implementation
- **Goal**: Define business logic and CRUD capabilities.
- **Action 1**: Create the Behavior Definition (`BDEF`).
- **Action 2**: Implement the Behavior Pool (Local Types) for actions, validations, and determinations.
- **Reference**: Follow the `rap-with-draft` pattern if draft handling is required.

### 3. Service Exposure
- **Goal**: Expose the BO as a consumable OData service.
- **Action 1**: Define the Service Definition (`SRV`).
- **Action 2**: Create the Service Binding (UI or Web API).

### 4. UI & Orchestration
- **Goal**: Provide a consumption layer.
- **Action**: Add UI Annotations via Metadata Extension (`MDE`) or directly in the CDS.
- **Tool**: Trigger `/fiori-app-development` if a custom UI is required.

### 5. Verification & Deployment
- **Goal**: Ensure quality and move to production.
- **Action**: Run ABAP Unit tests and verify authorization objects.
- **Tool**: Trigger `/quality-gate` before transport.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
