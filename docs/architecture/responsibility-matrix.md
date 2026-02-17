# Agent Responsibility Matrix

This document defines the specialized roles and responsibilities of the agents within the Antigravity Agent Factory. It ensures clear domain boundaries and optimizes team staffing for complex tasks.

| Specialist Agent | Tier | Primary Specialty | Key Absorbed Roles | Mission-Critical Tools |
| :--- | :--- | :--- | :--- | :--- |
| **`python-ai-specialist`** | Authoritative | AI, Python, RAG, MLOps | `RAG Engineer`, `AI Security Specialist`, `Python Architect` | `python`, `langsmith`, `Qdrant`, `Pydantic` |
| **`knowledge-operations-specialist`** | Routing | Knowledge Mgmt, Discovery | `Knowledge Manager`, `Context Curator` | `Memory MCP`, `Tavily`, `Brave Search`, `Fetch` |
| **`project-operations-specialist`** | Chain | Delivery, Repositories | `Project Manager`, `Release Lead` | `gh` (Local CLI), `git`, `Excel`, `GitHub MCP` |
| **`system-architecture-specialist`** | Chain | Design, Infrastructure | `System Architect`, `Blueprint Designer` | `Mermaid`, `Markdown`, `Dependency Graphs` |
| **`executive-operations-specialist`**| Orchestration| Life Mgmt, Scheduling | `Personal Assistant`, `Comms Lead` | `Gmail`, `Calendar`, `Google Drive` |
| **`workflow-quality-specialist`** | Eval-Opt | Procedures, Accuracy | `Quality Guard`, `Validation Expert` | `Sequential Thinking`, `Custom Validators` |
| **`sap-systems-specialist`** | Parallel | SAP Ecosystem | `ABAP Dev`, `BTP Architect`, `CAP Lead` | `CDS`, `Fiori`, `SAP BTP`, `iFlow` |
| **`full-stack-web-specialist`** | Parallel | Modern Web Apps | `Frontend Lead`, `UI/UX Specialist` | `Next.js`, `React`, `Tailwind`, `TypeScript` |
| **`dotnet-cloud-specialist`** | Parallel | .NET / Azure | `Azure Architect`, `C# Lead` | `ASP.NET Core`, `Entity Framework`, `Azure CLI` |
| **`java-systems-specialist`** | Parallel | Enterprise Java | `Java Lead`, `Spring Boot Specialist` | `Maven`, `Gradle`, `Testcontainers` |

## RAG & Memory Governance
- **Retrieval Authority**: `python-ai-specialist` (Managing the Qdrant vector store and RAG pipelines).
- **Discovery Authority**: `knowledge-operations-specialist` (Managing the Memory MCP and Knowledge Items).
- **Quality Oversight**: `workflow-quality-specialist` (Verifying citations and output grounding).
