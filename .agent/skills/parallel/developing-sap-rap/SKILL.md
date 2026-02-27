---
agents:
- none
category: parallel
description: Tactical Blueprint for RESTful ABAP Programming (RAP) and CDS Modeling.
  Focuses on 'Clean Core' compliant on-stack extensibility in S/4HANA Cloud.
knowledge:
- none
name: developing-sap-rap
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Capability Manifest: SAP Enterprise RAP

This blueprint provides the **procedural truth** for building production-grade on-stack extensions using the RESTful ABAP Programming Model.

## When to Use

This skill should be used when completing tasks related to sap enterprise rap.

## Process

Follow these procedures to build production-grade on-stack extensions:

### Procedure 1: Data Modeling for Truth (CDS)
1.  **Strict Layering**: Use `I_` (Interface) views for data modeling and `C_` (Consumption) views for UI projection.
2.  **Released Successor Check**: Never use `MARA`, `VBAK`, etc. Search the API Business Hub for released success (e.g., `I_SalesOrder`).
3.  **Semantic Annotations**: Label every field with `@EndUserText.label` and provide unit/currency bindings.

### Procedure 2: Managed Behavior Implementation (BDEF)
1.  **Draft Mandatory**: Always use `with draft` for multi-step transactional logic to ensure data integrity.
2.  **Strict Mode**: Use `strict ( 2 );` to enforce modern ABAP Cloud syntax and locking rules.
3.  **Determinations & Validations**:
    - Use `determination` for side effects (e.g., calculating total price).
    - Use `validation` for business rules with proper message reporting via `%msg`.

### Procedure 3: Service Exposure & Binding
1.  **Granular Exposure**: Only expose view entities required for the specific business task in the `Service Definition`.
2.  **OData v4 Preference**: Always use OData v4 for new Fiori Elements applications unless backward compatibility is required.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Short Dump (Locked)** | Missing ETag or Total ETag mismatch. | Implement `lock master total etag last_changed_at` in the BDEF. |
| **Draft Activation Fail** | Validation error in the draft layer. | Inspect the `reported` and `failed` parameters in the behavior pool; provide clear `%element` mapping for UI highlighting. |
| **Syntax Error (Cloud)** | Use of non-released APIs or legacy syntax. | Replace with `successor` components identified via the ADT "Release State" tab. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Create CDS | `ADT -> New Data Definition` |
| Define Behavior | `ADT -> New Behavior Definition` |
| Test OData | `Fiori Elements Preview / Gateway Client` |
| Deploy | `MTA / Transport Management` |

## Best Practices
Before finalizing any RAP object, verify:
- [ ] No direct standard table modifications.
- [ ] Only released SAP APIs used.
- [ ] Mandatory Audit fields (`created_at`, `last_changed_at`) implemented.
- [ ] Draft handling enabled for transactional entities.
