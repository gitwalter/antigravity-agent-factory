---
agents:
- workflow-quality-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for bdd-driven-development. Standardized for IDX
  Visual Editor.
domain: universal
name: bdd-driven-development
steps:
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Define examples with stakeholders and write Gherkin feature files.
  agents:
  - workflow-quality-specialist
  goal: Identify stakeholder requirements and translate them into Gherkin scenarios.
  name: Behavior Discovery & Gherkin Modeling
  skills:
  - bdd-driven-development
  - reviewing-requirements
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Generate step stubs and implement step definitions.
  - Implement production code to pass the feature tests.
  agents:
  - workflow-quality-specialist
  goal: Scale automated test stubs and implement the production logic to pass them.
  name: Test Automation & Implementation
  skills:
  - bdd-driven-development
  - developing-ai-agents
  tools:
  - behave-cli
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Run full feature suite and verify logic against unit tests.
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Verify all scenarios pass and integrate results into the CI/CD pipeline.
  name: Verification & SDLC Integration
  skills:
  - bdd-driven-development
  - verifying-artifact-structures
  tools:
  - behave-cli
  - python-interpreter
- actions:
  - '**Agents**: `knowledge-operations-specialist`'
  - '**Actions**:'
  - Generate documentation and share results with stakeholders.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - knowledge-operations-specialist
  goal: Generate live documentation and finalize behavioral sign-off.
  name: Documentation & Stakeholder Handoff
  skills:
  - generating-documentation
  - bdd-driven-development
  tools:
  - behave-formatter
  - write_to_file
tags: []
type: sequential
version: 2.0.0
---
# BDD Driven Development

**Version:** 1.0.0

## Overview
Antigravity workflow for behavior-driven development (BDD). Standardized for IDX Visual Editor.

## Trigger Conditions
- New feature requirements defined.
- Need for automated regression testing via Gherkin scenarios.
- User request: `/bdd-driven-development`.

**Trigger Examples:**
- "Implement the login feature using BDD."
- "Write Gherkin scenarios for the checkout process."

## Phases

### 1. Behavior Discovery & Gherkin Modeling
- **Goal**: Identify stakeholder requirements and translate them into Gherkin scenarios.
- **Agents**: `workflow-quality-specialist`
- **Skills**: bdd-driven-development, reviewing-requirements
- **Tools**: mcp_memory_search_nodes
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Define examples with stakeholders and write Gherkin feature files.

### 2. Test Automation & Implementation
- **Goal**: Scale automated test stubs and implement the production logic to pass them.
- **Agents**: `workflow-quality-specialist`
- **Skills**: bdd-driven-development, developing-ai-agents
- **Tools**: behave-cli, write_to_file
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Generate step stubs and implement step definitions.
- Implement production code to pass the feature tests.

### 3. Verification & SDLC Integration
- **Goal**: Verify all scenarios pass and integrate results into the CI/CD pipeline.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: bdd-driven-development, verifying-artifact-structures
- **Tools**: behave-cli, python-interpreter
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Run full feature suite and verify logic against unit tests.

### 4. Documentation & Stakeholder Handoff
- **Goal**: Generate live documentation and finalize behavioral sign-off.
- **Agents**: `knowledge-operations-specialist`
- **Skills**: generating-documentation, bdd-driven-development
- **Tools**: behave-formatter, write_to_file
- **Agents**: `knowledge-operations-specialist`
- **Actions**:
- Generate documentation and share results with stakeholders.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
