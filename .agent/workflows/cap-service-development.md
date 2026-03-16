---
description: End-to-end workflow for developing SAP Cloud Application Programming
  Model (CAP) services. Covers CDS modeling, servi...
version: 1.0.0
tags:
- cap
- service
- development
- standardized
---


# Cap Service Development

End-to-end workflow for developing SAP Cloud Application Programming Model (CAP) services. Covers CDS modeling, service implementation, testing-agents, and deployment to SAP BTP.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** sap-cap

## Trigger Conditions

This workflow is activated when:

- New CAP service required
- OData/REST API for SAP needed
- Full-stack BTP application
- Fiori Elements on CAP

**Trigger Examples:**
- "Create a CAP service for customer management"
- "Build a Fiori app with CAP backend"
- "Deploy CAP service to BTP"
- "Implement custom handlers in CAP"

## Phases

### Phase 1: Data Modeling & Entity Definition
- **Goal**: Design the application data model using CDS entity definitions and aspects.
- **Agents**: `python-ai-specialist`
- **Skills**: modeling-cds, analyzing-code
- **Tools**: write_to_file
- **Actions**:
    - Create entity definitions and add aspects.

### Phase 2: Service Definition & Handler Implementation
- **Goal**: Implement service logic and event handlers for business logic.
- **Agents**: `python-ai-specialist`
- **Skills**: modeling-cds
- **Tools**: write_to_file
- **Actions**:
    - Create service definitions and implement event handlers.

### Phase 3: UI & Integration Testing
- **Goal**: Add UI annotations, create the Fiori app, and perform tests.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: developing-fiori-apps, testing-agents
- **Tools**: run_tests.py, fiori-tools-cli
- **Actions**:
    - Perform unit and integration testing-agents.
    - Add UI annotations and create Fiori app.

### Phase 4: BTP Configuration & Deployment
- **Goal**: Configure MTA and deploy the application to SAP BTP.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp, committing-releases
- **Tools**: mta-tool, cf-cli
- **Actions**:
    - Configure MTA and build/deploy.


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
