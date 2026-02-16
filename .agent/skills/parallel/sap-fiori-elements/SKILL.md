---
description: Tactical Blueprint for SAP Fiori Elements development. Focuses on metadata-driven
  UI development via CDS annotations and SAP Fiori Tools.
name: sap-fiori-elements
type: skill
---
# Capability Manifest: SAP Fiori Elements

This blueprint provides the **procedural truth** for engineering high-fidelity, metadata-driven user interfaces in the SAP ecosystem.

## When to Use

This skill should be used when completing tasks related to sap fiori elements.

## Process

Follow these procedures to develop SAP Fiori Elements applications:

### Procedure 1: Layout Engineering (CDS Annotations)
1.  **List Report Config**:
    - Use `@UI.selectionField` for filter bar entries.
    - Use `@UI.lineItem` for table columns with proper `position` and `importance`.
    - Use `@EndUserText.label` for all column headers.
2.  **Object Page Config**:
    - Define `@UI.facet` hierarchy (Collection Facets for grouping, Reference Facets for content).
    - Use `@UI.fieldGroup` to organize fields into semantic sections.
    - Implement `HeaderInfo` with `Title` and `Description` for visual clarity.

### Procedure 2: Intelligent Interaction (Value Helps & Actions)
1.  **Semantic Value Helps**: Use `@Consumption.valueHelpDefinition` for all foreign key fields, ensuring search and validation are active.
2.  **Status Criticality**: Bind the `criticality` of status fields to a specific property (e.g., `StatusCriticality`) to provide visual feedback (Success/Warning/Error).
3.  **Action Exposure**: Expose `BDEF` actions via `@UI.lineItem: [ { type: #FOR_ACTION ... } ]` and `@UI.identification`.

### Procedure 3: Draft-Ready UI
1.  **Interaction Integrity**: Ensure the Fiori app is configured to handle the "Draft" lifecycle (Resume, Discard, Activate).
2.  **Side Effects**: Annotate fields that trigger updates in other parts of the UI via `@Common.SideEffects`.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Empty Filter Bar** | Selection fields missing in the projection view. | Add `@UI.selectionField: [ { position: X } ]` to the relevant CDS fields. |
| **Missing Navigation** | Semantic Object mapping failure. | Verify the `intent` (Action/Object) in the `manifest.json` and ensure the `@UI.lineItem` has the correct `type: #WITH_INTENT_BASED_NAVIGATION`. |
| **UI Not Updating** | Side effects not defined for determinations. | Add `@Common.SideEffects` to the triggering field in the CDS metadata. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Visual Modeling | `Page Map (SAP Fiori Tools)` |
| Metadata Check | `OData Service Preview ($metadata)` |
| Preview | `npm start` |
| Manifest Config | `manifest.json Editor` |

## Best Practices
Before finalized, verify:
- [ ] No manual JS logic for standard CRUD operations.
- [ ] All mandatory fields labeled correctly.
- [ ] Criticality used for all "Status" or "Progress" indicators.
- [ ] Value helps active for all ID-to-Text mappings.
