---
description: 'Workflow for FI-related development: reports, enhancements, validations.
  References BKPF, BSEG, FI-CAX/VIM where rele...'
version: 1.0.0
tags:
- fi
- development
- standardized
---


# Fi Development

Workflow for FI-related development: reports, enhancements, validations. References BKPF, BSEG, FI-CAX/VIM where relevant. S/4 on-prem and R/3/ECC.

**Version:** 1.0.0
**Applies To:** sap-s4-enterprise, sap-abap

## Trigger Conditions

This workflow is activated when:

- FI report (e.g. G/L balance, open items)
- FI document validation enhancement
- FI posting interface or extension

**Trigger Examples:**
- "Create a G/L balance report"
- "Add validation for FI document posting"
- "Build open items report for vendor accounts"
- "Enhance FI posting with custom fields"

## Steps

## Phases

### Phase 1: Finance Process Mapping
- **Goal**: Identify GL accounts and financial documents for mapping.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map requirements to core FI tables (`BKPF`, `BSEG`, `ACDOCA`).

### Phase 2: Enhancement Identification
- **Goal**: Find suitable SAP standard enhancement points (Validations, Substitutions).
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Search for Validations (`OB28`), Substitutions (`OBBH`), or BAdIs.

### Phase 3: Solution Implementation
- **Goal**: Build and configure financial enhancements or reports.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Actions**:
    - Implement custom logic using ABAP or BTEs.

### Phase 4: Post-Implementation Testing
- **Goal**: Verify financial integrity and document posting impact.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Actions**:
    - Test document posting and check ledger impact.

### Phase 5: Audit compliance & Release
- **Goal**: Ensure compliance and release transport request.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Actions**:
    - Update specifications and release transport.


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
