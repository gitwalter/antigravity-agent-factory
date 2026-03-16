---
description: GitHub Actions CI/CD pipeline setup and maintenance workflow. Covers
  workflow creation, test automation, linting, dep...
version: 1.0.0
tags:
- github
- actions
- ci
- standardized
---


# Github Actions Ci

GitHub Actions CI/CD pipeline setup and maintenance workflow. Covers workflow creation, test automation, linting, deployment automation, and pipeline logging-and-monitoring.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** ci-cd, github-actions

## Trigger Conditions

This workflow is activated when:

- New CI/CD pipeline needed
- GitHub Actions workflow to create or update
- Pipeline maintenance requested
- Deployment automation needed

**Trigger Examples:**
- "Set up GitHub Actions CI"
- "Create a deployment workflow"
- "Fix the CI pipeline"
- "Add a new job to GitHub Actions"

## Phases

### Phase 1: Workflow Design & Setup
- **Goal**: Define CI/CD stages and configure environment secrets.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: gh-cli
- **Actions**:
    - Define stages and set up repository secrets.

### Phase 2: Workflow Implementation
- **Goal**: Create YAML workflow files and add necessary jobs.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: write_to_file
- **Actions**:
    - Create `.github/workflows/*.yml` files.
    - Define jobs for build, test, and deploy.

### Phase 3: Trigger & Debugging
- **Goal**: Trigger the workflow and resolve any execution failures.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: debug-pipeline
- **Tools**: gh-run-view, gh-run-rerun
- **Actions**:
    - Trigger workflow and debug errors.

### Phase 4: Monitoring & Maintenance
- **Goal**: Set up logging-and-monitoring for pipeline health and perform maintenance.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring, github-actions-ci
- **Tools**: github-dashboard
- **Actions**:
    - Add logging-and-monitoring and document maintenance procedures.


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
