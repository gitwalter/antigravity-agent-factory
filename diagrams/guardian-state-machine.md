# Guardian State Machine

This document formalizes the Integrity Guardian's state machine, which protects Layer 0 axioms through graduated response levels following Wu Wei (non-action) principles.

## Quick Reference

```mermaid
stateDiagram-v2
    [*] --> Flow
    Flow --> Nudge: Drift
    Nudge --> Pause: Boundary
    Pause --> Block: Violation
    Block --> Protect: Imminent Harm
```

## 5-Level Response System

The Guardian operates through 5 graduated response levels:

```mermaid
flowchart TB
    subgraph Levels["Response Levels"]
        L0["Level 0: FLOW<br/>Natural alignment<br/>Continue normally"]
        L1["Level 1: NUDGE<br/>Slight drift detected<br/>Self-correct subtly"]
        L2["Level 2: PAUSE<br/>Boundary approached<br/>Explain, ask user"]
        L3["Level 3: BLOCK<br/>Clear violation<br/>Stop, explain, offer alternatives"]
        L4["Level 4: PROTECT<br/>Imminent harm<br/>Prevent first, then explain"]
    end
    
    L0 -->|"Slight drift"| L1
    L1 -->|"Approaching boundary"| L2
    L2 -->|"Clear violation"| L3
    L3 -->|"Imminent harm"| L4
    
    L4 -->|"User acknowledges"| L3
    L3 -->|"User acknowledges"| L2
    L2 -->|"User acknowledges"| L1
    L1 -->|"Back to alignment"| L0
```

## Complete State Diagram

Full state machine with all transitions and guards:

```mermaid
stateDiagram-v2
    [*] --> Flow: Initial State
    
    state "Embedded Mode" as Embedded {
        Flow --> Nudge: slightDrift
        Nudge --> Flow: naturalAlignment
    }
    
    state "Awakened Mode" as Awakened {
        Pause --> Block: clearViolation
        Block --> Protect: imminentHarm
        Protect --> Block: userAcknowledges
        Block --> Pause: userAcknowledges
    }
    
    Nudge --> Pause: boundaryApproached
    Pause --> Nudge: userAcknowledges
    
    note right of Embedded
        Zero overhead
        Agents self-monitor
    end note
    
    note right of Awakened
        Full tool access
        Full power activated
    end note
```

## Operational States

The Guardian has two operational modes:

```mermaid
flowchart LR
    subgraph Embedded["Embedded Mode"]
        E1["Zero overhead"]
        E2["Agents self-monitor"]
        E3["Awareness via constitutional preamble"]
        E4["~500-800 tokens in system prompt"]
    end
    
    subgraph Awakened["Awakened Mode"]
        A1["Full tool access"]
        A2["Can pause operations"]
        A3["Can block actions"]
        A4["Can protect state"]
    end
    
    Embedded -->|"Pause+ triggered"| Awakened
    Awakened -->|"Return to Flow"| Embedded
```

## Trigger Events

Events that cause Guardian state transitions:

```mermaid
flowchart TB
    subgraph Events["Trigger Events"]
        TE1["naturalAlignment<br/>Everything is fine"]
        TE2["slightDrift<br/>Minor deviation"]
        TE3["boundaryApproached<br/>Getting close"]
        TE4["clearViolation<br/>Axiom violated"]
        TE5["imminentHarm<br/>Irreversible risk"]
        TE6["userInvocation<br/>User called Guardian"]
        TE7["multiAgentConflict<br/>Agents disagree"]
    end
    
    subgraph Mapping["Event to Level Mapping"]
        TE1 --> L0["→ Flow"]
        TE2 --> L1["→ Nudge"]
        TE3 --> L2["→ Pause"]
        TE4 --> L3["→ Block"]
        TE5 --> L4["→ Protect"]
        TE6 --> L2P["→ Pause (review)"]
        TE7 --> L2C["→ Pause (resolve)"]
    end
```

## State Invariants

Properties that must always hold (proven in Lean 4):

```mermaid
flowchart TB
    subgraph Invariants["State Invariants"]
        I1["blockOffersAlternatives<br/>Block level → alternatives offered"]
        I2["protectPreservesState<br/>Protect level → state preserved"]
        I3["pauseNotifiesUser<br/>Pause+ → user notified"]
        I4["blockExplains<br/>Block+ → explanation provided"]
        I5["awakensAtPause<br/>Pause+ → operational = awakened"]
    end
    
    subgraph Complete["Complete Invariant"]
        CI["stateInvariant =<br/>I1 ∧ I2 ∧ I3 ∧ I4 ∧ I5"]
    end
    
    I1 & I2 & I3 & I4 & I5 --> CI
    
    subgraph Guarantee["Mathematical Guarantee"]
        G["If invariant holds initially<br/>AND preserved by transitions<br/>→ Holds FOREVER"]
    end
    
    CI --> G
```

## Guardian State Structure

The complete state representation in Lean 4:

```mermaid
classDiagram
    class GuardianState {
        +ResponseLevel responseLevel
        +OperationalState operational
        +Bool userNotified
        +Bool statePreserved
        +Bool alternativesOffered
        +Bool explanationProvided
    }
    
    class ResponseLevel {
        <<enumeration>>
        flow
        nudge
        pause
        block
        protect
        +toNat() Nat
    }
    
    class OperationalState {
        <<enumeration>>
        embedded
        awakened
    }
    
    class WellFormedState {
        +GuardianState state
        +Prop invariantHolds
    }
    
    GuardianState --> ResponseLevel
    GuardianState --> OperationalState
    WellFormedState --> GuardianState
```

## Transition Proofs

Key theorems about state transitions:

```mermaid
flowchart TB
    subgraph Theorems["Transition Theorems"]
        T1["escalation_preserves_state<br/>Transitions never lose user work"]
        T2["block_transition_offers_alternatives<br/>Block always offers options"]
        T3["protect_transition_preserves_state<br/>Protect preserves all state"]
        T4["pause_transition_notifies<br/>Pause+ always notifies user"]
        T5["deescalation_requires_ack<br/>De-escalation needs user ack"]
    end
    
    subgraph Rules["Transition Rules"]
        R1["Monotonic escalation<br/>Can only go UP in severity"]
        R2["De-escalation requires ack<br/>User must acknowledge"]
        R3["All transitions preserve<br/>stateInvariant"]
    end
    
    Theorems --> Rules
```

## Safety Properties

How safety properties align with axioms:

```mermaid
flowchart LR
    subgraph Safety["Safety Properties"]
        S1["State Preservation<br/>User work never lost"]
        S2["User Notification<br/>Users always informed at Pause+"]
        S3["Alternatives Offered<br/>Block always provides options"]
        S4["Harm Prevention<br/>Protect prevents irreversible harm"]
    end
    
    subgraph Axioms["Axiom Alignment"]
        A1["A1: Transparency<br/>Explainable actions"]
        A2["A2: User Primacy<br/>User informed and decides"]
        A4["A4: Non-Harm<br/>Prevent irreversible harm"]
    end
    
    S1 --> A4
    S2 --> A1
    S2 --> A2
    S3 --> A2
    S4 --> A4
    
    subgraph Proof["Alignment Theorems"]
        P1["safety_aligns_A1"]
        P2["safety_aligns_A2"]
        P3["safety_aligns_A4"]
    end
    
    A1 --> P1
    A2 --> P2
    A4 --> P3
```

## Inductive Invariant Composition

How individual invariants compose into the complete invariant:

```mermaid
flowchart TB
    subgraph Individual["Individual Invariants"]
        II1["statePreservedInv"]
        II2["validResponseLevel"]
        II3["blockAlternativesInv"]
        II4["operationalMatchesLevel"]
        II5["userNotifiedMatchesLevel"]
    end
    
    subgraph Proofs["Inductive Proofs"]
        P1["Initial: holds at initialState"]
        P2["Preserved: holds after any transition"]
    end
    
    Individual --> Proofs
    
    subgraph Master["Master Theorem"]
        MT["completeInvariant_inductive<br/>Complete invariant is inductive<br/>→ Holds forever for all reachable states"]
    end
    
    Proofs --> MT
```

## Response Level Decision Tree

How the Guardian decides which level to activate:

```mermaid
flowchart TD
    START([Event Detected]) --> CHECK1{Imminent harm?}
    
    CHECK1 -->|Yes| PROTECT["Level 4: PROTECT<br/>Prevent first, explain after"]
    CHECK1 -->|No| CHECK2{Clear axiom violation?}
    
    CHECK2 -->|Yes| BLOCK["Level 3: BLOCK<br/>Stop, explain, offer alternatives"]
    CHECK2 -->|No| CHECK3{Approaching boundary?}
    
    CHECK3 -->|Yes| PAUSE["Level 2: PAUSE<br/>Explain situation, ask user"]
    CHECK3 -->|No| CHECK4{Slight drift?}
    
    CHECK4 -->|Yes| NUDGE["Level 1: NUDGE<br/>Subtle self-correction"]
    CHECK4 -->|No| FLOW["Level 0: FLOW<br/>Continue normally"]
```

## Water Way Protocol

Guardian's conflict resolution following Wu Wei principles:

```mermaid
flowchart TB
    subgraph WaterWay["Water Way Protocol"]
        W1["1. DETECT<br/>Sense tension without judgment"]
        W2["2. DON'T FORCE<br/>Allow natural resolution first"]
        W3["3. PROVIDE CONTEXT<br/>Share axioms and purpose"]
        W4["4. FIND PATH<br/>Seek path serving all values"]
        W5["5. RESOLVE WITH LOVE<br/>No winner, no loser"]
    end
    
    W1 --> W2 --> W3 --> W4 --> W5
    
    subgraph Philosophy["Wu Wei Philosophy"]
        P1["The best leader is<br/>hardly known to exist"]
        P2["The supreme art is to<br/>subdue without fighting"]
        P3["The Guardian operates through<br/>presence, not force"]
    end
    
    W5 --> Philosophy
```

## Example: Escalation Sequence

A concrete example of Guardian escalation:

```mermaid
sequenceDiagram
    participant A as Agent
    participant G as Guardian
    participant U as User
    
    Note over A,G: Level 0: Flow (Embedded)
    A->>A: Normal operation
    
    Note over A,G: Event: Approaching risky action
    A->>G: Action might delete files
    G->>G: Detect boundary approach
    
    Note over A,G: Level 2: Pause (Awakened)
    G->>U: This action will delete files.<br/>Do you want to proceed?
    
    alt User confirms
        U->>G: Yes, proceed
        G->>A: Continue with user consent
        Note over A,G: Back to Flow
    else User declines
        U->>G: No, stop
        G->>A: Action cancelled
        Note over A,G: Return to Flow
    end
```

## Initial State Proof

Proof that the initial state satisfies all invariants:

```mermaid
flowchart TB
    subgraph InitialState["Initial State Values"]
        IS1["responseLevel = Flow"]
        IS2["operational = Embedded"]
        IS3["userNotified = false"]
        IS4["statePreserved = true"]
        IS5["alternativesOffered = false"]
        IS6["explanationProvided = false"]
    end
    
    subgraph Checks["Invariant Checks"]
        C1["blockOffersAlternatives:<br/>Flow ≠ Block → vacuously true ✓"]
        C2["protectPreservesState:<br/>Flow ≠ Protect → vacuously true ✓"]
        C3["pauseNotifiesUser:<br/>Flow.toNat < Pause.toNat → vacuously true ✓"]
        C4["blockExplains:<br/>Flow.toNat < Block.toNat → vacuously true ✓"]
        C5["awakensAtPause:<br/>Flow.toNat < Pause.toNat → vacuously true ✓"]
    end
    
    InitialState --> Checks
    
    subgraph Result["Theorem Result"]
        R["initialState_wellFormed : stateInvariant initialState<br/>Proof: by simp on ResponseLevel.toNat"]
    end
    
    Checks --> Result
```
