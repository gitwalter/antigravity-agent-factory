---
description: "Workflow for FI-related development: reports, enhancements, validations. References BKPF, BSEG, FI-CAX/VIM where rele..."
version: 1.0.0
---

# Fi Development

Workflow for FI-related development: reports, enhancements, validations. References BKPF, BSEG, FI-CAX/VIM where relevant. S/4 on-prem and R/3/ECC.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap

## Trigger Conditions

This workflow is activated when:

- FI report (e.g. G/L balance, open items)
- FI document validation enhancement
- FI posting interface or extension

**Trigger Examples:**
- "Create a G/L balance report"
- "Add validation for FI document posting"
- "Build open items report for vendor accounts"
- "Enhance FI posting with custom fields"

## Steps

## Phases

### 1. Finance Process Mapping
- **Goal**: Identify the correct GL accounts and financial documents.
- **Action**: Map requirements to core FI tables (`BKPF`, `BSEG`, `ACDOCA`).
- **Reference**: Check `knowledge/fi-patterns.json` for tax codes and payment schemas.

### 2. Enhancement Identification
- **Goal**: Find the suitable SAP standard enhancement points.
- **Action**: Search for suitable Validations (`OB28`), Substitutions (`OBBH`), or BAdIs.
- **Tool**: `mcp_memory_search_nodes` for existing FI custom logic.

### 3. Solution Implementation
- **Goal**: Build and configure the financial enhancement.
- **Action**: Implement custom logic using ABAP Cloud or classic BTEs/BAdIs.
- **Template**: Use `sap-abap-enhancement` blueprint.

### 4. Post-Implementation Testing
- **Goal**: Verify financial integrity and document posting.
- **Action**: Test document posting and check the impact on ledgers in the development client.
- **Tool**: Trigger `/quality-gate` for logic verification.

### 5. Final Audit & Release
- **Goal**: Ensure audit compliance and release.
- **Action**: Update the technical specification and release the transport.
- **Tool**: Trigger `/documentation-workflow`.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
