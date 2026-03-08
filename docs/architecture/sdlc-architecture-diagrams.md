# Antigravity SDLC: Architecture Diagrams

## 1. Agent-Skill-MCP Interaction Matrix
This diagram illustrates how a typical SDLC phase (Phase 2: Requirements) orchestrates across the factory's infrastructure.

```mermaid
graph LR
    User[USER] -->|Input| WA[Workflow Architect]

    subgraph "Skill Execution Layer"
        WA --> S1[Skill: eliciting-nfr]
        WA --> S2[Skill: writing-prd]
    end

    subgraph "Infrastructure Layer (MCP)"
        S1 --> Memory[Memory MCP: Context]
        S2 --> Plane[Plane MCP: Ticket Sync]
        S2 --> Files[File System: knowledge/prd.md]
    end

    subgraph "Verification Layer"
        Files --> TG[Integrity Guardian]
        TG -->|Validate| Axioms[Axiom Rules]
    end
```

## 2. The 7-Phase Linear Progression
Each phase acts as a transformation function, passing validated artifacts forward.

```mermaid
graph TD
    subgraph "UPSTREAM"
        P1["Phase 1: IDEATION<br/>(Goal: Vision)"]
    end

    subgraph "CORE"
        P2["Phase 2: REQUIREMENTS<br/>(Goal: READY PRD)"]
        P3["Phase 3: ARCHITECTURE<br/>(Goal: System Design)"]
        P4["Phase 4: BUILD<br/>(Goal: Code)"]
    end

    subgraph "DOWNSTREAM"
        P5["Phase 5: TEST & EVAL<br/>(Goal: Validation)"]
        P6["Phase 6: DEPLOY<br/>(Goal: Release)"]
        P7["Phase 7: MONITOR<br/>(Goal: Feedback)"]
    end

    P1 -->|Gate: brief.md| P2
    P2 -->|Gate: prd.md| P3
    P3 -->|Gate: design.md| P4
    P4 -->|Gate: PR| P5
    P5 -->|Gate: Report| P6
    P6 -->|Gate: Live| P7
    P7 -.->|Loop| P1
```

## 3. High-Fidelity Infographic
![SDLC Flow Infographic](assets/sdlc_flow_chart.png)
