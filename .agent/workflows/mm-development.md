---
description: "Workflow for MM-related development: procurement, inventory, movements, reports, RAP. References EKKO, EKPO, MKPF, MS..."
version: 1.0.0
---

# Mm Development

Workflow for MM-related development: procurement, inventory, movements, reports, RAP. References EKKO, EKPO, MKPF, MSEG, RSEG.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap, sap-rap

## Trigger Conditions

This workflow is activated when:

- MM report (PO, goods movement, inventory)
- Procurement or invoice verification enhancement
- RAP BO over purchase or material document

**Trigger Examples:**
- "Create a purchase order status report"
- "Enhance goods receipt processing"
- "Build RAP BO for material documents"
- "Implement custom procurement validation"

## Steps

## Phases

### 1. Requirement & Data Mapping
- **Goal**: Identify the correct SAP tables and fields.
- **Action**: Map requirements to core MM tables (`EKKO`, `EKPO`, `MKPF`, `MSEG`).
- **Reference**: Check `knowledge/mm-patterns.json` for movement types and procurement schemas.

### 2. Technical Design
- **Goal**: Choose the implementation technique (User Exit, BAdI, Report, or RAP).
- **Action**: Search for suitable enhancement points or BAPIs (e.g., `BAPI_PO_CREATE1`).
- **Tool**: `mcp_memory_search_nodes` for existing MM enhancements.

### 3. Development & Implementation
- **Goal**: Build the solution.
- **Action**: Implement custom logic using ABAP Cloud or Classic ABAP depending on the target system.
- **Template**: Use `sap-abap-report` or `sap-rap-bo` blueprints.

### 4. Verification & Testing
- **Goal**: Validate against business processes.
- **Action**: Test goods movements or procurement cycles in the development client.
- **Tool**: Trigger `/quality-gate` for automated logic checks.

### 5. Transport & Documentation
- **Goal**: Formally release the change.
- **Action**: Update the functional specification and release the transport request.
- **Tool**: Trigger `/documentation-workflow`.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
