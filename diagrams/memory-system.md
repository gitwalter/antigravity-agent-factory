# Memory System Architecture

This document visualizes the user-validated learning system that enables the Factory to learn from experience while respecting user consent and layer immutability.

## Quick Reference

```mermaid
flowchart LR
    O[Observe] --> P[Propose] --> A{Approve?}
    A -->|Yes| S[Store]
    A -->|No| D[Discard]
```

## Memory System Overview

Complete architecture of the memory system:

```mermaid
flowchart TB
    subgraph Observation["Observation Layer"]
        AE["Agent Actions & Events"]
        OBS["Memory System Observer"]
        PAT["Pattern Detection"]
    end

    subgraph Processing["Processing Layer"]
        IND["Induction Engine"]
        GEN["Generalization"]
        CONF["Confidence Scoring"]
    end

    subgraph Validation["User Validation Layer"]
        PROP["Proposal Generation"]
        USER["User Review"]
        DEC{Decision}
    end

    subgraph Storage["Storage Layer"]
        SEM["Semantic Memory<br/>(Permanent)"]
        EPI["Episodic Memory<br/>(Session)"]
        REJ["Rejected<br/>(Permanent)"]
    end

    AE --> OBS --> PAT --> IND --> GEN --> CONF --> PROP --> USER --> DEC
    DEC -->|Approve| SEM
    DEC -->|Reject| REJ
    PAT --> EPI
```

## Memory Observation Flow

How the system observes and captures patterns:

```mermaid
sequenceDiagram
    participant A as Agent
    participant M as Memory System
    participant I as Induction Engine
    participant U as User

    A->>M: Perform action
    M->>M: Observe action
    M->>M: Check for significant pattern

    alt Significant Pattern Found
        M->>I: Send observation
        I->>I: Generalize pattern
        I->>I: Calculate confidence
        I->>M: Return proposal
        M->>U: Present proposal

        alt User Approves
            U->>M: Approve
            M->>M: Store in Semantic Memory
        else User Rejects
            U->>M: Reject
            M->>M: Store rejection (prevent re-proposal)
        end
    else Not Significant
        M->>M: Store in Episodic Memory (session only)
    end
```

## User Validation Loop

The core consent mechanism:

```mermaid
flowchart TB
    subgraph Proposal["Memory Proposal"]
        P1["Observation: What was seen"]
        P2["Generalization: Proposed pattern"]
        P3["Confidence: How certain"]
        P4["Context: When/where observed"]
    end

    subgraph UserReview["User Review"]
        R1["Review proposal content"]
        R2["Understand implications"]
        R3["Make decision"]
    end

    Proposal --> UserReview

    subgraph Decision["User Decision"]
        D1["APPROVE<br/>Store permanently"]
        D2["REJECT<br/>Never propose again"]
        D3["DEFER<br/>Ask later"]
        D4["MODIFY<br/>Adjust and approve"]
    end

    UserReview --> D1 & D2 & D3 & D4

    subgraph Outcome["Outcome"]
        O1["Semantic Memory<br/>User-approved knowledge"]
        O2["Rejected Memory<br/>Similarity checked"]
        O3["Pending Queue<br/>Re-propose later"]
    end

    D1 --> O1
    D2 --> O2
    D3 --> O3
    D4 --> O1
```

## Memory Types Relationship

How different memory types relate:

```mermaid
flowchart TB
    subgraph Types["Memory Types"]
        SEM["Semantic Memory<br/>Type: permanent<br/>Requires: user approval<br/>Content: validated knowledge"]
        EPI["Episodic Memory<br/>Type: session<br/>Requires: none<br/>Content: session observations"]
        PEN["Pending Memory<br/>Type: temporary<br/>Requires: user review<br/>Content: proposed patterns"]
        REJ["Rejected Memory<br/>Type: permanent<br/>Requires: none<br/>Content: rejected proposals"]
    end

    subgraph Transitions["State Transitions"]
        OBS["Observation"] --> EPI
        OBS --> PEN
        PEN -->|"approve"| SEM
        PEN -->|"reject"| REJ
    end

    subgraph Properties["Key Properties"]
        PROP1["Semantic: Only created via explicit approval"]
        PROP2["Episodic: Cleared at session end"]
        PROP3["Rejected: Used for similarity check (0.9 threshold)"]
    end
```

## Layer Protection Boundaries

Memory system respects 5-layer immutability:

```mermaid
flowchart TB
    subgraph Immutable["Protected Layers (Cannot Modify)"]
        L0["Layer 0: Axioms<br/>A0-A5 definitions"]
        L1["Layer 1: Purpose<br/>Mission, stakeholders"]
        L2["Layer 2: Principles<br/>Ethical boundaries"]
    end

    subgraph Mutable["Learnable Layers (Can Modify)"]
        L3["Layer 3: Methodology<br/>Workflow patterns"]
        L4["Layer 4: Technical<br/>Code patterns, preferences"]
    end

    subgraph Memory["Memory System"]
        MEM["Memory can only<br/>affect L3 and L4"]
    end

    MEM -->|"blocked"| Immutable
    MEM -->|"allowed"| Mutable

    subgraph Proofs["Lean 4 Theorems"]
        T1["memory_cannot_modify_layer0"]
        T2["memory_cannot_modify_layer1"]
        T3["memory_cannot_modify_layer2"]
    end

    Immutable -.-> Proofs
```

## Memory Collection Architecture

ChromaDB storage structure:

```mermaid
flowchart TB
    subgraph ChromaDB["ChromaDB Instance"]
        subgraph Collections["Collections"]
            C1["semantic_memories<br/>Permanent, user-approved"]
            C2["episodic_memories<br/>Session-based"]
            C3["pending_proposals<br/>Awaiting review"]
            C4["rejected_proposals<br/>Never re-propose"]
        end

        subgraph Metadata["Metadata per Entry"]
            M1["id: unique identifier"]
            M2["content: memory text"]
            M3["embedding: vector representation"]
            M4["timestamp: creation time"]
            M5["layer: affected layer (3 or 4)"]
            M6["confidence: 0.0-1.0"]
            M7["session_id: for episodic"]
        end
    end

    Collections --> Metadata
```

## Consent Proofs Visualization

Lean 4 theorems guaranteeing user consent:

```mermaid
flowchart TB
    subgraph Theorems["Consent Theorems"]
        T1["consent_always_maintained<br/>Semantic memories always require approval"]
        T2["only_approve_creates_semantic<br/>Only explicit approval creates permanent memories"]
        T3["pending_distinct_from_semantic<br/>Pending and semantic are distinct states"]
        T4["consent_preserved<br/>Consent invariant preserved by all transitions"]
    end

    subgraph Transitions["Memory Transitions"]
        TR1["Propose → Pending"]
        TR2["Approve → Semantic (with consent)"]
        TR3["Reject → Rejected (no semantic created)"]
    end

    subgraph Invariant["Consent Invariant"]
        INV["∀ m ∈ SemanticMemory:<br/>m.userApproved = true"]
    end

    Theorems --> Invariant
    Transitions --> Invariant
```

## Induction Engine Flow

How patterns are generalized:

```mermaid
flowchart TB
    subgraph Input["Observation Input"]
        OBS["Raw observation"]
        CTX["Context (agent, action, result)"]
    end

    subgraph Processing["Induction Processing"]
        SIM["Check similarity to existing"]

        subgraph Checks["Rejection Checks"]
            REJ_CHECK["Similar to rejected? (0.9 threshold)"]
            DUP_CHECK["Duplicate of existing?"]
        end

        GEN["Generalize pattern"]
        CONF["Calculate confidence"]
    end

    subgraph Scoring["Confidence Scoring"]
        S1["Explicit user feedback: 0.9"]
        S2["Repeated success: 0.7"]
        S3["Single observation: 0.3"]
        S4["Inferred pattern: 0.5"]
    end

    subgraph Output["Proposal Output"]
        PROP["Memory Proposal"]
        SKIP["Skip (too similar to rejected)"]
    end

    Input --> SIM
    SIM --> REJ_CHECK
    REJ_CHECK -->|">0.9"| SKIP
    REJ_CHECK -->|"<0.9"| DUP_CHECK
    DUP_CHECK -->|"duplicate"| SKIP
    DUP_CHECK -->|"new"| GEN --> CONF --> PROP

    Scoring -.-> CONF
```

## Memory Integration with Agents

How agents interact with memory:

```mermaid
sequenceDiagram
    participant A as Agent
    participant Q as Query Interface
    participant SEM as Semantic Memory
    participant EPI as Episodic Memory
    participant P as Proposal System

    Note over A,P: Agent Querying Memory
    A->>Q: Query for relevant context
    Q->>SEM: Search semantic (permanent)
    Q->>EPI: Search episodic (session)
    SEM-->>Q: User-approved patterns
    EPI-->>Q: Recent observations
    Q-->>A: Combined context

    Note over A,P: Agent Contributing to Memory
    A->>P: Complete action (observation)
    P->>P: Detect significant pattern
    P->>P: Generate proposal (if significant)
    P->>P: Queue for user review
```

## Session Lifecycle

Memory behavior across sessions:

```mermaid
flowchart TB
    subgraph Session1["Session 1"]
        S1_OBS["Observations made"]
        S1_EPI["Stored in episodic"]
        S1_PROP["Proposals generated"]
        S1_APP["User approves some"]
    end

    subgraph Transition["Session End"]
        T_EPI["Episodic cleared"]
        T_SEM["Semantic persists"]
        T_REJ["Rejected persists"]
    end

    subgraph Session2["Session 2"]
        S2_START["New session starts"]
        S2_SEM["Semantic available"]
        S2_EPI["Fresh episodic"]
    end

    Session1 --> Transition --> Session2

    S1_EPI -->|"cleared"| T_EPI
    S1_APP -->|"persists"| T_SEM
```

## Memory Query Flow

How agents query memory for context:

```mermaid
flowchart TB
    subgraph Query["Query Request"]
        Q1["Agent needs context"]
        Q2["Specify query type"]
        Q3["Provide search terms"]
    end

    subgraph Search["Search Process"]
        EMBED["Generate query embedding"]

        subgraph Sources["Search Sources"]
            SEM_S["Semantic Memory<br/>Permanent patterns"]
            EPI_S["Episodic Memory<br/>Recent observations"]
        end

        RANK["Rank by relevance"]
        FILTER["Filter by layer/context"]
    end

    subgraph Result["Query Result"]
        RES["Relevant memories"]
        CTX["Contextual information"]
        CONF["Confidence scores"]
    end

    Query --> EMBED --> Sources --> RANK --> FILTER --> Result
```

## Memory System State Diagram

Complete state machine for memory entries:

```mermaid
stateDiagram-v2
    [*] --> Observed: Action detected

    Observed --> Episodic: Not significant enough
    Observed --> Pending: Significant pattern

    Pending --> Semantic: User approves
    Pending --> Rejected: User rejects
    Pending --> Pending: User defers

    Semantic --> [*]: Permanent storage
    Rejected --> [*]: Permanent rejection
    Episodic --> [*]: Session ends (cleared)

    note right of Semantic
        Only state requiring
        explicit user consent
    end note

    note right of Rejected
        Used for similarity
        checking (0.9 threshold)
    end note
```

## Observation Categories

Types of observations and their default confidence:

```mermaid
flowchart TB
    subgraph Categories["Observation Categories"]
        C1["Explicit Feedback<br/>User directly states preference"]
        C2["Repeated Success<br/>Pattern works multiple times"]
        C3["Single Success<br/>Pattern worked once"]
        C4["Inferred Pattern<br/>Derived from behavior"]
        C5["Error Recovery<br/>What fixed an error"]
    end

    subgraph Confidence["Default Confidence"]
        CONF1["0.9 - Very High"]
        CONF2["0.7 - High"]
        CONF3["0.3 - Low"]
        CONF4["0.5 - Medium"]
        CONF5["0.6 - Medium-High"]
    end

    C1 --> CONF1
    C2 --> CONF2
    C3 --> CONF3
    C4 --> CONF4
    C5 --> CONF5
```

## Memory System Axiom Alignment

How memory system aligns with core axioms:

```mermaid
flowchart LR
    subgraph Axioms["Core Axioms"]
        A1["A1: Transparency"]
        A2["A2: User Primacy"]
        A4["A4: Non-Harm"]
    end

    subgraph Alignment["Memory System Alignment"]
        AL1["All proposals shown to user<br/>Nothing hidden"]
        AL2["User approves all permanent storage<br/>User can reject any proposal"]
        AL3["Cannot modify L0-L2<br/>Protects core values"]
    end

    A1 --> AL1
    A2 --> AL2
    A4 --> AL3
```
