---
description: SAP Cloud Platform Integration (CPI) iFlow development workflow. Covers
  integration design, iFlow development, Groovy...
version: 1.0.0
tags:
- iflow
- development
- standardized
---


# Iflow Development

SAP Cloud Platform Integration (CPI) iFlow development workflow. Covers integration design, iFlow development, Groovy scripting, testing-agents, and deployment to CPI tenant.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** integrating-sap-systems, cpi-iflow

## Trigger Conditions

This workflow is activated when:

- CPI integration needed
- iFlow development requested
- System-to-system integration
- SAP Integration Suite project

**Trigger Examples:**
- "Create a CPI iFlow for order sync"
- "Develop integration between S/4 and SuccessFactors"
- "Build an iFlow with content-based routing"
- "Implement CPI integration for OData"

## Phases

### Phase 1: Integration Design
- **Goal**: Define the source and target systems and the integration pattern.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems
- **Tools**: search_web
- **Actions**:
    - Identify systems (S/4HANA, Salesforce, etc.) and communication protocols (SOAP, REST, OData).

### Phase 2: iFlow Modeling
- **Goal**: Create the iFlow and model the message flow and transformations.
- **Agents**: `python-ai-specialist`
- **Skills**: iflow-development
- **Tools**: write_to_file
- **Actions**:
    - Create iFlow and add adapters (Request-Reply, Content Modifier).
    - Model XML/JSON transformations.

### Phase 3: Groovy Scripting & Logic
- **Goal**: Implement complex logic using Groovy or custom scripts.
- **Agents**: `python-ai-specialist`
- **Skills**: iflow-development
- **Tools**: write_to_file
- **Actions**:
    - Write Groovy scripts for custom header/body manipulation.

### Phase 4: Verification & Testing
- **Goal**: Validate the iFlow in the simulation environment and CPI tenant.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: run_tests.py
- **Actions**:
    - Test iFlow with sample payloads and verify transformations.

### Phase 5: Deployment & Monitoring
- **Goal**: Deploy the iFlow to production and set up logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: cpi-dashboard, grafana
- **Actions**:
    - Deploy iFlow and configure message logging.


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
