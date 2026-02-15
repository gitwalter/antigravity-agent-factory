# Antigravity Agent Factory: System Blueprint

> **Status**: Canonical Reference
> **Version**: 2.0.0
> **Purpose**: Master registry of all system components organized for task and purpose fulfillment.

This document maps the entire active ecosystem of the Antigravity Agent Factory. It details how Blueprints, Workflows, Teams, Skills, and Knowledge combine to execute complex tasks.

---

## 1. The Core Architecture (5-Layer Model)

The system operates on a hierarchical model ensuring every action is grounded in verified patterns.

| Layer | Component | Description |
|-------|-----------|-------------|
| **L0** | **Integrity** | Axioms (Love, Truth, Beauty) and Guardian protocols. |
| **L1** | **Purpose** | Mission statements, stakeholder definitions, and success criteria. |
| **L2** | **Principles** | Ethical boundaries, quality standards, and decision heuristics. |
| **L3** | **Methodology** | Operations (Agile/Kanban), Workflows, and Team structures. |
| **L4** | **Implementation** | Agents, Skills, Tools, Code, and Infrastructure. |

---

## 2. Agent Team Roster

Agents are specialized roles that can be staffed into teams.

### Core Orchestrators
- **`system-steward`**: Repository maintenance, health checks, and structural integrity.
- **`workflow-architect`**: Design and selection of operational workflows.
- **`integrity-guardian`**: Safety, alignment, and axiom enforcement.
- **`pm-sprint-master`**: Agile process management and sprint coordination.

### Domain Specialists
- **`ai-app-developer`**: AI-driven application development.
- **`python-backend-developer`**: Python/FastAPI/Django development.
- **`fullstack-ts-developer`**: TypeScript/React/Node.js development.
- **`sap-developer`**: SAP ecosystem (CAP, RAP, BTP) development.
- **`dotnet-architect` / `developer`**: .NET ecosystem development.
- **`ml-engineer` / `mlops-engineer`**: Machine learning model training and deployment.

### Support & Services
- **`git-specialist`**: Version control operations and release management.
- **`test-conductor`**: Testing strategies, execution, and validation.
- **`onboarding-architect`**: New project setup and team onboarding.
- **`knowledge-manager`**: Knowledge base curation and expansion.

---

## 3. Workflow Registry

Workflows define the "How-To" for specific objectives.

### Development Workflows
- **Feature Dev**: `feature-development`, `nextjs-feature-development`, `confluence-feature`
- **Backend**: `fastapi-api-development`, `dotnet-api-development`, `spring-microservice-development`
- **SAP**: `cap-service-development`, `rap-development`, `fiori-app-development`, `iflow-development`
- **AI/ML**: `llm-app-development`, `rag-pipeline-development`, `multi-agent-development`

### Operational Workflows
- **CI/CD**: `cicd-pipeline`, `github-actions-ci`, `jenkins-pipeline` (if avail)
- **Maintenance**: `repository-maintenance`, `backlog-refinement`, `security-audit`
- **Management**: `sprint-planning`, `sprint-closure`, `daily-standup`

---

## 4. Skill Catalog

Skills are modular capabilities injected into agents.

### Integration & Infrastructure
- **Cloud**: `azure-integration`, `aws-integration` (future), `btp-deployment`
- **Containers**: `docker-deployment`, `kubernetes-deployment`
- **Tools**: `git-operations`, `github-operations`, `filesystem-ops`

### AI & Data
- **LLM**: `agent-generation`, `prompt-optimization`, `rag-patterns`, `vector-db`
- **Data**: `data-pipeline`, `excel-processing`, `sql-generation`

### Domain Specific
- **SAP**: `cds-modeling`, `s4-process-guide`, `sap-integration`
- **Web**: `react-patterns`, `nextjs-development`, `fastapi-development`
- **Docs**: `documentation-generation`, `markdown-validation`

---

## 5. MCP Integration Network

Model Context Protocol (MCP) servers bridge the gap between AI and external systems.

| Category | Servers | Capability |
|----------|---------|------------|
| **Productivity** | `google-workspace` (Gmail, Calendar, Drive) | Manage scheduling, files, and comms. |
| **DevOps** | `github`, `azure-devops` | Repository and issue management. |
| **Data** | `excel-mcp`, `filesystem`, `brave-search` | Local and web data access. |
| **Enterprise** | `atlassian` (Jira/Confluence), `linear` | Project tracking and spec retrieval. |

---

## 6. How It All Connects

To fulfill a Task:

1.  **Select Workflow**: Choose the path (e.g., `feature-development`).
2.  **Staff Team**: Workflow defines the required agents (e.g., `workflow-architect` + `ai-app-developer`).
3.  **Inject Skills**: Agents receive relevant skills (e.g., `nextjs-development`, `git-operations`).
4.  **Connect MCPs**: System connects to required tools (e.g., `github` for PRs).
5.  **Execute & Verify**: Team iterates through the workflow phases until success criteria are met.

> **Note**: This blueprint is a living document. Run `repository-maintenance` to keep artifact lists synchronized.
