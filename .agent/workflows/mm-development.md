---
description: 'Workflow for MM-related development: procurement, inventory, movements,
  reports, RAP. References EKKO, EKPO, MKPF, MS...'
version: 1.0.0
tags:
- mm
- development
- standardized
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

### Phase 1: Requirement & Data Mapping
- **Goal**: Identify the correct SAP tables and fields for procurement and inventory.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map requirements to core MM tables (`EKKO`, `EKPO`, `MKPF`, `MSEG`).

### Phase 2: Technical Design & Enhancement
- **Goal**: Select the enhancement technique (BAdI, Exit, RAP) and define logic.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify enhancement points or BAPIs.
    - Create technical design.

### Phase 3: Development & Implementation
- **Goal**: Build the MM solution using ABAP Cloud or Classic ABAP.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Actions**:
    - Implement custom logic and report/BO logic.

### Phase 4: Verification & Integration Testing
- **Goal**: Validate the procurement cycle and inventory movements.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Actions**:
    - Test goods movements and procurement cycles.

### Phase 5: Transport & Documentation
- **Goal**: Formally release the change and update technical documentation.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Actions**:
    - Update specifications and release transport.


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
