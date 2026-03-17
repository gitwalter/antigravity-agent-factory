---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for fi-development. Standardized for IDX Visual
  Editor.
domain: universal
name: fi-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Map requirements to core FI tables (`BKPF`, `BSEG`, `ACDOCA`).
  agents:
  - python-ai-specialist
  goal: Identify GL accounts and financial documents for mapping.
  name: Finance Process Mapping
  skills:
  - guiding-s4-processes
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Search for Validations (`OB28`), Substitutions (`OBBH`), or BAdIs.
  agents:
  - python-ai-specialist
  goal: Find suitable SAP standard enhancement points (Validations, Substitutions).
  name: Enhancement Identification
  skills:
  - guiding-s4-processes
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement custom logic using ABAP or BTEs.
  agents:
  - python-ai-specialist
  goal: Build and configure financial enhancements or reports.
  name: Solution Implementation
  skills:
  - guiding-s4-processes
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test document posting and check ledger impact.
  agents:
  - workflow-quality-specialist
  goal: Verify financial integrity and document posting impact.
  name: Post-Implementation Testing
  skills:
  - verifying-artifact-structures
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Update specifications and release transport.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  - knowledge-operations-specialist
  goal: Ensure compliance and release transport request.
  name: Audit compliance & Release
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
tags: []
type: sequential
version: 2.0.0
---
# Finance (FI) Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP Finance (FI) development in S/4HANA. Standardized for IDX Visual Editor.

## Trigger Conditions
- Business requirement for financial process enhancements or custom reports.
- Need to implement SAP Validations, Substitutions, or BTEs in the FI module.
- User request: `/fi-development`.

**Trigger Examples:**
- "Implement a validation rule for document posting in company code 1000."
- "Create a report for analyzing open items in the accounts receivable ledger."

## Phases

### 1. Finance Process Mapping
- **Goal**: Identify GL accounts and financial documents for mapping.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Map requirements to core FI tables (`BKPF`, `BSEG`, `ACDOCA`).

### 2. Enhancement Identification
- **Goal**: Find suitable SAP standard enhancement points (Validations, Substitutions).
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Search for Validations (`OB28`), Substitutions (`OBBH`), or BAdIs.

### 3. Solution Implementation
- **Goal**: Build and configure financial enhancements or reports.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement custom logic using ABAP or BTEs.

### 4. Post-Implementation Testing
- **Goal**: Verify financial integrity and document posting impact.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test document posting and check ledger impact.

### 5. Audit compliance & Release
- **Goal**: Ensure compliance and release transport request.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Update specifications and release transport.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
