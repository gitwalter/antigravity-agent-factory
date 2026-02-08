# Agent and Skill Architecture Diagrams

This document describes the relationship between agents, skills, knowledge files, and patterns in the Cursor Agent Factory.

## Factory Agent Hierarchy

```mermaid
flowchart TB
    subgraph Factory["Cursor Agent Factory"]
        subgraph Agents["Factory Agents"]
            RA["requirements-architect"]
            SB["stack-builder"]
            WD["workflow-designer"]
            KM["knowledge-manager"]
            TG["template-generator"]
        end
        
        subgraph Skills["Factory Skills"]
            RG["requirements-gathering"]
            SC["stack-configuration"]
            WG["workflow-generation"]
            AG["agent-generation"]
            SG["skill-generation"]
            KG["knowledge-generation"]
            TEG["template-generation"]
            CG["cursorrules-generation"]
        end
    end

    RA --> RG
    SB --> SC
    WD --> WG
    KM --> KG
    TG --> AG
    TG --> SG
    TG --> TEG
    TG --> CG

    style Factory fill:#f5f5f5
    style Agents fill:#e3f2fd
    style Skills fill:#e8f5e9
```

## Agent Activation Flow

```mermaid
sequenceDiagram
    participant User
    participant Cursorrules as .cursorrules
    participant Agent
    participant Skills
    participant Knowledge
    participant Output

    User->>Cursorrules: "Create agent system"
    Cursorrules->>Agent: Activate requirements-architect
    
    loop 5 Phases
        Agent->>Skills: Use requirements-gathering
        Skills->>Knowledge: Query patterns
        Knowledge-->>Skills: Return patterns
        Skills-->>Agent: Phase complete
        Agent->>User: Ask next questions
        User-->>Agent: Provide answers
    end
    
    Agent->>Output: Generate project configuration
    Agent->>Agent: Hand off to stack-builder
```

## Pattern Library Structure

```mermaid
flowchart TB
    subgraph Patterns["patterns/"]
        subgraph AP["agents/"]
            AP1["agent-pattern.json"]
            AP2["code-reviewer.json"]
            AP3["test-generator.json"]
            AP4["explorer.json"]
        end
        
        subgraph SP["skills/"]
            SP1["skill-pattern.json"]
            SP2["bugfix-workflow.json"]
            SP3["feature-workflow.json"]
            SP4["tdd.json"]
            SP5["grounding.json"]
            SP6["strawberry-verification.json"]
        end
        
        subgraph WP["workflows/"]
            WP1["workflow-pattern.json"]
        end
        
        subgraph STP["stacks/"]
            STP1["stack-blueprint.json"]
        end
        
        subgraph TP["templates/"]
            TP1["template-pattern.json"]
        end
    end

    subgraph Blueprints["blueprints/"]
        BP1["python-fastapi/"]
        BP2["typescript-react/"]
        BP3["java-spring/"]
        BP4["sap-abap/"]
    end

    Blueprints --> |references| AP
    Blueprints --> |references| SP
    Blueprints --> |references| WP

    style Patterns fill:#fff3e0
    style Blueprints fill:#e8f5e9
```

## Skill Composition Model

Skills are composable - complex workflows combine multiple skills:

```mermaid
flowchart TB
    subgraph Composite["Feature Development Workflow"]
        FW["feature-workflow"]
    end

    subgraph Core["Core Skills"]
        GR["grounding"]
        TDD["tdd"]
        CT["code-templates"]
    end

    subgraph Verification["Verification Layer"]
        SV["strawberry-verification"]
    end

    FW --> GR
    FW --> TDD
    FW --> CT
    GR --> SV
    TDD --> GR

    style Composite fill:#e3f2fd
    style Core fill:#fff3e0
    style Verification fill:#f3e5f5
```

## Generated Project Architecture

When the factory generates a project, it creates this structure:

```mermaid
flowchart TB
    subgraph Generated["Generated Project"]
        subgraph Cursor[".cursor/"]
            subgraph A["agents/"]
                A1["code-reviewer.md"]
                A2["test-generator.md"]
                A3["custom-agent.md"]
            end
            
            subgraph S["skills/"]
                S1["bugfix-workflow/SKILL.md"]
                S2["feature-workflow/SKILL.md"]
                S3["tdd/SKILL.md"]
            end
        end
        
        subgraph K["knowledge/"]
            K1["data-patterns.json"]
            K2["api-catalog.json"]
            K3["conventions.json"]
        end
        
        subgraph T["templates/"]
            T1["service-class.py"]
            T2["test-template.py"]
        end
        
        CR[".cursorrules"]
        README["README.md"]
    end

    A1 --> S1
    A1 --> S2
    A2 --> S3
    S1 --> K1
    S2 --> K2
    S3 --> K3

    style Generated fill:#f5f5f5
    style Cursor fill:#e3f2fd
    style K fill:#fff3e0
    style T fill:#e8f5e9
```

## Agent vs Skill Comparison

```mermaid
flowchart LR
    subgraph Agent["Agent Characteristics"]
        A1["Orchestrates workflows"]
        A2["Has activation triggers"]
        A3["Invokes multiple skills"]
        A4["Produces structured output"]
        A5["Defined in .md files"]
    end

    subgraph Skill["Skill Characteristics"]
        S1["Focused procedure"]
        S2["Reusable across agents"]
        S3["References knowledge"]
        S4["Step-by-step process"]
        S5["Defined in SKILL.md"]
    end

    subgraph Knowledge["Knowledge Files"]
        K1["JSON format"]
        K2["Queryable data"]
        K3["Cached definitions"]
        K4["Source of truth"]
    end

    Agent --> |"uses"| Skill
    Skill --> |"queries"| Knowledge

    style Agent fill:#e3f2fd
    style Skill fill:#e8f5e9
    style Knowledge fill:#fff3e0
```

## Skill Execution Flow

```mermaid
sequenceDiagram
    participant Agent
    participant Skill
    participant Knowledge as knowledge/*.json
    participant MCP as MCP Servers
    participant Output

    Agent->>Skill: Invoke skill
    
    Skill->>Knowledge: Check cached data
    alt Found in cache
        Knowledge-->>Skill: Return cached result
    else Not cached
        Skill->>MCP: Query external source
        MCP-->>Skill: Return result
        Skill->>Knowledge: Cache for future
    end
    
    Skill->>Skill: Execute process steps
    Skill->>Output: Generate artifacts
    Skill-->>Agent: Return completion status
```

## Blueprint to Project Transformation

```mermaid
flowchart LR
    subgraph Blueprint["Blueprint Input"]
        B1["metadata"]
        B2["stack config"]
        B3["agent refs"]
        B4["skill refs"]
        B5["mcp servers"]
    end

    subgraph Factory["Factory Processing"]
        F1["Resolve patterns"]
        F2["Customize for project"]
        F3["Generate files"]
    end

    subgraph Project["Generated Output"]
        P1[".cursor/agents/*.md"]
        P2[".cursor/skills/*/SKILL.md"]
        P3["knowledge/*.json"]
        P4[".cursorrules"]
    end

    B1 --> F1
    B2 --> F1
    B3 --> F1
    B4 --> F1
    B5 --> F1
    
    F1 --> F2 --> F3
    
    F3 --> P1
    F3 --> P2
    F3 --> P3
    F3 --> P4

    style Blueprint fill:#e3f2fd
    style Factory fill:#fff3e0
    style Project fill:#e8f5e9
```
