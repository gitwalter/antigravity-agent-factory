---
description: End-to-end workflow for developing RAP business objects with draft handling.
  Covers data model, behavior definition, ...
version: 1.0.0
tags:
- rap
- with
- draft
- standardized
---


# Rap With Draft

End-to-end workflow for developing RAP business objects with draft handling. Covers data model, behavior definition, draft configuration, actions, authorization, and testing-agents.

**Version:** 1.0.0
**Created:** 2026-02-09
**Applies To:** sap-systems-specialist, developing-rap-objects

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

## Phases

### Phase 1: Data Model & Draft Configuration
- **Goal**: Define the persistent and draft tables and the initial CDS views.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects, developing-rap-objects
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Create database and draft tables.
    - Create CDS Interface and Projection views.

### Phase 2: Behavior Definition with Draft
- **Goal**: Configure the Behavior Definition to support draft handling and ETag.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: write_to_file
- **Actions**:
    - Create Behavior Definition with `with draft`.
    - Configure Draft Indicator and Draft Actions.

### Phase 3: Implementation of Actions & Authorization
- **Goal**: Implement logic for draft activation, custom actions, and instance-based authorization.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects, securing-ai-systems
- **Tools**: replace_file_content
- **Actions**:
    - Implement Submit and other custom actions.
    - Configure instance authorization and DCL rules.

### Phase 4: Verification & Testing
- **Goal**: Rigorously test draft lifecycle (Create, Activate, Resume, ETag).
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: run_tests.py
- **Actions**:
    - Test draft creation, activation, and resume.
    - Verify ETag handling and action logic.


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
