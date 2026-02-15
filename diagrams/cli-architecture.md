# CLI Architecture

This document visualizes the command-line interface architecture, from command parsing to agent invocation and output generation.

## Quick Reference

```mermaid
flowchart LR
    C[Command] --> P[Parse] --> V[Validate] --> A[Agent] --> O[Output]
```

## CLI Command Flow

Complete command processing flow:

```mermaid
flowchart TB
    subgraph Input["User Input"]
        CMD["factory_cli.py command [options]"]
    end

    subgraph Parsing["Command Parsing"]
        P1["Parse command name"]
        P2["Parse arguments"]
        P3["Parse options/flags"]
        P4["Load config file (if --config)"]
    end

    subgraph Validation["Validation"]
        V1["Validate command exists"]
        V2["Validate required args"]
        V3["Validate option values"]
        V4["Check file paths"]
    end

    subgraph Execution["Agent Execution"]
        E1["Select appropriate agent"]
        E2["Prepare context"]
        E3["Execute agent"]
        E4["Collect output"]
    end

    subgraph Output["Output Generation"]
        O1["Write generated files"]
        O2["Display status"]
        O3["Show next steps"]
    end

    Input --> Parsing --> Validation --> Execution --> Output
```

## Available Commands

CLI command structure:

```mermaid
flowchart TB
    subgraph CLI["factory_cli.py"]
        subgraph Core["Core Commands"]
            GEN["generate<br/>Generate new project"]
            ONB["onboard<br/>Onboard existing repo"]
            VAL["validate<br/>Validate configuration"]
        end

        subgraph Utils["Utility Commands"]
            LIST["list<br/>List blueprints/patterns"]
            INFO["info<br/>Show blueprint details"]
            UPDATE["update<br/>Update knowledge"]
        end

        subgraph Config["Configuration"]
            INIT["init<br/>Initialize config"]
            CFG["config<br/>Manage settings"]
        end
    end
```

## Command Parsing Detail

How commands are parsed:

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Parser
    participant ARG as Argument Parser
    participant VAL as Validator
    participant CFG as Config Loader

    U->>CLI: factory_cli.py generate --blueprint python-fastapi
    CLI->>ARG: Parse command line
    ARG->>ARG: Split command from args
    ARG->>ARG: Parse --blueprint option

    alt Config file specified
        ARG->>CFG: Load --config file
        CFG-->>ARG: Merged configuration
    end

    ARG->>VAL: Validate parsed args
    VAL->>VAL: Check required fields
    VAL->>VAL: Validate blueprint exists

    alt Validation passes
        VAL-->>CLI: Valid configuration
    else Validation fails
        VAL-->>CLI: Error with details
        CLI-->>U: Display error message
    end
```

## Interactive vs Non-Interactive Mode

Mode selection and behavior:

```mermaid
flowchart TD
    START([CLI Invoked]) --> CHECK{Mode?}

    CHECK -->|"--interactive"| INTER["Interactive Mode"]
    CHECK -->|"--config file"| NON["Non-Interactive Mode"]
    CHECK -->|"neither"| DEFAULT["Detect based on args"]

    subgraph Interactive["Interactive Mode"]
        I1["Prompt for missing values"]
        I2["Show progress"]
        I3["Confirm before writing"]
        I4["Display rich output"]
    end

    subgraph NonInteractive["Non-Interactive Mode"]
        N1["Use config file values"]
        N2["Fail on missing required"]
        N3["Write without confirm"]
        N4["Machine-readable output"]
    end

    INTER --> Interactive
    NON --> NonInteractive
    DEFAULT --> CHECK2{All required present?}
    CHECK2 -->|"Yes"| NonInteractive
    CHECK2 -->|"No"| Interactive
```

## Agent Invocation

How CLI invokes agents:

```mermaid
flowchart TB
    subgraph CLI["CLI Layer"]
        CMD["Parsed command"]
        CTX["Build context"]
    end

    subgraph AgentSelection["Agent Selection"]
        SEL{Command type?}
        RA["requirements-architect"]
        SB["stack-builder"]
        OA["onboarding-architect"]
    end

    subgraph Execution["Agent Execution"]
        PREP["Prepare agent context"]
        RUN["Run agent workflow"]
        COLL["Collect outputs"]
    end

    subgraph Output["Output Handling"]
        FILES["Write files to --output"]
        DISP["Display summary"]
        LOG["Log operations"]
    end

    CLI --> SEL
    SEL -->|"generate"| RA --> SB
    SEL -->|"onboard"| OA
    AgentSelection --> Execution --> Output
```

## Output Generation

How outputs are written:

```mermaid
flowchart TB
    subgraph Artifacts["Generated Artifacts"]
        A1[".cursorrules"]
        A2[".cursor/agents/*"]
        A3[".cursor/skills/*"]
        A4["knowledge/*"]
        A5["templates/*"]
        A6["workflows/*"]
    end

    subgraph Writing["File Writing"]
        CHK["Check output directory"]
        CREATE["Create directories"]
        WRITE["Write files"]
        VERIFY["Verify written files"]
    end

    subgraph Conflict["Conflict Handling"]
        DET{File exists?}
        OVER["Overwrite (if --force)"]
        SKIP["Skip (if --no-overwrite)"]
        ASK["Ask user (interactive)"]
    end

    Artifacts --> Writing
    Writing --> DET
    DET -->|"Yes"| Conflict
    DET -->|"No"| WRITE
```

## Error Handling Flow

How errors are handled:

```mermaid
flowchart TD
    ERR([Error Occurs]) --> TYPE{Error Type?}

    TYPE -->|"Parse error"| PARSE["Show usage help"]
    TYPE -->|"Validation error"| VAL["Show what's missing/invalid"]
    TYPE -->|"Blueprint not found"| BP["List available blueprints"]
    TYPE -->|"File error"| FILE["Show file path issue"]
    TYPE -->|"Agent error"| AGENT["Show agent error + context"]

    PARSE & VAL & BP & FILE & AGENT --> EXIT["Exit with error code"]

    subgraph Codes["Exit Codes"]
        C0["0: Success"]
        C1["1: General error"]
        C2["2: Validation error"]
        C3["3: File error"]
        C4["4: Agent error"]
    end
```

## Configuration File Format

Structure of config files:

```mermaid
flowchart TB
    subgraph ConfigFile["config.yaml"]
        subgraph Project["project:"]
            P1["name: my-project"]
            P2["description: ..."]
            P3["domain: fintech"]
        end

        subgraph Stack["stack:"]
            S1["language: python"]
            S2["framework: fastapi"]
            S3["database: postgresql"]
        end

        subgraph Methodology["methodology:"]
            M1["type: agile"]
            M2["triggers: [pr, push]"]
        end

        subgraph Agents["agents:"]
            A1["- code-reviewer"]
            A2["- test-generator"]
        end
    end
```

## CLI Options Reference

Available options and flags:

```mermaid
flowchart TB
    subgraph Global["Global Options"]
        G1["--help, -h"]
        G2["--version, -v"]
        G3["--verbose"]
        G4["--quiet"]
    end

    subgraph Generate["Generate Options"]
        GEN1["--blueprint, -b"]
        GEN2["--config, -c"]
        GEN3["--output, -o"]
        GEN4["--interactive, -i"]
        GEN5["--force, -f"]
    end

    subgraph Onboard["Onboard Options"]
        ONB1["--repo, -r"]
        ONB2["--mode"]
        ONB3["--preserve"]
        ONB4["--merge"]
    end

    subgraph List["List Options"]
        LST1["--type"]
        LST2["--format"]
        LST3["--filter"]
    end
```

## Progress Display

How progress is shown to users:

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI
    participant AG as Agent
    participant FS as Filesystem

    CLI->>U: Starting generation...
    CLI->>AG: Execute

    loop Each Phase
        AG->>CLI: Phase N started
        CLI->>U: [Phase N/5] Processing...
        AG->>AG: Work
        AG->>CLI: Phase N complete
        CLI->>U: [Phase N/5] Complete ✓
    end

    AG->>FS: Write files
    FS-->>AG: Written
    AG->>CLI: Generation complete

    CLI->>U: ✓ Generated X files
    CLI->>U: Output: /path/to/output
    CLI->>U: Next steps: ...
```

## Pipeline Integration

How CLI integrates with CI/CD:

```mermaid
flowchart TB
    subgraph CI["CI/CD Pipeline"]
        TRIGGER["Pipeline triggered"]
        CHECKOUT["Checkout code"]
        INSTALL["Install dependencies"]
    end

    subgraph CLI["CLI Execution"]
        RUN["factory_cli.py validate --config ci.yaml"]
        VAL["Validate configuration"]
        CHECK["Check consistency"]
    end

    subgraph Result["Pipeline Result"]
        PASS["Exit 0: Pass"]
        FAIL["Exit non-0: Fail"]
    end

    CI --> CLI --> Result
```

## Command Examples

Common usage patterns:

```mermaid
flowchart LR
    subgraph Examples["Command Examples"]
        E1["Generate with blueprint:<br/>factory_cli.py generate -b python-fastapi"]
        E2["Generate with config:<br/>factory_cli.py generate -c project.yaml"]
        E3["Interactive mode:<br/>factory_cli.py generate -i"]
        E4["Onboard existing:<br/>factory_cli.py onboard --repo ."]
        E5["List blueprints:<br/>factory_cli.py list --type blueprints"]
    end
```
