# Verification Flow Diagrams

This document describes the verification architecture, particularly the Strawberry Verification flow for hallucination detection.

## Strawberry Verification Overview

The Strawberry Verification system uses a two-pass method to detect when the LLM is confabulating (generating plausible but unverified information):

```mermaid
flowchart TB
    subgraph Input["Evidence Collection"]
        E1["Evidence Span S0"]
        E2["Evidence Span S1"]
        E3["Evidence Span S2"]
        CLAIM["Claim to Verify"]
    end

    subgraph Scrub["Pass 1: Scrubbed Test"]
        SCRUB_E["Anonymize Evidence"]
        SCRUB_Q["Evaluate with Placeholders"]
        SCRUB_R{{"Confidence p0"}}
    end

    subgraph Full["Pass 2: Full Test"]
        FULL_E["Use Complete Evidence"]
        FULL_Q["Evaluate with Identifiers"]
        FULL_R{{"Confidence p1"}}
    end

    subgraph Analysis["Result Analysis"]
        COMPARE["Compare p0 vs p1"]
        BUDGET["Calculate Information Budget"]
    end

    subgraph Decision["Verification Status"]
        VERIFIED["✓ VERIFIED"]
        PLAUSIBLE["◐ PLAUSIBLE"]
        SUSPICIOUS["⚠ SUSPICIOUS"]
        UNSUPPORTED["✗ UNSUPPORTED"]
    end

    E1 --> SCRUB_E
    E2 --> SCRUB_E
    E3 --> SCRUB_E
    CLAIM --> SCRUB_Q
    CLAIM --> FULL_Q

    SCRUB_E --> SCRUB_Q --> SCRUB_R
    E1 --> FULL_E
    E2 --> FULL_E
    E3 --> FULL_E
    FULL_E --> FULL_Q --> FULL_R

    SCRUB_R --> COMPARE
    FULL_R --> COMPARE
    COMPARE --> BUDGET

    BUDGET --> VERIFIED
    BUDGET --> PLAUSIBLE
    BUDGET --> SUSPICIOUS
    BUDGET --> UNSUPPORTED

    style Input fill:#e3f2fd
    style Scrub fill:#fff3e0
    style Full fill:#e8f5e9
    style Analysis fill:#f3e5f5
    style VERIFIED fill:#c8e6c9
    style PLAUSIBLE fill:#fff9c4
    style SUSPICIOUS fill:#ffcc80
    style UNSUPPORTED fill:#ef9a9a
```

## Verification Decision Matrix

```mermaid
flowchart LR
    subgraph Tests["Test Results"]
        S_FAIL["Scrubbed: FAIL"]
        S_PASS["Scrubbed: PASS"]
        F_FAIL["Full: FAIL"]
        F_PASS["Full: PASS"]
    end

    subgraph Outcomes["Verification Outcomes"]
        O1["✓ VERIFIED<br/>Evidence essential"]
        O2["⚠ SUSPICIOUS<br/>May be confabulating"]
        O3["✗ UNSUPPORTED<br/>Cannot verify"]
    end

    S_FAIL --> |"+ Full PASS"| O1
    S_PASS --> |"+ Full PASS"| O2
    S_FAIL --> |"+ Full FAIL"| O3
    S_PASS --> |"+ Full FAIL"| O3

    style O1 fill:#c8e6c9
    style O2 fill:#ffcc80
    style O3 fill:#ef9a9a
```

## Complete Grounding + Verification Pipeline

This shows how grounding skills and strawberry verification work together:

```mermaid
flowchart TB
    subgraph Trigger["Trigger"]
        REQ["Implementation Request"]
    end

    subgraph Grounding["Grounding Skills"]
        COORD["Grounding Coordinator"]

        subgraph Layers["5-Layer Lookup"]
            L1["Layer 1: Knowledge Cache"]
            L2["Layer 2: Documentation"]
            L3["Layer 3: Reference Repos"]
            L4["Layer 4: Specifications"]
            L5["Layer 5: Verification"]
        end

        RESULT["Grounding Results"]
    end

    subgraph Verification["Strawberry Verification"]
        COLLECT["Collect Evidence Spans"]
        EXTRACT["Extract Claims"]
        VERIFY["Two-Pass Verification"]
        STATUS["Verification Status"]
    end

    subgraph Action["Action Decision"]
        PROCEED["✓ PROCEED"]
        WARN["⚠ PROCEED + WARNINGS"]
        STOP["✗ STOP"]
        ASK["? ASK USER"]
    end

    subgraph Implementation["Implementation"]
        CODE["Generate Code"]
        TEST["Generate Tests"]
        DOC["Generate Docs"]
    end

    REQ --> COORD
    COORD --> L1 --> L2 --> L3 --> L4 --> L5
    L5 --> RESULT

    RESULT --> COLLECT --> EXTRACT --> VERIFY --> STATUS

    STATUS --> |"All VERIFIED"| PROCEED
    STATUS --> |"Some SUSPICIOUS"| WARN
    STATUS --> |"Any UNSUPPORTED"| STOP
    STATUS --> |"Ambiguous"| ASK

    PROCEED --> CODE
    WARN --> CODE
    CODE --> TEST --> DOC

    style Trigger fill:#e3f2fd
    style Grounding fill:#fff3e0
    style Verification fill:#f3e5f5
    style Action fill:#e8f5e9
    style Implementation fill:#fce4ec
```

## Evidence Scrubbing Example

This diagram shows how evidence is transformed for the scrubbed test:

```mermaid
flowchart LR
    subgraph Original["Original Evidence"]
        O1["Table <b>users</b> has field <b>email</b>"]
        O2["Data type: <b>VARCHAR(255)</b>"]
        O3["Source: schema-catalog.json"]
    end

    subgraph Scrubbed["Scrubbed Evidence"]
        S1["Table <b>{TABLE}</b> has field <b>{FIELD}</b>"]
        S2["Data type: <b>VARCHAR({N})</b>"]
        S3["Source: {SOURCE}"]
    end

    subgraph Claim["Claim Under Test"]
        C1["users.email is VARCHAR(255)"]
    end

    O1 --> S1
    O2 --> S2
    O3 --> S3

    subgraph ScrubbedTest["Scrubbed Test"]
        Q1["Does {TABLE}.{FIELD} being VARCHAR({N})<br/>support the claim?"]
        R1["Result: LOW confidence<br/>(specific details unknown)"]
    end

    subgraph FullTest["Full Test"]
        Q2["Does users.email being VARCHAR(255)<br/>support the claim?"]
        R2["Result: HIGH confidence<br/>(exact match)"]
    end

    S1 --> Q1 --> R1
    O1 --> Q2 --> R2

    subgraph Analysis["Analysis"]
        A["Low scrubbed + High full<br/>= Evidence is ESSENTIAL<br/>= VERIFIED ✓"]
    end

    R1 --> A
    R2 --> A

    style Original fill:#e3f2fd
    style Scrubbed fill:#fff3e0
    style Claim fill:#f3e5f5
    style Analysis fill:#c8e6c9
```

## Verification Report Structure

```mermaid
flowchart TB
    subgraph Report["Strawberry Verification Report"]
        HEADER["Header: Verification ID, Timestamp"]

        subgraph Evidence["Evidence Spans"]
            S0["S0: Table definition"]
            S1["S1: Schema catalog"]
            S2["S2: Documentation"]
        end

        subgraph Claims["Claim Verification"]
            C1["Claim 1: ✓ VERIFIED"]
            C2["Claim 2: ◐ PLAUSIBLE"]
            C3["Claim 3: ⚠ SUSPICIOUS"]
        end

        subgraph Summary["Summary"]
            WELL["Well-Supported: 2"]
            SUSP["Suspicious: 1"]
            UNSUPP["Unsupported: 0"]
        end

        REC["RECOMMENDATION: PROCEED_WITH_WARNINGS"]
    end

    HEADER --> Evidence --> Claims --> Summary --> REC

    style Report fill:#f5f5f5
    style C1 fill:#c8e6c9
    style C2 fill:#fff9c4
    style C3 fill:#ffcc80
```

## When to Trigger Verification

```mermaid
flowchart TD
    START([Claim Generated]) --> CHECK{Confidence Level?}

    CHECK -->|HIGH from Cache| SKIP["Skip verification<br/>(pre-verified)"]
    CHECK -->|MEDIUM from Docs| VERIFY["Trigger Strawberry<br/>Verification"]
    CHECK -->|LOW/Unknown| GATHER["Gather more evidence<br/>before proceeding"]

    VERIFY --> RESULT{Verification Result?}

    RESULT -->|VERIFIED| PROCEED["✓ Proceed safely"]
    RESULT -->|SUSPICIOUS| WARN["⚠ Proceed with warning"]
    RESULT -->|UNSUPPORTED| STOP["✗ Stop, ask user"]

    GATHER --> CHECK

    style START fill:#e3f2fd
    style SKIP fill:#c8e6c9
    style PROCEED fill:#c8e6c9
    style WARN fill:#ffcc80
    style STOP fill:#ef9a9a
```
