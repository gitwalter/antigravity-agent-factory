---
description: Confluence-documented feature development workflow. Covers requirements
  from Confluence, design documentation, implem...
version: 1.0.0
tags:
- confluence
- feature
- standardized
---


# Confluence Feature

Confluence-documented feature development workflow. Covers requirements from Confluence, design documentation, implementation, and documentation updates back to Confluence.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** developing-ai-agents, confluence-integration

## Trigger Conditions

This workflow is activated when:

- Feature documented in Confluence
- User references Confluence page for implementation
- Requirements in Confluence to implement
- Feature spec lives in Confluence

**Trigger Examples:**
- "Implement the feature from Confluence page 12345"
- "Build the feature as documented in Confluence"
- "Develop based on the spec in Confluence"
- "Follow the Confluence design doc"

## Phases

### Phase 1: Requirement Extraction & Analysis
- **Goal**: Fetch documentation from Confluence and analyze features for technical gaps.
- **Agents**: `system-architecture-specialist`
- **Skills**: confluence-feature, reviewing-requirements
- **Tools**: confluence-mcp, mcp_memory_search_nodes
- **Actions**:
    - Fetch Confluence page and clarify requirements.

### Phase 2: Design & Blueprinting
- **Goal**: Create technical blueprints and implementation plans based on Confluence specs.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, confluence-feature
- **Tools**: write_to_file
- **Actions**:
    - Initialize implementation plans.

### Phase 3: Execution & implementation
- **Goal**: Implement the feature and verify correctness through testing-agents.
- **Agents**: `project-operations-specialist`
- **Skills**: confluence-feature, developing-ai-agents
- **Tools**: write_to_file, pytest-cli
- **Actions**:
    - Implement production code and verify with tests.

### Phase 4: Documentation Loop-back
- **Goal**: Update Confluence with implementation details and close the feature loop.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation, confluence-feature
- **Tools**: confluence-mcp
- **Actions**:
    - Update Confluence page and finalize closure.


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
