# Antigravity SDLC Usage Guide

This guide describes the 7 phases of the Automated Software Development Life Cycle (SDLC) used in the Antigravity Agent Factory. Every phase is enforced by a specific workflow and requires a formal "Phase Gate" artifact before proceeding.

**Crucially, this 7-Phase Meta-Orchestration is completely Stack-Agnostic.** The factory seamlessly adapts its execution context—whether you are building a Python AI Agent, a Java Spring Boot Microservice, a Next.js Frontend, or an SAP S/4HANA extension.

---

## The Axiomatic Foundation
The SDLC is grounded in the **5-Layer Deductive-Inductive Architecture**. Every line of code or documentation produced is checked against **Axiom 0 (Love, Truth, Beauty)** via the **Integrity Guardian**.

> **"No Code without a Gate. No Release without a Note."**

---

## SDLC Phase Overview (Agnostic Meta-Orchestration)

The factory orchestrator (`/sdlc-meta-orchestrator`) manages transitions between these 7 phases regardless of the target programming language.

| Phase | Goal | Primary Pipeline | Gate Artifact |
| :--- | :--- | :--- | :--- |
| **P1: Ideation** | Transform vague requests into formal, approvable briefs. | `/brief-prototype` | `knowledge/prototype-brief.md` |
| **P2: Requirements** | Transform briefs into structured PRDs and NFRs. | `/write-prd` | `knowledge/prd.md` |
| **P3: Architecture** | Design robust, scalable, and cost-effective systems. | `/ai-system-design` | `knowledge/ai-design.md` |
| **P4: Build** | Safe, axiomatic implementation with automated walkthroughs. | `/feature-development` (or Stack-Specific) | `knowledge/walkthrough.md` |
| **P5: Test & Eval** | Verification against requirements via rigorous evaluation. | `/quality-gate` (Adapts to Context) | `knowledge/eval-report.md` |
| **P6: Deploy** | Coordinate deployment, versioning, and formal release. | `/release-management` | `knowledge/release-notes.md` |
| **P7: Monitor** | Track production health and feed insights back to P1. | `/monitor`, `/incident-response` | `knowledge/monitor-report.md` |

---

## Workflow Interaction Patterns

Working with the Antigravity system involves a specific "Call-and-Response" pattern. Each workflow is designed to be highly interactive, guiding you through the axiomatic verification steps.

### IDE Interaction (Slash Commands)
- **Direct Trigger**: Type `@[/workflow-name]` in the developer prompt.
- **Context Awareness**: The agent reads your open files, Memory MCP graph, and active stack configurations to "prime" the workflow.
- **Verification Gates**: Agents will often pause and ask for your approval using the `notify_user` system before making destructive changes.

### CLI Interaction (Automated)
Many workflows can be triggered or inspected via the CLI for CI/CD or batch operations:
```powershell
# List all available workflows
conda run -p D:\Anaconda\envs\cursor-factory python cli/factory_cli.py list-workflows

# Execute a specific workflow
conda run -p D:\Anaconda\envs\cursor-factory python cli/factory_cli.py run-workflow feature-development --project AGENT-123
```

---

## Phase Deep Dives & Multi-Stack Dynamics

### P1: Ideation (The Spark)
*   **Agnostic Nature**: Business ideas and problem statements are language-independent.
*   **Workflow**: `@[/brainstorm]`, `@[/cluster]`, `@[/brief-prototype]`
*   **Gate Artifact**: `knowledge/prototype-brief.md`

### P2: Requirements (The Blueprint)
*   **Agnostic Nature**: Functional and Non-Functional Requirements dictate the *what*, not the *how*.
*   **Workflow**: `@[/write-prd]`, `@[/elicit-nfr]`, `@[/review-requirements]`
*   **Gate Artifact**: `knowledge/prd.md`

### P3: Architecture (The Skeleton)
*   **Stack-Aware Design**: This is where stack decisions are solidified. The Multi-Agent Debate pattern determines if a Next.js or an SAP UI5 interface is better suited for the PRD.
*   **Workflow**: `@[/ai-system-design]`
*   **Gate Artifact**: `knowledge/ai-design.md`

### P4: Build (The Flesh)
*   **Stack Adaptation**: Execution branches dramatically here. The factory will invoke the appropriate stack-specific workflow based on P3 decisions.
    *   *Python/AI*: Uses `@[/fastapi-api-development]` or `@[/agent-development]`
    *   *Java*: Uses `@[/spring-microservice-development]`
    *   *SAP*: Uses `@[/cap-service-development]` or `@[/rap-development]`
    *   *Cloud/IaC*: Uses `@[/azure-deployment]` or Go-based microservice patterns.
    *   *Mobile (Native)*: Dedicated workflows for **iOS (Swift)** and **Android (Kotlin)**.
    *   *Mobile (Cross-Platform)*: Shared codebase workflows for **Flutter** and **React Native**.
    *   *Data*: Uses `@[/fetch-external-data]` and dbt-based analytics pipelines.
*   **Workflow**: `@[/feature-development]` (Base) -> Routes to Stack Workflows
*   **Gate Artifact**: `knowledge/walkthrough.md`

### P5: Test & Eval (The Mirror)
*   **Stack Adaptation**: The orchestrator triggers tests using the correct runner for the ecosystem environment (e.g., `pytest` for Python, `mvn test` for Java, `npm run test` for TS/React, `abaplint` for SAP).
*   **Workflow**: `@[/agent-testing]`, `@[/quality-gate]`
*   **Gate Artifact**: `knowledge/eval-report.md`

### P6: Deploy (The Birth)
*   **Workflow**: `@[/release-management]`, `@[/cicd-pipeline]`
*   **Gate Artifact**: `knowledge/release-notes.md`

### P7: Monitor (The Pulse)
*   **Workflow**: `@[/monitor]`, `@[/incident-response]`
*   **Gate Artifact**: `knowledge/monitor-report.md`

---

## Multi-Stack Context & Memory

The factory utilizes the **Memory MCP** to persist knowledge of the current stack. Before initiating a build, the agent queries the Memory graph for an `SDLC_Stack` entity (e.g., `Python_FastAPI`, `DotNet_CSharp`).

If no explicit stack configuration is found, the system will prompt the user to define it before executing P4 (Build) workflows.

---

## Best Practices
- **Atomic Commits**: Link every commit to a Phase Gate or Plane issue.
- **Evidence-First**: Always include screenshots, terminal logs, or recordings in your `walkthrough.md`.
- **Axiomatic Alignment**: If a requirement feels "wrong," trigger a `@[/review-requirements]` session immediately.
- **Context Initialization**: Ensure the Memory MCP knows what stack you are targeting before starting P4 coding workflows.

## Related Resources
- [Architecture Overview](../architecture/architecture-overview.md) - System context and C4 diagrams.
- [Workflow Patterns Catalog](../reference/workflow-patterns.md) - Full list of stack-specific and agnostic workflow endpoints.
- [Axiomatic Principles](../architecture/axiomatic-principles.md) - Philosophy and L0 logic.

---
*Last Updated: March 2026*
