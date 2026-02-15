# Factory Workflow Diagrams

This document contains the core workflow diagrams for the Cursor Agent Factory.

## Factory Generation Workflow

The complete workflow from user request to generated project:

```mermaid
flowchart TB
    subgraph Input["User Input"]
        A[/"Create new agent system"/]
        B[/"Use blueprint: python-fastapi"/]
        C[/"Load config.yaml"/]
    end

    subgraph Requirements["Phase 1-5: Requirements Gathering"]
        D[Requirements Architect]
        D --> E[Phase 1: Project Context]
        E --> F[Phase 2: Technology Stack]
        F --> G[Phase 3: Workflow Methodology]
        G --> H[Phase 4: Knowledge Domain]
        H --> I[Phase 5: Agent Capabilities]
    end

    subgraph Processing["Configuration & Selection"]
        J[Stack Builder]
        K[Blueprint Matching]
        L[Pattern Selection]
    end

    subgraph Generation["Artifact Generation"]
        M[Workflow Designer]
        N[Knowledge Manager]
        O[Template Generator]
    end

    subgraph Output["Generated Project"]
        P[".cursor/agents/"]
        Q[".cursor/skills/"]
        R["knowledge/"]
        S["templates/"]
        T[".cursorrules"]
        U["README.md"]
    end

    A --> D
    B --> J
    C --> J

    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O

    O --> P
    O --> Q
    O --> R
    O --> S
    O --> T
    O --> U

    style Input fill:#e1f5fe
    style Requirements fill:#fff3e0
    style Processing fill:#f3e5f5
    style Generation fill:#e8f5e9
    style Output fill:#fce4ec
```

## Requirements Gathering Flow

Detailed view of the 5-phase questionnaire:

```mermaid
flowchart LR
    subgraph P1["Phase 1"]
        A1[Project Name]
        A2[Description]
        A3[Domain/Industry]
        A4[Team Size]
    end

    subgraph P2["Phase 2"]
        B1[Primary Language]
        B2[Frameworks]
        B3[Database]
        B4[External APIs]
    end

    subgraph P3["Phase 3"]
        C1[Methodology]
        C2[Trigger Sources]
        C3[Output Artifacts]
    end

    subgraph P4["Phase 4"]
        D1[Domain Concepts]
        D2[Reference Repos]
        D3[Best Practices]
    end

    subgraph P5["Phase 5"]
        E1[Core Agents]
        E2[Required Skills]
        E3[MCP Servers]
    end

    P1 --> P2 --> P3 --> P4 --> P5

    style P1 fill:#bbdefb
    style P2 fill:#c8e6c9
    style P3 fill:#fff9c4
    style P4 fill:#ffccbc
    style P5 fill:#e1bee7
```

## CLI vs Chat Workflow

```mermaid
flowchart TB
    subgraph Entry["Entry Points"]
        CHAT["Chat: 'Create agent system'"]
        CLI["CLI: factory_cli.py"]
    end

    subgraph CLI_Options["CLI Options"]
        BLUEPRINT["--blueprint python-fastapi"]
        CONFIG["--config project.yaml"]
        INTERACTIVE["--interactive"]
    end

    subgraph Processing["Common Processing"]
        VALIDATE[Validate Configuration]
        MATCH[Match Patterns]
        GENERATE[Generate Artifacts]
    end

    subgraph Output["Output"]
        PROJECT["Complete Project at --output path"]
    end

    CHAT --> VALIDATE
    CLI --> CLI_Options
    BLUEPRINT --> VALIDATE
    CONFIG --> VALIDATE
    INTERACTIVE --> VALIDATE

    VALIDATE --> MATCH --> GENERATE --> PROJECT

    style Entry fill:#e3f2fd
    style CLI_Options fill:#f1f8e9
    style Processing fill:#fff8e1
    style Output fill:#fce4ec
```

## Blueprint Selection Logic

```mermaid
flowchart TD
    START([User specifies stack]) --> CHECK{Blueprint exists?}

    CHECK -->|Yes| USE[Use matching blueprint]
    CHECK -->|No| GENERIC[Use generic patterns]

    USE --> CUSTOMIZE{Customize?}
    GENERIC --> CUSTOMIZE

    CUSTOMIZE -->|Yes| MODIFY[Modify blueprint settings]
    CUSTOMIZE -->|No| PROCEED[Proceed to generation]

    MODIFY --> PROCEED
    PROCEED --> GENERATE[Generate project]

    style START fill:#e8f5e9
    style GENERATE fill:#c8e6c9
```
