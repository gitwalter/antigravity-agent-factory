# Rule: Workflow Execution

## Context
Rules for creating, extending, and executing workflows in `.agent/workflows/`.

## Requirements
- **Schema Adherence**: MUST follow `schemas/workflow.schema.json`.
- **Workflow Primacy**: All major system operations MUST be orchestrated by a designated workflow.
- **Phased Execution**:
    - Break workflows into logical, verifiable phases.
    - Define clear entry and exit criteria for each phase.
- **Automation (Turbo)**:
    - Use `// turbo` for safe, repetitive commands.
    - Use `// turbo-all` ONLY for highly standardized, verified automation paths.
- **Complex Logic**: For workflows with >3 dependent steps, use the `sequential-thinking` MCP to validate the execution path.

## Execution Standards
- **Supervisor Role**: Every workflow MUST have a designated Supervisor agent (e.g., MSO).
- **Quality Gates**: Implement quality gates between phases to prevent error propagation.
- **Recovery**: Define fallback procedures for phase failures.
