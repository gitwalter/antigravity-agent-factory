---
description: 'Workflow for SD-related development: pricing, billing, delivery, reports,
  RAP. References VBAK, VBAP, VBRK, VBRP.'
version: 1.0.0
tags:
- sd
- development
- standardized
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

### Phase 1: Sales Process Analysis
- **Goal**: Identify sales document types and pricing rules.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map requirements to core SD tables (`VBAK`, `VBAP`, `VBRK`, `VBRP`).

### Phase 2: Pricing & Logic Design
- **Goal**: Define custom pricing requirements or processing logic.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Search for Condition Techniques or User Exits (`MV45AFZZ`).

### Phase 3: Implementation (RAP or Classic)
- **Goal**: Build sales enhancements or RAP BOs for sales.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Actions**:
    - Implement custom logic via ABAP or RAP.

### Phase 4: Integration Verification
- **Goal**: Ensure sales cycle flows correctly to delivery and billing.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Actions**:
    - Test end-to-end sales scenarios.

### Phase 5: Release & Documentation
- **Goal**: Formally deploy and document sales changes.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Actions**:
    - Update design documents and release transport.


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
