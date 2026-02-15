---
## Overview

description: End-to-end workflow for developing RAP business objects with draft handling. Covers data model, behavior definition, ...
---

# Rap With Draft

End-to-end workflow for developing RAP business objects with draft handling. Covers data model, behavior definition, draft configuration, actions, authorization, and testing.

**Version:** 1.0.0
**Created:** 2026-02-09
**Applies To:** sap-developer, rap-development

## Trigger Conditions

This workflow is activated when:

- RAP BO with draft handling required
- Multi-session editing needed
- Complex approval workflows
- Draft-enabled Fiori apps

**Trigger Examples:**
- "Create a RAP BO with draft handling for purchase orders"
- "Build draft-enabled business object"
- "Implement RAP BO with draft and actions"
- "Create managed BO with draft support"

## Steps

### Create Database Table

### Create Draft Table

### Create CDS Interface View (I_)

### Create CDS Projection View (C_)

### Create Behavior Definition with Draft

### Configure Draft Indicator

### Configure Draft Actions

### Implement Submit Action

### Implement Other Actions

### Configure Instance Authorization

### Create DCL Rules (if needed)

### Test Draft Creation

### Test Draft Activation

### Test Draft Resume

### Test ETag Handling

### Test Actions

### Test Authorization


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
