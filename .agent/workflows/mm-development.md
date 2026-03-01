---
## Overview

description: "Workflow for MM-related development: procurement, inventory, movements, reports, RAP. References EKKO, EKPO, MKPF, MS..."
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

Standard PABP development phases apply:
1.  **Define Requirements**
2.  **Design Architecture**
3.  **Implementation**
4.  **Verification**
5.  **Deployment**


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
