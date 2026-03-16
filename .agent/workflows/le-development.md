---
description: 'Workflow for Logistics Execution: shipping, transportation, delivery
  processing. References LIKP, LIPS; links to SD/M...'
version: 1.0.0
tags:
- le
- development
- standardized
---


# Le Development

Workflow for Logistics Execution: shipping, transportation, delivery processing. References LIKP, LIPS; links to SD/MM/EWM.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap

## Trigger Conditions

This workflow is activated when:

- LE report or enhancement (shipping, delivery)
- Transportation or delivery document extension

**Trigger Examples:**
- "Create a delivery status report"
- "Enhance shipping point determination"
- "Build outbound delivery logging-and-monitoring"
- "Implement transportation planning extension"

## Phases

### Phase 1: Requirement Analysis
- **Goal**: Define shipping and delivery requirements and identify LE tables.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map requirements to `LIKP` and `LIPS` tables.

### Phase 2: Technical Design
- **Goal**: Design the technical solution for shipping determination or delivery extensions.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Identify enhancement points and design the logic.

### Phase 3: Implementation
- **Goal**: Implement the LE solution using ABAP.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Actions**:
    - Implement custom logic and logging-and-monitoring reports.

### Phase 4: Verification
- **Goal**: Validate delivery processing and shipping point determination.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Actions**:
    - Test LE scenarios and status tracking.

### Phase 5: Deployment
- **Goal**: Release transport and document LE changes.
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
