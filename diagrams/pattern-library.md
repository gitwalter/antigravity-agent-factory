# Pattern Library Architecture

This document visualizes the pattern organization, inheritance, selection algorithms, and how patterns are used to generate artifacts.

## Quick Reference

```mermaid
flowchart LR
    C[Categories] --> P[Patterns] --> S[Selection] --> T[Templates]
```

## Pattern Library Overview

Complete pattern organization:

```mermaid
flowchart TB
    subgraph Library["patterns/"]
        subgraph Agents["agents/"]
            A1["code-reviewer.json"]
            A2["test-generator.json"]
            A3["doc-writer.json"]
        end

        subgraph Skills["skills/"]
            S1["code-analysis.json"]
            S2["refactoring.json"]
            S3["agent-coordination.json"]
        end

        subgraph Axioms["axioms/"]
            AX1["core-axioms.json"]
            AX2["optional-axioms.json"]
        end

        subgraph Methodologies["methodologies/"]
            M1["agile.json"]
            M2["kanban.json"]
            M3["r-and-d.json"]
        end

        subgraph Enforcement["enforcement/"]
            E1["strict.json"]
            E2["balanced.json"]
            E3["minimal.json"]
        end

        subgraph Practices["practices/"]
            P1["tdd.json"]
            P2["code-review.json"]
            P3["pair-programming.json"]
        end

        subgraph Workshops["workshops/"]
            W1["foundation.json"]
            W2["principles.json"]
            W3["technical.json"]
        end
    end
```

## Pattern Categories

Detailed category breakdown:

```mermaid
flowchart TB
    subgraph Categories["Pattern Categories"]
        subgraph AgentPatterns["Agent Patterns"]
            AP1["Role definition"]
            AP2["Capabilities"]
            AP3["Trigger conditions"]
            AP4["Output formats"]
        end

        subgraph SkillPatterns["Skill Patterns"]
            SP1["Procedure steps"]
            SP2["Tool requirements"]
            SP3["Input/output specs"]
            SP4["Error handling"]
        end

        subgraph AxiomPatterns["Axiom Patterns"]
            AXP1["Core axioms (A0-A5)"]
            AXP2["Domain-specific extensions"]
            AXP3["Enforcement rules"]
        end

        subgraph MethodPatterns["Methodology Patterns"]
            MP1["Workflow phases"]
            MP2["Ceremony definitions"]
            MP3["Artifact templates"]
        end
    end
```

## Pattern JSON Schema

Structure of pattern files:

```mermaid
classDiagram
    class Pattern {
        +String id
        +String name
        +String description
        +String category
        +String version
        +Array~String~ tags
        +Object metadata
    }

    class AgentPattern {
        +String role
        +Array~String~ capabilities
        +Array~Trigger~ triggers
        +Array~String~ skills
        +Object configuration
    }

    class SkillPattern {
        +Array~Step~ procedure
        +Array~String~ tools
        +Object inputs
        +Object outputs
        +Object error_handling
    }

    class MethodologyPattern {
        +Array~Phase~ phases
        +Array~Ceremony~ ceremonies
        +Object metrics
        +Object artifacts
    }

    Pattern <|-- AgentPattern
    Pattern <|-- SkillPattern
    Pattern <|-- MethodologyPattern
```

## Pattern Inheritance

How patterns extend each other:

```mermaid
flowchart TB
    subgraph Base["Base Patterns"]
        B1["base-agent.json"]
        B2["base-skill.json"]
        B3["base-methodology.json"]
    end

    subgraph Derived["Derived Patterns"]
        D1["code-reviewer.json<br/>extends: base-agent"]
        D2["refactoring.json<br/>extends: base-skill"]
        D3["agile.json<br/>extends: base-methodology"]
    end

    subgraph Specialized["Specialized Patterns"]
        S1["security-reviewer.json<br/>extends: code-reviewer"]
        S2["safe-refactoring.json<br/>extends: refactoring"]
    end

    Base --> Derived --> Specialized

    subgraph Inheritance["Inheritance Rules"]
        I1["Child inherits parent properties"]
        I2["Child can override properties"]
        I3["Child can add new properties"]
    end
```

## Pattern to Template Relationship

How patterns drive template generation:

```mermaid
flowchart TB
    subgraph Patterns["Selected Patterns"]
        P1["Agent patterns"]
        P2["Skill patterns"]
        P3["Methodology patterns"]
    end

    subgraph Mapping["Pattern-Template Mapping"]
        M1["agent-pattern → agent.md.tmpl"]
        M2["skill-pattern → SKILL.md.tmpl"]
        M3["methodology → workflows/*.tmpl"]
    end

    subgraph Templates["Generated from Templates"]
        T1[".cursor/agents/*.md"]
        T2[".cursor/skills/*/SKILL.md"]
        T3["workflows/*.yaml"]
    end

    Patterns --> Mapping --> Templates
```

## Blueprint Selection Algorithm

How patterns are selected based on requirements:

```mermaid
flowchart TD
    START([Requirements Input]) --> SCORE["Score each blueprint"]

    subgraph Scoring["Scoring Process"]
        S1["Language match: 40%"]
        S2["Framework match: 60%"]
        S3["Bonus: Domain match"]
    end

    SCORE --> Scoring --> CALC["Calculate total score"]

    CALC --> RANK["Rank blueprints"]
    RANK --> TOP["Select top match"]

    TOP --> CONF{Confidence?}
    CONF -->|"> 80%"| AUTO["Auto-select"]
    CONF -->|"50-80%"| SUGGEST["Suggest with options"]
    CONF -->|"< 50%"| ASK["Ask user to choose"]
```

## Pattern Selection Criteria

What factors influence pattern selection:

```mermaid
flowchart TB
    subgraph Criteria["Selection Criteria"]
        subgraph Primary["Primary Factors"]
            P1["Stack compatibility"]
            P2["Domain relevance"]
            P3["Team size match"]
        end

        subgraph Secondary["Secondary Factors"]
            S1["Complexity level"]
            S2["Maturity status"]
            S3["Community adoption"]
        end

        subgraph Constraints["Constraints"]
            C1["Must satisfy axioms"]
            C2["Must be consistent"]
            C3["Must have templates"]
        end
    end

    Criteria --> FILTER["Filter by constraints"]
    FILTER --> RANK["Rank by factors"]
    RANK --> SELECT["Select best matches"]
```

## Pattern Composition

How multiple patterns combine:

```mermaid
flowchart TB
    subgraph Selected["Selected Patterns"]
        P1["Agent: code-reviewer"]
        P2["Skill: code-analysis"]
        P3["Methodology: agile"]
        P4["Practice: tdd"]
    end

    subgraph Composition["Composition Process"]
        C1["Check compatibility"]
        C2["Resolve conflicts"]
        C3["Merge configurations"]
        C4["Build unified context"]
    end

    subgraph Output["Composed Result"]
        O1["Unified agent definition"]
        O2["Complete skill set"]
        O3["Configured methodology"]
        O4["Integrated practices"]
    end

    Selected --> Composition --> Output
```

## Pattern File Structure

Detailed JSON structure:

```mermaid
flowchart TB
    subgraph File["Pattern JSON File"]
        subgraph Header["Header"]
            H1["id: unique-identifier"]
            H2["name: Human Readable Name"]
            H3["version: 1.0.0"]
            H4["category: agent|skill|methodology"]
        end

        subgraph Body["Body"]
            B1["description: ..."]
            B2["extends: base-pattern (optional)"]
            B3["tags: [tag1, tag2]"]
            B4["configuration: {...}"]
        end

        subgraph Content["Type-Specific Content"]
            C1["(varies by category)"]
        end

        subgraph Meta["Metadata"]
            M1["author: ..."]
            M2["created: timestamp"]
            M3["updated: timestamp"]
            M4["status: active|deprecated"]
        end
    end
```

## Pattern Matching Flow

How patterns are matched to requirements:

```mermaid
sequenceDiagram
    participant R as Requirements
    participant PM as Pattern Matcher
    participant PL as Pattern Library
    participant S as Scorer
    participant O as Output

    R->>PM: Match requirements
    PM->>PL: Load available patterns
    PL-->>PM: All patterns

    loop For each pattern
        PM->>S: Score against requirements
        S->>S: Calculate language match
        S->>S: Calculate framework match
        S->>S: Calculate domain match
        S-->>PM: Score result
    end

    PM->>PM: Sort by score
    PM->>PM: Filter by constraints
    PM->>O: Return ranked matches
```

## Pattern Versioning

How pattern versions are managed:

```mermaid
flowchart TB
    subgraph Versioning["Version Management"]
        V1["Semantic versioning"]
        V2["MAJOR.MINOR.PATCH"]
    end

    subgraph Changes["Change Types"]
        C1["MAJOR: Breaking changes"]
        C2["MINOR: New features"]
        C3["PATCH: Bug fixes"]
    end

    subgraph Compatibility["Compatibility"]
        CP1["Same MAJOR: Compatible"]
        CP2["Different MAJOR: Check migration"]
    end

    Versioning --> Changes --> Compatibility
```

## Pattern Validation

How patterns are validated:

```mermaid
flowchart TD
    VAL([Validate Pattern]) --> SCHEMA["Check JSON schema"]

    SCHEMA --> SCH_OK{Valid schema?}
    SCH_OK -->|"No"| SCH_ERR["Schema error"]
    SCH_OK -->|"Yes"| REF["Check references"]

    REF --> REF_OK{References valid?}
    REF_OK -->|"No"| REF_ERR["Reference error"]
    REF_OK -->|"Yes"| DEP["Check dependencies"]

    DEP --> DEP_OK{Dependencies available?}
    DEP_OK -->|"No"| DEP_ERR["Dependency error"]
    DEP_OK -->|"Yes"| CONS["Check consistency"]

    CONS --> CONS_OK{Internally consistent?}
    CONS_OK -->|"No"| CONS_ERR["Consistency error"]
    CONS_OK -->|"Yes"| VALID["Pattern valid ✓"]
```

## Pattern Discovery

How patterns are discovered and loaded:

```mermaid
flowchart TB
    subgraph Discovery["Pattern Discovery"]
        D1["Scan patterns/ directory"]
        D2["Find all *.json files"]
        D3["Parse and validate"]
        D4["Build index"]
    end

    subgraph Index["Pattern Index"]
        I1["By ID: quick lookup"]
        I2["By Category: filter"]
        I3["By Tags: search"]
        I4["By Stack: filter"]
    end

    subgraph Cache["Index Cache"]
        C1["In-memory index"]
        C2["Invalidate on change"]
        C3["Rebuild on startup"]
    end

    Discovery --> Index --> Cache
```

## Pattern Usage Statistics

Tracking pattern usage:

```mermaid
flowchart TB
    subgraph Tracking["Usage Tracking"]
        T1["Pattern selected"]
        T2["Generation success/failure"]
        T3["User feedback"]
    end

    subgraph Metrics["Usage Metrics"]
        M1["Selection frequency"]
        M2["Success rate"]
        M3["User satisfaction"]
    end

    subgraph Actions["Improvement Actions"]
        A1["Promote popular patterns"]
        A2["Deprecate unused patterns"]
        A3["Improve low-rated patterns"]
    end

    Tracking --> Metrics --> Actions
```
