---
description: Behavior-Driven Development workflow that starts with stakeholder-readable
  Gherkin scenarios and translates them into...
version: 1.0.0
tags:
- bdd
- driven
- development
- standardized
---


# Bdd Driven Development

Behavior-Driven Development workflow that starts with stakeholder-readable Gherkin scenarios and translates them into executable tests. Emphasizes collaboration between business, development, and QA through the Three Amigos process.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** workflow-quality-specialist

## Trigger Conditions

This workflow is activated when:

- User requests BDD-style development
- Feature file or Gherkin scenario is provided
- Stakeholder-readable specifications needed
- Behavior-first approach requested

**Trigger Examples:**
- "Implement this feature using BDD"
- "Write Gherkin scenarios for user login"
- "Create feature files for the checkout process"
- "BDD for the payment module"

## Phases

### Phase 1: Behavior Discovery & Gherkin Modeling
- **Goal**: Identify stakeholder requirements and translate them into Gherkin scenarios.
- **Agents**: `workflow-quality-specialist`
- **Skills**: bdd-driven-development, reviewing-requirements
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Define examples with stakeholders and write Gherkin feature files.

### Phase 2: Test Automation & Implementation
- **Goal**: Scale automated test stubs and implement the production logic to pass them.
- **Agents**: `workflow-quality-specialist`
- **Skills**: bdd-driven-development, developing-ai-agents
- **Tools**: behave-cli, write_to_file
- **Actions**:
    - Generate step stubs and implement step definitions.
    - Implement production code to pass the feature tests.

### Phase 3: Verification & SDLC Integration
- **Goal**: Verify all scenarios pass and integrate results into the CI/CD pipeline.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: bdd-driven-development, verifying-artifact-structures
- **Tools**: behave-cli, python-interpreter
- **Actions**:
    - Run full feature suite and verify logic against unit tests.

### Phase 4: Documentation & Stakeholder Handoff
- **Goal**: Generate live documentation and finalize behavioral sign-off.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation, bdd-driven-development
- **Tools**: behave-formatter, write_to_file
- **Actions**:
    - Generate documentation and share results with stakeholders.


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
