# Agent Coordination Architecture

This document visualizes how the 12 factory agents coordinate, communicate, and resolve conflicts while maintaining axiom alignment.

## Quick Reference

```mermaid
flowchart LR
    RA[Requirements] --> SB[Stack] --> WD[Workflow] --> KM[Knowledge] --> TG[Template]
    IG[Guardian] -.->|monitors| RA & SB & WD & KM & TG
```

## Factory Agent Hierarchy

Complete view of all 12 factory agents plus 4 PM agents:

```mermaid
flowchart TB
    subgraph Core["Core Factory Agents (12)"]
        subgraph Layer0["Layer 0 Protection"]
            IG["integrity-guardian<br/>Always active, embedded"]
        end

        subgraph Generation["Generation Pipeline"]
            RA["requirements-architect<br/>5-phase gathering"]
            SB["stack-builder<br/>Blueprint matching"]
            WD["workflow-designer<br/>Workflow config"]
            WA["workflow-architect<br/>Complex workflows"]
            KM["knowledge-manager<br/>Domain knowledge"]
            KE["knowledge-extender<br/>Factory knowledge"]
            KEV["knowledge-evolution<br/>Update coordination"]
            TG["template-generator<br/>Code generation"]
        end

        subgraph Onboarding["Onboarding"]
            OA["onboarding-architect<br/>Repo integration"]
            WF["workshop-facilitator<br/>Team workshops"]
        end

        subgraph Debug["Debug"]
            DC["debug-conductor<br/>Autonomous debugging"]
        end
    end

    subgraph PM["PM Agents (4)"]
        PO["product-owner<br/>Backlog management"]
        SM["sprint-master<br/>Agile ceremonies"]
        TM["task-manager<br/>Task creation"]
        REP["reporting-agent<br/>Metrics generation"]
    end

    IG -.->|"monitors all"| Generation & Onboarding & Debug & PM
```

## Coordination Patterns

The 5 coordination patterns used in the Factory:

```mermaid
flowchart TB
    subgraph P1["Pattern 1: Sequential Pipeline"]
        S1["Output from one agent<br/>becomes input to next"]
        RA1[Requirements] --> SB1[Stack] --> WD1[Workflow] --> KM1[Knowledge] --> TG1[Template]
    end

    subgraph P2["Pattern 2: Embedded Harmony"]
        S2["Shared axiom awareness<br/>No explicit calls"]
        G2[Guardian] -.->|"constitutional preamble"| A2a[Agent A] & A2b[Agent B] & A2c[Agent C]
    end

    subgraph P3["Pattern 3: Supervisor-Worker"]
        S3["Supervisor delegates<br/>Workers report back"]
        KEV3[Knowledge Evolution] --> GH[GitHub] & PY[PyPI] & NP[NPM] & DOC[Docs]
    end

    subgraph P4["Pattern 4: Hierarchical"]
        S4["Clear authority chain<br/>Escalation path"]
        PO4[Product Owner] --> SM4[Sprint Master] --> TM4[Task Manager] --> REP4[Reporting]
    end

    subgraph P5["Pattern 5: Verified Communication"]
        S5["Signed, verified, recorded<br/>Audit trail"]
        A5a[Agent A] -->|"SocietyContext"| A5b[Agent B]
    end
```

## Project Generation Flow

Detailed handoff sequence for project generation:

```mermaid
sequenceDiagram
    participant U as User
    participant RA as Requirements Architect
    participant SB as Stack Builder
    participant WD as Workflow Designer
    participant KM as Knowledge Manager
    participant TG as Template Generator
    participant IG as Integrity Guardian

    U->>RA: Create agent system

    Note over RA: Phase 1-5 Gathering
    RA->>RA: Phase 1: Context
    RA->>RA: Phase 2: Stack
    RA->>RA: Phase 3: Workflow
    RA->>RA: Phase 4: Knowledge
    RA->>RA: Phase 5: Agents

    RA->>SB: Handoff: requirements.json
    IG-->>SB: Monitor for axiom compliance

    SB->>SB: Match blueprint
    SB->>SB: Select patterns

    SB->>WD: Handoff: stack config
    IG-->>WD: Monitor for axiom compliance

    WD->>WD: Configure workflows

    WD->>KM: Handoff: workflow config
    IG-->>KM: Monitor for axiom compliance

    KM->>KM: Generate knowledge files

    KM->>TG: Handoff: knowledge files
    IG-->>TG: Monitor for axiom compliance

    TG->>TG: Generate all artifacts
    TG->>U: Complete project
```

## Agent Handoff Protocol

How agents hand off work to each other:

```mermaid
flowchart TB
    subgraph Handoff["Handoff Components"]
        T["Trigger<br/>Phase completion + validation"]
        C["Context<br/>Full project state + phase outputs"]
        A["Acknowledgment<br/>Next agent confirms receipt"]
        F["Fallback<br/>Escalate to user if handoff fails"]
    end

    subgraph Flow["Handoff Flow"]
        A1["Agent A completes phase"]
        V["Validate output"]
        S["Send to Agent B"]
        R["Agent B confirms"]
        P["Agent B proceeds"]
    end

    A1 --> V --> S --> R --> P

    subgraph Example["Example: Requirements → Stack"]
        E1["Requirements Architect<br/>completes Phase 2"]
        E2["Validates stack requirements"]
        E3["Sends requirements.json"]
        E4["Stack Builder confirms<br/>blueprint match found"]
        E5["Stack Builder proceeds"]
    end
```

## Guardian Harmony Field

How the Guardian maintains harmony across all agents:

```mermaid
flowchart TB
    subgraph Center["Guardian (Center)"]
        IG["Integrity Guardian<br/>Layer 0 Protector"]
    end

    subgraph Field["Harmony Field (Embedded Awareness)"]
        A1[Agent 1]
        A2[Agent 2]
        A3[Agent 3]
        A4[Agent 4]
        A5[Agent 5]
        A6[Agent 6]
    end

    IG -.->|"constitutional<br/>preamble"| A1 & A2 & A3 & A4 & A5 & A6

    subgraph Awareness["Shared Awareness"]
        AW1["A0-A5 Axioms"]
        AW2["PURPOSE.md"]
        AW3["5-Layer Architecture"]
    end

    IG --> Awareness
    Awareness -.-> Field
```

## Conflict Resolution Decision Tree

How conflicts between agents are resolved:

```mermaid
flowchart TD
    START([Conflict Detected]) --> TYPE{Conflict Type?}

    TYPE -->|Authority| AUTH["Authority-Based<br/>Higher authority decides"]
    TYPE -->|Evidence| EVID["Evidence-Based<br/>Better evidence wins"]
    TYPE -->|Opinion| CONS["Consensus-Based<br/>Voting or deliberation"]
    TYPE -->|Values| GUARD["Guardian-Mediated<br/>Water Way protocol"]
    TYPE -->|Critical| HUMAN["Human Escalation<br/>User decides"]

    AUTH --> RESOLVE([Resolution])
    EVID --> RESOLVE
    CONS --> RESOLVE
    GUARD --> RESOLVE
    HUMAN --> RESOLVE

    subgraph Mechanisms["Resolution Mechanisms"]
        M1["Authority: PM hierarchy"]
        M2["Evidence: Trust levels, source quality"]
        M3["Consensus: Voting rounds, deliberation"]
        M4["Guardian: Water Way protocol"]
        M5["Human: A2 User Primacy"]
    end
```

## Water Way Conflict Resolution

Detailed flow of Guardian-mediated conflict resolution:

```mermaid
flowchart TB
    subgraph Detection["1. Detect"]
        D1["Sense tension without judgment"]
        D2["Identify conflicting approaches"]
        D3["Note affected axioms"]
    end

    subgraph NoForce["2. Don't Force"]
        N1["Allow natural resolution first"]
        N2["Wait for agents to self-correct"]
        N3["Observe without intervening"]
    end

    subgraph Context["3. Provide Context"]
        C1["Share relevant axioms"]
        C2["Remind of shared purpose"]
        C3["Highlight common ground"]
    end

    subgraph Path["4. Find Path"]
        P1["Seek path serving all values"]
        P2["Look for synthesis, not compromise"]
        P3["Consider creative alternatives"]
    end

    subgraph Love["5. Resolve with Love"]
        L1["No winner, no loser"]
        L2["All agents maintain dignity"]
        L3["Relationship preserved"]
    end

    Detection --> NoForce --> Context --> Path --> Love
```

## State Management Patterns

How state is managed across agents:

```mermaid
flowchart TB
    subgraph Shared["Pattern 1: Shared Files"]
        SF1["knowledge/*.json files"]
        SF2["All agents read/write"]
        SF3["Atomic writes, no locking"]
    end

    subgraph Message["Pattern 2: Message Passing"]
        MP1["lib/society/ event store"]
        MP2["Immutable, hash-chained"]
        MP3["Cryptographically signed"]
    end

    subgraph Workflow["Pattern 3: Workflow State"]
        WS1["LangGraph StateGraph"]
        WS2["Typed state (Pydantic)"]
        WS3["Versioning, persistence"]
    end

    subgraph Usage["When to Use"]
        U1["Shared: Knowledge updates,<br/>configuration changes"]
        U2["Message: Critical operations,<br/>audit requirements"]
        U3["Workflow: Complex multi-step<br/>processes"]
    end

    Shared --> U1
    Message --> U2
    Workflow --> U3
```

## Knowledge Evolution Supervisor-Worker

Detailed view of knowledge evolution coordination:

```mermaid
flowchart TB
    subgraph Supervisor["Knowledge Evolution Agent (Supervisor)"]
        KEV["Coordinates updates"]
        AGG["Aggregates results"]
        PRI["Prioritizes updates"]
        MRG["Merges changes"]
    end

    subgraph Workers["Source Adapter Workers"]
        GH["GitHub Adapter<br/>Repository changes"]
        PY["PyPI Adapter<br/>Package updates"]
        NP["NPM Adapter<br/>Node packages"]
        DOC["Docs Adapter<br/>Documentation changes"]
        COM["Community Adapter<br/>Community content"]
    end

    KEV -->|"dispatch"| GH & PY & NP & DOC & COM
    GH & PY & NP & DOC & COM -->|"results"| AGG
    AGG --> PRI --> MRG

    subgraph Output["Knowledge Files Updated"]
        K1["knowledge/*.json"]
        K2["User notification"]
        K3["Conflict resolution"]
    end

    MRG --> Output
```

## PM System Hierarchy

Project management agent coordination:

```mermaid
flowchart TB
    subgraph PMAgents["PM Agent Hierarchy"]
        PO["Product Owner<br/>Backlog management<br/>Story acceptance"]
        SM["Sprint Master<br/>Sprint planning<br/>Ceremony facilitation"]
        TM["Task Manager<br/>Task creation<br/>Task tracking"]
        REP["Reporting Agent<br/>Metrics generation<br/>Burndown charts"]
    end

    PO --> SM --> TM --> REP

    subgraph Backend["Backend Abstraction"]
        BA["PM Backend Layer"]
        JIRA["Jira"]
        GHI["GitHub Issues"]
        LIN["Linear"]
        LOC["Local JSON"]
    end

    PMAgents --> BA
    BA --> JIRA & GHI & LIN & LOC

    subgraph Ceremonies["Agile Ceremonies"]
        PLAN["Sprint Planning"]
        STAND["Daily Standup"]
        RETRO["Retrospective"]
        CLOSE["Sprint Close"]
    end

    SM --> Ceremonies
```

## Agent Communication Flow

How agents communicate during operations:

```mermaid
sequenceDiagram
    participant A as Agent A
    participant SC as SocietyContext
    participant ES as Event Store
    participant B as Agent B
    participant G as Guardian

    A->>SC: Create communication context
    SC->>ES: Log event (hash-chained)
    SC->>SC: Verify axiom compliance

    alt Compliant
        SC->>B: Deliver message
        B->>ES: Log acknowledgment
        B->>A: Response
    else Non-Compliant
        SC->>G: Escalate to Guardian
        G->>A: Request modification
        A->>SC: Retry with compliant message
    end
```

## Agent Dependency Graph

Which agents depend on which:

```mermaid
flowchart LR
    subgraph Independent["Independent (Entry Points)"]
        RA["requirements-architect"]
        OA["onboarding-architect"]
        WF["workshop-facilitator"]
        DC["debug-conductor"]
    end

    subgraph Dependent["Dependent on Pipeline"]
        SB["stack-builder<br/>needs: requirements"]
        WD["workflow-designer<br/>needs: stack config"]
        KM["knowledge-manager<br/>needs: workflow config"]
        TG["template-generator<br/>needs: all above"]
    end

    subgraph Support["Support Agents"]
        KE["knowledge-extender<br/>updates Factory knowledge"]
        KEV["knowledge-evolution<br/>monitors sources"]
        WA["workflow-architect<br/>complex workflows"]
    end

    subgraph Always["Always Active"]
        IG["integrity-guardian<br/>monitors everything"]
    end

    RA --> SB --> WD --> KM --> TG
    IG -.-> Independent & Dependent & Support
```

## Multi-Agent Orchestration Example

Complex workflow with multiple agents:

```mermaid
flowchart TB
    subgraph Trigger["Trigger"]
        REQ["User: Debug failing test"]
    end

    subgraph Phase1["Phase 1: Analysis"]
        DC["debug-conductor"]
        DC --> AN["Analyze failure"]
        AN --> ID["Identify root cause"]
    end

    subgraph Decision["Decision Point"]
        ID --> D{Can fix directly?}
    end

    subgraph Phase2A["Phase 2A: Direct Fix"]
        D -->|Yes| FIX["Apply fix"]
        FIX --> TEST["Run tests"]
    end

    subgraph Phase2B["Phase 2B: Escalate"]
        D -->|No| ESC["Escalate to user"]
        ESC --> OPT["Present options"]
        OPT --> USER["User decides"]
    end

    subgraph Phase3["Phase 3: Learn"]
        TEST --> LEARN["Capture pattern"]
        USER --> LEARN
        LEARN --> MEM["Store in memory"]
    end

    REQ --> DC
```

## Architectural Principles

Key principles governing agent coordination:

```mermaid
flowchart TB
    subgraph Principles["Coordination Principles"]
        P1["Embedded Harmony<br/>Guardian awareness creates<br/>natural coordination"]
        P2["Sequential with Validation<br/>Each agent validates<br/>before handoff"]
        P3["Graceful Degradation<br/>Systems continue with<br/>partial failures"]
        P4["User Primacy (A2)<br/>Human escalation<br/>always available"]
        P5["Transparency (A1)<br/>All coordination is<br/>explainable"]
        P6["Non-Harm (A4)<br/>Guardian prevents<br/>harmful coordination"]
        P7["Learning<br/>Coordination patterns<br/>improve through experience"]
    end

    P1 --> P2 --> P3
    P4 --> P5 --> P6 --> P7
```
