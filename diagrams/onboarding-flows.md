# Onboarding Flow Architecture

This document visualizes the three onboarding modes and non-destructive integration flow for bringing existing repositories into the Antigravity Agent Factory ecosystem.

## Quick Reference

```mermaid
flowchart LR
    subgraph Modes["Onboarding Modes"]
        E["Express<br/>10-15 min"]
        H["Team Huddle<br/>1-2 hours"]
        W["Workshop<br/>Multi-session"]
    end
```

## Three Onboarding Modes Comparison

Overview of all onboarding approaches:

```mermaid
flowchart TB
    subgraph Express["Express Onboarding"]
        E1["Duration: 10-15 minutes"]
        E2["Participants: 1 developer"]
        E3["Approach: Guided prompts"]
        E4["Output: Basic agent system"]
        E5["Best for: Solo devs, quick start"]
    end

    subgraph Huddle["Team Huddle"]
        H1["Duration: 1-2 hours"]
        H2["Participants: 2-5 people"]
        H3["Approach: Mini-games, shared decisions"]
        H4["Output: Team-aligned system"]
        H5["Best for: Small teams, alignment"]
    end

    subgraph Workshop["Workshop Series"]
        W1["Duration: Multi-session"]
        W2["Participants: Enterprise teams"]
        W3["Approach: 5 workshops"]
        W4["Output: Comprehensive system"]
        W5["Best for: Enterprise, complex needs"]
    end
```

## Express Onboarding Flow

Quick 10-15 minute onboarding:

```mermaid
flowchart TB
    subgraph Start["Start"]
        S1["Welcome message"]
        S2["Quick context scan"]
    end

    subgraph Questions["Guided Questions (5-6)"]
        Q1["1. Project purpose?"]
        Q2["2. Primary stack?"]
        Q3["3. Main workflow?"]
        Q4["4. Key challenges?"]
        Q5["5. Team preferences?"]
    end

    subgraph Generation["Generation"]
        G1["Match blueprint"]
        G2["Apply patterns"]
        G3["Generate artifacts"]
    end

    subgraph Celebration["Celebration"]
        C1["Show generated files"]
        C2["Quick tour"]
        C3["Next steps"]
    end

    Start --> Questions --> Generation --> Celebration
```

## Team Huddle Flow

1-2 hour collaborative session:

```mermaid
flowchart TB
    subgraph Opening["Opening (10 min)"]
        O1["Welcome & introductions"]
        O2["Session overview"]
        O3["Set shared goals"]
    end

    subgraph Discovery["Discovery (30 min)"]
        D1["Project context mapping"]
        D2["Tech stack discussion"]
        D3["Pain point identification"]
    end

    subgraph Games["Mini-Games (30 min)"]
        G1["Values voting"]
        G2["Workflow prioritization"]
        G3["Agent naming contest"]
    end

    subgraph Decisions["Shared Decisions (20 min)"]
        DE1["Blueprint selection"]
        DE2["Customization choices"]
        DE3["Ownership assignment"]
    end

    subgraph Closing["Closing (15 min)"]
        C1["Review generated system"]
        C2["Action items"]
        C3["Celebration"]
    end

    Opening --> Discovery --> Games --> Decisions --> Closing
```

## Workshop Series Flow

Enterprise multi-session approach:

```mermaid
flowchart TB
    subgraph W1["Workshop 1: Foundation"]
        W1A["Axiom exploration"]
        W1B["Purpose definition"]
        W1C["Stakeholder mapping"]
    end

    subgraph W2["Workshop 2: Principles"]
        W2A["Value translation"]
        W2B["Boundary setting"]
        W2C["Quality standards"]
    end

    subgraph W3["Workshop 3: Methodology"]
        W3A["Workflow design"]
        W3B["Trigger identification"]
        W3C["Automation planning"]
    end

    subgraph W4["Workshop 4: Technical"]
        W4A["Stack finalization"]
        W4B["Agent design"]
        W4C["Skill mapping"]
    end

    subgraph W5["Workshop 5: Launch"]
        W5A["System review"]
        W5B["Training"]
        W5C["Deployment"]
    end

    W1 --> W2 --> W3 --> W4 --> W5
```

## Non-Destructive Integration Flow

How existing files are preserved:

```mermaid
flowchart TB
    subgraph Analysis["Repository Analysis"]
        A1["Scan existing files"]
        A2["Detect tech stack"]
        A3["Find config files"]
        A4["Identify patterns"]
    end

    subgraph Detection["Conflict Detection"]
        D1["Check for .cursorrules"]
        D2["Check for .cursor/ directory"]
        D3["Check for workflows/"]
        D4["Check for knowledge/"]
    end

    subgraph Resolution["Conflict Resolution"]
        R1{Existing files?}
        MERGE["Merge strategy"]
        PRESERVE["Preserve existing"]
        CREATE["Create new"]
    end

    subgraph Output["Integration Output"]
        O1["Enhanced, not replaced"]
        O2["Original preserved"]
        O3["New files added"]
        O4["Conflicts logged"]
    end

    Analysis --> Detection --> Resolution --> Output
    R1 -->|"Yes"| MERGE & PRESERVE
    R1 -->|"No"| CREATE
```

## Pre-existing File Preservation

How different file types are handled:

```mermaid
flowchart TB
    subgraph ExistingFiles["Pre-existing Files"]
        F1[".cursorrules"]
        F2[".cursor/ directory"]
        F3["README.md"]
        F4["workflows/"]
    end

    subgraph Strategy["Handling Strategy"]
        S1["MERGE: Combine rules"]
        S2["AUGMENT: Add new files"]
        S3["ENHANCE: Add sections"]
        S4["ADD: New workflows"]
    end

    subgraph Safeguards["Safeguards"]
        G1["Backup original"]
        G2["Track changes"]
        G3["Revert option"]
        G4["User approval"]
    end

    F1 --> S1 --> G1
    F2 --> S2 --> G2
    F3 --> S3 --> G3
    F4 --> S4 --> G4
```

## Repository Analysis Flow

How existing repositories are analyzed:

```mermaid
sequenceDiagram
    participant U as User
    participant OA as Onboarding Architect
    participant RA as Repo Analyzer
    participant SB as Stack Builder
    participant TG as Template Generator

    U->>OA: Onboard this repo
    OA->>RA: Analyze repository

    RA->>RA: Scan file structure
    RA->>RA: Detect languages
    RA->>RA: Identify frameworks
    RA->>RA: Find config files

    RA-->>OA: Analysis report
    OA->>SB: Match blueprint
    SB-->>OA: Best match + confidence

    OA->>U: Suggested blueprint: X<br/>Confidence: Y%<br/>Proceed?

    alt User Confirms
        U->>OA: Yes, proceed
        OA->>TG: Generate with preservation
        TG-->>U: Enhanced repository
    else User Modifies
        U->>OA: Use blueprint Z instead
        OA->>TG: Generate with override
        TG-->>U: Enhanced repository
    end
```

## Blueprint Matching Algorithm

How the right blueprint is selected:

```mermaid
flowchart TD
    START([Repository Files]) --> LANG["Detect Languages"]

    LANG --> SCORE["Score each blueprint"]

    subgraph Scoring["Scoring Weights"]
        S1["Language match: 40%"]
        S2["Framework match: 60%"]
    end

    SCORE --> RANK["Rank by score"]

    RANK --> CONF{Confidence?}

    CONF -->|">80%"| HIGH["High confidence<br/>Suggest top match"]
    CONF -->|"50-80%"| MED["Medium confidence<br/>Present options"]
    CONF -->|"<50%"| LOW["Low confidence<br/>Ask user"]

    HIGH & MED & LOW --> FINAL["Final blueprint selection"]
```

## Conflict Detection Matrix

What conflicts are detected and how:

```mermaid
flowchart TB
    subgraph Conflicts["Conflict Types"]
        subgraph File["File Conflicts"]
            F1[".cursorrules exists"]
            F2["PURPOSE.md exists"]
            F3["Agent files exist"]
        end

        subgraph Config["Config Conflicts"]
            C1["Different Python version"]
            C2["Conflicting dependencies"]
            C3["Incompatible settings"]
        end

        subgraph Structure["Structure Conflicts"]
            S1["Different project layout"]
            S2["Existing .cursor/ structure"]
            S3["Custom workflows"]
        end
    end

    subgraph Resolution["Resolution Strategy"]
        R1["Merge with user review"]
        R2["Preserve original + add new"]
        R3["User decides"]
    end

    Conflicts --> Resolution
```

## Integration Outcome

What gets created during onboarding:

```mermaid
flowchart TB
    subgraph Before["Before Onboarding"]
        B1["Existing codebase"]
        B2["No agent system"]
        B3["Manual workflows"]
    end

    subgraph Added["Added by Onboarding"]
        A1[".cursorrules<br/>(or merged)"]
        A2[".cursor/agents/<br/>Custom agents"]
        A3[".cursor/skills/<br/>Project skills"]
        A4["knowledge/<br/>Domain knowledge"]
        A5["PURPOSE.md<br/>(if not exists)"]
    end

    subgraph Preserved["Preserved"]
        P1["All existing code"]
        P2["Existing configs"]
        P3["User customizations"]
        P4["Git history"]
    end

    subgraph After["After Onboarding"]
        AF1["Original + Agent System"]
        AF2["Non-destructive enhancement"]
    end

    Before --> Added
    Before --> Preserved
    Added & Preserved --> After
```

## Mode Selection Decision Tree

Helping users choose the right mode:

```mermaid
flowchart TD
    START([Choose Onboarding]) --> SIZE{Team size?}

    SIZE -->|"1 person"| SOLO["Solo developer"]
    SIZE -->|"2-5 people"| SMALL["Small team"]
    SIZE -->|"6+ people"| LARGE["Large team"]

    SOLO --> TIME1{Available time?}
    TIME1 -->|"< 30 min"| EXPRESS["Express Onboarding"]
    TIME1 -->|"> 30 min"| EXPRESS

    SMALL --> ALIGN{Need alignment?}
    ALIGN -->|"High"| HUDDLE["Team Huddle"]
    ALIGN -->|"Low"| EXPRESS

    LARGE --> COMPLEX{Complexity?}
    COMPLEX -->|"High"| WORKSHOP["Workshop Series"]
    COMPLEX -->|"Medium"| HUDDLE
    COMPLEX -->|"Low"| EXPRESS
```

## Onboarding Metrics

Success indicators for onboarding:

```mermaid
flowchart TB
    subgraph Metrics["Success Metrics"]
        M1["Completion rate"]
        M2["Time to completion"]
        M3["User satisfaction"]
        M4["System adoption rate"]
        M5["Conflict resolution success"]
    end

    subgraph Targets["Target Values"]
        T1[">90% complete"]
        T2["Within mode time"]
        T3[">4.0/5.0 rating"]
        T4[">70% active use"]
        T5[">95% resolved"]
    end

    M1 --> T1
    M2 --> T2
    M3 --> T3
    M4 --> T4
    M5 --> T5
```

## Post-Onboarding Flow

What happens after onboarding:

```mermaid
flowchart TB
    subgraph Complete["Onboarding Complete"]
        C1["Agent system generated"]
        C2["Files in place"]
        C3["Ready to use"]
    end

    subgraph NextSteps["Next Steps"]
        N1["Review generated files"]
        N2["Customize as needed"]
        N3["Start using agents"]
        N4["Iterate and improve"]
    end

    subgraph Support["Ongoing Support"]
        S1["Documentation links"]
        S2["Quick start guide"]
        S3["Community resources"]
        S4["Feedback channel"]
    end

    Complete --> NextSteps --> Support
```
