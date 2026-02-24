# System Architecture: Antigravity Agent Ecosystem

This document serves as the **High-Fidelity Source of Truth** for the Antigravity Agent Ecosystem. It follows the C4 model (Context, Containers, Components) to illustrate the structural relationships, data flows, and execution boundaries.

## 1. System Context Diagram (L1)
The global view of how the Antigravity Factory interacts with users and external entities.

```mermaid
graph TD
    User["Developer/Analyst"] -->|Directs| Factory["Antigravity Agent Factory"]
    Factory -->|Integrated Documentation| Wiki["DeepWiki / GitHub"]
    Factory -->|Task Management| Plane["Plane PMS (Docker Stack)"]
    Factory -->|Knowledge Base| Qdrant["Qdrant RAG (Vector Data)"]
    Factory -->|External Data| Orbit["External Orbit (Financial/Eco/News)"]

    subgraph Data_Sources ["External Data Orbit"]
        WBank["World Bank API"]
        YFin["Yahoo Finance"]
        NewsAPI["Market News APIs"]
    end

    Orbit --> Data_Sources
```

## 2. Container Diagram (L2)
Visualizes the execution boundaries and high-level technical blocks.

```mermaid
graph TD
    subgraph Client_Env ["Local Environment"]
        Conda["Conda: cursor-factory (Python 3.12)"]
        VSCode["VS Code / Agentic UI"]
    end

    subgraph Factory_Core ["Factory Containers / Processes"]
        MSO["Master System Orchestrator (LangGraph)"]

        subgraph Registries ["Unified Registry Layer (JSON/MD)"]
            AS["agent-staffing"]
            WC["workflow-catalog"]
            OE["orchestration-engine"]
        end

        subgraph Specialty_Squads ["Agent Specialist Squads"]
            Engineers["PAIS / SYARCH / DNCS"]
            Quality["WQSS / Integrity Guardian"]
            Knowledge["KNOPS / KM / KEV"]
        end
    end

    subgraph Service_Containers ["Infrastructure Services (Docker)"]
        subgraph Plane_Stack ["Plane PMS"]
            P_API["plane-api (Django)"]
            P_DB["plane-db (Postgres)"]
            P_Worker["plane-worker (Redis)"]
        end

        subgraph Retrieval_Stack ["RAG Infrastructure"]
            Q_CORE["Qdrant Vector DB"]
            P_STORE["Parent Doc Store (Disk/RAM)"]
        end
    end

    VSCode -->|Invoke| Conda
    Conda -->|Execute| MSO
    MSO -->|Consult| Registries
    MSO -->|Delegate| Specialty_Squads

    %% Execution Paths
    Specialty_Squads -->|Docker Exec / ORM| P_API
    Specialty_Squads -->|ParentDocumentRetriever| Retrieval_Stack
```

## 3. Component & Sequence: Core Execution Flow (L3)
How a specialist retrieves knowledge and updates the PMS.

```mermaid
sequenceDiagram
    participant S as Specialist (e.g., PAIS)
    participant R as RAG (OptimizedRAG)
    participant Q as Qdrant (Child Vectors)
    participant P as Plane (Docker-Django)

    S->>R: Invoke search_ebook_library("auth patterns")
    R->>Q: Query child vectors (Distance: Cosine)
    Q-->>R: Return top child matches
    R->>R: Match children to Parent IDs
    R->>R: Hydrate context from Parent Store (RAM)
    R-->>S: Return high-context narrative chunks

    S->>S: Synthesize Implementation Plan

    S->>P: run_pms_command("update --id AGENT-23 --state Done")
    P->>P: Base64 Decode & Execute Django Shell
    P-->>S: Result: Updated Issue: AGENT-23
```

## 4. Hierarchical Specialist Definition
The ecosystem utilizes 16 distinct agent roles governed by the **Integrity Guardian**.

| Layer | Lead Agent | Primary Responsibility |
| :--- | :--- | :--- |
| **L0: Protection** | `integrity-guardian` | Verifies axiom alignment (Flow, Nudge, Pause, Block, Protect) |
| **L1: Strategy** | `requirements-architect` | 5-phase requirements gathering and context building |
| **L2: Design** | `syarch` / `stack-builder` | Blueprint matching and system-context mapping |
| **L3: Engineering** | `pais` / `dncs` / `fsws` | High-fidelity implementation and code generation |
| **L4: Knowledge** | `knops` / `km` / `ke` | RAG ingestion, TOC extraction, and pattern discovery |
| **L5: Quality** | `wqss` | 5-phase quality gate validation and verification |

## 5. System Audit Status (Feb 2026)
- **RAG Latency**: Optimized via FastEmbed (ONNX) and INT8 Quantization.
- **PMS Reliability**: Secured via Base64-encoded shell injection.
- **Data Integrity**: Parent-Child retrieval prevents context fragmentation.
