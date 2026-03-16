---
description: 'Workflow for EWM-related development: warehouse structure, movements,
  custom logic. Embedded EWM in S/4HANA.'
version: 1.0.0
tags:
- ewm
- development
- standardized
---


# Ewm Development

Workflow for EWM-related development: warehouse structure, movements, custom logic. Embedded EWM in S/4HANA.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap

## Trigger Conditions

This workflow is activated when:

- EWM custom logic or report
- Movement type or warehouse task extension
- Integration with MM/SD

**Trigger Examples:**
- "Create warehouse task logging-and-monitoring report"
- "Enhance putaway strategy logic"
- "Build custom EWM process for quality inspection"
- "Implement wave management extension"

## Phases

### Phase 1: Requirements & Mapping
- **Goal**: Define warehouse logic and map entities to EWM structures.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify warehouse types and movement structures.

### Phase 2: Technical Design
- **Goal**: Design the EWM extension or report for warehouse tasks.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify BAPIs or enhancement points.

### Phase 3: Implementation
- **Goal**: Build the EWM solution in S/4HANA.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Actions**:
    - Implement custom logic and logging-and-monitoring reports.

### Phase 4: Verification
- **Goal**: Validate warehouse tasks and movement strategies.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Actions**:
    - Test warehouse tasks and putaway/picking strategies.

### Phase 5: Deployment
- **Goal**: Release transport and document EWM changes.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Actions**:
    - Release transport and update documentation.


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
