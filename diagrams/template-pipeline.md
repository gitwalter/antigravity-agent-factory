# Template Generation Pipeline

This document visualizes the template discovery, context building, and rendering process that generates project artifacts.

## Quick Reference

```mermaid
flowchart LR
    D[Discover] --> L[Load] --> C[Context] --> R[Render] --> W[Write]
```

## Template Pipeline Overview

Complete template generation flow:

```mermaid
flowchart TB
    subgraph Discovery["Template Discovery"]
        D1["Identify required templates"]
        D2["Locate template files"]
        D3["Resolve inheritance"]
    end
    
    subgraph Loading["Template Loading"]
        L1["Load base templates"]
        L2["Load overrides"]
        L3["Merge template chains"]
    end
    
    subgraph Context["Context Building"]
        C1["Gather requirements"]
        C2["Apply blueprint"]
        C3["Include patterns"]
        C4["Add metadata"]
    end
    
    subgraph Rendering["Template Rendering"]
        R1["Jinja2 processing"]
        R2["Variable substitution"]
        R3["Conditional logic"]
    end
    
    subgraph Output["Output Generation"]
        O1["Write files"]
        O2["Create directories"]
        O3["Set permissions"]
    end
    
    Discovery --> Loading --> Context --> Rendering --> Output
```

## Template Discovery Flow

How templates are located:

```mermaid
flowchart TB
    subgraph Input["Discovery Input"]
        I1["Blueprint name"]
        I2["Required artifacts"]
        I3["Custom templates"]
    end
    
    subgraph Resolution["Template Resolution"]
        R1["Check blueprint templates/"]
        R2["Check factory templates/"]
        R3["Check custom templates/"]
        R4["Apply inheritance chain"]
    end
    
    subgraph Hierarchy["Template Hierarchy"]
        H1["1. Custom (highest priority)"]
        H2["2. Blueprint-specific"]
        H3["3. Stack-specific"]
        H4["4. Generic (fallback)"]
    end
    
    subgraph Output["Resolved Templates"]
        O1["List of template files"]
        O2["Inheritance order"]
        O3["Override mapping"]
    end
    
    Input --> Resolution --> Hierarchy --> Output
```

## Template Directory Structure

Organization of templates:

```mermaid
flowchart TB
    subgraph Templates["templates/"]
        subgraph Factory["factory/"]
            F1[".cursorrules.tmpl"]
            F2["PURPOSE.md.tmpl"]
            F3["README.md.tmpl"]
        end
        
        subgraph Python["python/"]
            P1["requirements.txt.tmpl"]
            P2["setup.py.tmpl"]
            P3["main.py.tmpl"]
        end
        
        subgraph TypeScript["typescript/"]
            T1["package.json.tmpl"]
            T2["tsconfig.json.tmpl"]
            T3["index.ts.tmpl"]
        end
        
        subgraph AI["ai/"]
            A1["agent.py.tmpl"]
            A2["skill.py.tmpl"]
            A3["workflow.yaml.tmpl"]
        end
        
        subgraph Workflows["workflows/"]
            W1["github-actions.yml.tmpl"]
            W2["gitlab-ci.yml.tmpl"]
        end
    end
```

## Context Building Process

How rendering context is assembled:

```mermaid
flowchart TB
    subgraph Sources["Context Sources"]
        S1["Requirements<br/>(user input)"]
        S2["Blueprint<br/>(predefined)"]
        S3["Patterns<br/>(selected)"]
        S4["Metadata<br/>(computed)"]
    end
    
    subgraph Building["Context Assembly"]
        B1["Merge sources"]
        B2["Apply defaults"]
        B3["Compute derived values"]
        B4["Validate completeness"]
    end
    
    subgraph Context["Final Context"]
        subgraph Project["project.*"]
            P1["name, description"]
            P2["version, author"]
        end
        
        subgraph Stack["stack.*"]
            ST1["language, framework"]
            ST2["database, apis"]
        end
        
        subgraph Agents["agents.*"]
            AG1["list of agents"]
            AG2["capabilities"]
        end
        
        subgraph Meta["meta.*"]
            M1["timestamp"]
            M2["factory_version"]
        end
    end
    
    Sources --> Building --> Context
```

## Jinja Rendering Process

Template processing details:

```mermaid
flowchart TB
    subgraph Template["Template File"]
        T1["Static text"]
        T2["{{ variables }}"]
        T3["{% control flow %}"]
        T4["{# comments #}"]
    end
    
    subgraph Environment["Jinja Environment"]
        E1["Configure autoescape"]
        E2["Register filters"]
        E3["Register globals"]
        E4["Set up loader"]
    end
    
    subgraph Processing["Rendering Steps"]
        P1["Parse template"]
        P2["Build AST"]
        P3["Evaluate expressions"]
        P4["Execute control flow"]
        P5["Substitute variables"]
    end
    
    subgraph Output["Rendered Output"]
        O1["Final text content"]
        O2["Ready to write"]
    end
    
    Template --> Environment --> Processing --> Output
```

## Variable Resolution Chain

Where variables come from:

```mermaid
flowchart TD
    VAR([Variable Lookup]) --> CHECK1{In user input?}
    
    CHECK1 -->|"Yes"| USE1["Use user value"]
    CHECK1 -->|"No"| CHECK2{In blueprint?}
    
    CHECK2 -->|"Yes"| USE2["Use blueprint value"]
    CHECK2 -->|"No"| CHECK3{In patterns?}
    
    CHECK3 -->|"Yes"| USE3["Use pattern value"]
    CHECK3 -->|"No"| CHECK4{Has default?}
    
    CHECK4 -->|"Yes"| USE4["Use default value"]
    CHECK4 -->|"No"| ERROR["Raise: Missing variable"]
    
    USE1 & USE2 & USE3 & USE4 --> RENDER["Render template"]
```

## Multi-Template Orchestration

How multiple templates are coordinated:

```mermaid
sequenceDiagram
    participant TG as Template Generator
    participant TE as Template Engine
    participant CTX as Context Builder
    participant FS as Filesystem
    
    TG->>CTX: Build shared context
    CTX-->>TG: Context object
    
    loop For each template
        TG->>TE: Render template with context
        TE->>TE: Load template
        TE->>TE: Resolve variables
        TE->>TE: Process conditionals
        TE-->>TG: Rendered content
        TG->>FS: Write to output path
    end
    
    TG->>TG: Verify all files written
    TG-->>TG: Generation complete
```

## Template Inheritance

How templates extend each other:

```mermaid
flowchart TB
    subgraph Base["Base Template"]
        B1["{% block header %}...{% endblock %}"]
        B2["{% block content %}...{% endblock %}"]
        B3["{% block footer %}...{% endblock %}"]
    end
    
    subgraph Child["Child Template"]
        C1["{% extends 'base.tmpl' %}"]
        C2["{% block content %}<br/>Custom content<br/>{% endblock %}"]
    end
    
    subgraph Result["Rendered Result"]
        R1["Base header"]
        R2["Custom content"]
        R3["Base footer"]
    end
    
    Base --> Child --> Result
```

## Conditional Template Logic

How conditionals work in templates:

```mermaid
flowchart TB
    subgraph Template["Template with Conditionals"]
        T1["{% if stack.database %}"]
        T2["Include database config"]
        T3["{% endif %}"]
        
        T4["{% if methodology == 'agile' %}"]
        T5["Include sprint workflow"]
        T6["{% else %}"]
        T7["Include kanban workflow"]
        T8["{% endif %}"]
    end
    
    subgraph Context["Context Values"]
        C1["stack.database = 'postgresql'"]
        C2["methodology = 'agile'"]
    end
    
    subgraph Output["Rendered Output"]
        O1["Database config included"]
        O2["Sprint workflow included"]
    end
    
    Template --> Context --> Output
```

## Custom Jinja Filters

Available custom filters:

```mermaid
flowchart TB
    subgraph Filters["Custom Jinja Filters"]
        F1["| snake_case<br/>Convert to snake_case"]
        F2["| camel_case<br/>Convert to camelCase"]
        F3["| pascal_case<br/>Convert to PascalCase"]
        F4["| kebab_case<br/>Convert to kebab-case"]
        F5["| pluralize<br/>Make plural"]
        F6["| indent<br/>Add indentation"]
        F7["| quote<br/>Add quotes"]
        F8["| escape_json<br/>JSON-safe escape"]
    end
    
    subgraph Usage["Usage Examples"]
        U1["{{ name | snake_case }}"]
        U2["{{ agents | length }}"]
        U3["{{ description | indent(4) }}"]
    end
```

## Template Engine Configuration

How the template engine is configured:

```mermaid
flowchart TB
    subgraph Config["Engine Configuration"]
        C1["Template directories"]
        C2["Autoescape settings"]
        C3["Undefined behavior"]
        C4["Custom filters"]
        C5["Global functions"]
    end
    
    subgraph Settings["Default Settings"]
        S1["autoescape = select_autoescape(['html'])"]
        S2["undefined = StrictUndefined"]
        S3["trim_blocks = True"]
        S4["lstrip_blocks = True"]
    end
    
    Config --> Settings
```

## File Writing Process

How rendered content is written:

```mermaid
flowchart TB
    subgraph Input["Rendered Content"]
        I1["File content"]
        I2["Target path"]
        I3["File mode"]
    end
    
    subgraph Preparation["Write Preparation"]
        P1["Resolve absolute path"]
        P2["Create parent directories"]
        P3["Check for existing file"]
    end
    
    subgraph Conflict["Conflict Handling"]
        CH{File exists?}
        OVER["Overwrite if --force"]
        MERGE["Merge if configured"]
        SKIP["Skip if --no-overwrite"]
        BACKUP["Backup if --backup"]
    end
    
    subgraph Write["File Writing"]
        W1["Write content"]
        W2["Set permissions"]
        W3["Verify written"]
    end
    
    Input --> Preparation --> CH
    CH -->|"Yes"| Conflict --> Write
    CH -->|"No"| Write
```

## Template Batch Processing

Processing multiple templates efficiently:

```mermaid
flowchart TB
    subgraph Batch["Batch Processing"]
        subgraph Group1["Group 1: Config Files"]
            G1A[".cursorrules"]
            G1B["PURPOSE.md"]
            G1C["README.md"]
        end
        
        subgraph Group2["Group 2: Agent Files"]
            G2A["agent-1.md"]
            G2B["agent-2.md"]
            G2C["agent-n.md"]
        end
        
        subgraph Group3["Group 3: Skill Files"]
            G3A["skill-1/SKILL.md"]
            G3B["skill-2/SKILL.md"]
        end
    end
    
    subgraph Processing["Parallel Processing"]
        P1["Process Group 1"]
        P2["Process Group 2"]
        P3["Process Group 3"]
    end
    
    Group1 --> P1
    Group2 --> P2
    Group3 --> P3
    
    P1 & P2 & P3 --> COMPLETE["All files written"]
```

## Template Validation

Pre-render validation:

```mermaid
flowchart TD
    START([Template Validation]) --> SYNTAX["Check Jinja syntax"]
    
    SYNTAX --> SYN_OK{Valid syntax?}
    SYN_OK -->|"No"| SYNTAX_ERR["Syntax error report"]
    SYN_OK -->|"Yes"| VARS["Check required variables"]
    
    VARS --> VARS_OK{All variables available?}
    VARS_OK -->|"No"| VARS_ERR["Missing variable report"]
    VARS_OK -->|"Yes"| DEPS["Check template dependencies"]
    
    DEPS --> DEPS_OK{Dependencies exist?}
    DEPS_OK -->|"No"| DEPS_ERR["Missing dependency report"]
    DEPS_OK -->|"Yes"| VALID["Template valid ✓"]
    
    SYNTAX_ERR & VARS_ERR & DEPS_ERR --> FAIL["Validation failed"]
```
