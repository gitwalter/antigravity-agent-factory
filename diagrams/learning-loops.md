# Learning Loops Architecture

This document visualizes the inductive learning system that enables the Factory to learn from experience and improve over time while respecting user consent.

## Quick Reference

```mermaid
flowchart LR
    O[Observe] --> G[Generalize] --> V[Validate] --> I[Integrate]
```

## Complete Learning Loop Architecture

End-to-end learning flow:

```mermaid
flowchart TB
    subgraph Observation["1. Observation Layer"]
        AE["Agent Actions & Events"]
        OBS["Observer"]
        PAT["Pattern Detector"]
    end

    subgraph Generalization["2. Generalization Layer"]
        IND["Induction Engine"]
        GEN["Pattern Generalizer"]
        CONF["Confidence Scorer"]
    end

    subgraph Validation["3. Validation Layer"]
        AX["Axiom Alignment Check"]
        USER["User Approval"]
        REJ["Rejection Check"]
    end

    subgraph Integration["4. Integration Layer"]
        MEM["Memory Storage"]
        KNOW["Knowledge Update"]
        PATT["Pattern Library"]
    end

    Observation --> Generalization --> Validation --> Integration
    Integration -.->|"Improves"| Observation
```

## Induction Engine Flow

How patterns are induced from observations:

```mermaid
flowchart TB
    subgraph Input["Observation Input"]
        O1["Raw observation"]
        O2["Context metadata"]
        O3["Success/failure outcome"]
    end

    subgraph Analysis["Pattern Analysis"]
        A1["Extract key features"]
        A2["Identify variables"]
        A3["Detect structure"]
    end

    subgraph Generalization["Generalization"]
        G1["Abstract specific values"]
        G2["Create template pattern"]
        G3["Define applicability conditions"]
    end

    subgraph Scoring["Confidence Scoring"]
        subgraph Types["Observation Types"]
            T1["Explicit feedback: 0.9"]
            T2["Repeated success: 0.7"]
            T3["Error recovery: 0.6"]
            T4["Inferred: 0.5"]
            T5["Single observation: 0.3"]
        end
    end

    subgraph Output["Pattern Output"]
        P["Proposed Pattern"]
        C["Confidence Score"]
        M["Metadata"]
    end

    Input --> Analysis --> Generalization --> Scoring --> Output
```

## Proposal Lifecycle

Complete lifecycle of a learning proposal:

```mermaid
stateDiagram-v2
    [*] --> Observed: Pattern detected

    Observed --> Pending: Significant (confidence > threshold)
    Observed --> Discarded: Not significant

    Pending --> Reviewed: User views proposal

    Reviewed --> Approved: User accepts
    Reviewed --> Rejected: User rejects
    Reviewed --> Modified: User edits
    Reviewed --> Deferred: User postpones

    Approved --> Integrated: Stored in memory
    Modified --> Integrated: Edited version stored
    Rejected --> Blocked: Similar patterns filtered
    Deferred --> Pending: Re-queue for later

    Integrated --> [*]: Learning complete
    Blocked --> [*]: Pattern blocked
    Discarded --> [*]: Not learned
```

## Rejection Similarity Checking

Preventing re-proposal of rejected patterns:

```mermaid
flowchart TB
    subgraph NewProposal["New Pattern Proposal"]
        NP["Proposed pattern"]
        NE["Pattern embedding"]
    end

    subgraph RejectedDB["Rejected Patterns DB"]
        R1["Rejected pattern 1"]
        R2["Rejected pattern 2"]
        R3["Rejected pattern 3"]
    end

    subgraph Check["Similarity Check"]
        SIM["Calculate similarity"]
        THRESH["Threshold: 0.9"]

        DEC{Similarity > 0.9?}
    end

    subgraph Outcome["Outcome"]
        SKIP["SKIP: Too similar to rejected"]
        PROCEED["PROCEED: New enough to propose"]
    end

    NewProposal --> Check
    RejectedDB --> Check
    Check --> DEC
    DEC -->|"Yes"| SKIP
    DEC -->|"No"| PROCEED
```

## Pattern Feedback Skill

How patterns feed back to improve the system:

```mermaid
flowchart TB
    subgraph Input["L4 Observations"]
        O1["Technical patterns"]
        O2["Workflow patterns"]
        O3["Error patterns"]
    end

    subgraph Validation["L0 Validation"]
        V1["Check axiom alignment"]
        V2["Verify non-harm"]
        V3["Ensure consistency"]
    end

    subgraph Decision["Integration Decision"]
        DEC{Valid pattern?}
        APPROVE["Integrate into L3-L4"]
        REJECT["Discard with reason"]
    end

    subgraph Output["Pattern Library Update"]
        PL["patterns/*.json"]
        KN["knowledge/*.json"]
    end

    Input --> Validation --> DEC
    DEC -->|"Valid"| APPROVE --> Output
    DEC -->|"Invalid"| REJECT
```

## Workflow Learning Hooks

Learning integrated into workflow execution:

```mermaid
sequenceDiagram
    participant W as Workflow
    participant L as Learning System
    participant M as Memory
    participant U as User

    W->>W: Execute phase

    alt Phase Succeeds
        W->>L: on_success hook
        L->>L: Capture success pattern
        L->>M: Store as candidate
    else Phase Fails
        W->>L: on_failure hook
        L->>L: Capture failure context
        L->>M: Store for analysis
    end

    W->>W: Continue workflow...

    Note over L,M: After workflow completes
    L->>L: Analyze patterns
    L->>U: Propose significant learnings

    alt User Approves
        U->>L: Accept pattern
        L->>M: Store in semantic memory
    else User Rejects
        U->>L: Reject pattern
        L->>M: Store rejection
    end
```

## Learning from Debug Sessions

How debugging improves the system:

```mermaid
flowchart TB
    subgraph Debug["Debug Session"]
        D1["Error detected"]
        D2["Root cause identified"]
        D3["Fix applied"]
        D4["Fix verified"]
    end

    subgraph Capture["Pattern Capture"]
        C1["Error signature"]
        C2["Root cause pattern"]
        C3["Fix template"]
        C4["Verification steps"]
    end

    subgraph Learning["Learning"]
        L1["Generalize error pattern"]
        L2["Create fix template"]
        L3["Calculate confidence"]
    end

    subgraph Future["Future Application"]
        F1["Proactive error detection"]
        F2["Suggested fixes"]
        F3["Auto-remediation (if approved)"]
    end

    Debug --> Capture --> Learning --> Future
```

## Confidence Accumulation

How confidence grows over time:

```mermaid
flowchart TB
    subgraph Initial["Initial Observation"]
        I1["First occurrence"]
        I2["Confidence: 0.3"]
    end

    subgraph Accumulation["Confidence Accumulation"]
        A1["Second success: +0.2"]
        A2["Third success: +0.15"]
        A3["User confirms: +0.25"]
        A4["Repeated across projects: +0.1"]
    end

    subgraph Final["Final Confidence"]
        F1["Combined confidence"]
        F2["Threshold check"]

        DEC{> 0.7?}
        PROPOSE["Auto-propose"]
        WAIT["Wait for more evidence"]
    end

    Initial --> Accumulation --> Final
    DEC -->|"Yes"| PROPOSE
    DEC -->|"No"| WAIT
```

## Cross-Project Learning

Learning patterns across projects:

```mermaid
flowchart TB
    subgraph Projects["Individual Projects"]
        P1["Project A patterns"]
        P2["Project B patterns"]
        P3["Project C patterns"]
    end

    subgraph Analysis["Cross-Project Analysis"]
        A1["Find common patterns"]
        A2["Identify stack-specific patterns"]
        A3["Detect universal patterns"]
    end

    subgraph Promotion["Pattern Promotion"]
        PR1["Project-specific → stays local"]
        PR2["Stack-specific → stack knowledge"]
        PR3["Universal → core patterns"]
    end

    subgraph Storage["Storage Location"]
        S1["Project memory"]
        S2["knowledge/*.json"]
        S3["patterns/*.json"]
    end

    Projects --> Analysis --> Promotion --> Storage
```

## Learning Types

Different types of learning in the system:

```mermaid
flowchart TB
    subgraph Types["Learning Types"]
        subgraph Code["Code Patterns"]
            C1["Successful implementations"]
            C2["Bug fixes"]
            C3["Optimizations"]
        end

        subgraph Workflow["Workflow Patterns"]
            W1["Effective sequences"]
            W2["Failure recovery"]
            W3["Escalation triggers"]
        end

        subgraph User["User Preferences"]
            U1["Style preferences"]
            U2["Tool choices"]
            U3["Communication patterns"]
        end

        subgraph Domain["Domain Knowledge"]
            D1["Business rules"]
            D2["API patterns"]
            D3["Integration patterns"]
        end
    end
```

## Axiom Alignment Validation

Ensuring learned patterns align with axioms:

```mermaid
flowchart TD
    PATTERN([Proposed Pattern]) --> CHECK["Axiom Alignment Check"]

    CHECK --> A1{A1: Transparent?}
    A1 -->|"No"| REJECT1["Reject: Not explainable"]
    A1 -->|"Yes"| A2{A2: User-centric?}

    A2 -->|"No"| REJECT2["Reject: Against user interest"]
    A2 -->|"Yes"| A3{A3: Derivable?}

    A3 -->|"No"| REJECT3["Reject: Can't trace to axioms"]
    A3 -->|"Yes"| A4{A4: Non-harmful?}

    A4 -->|"No"| REJECT4["Reject: Could cause harm"]
    A4 -->|"Yes"| A5{A5: Consistent?}

    A5 -->|"No"| REJECT5["Reject: Contradicts existing"]
    A5 -->|"Yes"| APPROVE["Approve for integration"]
```

## Learning Metrics

Tracking learning effectiveness:

```mermaid
flowchart TB
    subgraph Metrics["Learning Metrics"]
        M1["Patterns proposed"]
        M2["Patterns accepted"]
        M3["Patterns rejected"]
        M4["Application success rate"]
        M5["User satisfaction"]
    end

    subgraph Derived["Derived Metrics"]
        D1["Acceptance rate: accepted/proposed"]
        D2["Effectiveness: applications with success"]
        D3["Coverage: unique scenarios learned"]
    end

    subgraph Actions["Improvement Actions"]
        A1["Low acceptance → Improve proposals"]
        A2["Low effectiveness → Refine patterns"]
        A3["Low coverage → Expand observation"]
    end

    Metrics --> Derived --> Actions
```

## Memory System Integration

How learning integrates with memory:

```mermaid
flowchart TB
    subgraph Learning["Learning System"]
        L1["Induction Engine"]
        L2["Pattern Generalizer"]
        L3["Confidence Scorer"]
    end

    subgraph Memory["Memory System"]
        M1["Episodic: Observations"]
        M2["Pending: Proposals"]
        M3["Semantic: Approved patterns"]
        M4["Rejected: Blocked patterns"]
    end

    subgraph Knowledge["Knowledge System"]
        K1["Pattern files"]
        K2["Knowledge files"]
        K3["Workflow patterns"]
    end

    Learning --> Memory
    M3 -->|"Promote"| Knowledge
```

## Continuous Improvement Cycle

Ongoing system improvement:

```mermaid
flowchart TB
    subgraph Cycle["Improvement Cycle"]
        O["OBSERVE<br/>Capture interactions"]
        A["ANALYZE<br/>Find patterns"]
        L["LEARN<br/>Generalize patterns"]
        V["VALIDATE<br/>User approval"]
        I["INTEGRATE<br/>Update system"]
        M["MEASURE<br/>Track effectiveness"]
    end

    O --> A --> L --> V --> I --> M --> O

    subgraph Outcomes["Outcomes"]
        OUT1["Better predictions"]
        OUT2["Faster resolutions"]
        OUT3["Fewer errors"]
        OUT4["Improved user experience"]
    end

    M --> Outcomes
```
