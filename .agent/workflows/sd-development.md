---
description: "Workflow for SD-related development: pricing, billing, delivery, reports, RAP. References VBAK, VBAP, VBRK, VBRP."
version: 1.0.0
---

# Sd Development

Workflow for SD-related development: pricing, billing, delivery, reports, RAP. References VBAK, VBAP, VBRK, VBRP.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap, sap-rap

## Trigger Conditions

This workflow is activated when:

- SD report or RAP BO over sales/billing data
- Pricing or billing enhancement
- Delivery or document flow logic

**Trigger Examples:**
- "Create a sales order report"
- "Enhance pricing procedure with custom condition"
- "Build RAP BO for billing documents"
- "Implement delivery split logic"

## Steps

## Phases

### 1. Sales Process Analysis
- **Goal**: Identify the correct sales document types and pricing rules.
- **Action**: Map requirements to core SD tables (`VBAK`, `VBAP`, `VBRK`, `VBRP`).
- **Reference**: Check `knowledge/sd-patterns.json` for pricing procedures and partner functions.

### 2. Pricing & Logic Design
- **Goal**: Define custom pricing requirements or processing logic.
- **Action**: Search for suitable Condition Techniques or User Exits (e.g., `MV45AFZZ`).
- **Tool**: `mcp_memory_search_nodes` for existing SD enhancements.

### 3. Implementation (RAP or Classic)
- **Goal**: Build the sales enhancement.
- **Action**: Implement custom logic via ABAP or RAP BOs for sales orders.
- **Template**: Use `sap-sd-pricing-routine` or `sap-rap-bo` blueprints.

### 4. Integration Verification
- **Goal**: Ensure the sales cycle flows correctly to delivery/billing.
- **Action**: Test end-to-end sales scenarios in the development sandbox.
- **Tool**: Trigger `/quality-gate` for automated checks.

### 5. Release & Documentation
- **Goal**: Formally deploy and document the change.
- **Action**: Update the functional design and release the transport request.
- **Tool**: Trigger `/documentation-workflow`.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
