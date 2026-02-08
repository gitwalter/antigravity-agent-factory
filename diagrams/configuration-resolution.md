# Configuration Resolution Architecture

This document visualizes how configuration is resolved from multiple sources with precedence rules and fallback chains.

## Quick Reference

```mermaid
flowchart LR
    S[Session Cache] --> E[Env Var] --> C[Config File] --> A[Auto-Detect] --> D[Default]
```

## Configuration Resolution Overview

Complete resolution hierarchy:

```mermaid
flowchart TB
    subgraph Sources["Configuration Sources"]
        S1["1. Session Cache<br/>(highest priority)"]
        S2["2. Environment Variables"]
        S3["3. Config File"]
        S4["4. Auto-Detection"]
        S5["5. Default Values<br/>(lowest priority)"]
    end
    
    subgraph Resolution["Resolution Process"]
        R1["Check each source in order"]
        R2["Use first found value"]
        R3["Cache result for session"]
    end
    
    subgraph Output["Resolved Configuration"]
        O1["Final configuration values"]
        O2["Cached for performance"]
    end
    
    Sources --> Resolution --> Output
```

## Tool Path Resolution

How tool paths are resolved:

```mermaid
flowchart TD
    START([Tool Path Requested]) --> CACHE{In session cache?}
    
    CACHE -->|"Yes"| USE_CACHE["Use cached path"]
    CACHE -->|"No"| ENV{Environment variable set?}
    
    ENV -->|"Yes"| VAL_ENV["Validate env path"]
    VAL_ENV -->|"Valid"| USE_ENV["Use env path"]
    VAL_ENV -->|"Invalid"| CONFIG
    
    ENV -->|"No"| CONFIG{In config file?}
    CONFIG -->|"Yes"| VAL_CFG["Validate config path"]
    VAL_CFG -->|"Valid"| USE_CFG["Use config path"]
    VAL_CFG -->|"Invalid"| AUTO
    
    CONFIG -->|"No"| AUTO["Auto-detect"]
    AUTO --> FOUND{Found on PATH?}
    FOUND -->|"Yes"| USE_AUTO["Use detected path"]
    FOUND -->|"No"| DEFAULT["Use default path"]
    
    USE_CACHE & USE_ENV & USE_CFG & USE_AUTO & DEFAULT --> SAVE["Save to session cache"]
    SAVE --> RETURN["Return path"]
```

## Precedence Hierarchy Visualization

Visual representation of precedence:

```mermaid
flowchart TB
    subgraph Hierarchy["Precedence Hierarchy"]
        subgraph Highest["Highest Priority"]
            H1["Session Cache<br/>Runtime overrides"]
        end
        
        subgraph High["High Priority"]
            H2["Environment Variables<br/>CI/CD, deployment"]
        end
        
        subgraph Medium["Medium Priority"]
            H3["Config Files<br/>Project settings"]
        end
        
        subgraph Low["Low Priority"]
            H4["Auto-Detection<br/>System scanning"]
        end
        
        subgraph Lowest["Lowest Priority"]
            H5["Default Values<br/>Built-in fallbacks"]
        end
    end
    
    Highest --> High --> Medium --> Low --> Lowest
```

## Environment Variable Resolution

How environment variables are processed:

```mermaid
flowchart TB
    subgraph Input["Environment Variable"]
        I1["Variable name"]
        I2["Expected format"]
    end
    
    subgraph Check["Resolution Check"]
        C1["Check if variable exists"]
        C2["Get variable value"]
        C3["Validate format"]
    end
    
    subgraph Interpolation["Variable Interpolation"]
        INT["${VAR_NAME} syntax"]
        EXP["Expand nested variables"]
        ESC["Handle escape sequences"]
    end
    
    subgraph Output["Resolved Value"]
        O1["Validated value"]
        O2["Or continue to next source"]
    end
    
    Input --> Check --> Interpolation --> Output
```

## Platform Detection

Platform-specific configuration:

```mermaid
flowchart TD
    START([Detect Platform]) --> CHECK{Operating System?}
    
    CHECK -->|"Windows"| WIN["Windows Defaults"]
    CHECK -->|"Linux"| LIN["Linux Defaults"]
    CHECK -->|"macOS"| MAC["macOS Defaults"]
    
    subgraph Windows["Windows Defaults"]
        W1["Python: C:\\App\\Anaconda\\python.exe"]
        W2["Conda: C:\\App\\Anaconda\\Scripts\\conda.exe"]
        W3["Pip: C:\\App\\Anaconda\\Scripts\\pip.exe"]
        W4["Shell: powershell"]
    end
    
    subgraph Linux["Linux Defaults"]
        L1["Python: /usr/bin/python3"]
        L2["Conda: ~/miniconda3/bin/conda"]
        L3["Pip: /usr/bin/pip3"]
        L4["Shell: bash"]
    end
    
    subgraph macOS["macOS Defaults"]
        M1["Python: /usr/local/bin/python3"]
        M2["Conda: ~/opt/anaconda3/bin/conda"]
        M3["Pip: /usr/local/bin/pip3"]
        M4["Shell: zsh"]
    end
    
    WIN --> Windows
    LIN --> Linux
    MAC --> macOS
```

## Fallback Chain Visualization

Complete fallback chain for a tool:

```mermaid
flowchart TB
    subgraph Python["Python Path Resolution"]
        P1["1. SESSION: cached_python_path"]
        P2["2. ENV: FACTORY_PYTHON_PATH"]
        P3["3. CONFIG: tools.python.path"]
        P4["4. AUTO: which python / where python"]
        P5["5. PLATFORM: Platform-specific default"]
    end
    
    P1 -->|"miss"| P2 -->|"miss"| P3 -->|"miss"| P4 -->|"miss"| P5
    
    P1 -->|"hit"| RES["Resolved: /path/to/python"]
    P2 -->|"hit"| RES
    P3 -->|"hit"| RES
    P4 -->|"hit"| RES
    P5 --> RES
```

## Config File Structure

Structure of configuration files:

```mermaid
flowchart TB
    subgraph ConfigFiles["Configuration Files"]
        subgraph Tools["tools.json"]
            T1["python.path"]
            T2["conda.path"]
            T3["git.path"]
            T4["docker.path"]
        end
        
        subgraph Settings["settings.json"]
            S1["project.default_output"]
            S2["generation.interactive"]
            S3["logging.level"]
            S4["memory.enabled"]
        end
        
        subgraph Overrides["local.json"]
            O1["User-specific overrides"]
            O2["Not in version control"]
        end
    end
```

## Auto-Detection Process

How tools are automatically detected:

```mermaid
flowchart TB
    subgraph Detection["Auto-Detection"]
        D1["Search PATH environment"]
        D2["Check common locations"]
        D3["Query package managers"]
        D4["Check registry (Windows)"]
    end
    
    subgraph Validation["Path Validation"]
        V1["File exists?"]
        V2["Is executable?"]
        V3["Correct version?"]
    end
    
    subgraph Locations["Common Locations"]
        subgraph Win["Windows"]
            W1["C:\\Python\\"]
            W2["C:\\App\\Anaconda\\"]
            W3["%USERPROFILE%\\AppData\\"]
        end
        
        subgraph Unix["Unix/Linux/macOS"]
            U1["/usr/bin/"]
            U2["/usr/local/bin/"]
            U3["~/miniconda3/bin/"]
        end
    end
    
    Detection --> Validation --> Locations
```

## Configuration Caching

How configuration is cached:

```mermaid
flowchart TB
    subgraph Cache["Session Cache"]
        C1["In-memory storage"]
        C2["Per-session lifetime"]
        C3["Auto-update on change"]
    end
    
    subgraph Operations["Cache Operations"]
        O1["Get: Check cache first"]
        O2["Set: Store after resolution"]
        O3["Invalidate: On config change"]
    end
    
    subgraph Benefits["Caching Benefits"]
        B1["Avoid repeated resolution"]
        B2["Consistent values in session"]
        B3["Performance improvement"]
    end
    
    Cache --> Operations --> Benefits
```

## Configuration Manager Flow

ConfigManager class behavior:

```mermaid
sequenceDiagram
    participant C as Caller
    participant CM as ConfigManager
    participant CA as Cache
    participant EN as Environment
    participant CF as Config File
    participant AD as Auto-Detect
    
    C->>CM: get_python_path()
    CM->>CA: Check cache
    
    alt Cache hit
        CA-->>CM: Cached path
        CM-->>C: Return cached
    else Cache miss
        CM->>EN: Check FACTORY_PYTHON_PATH
        
        alt Env set
            EN-->>CM: Env path
            CM->>CM: Validate path
            CM->>CA: Store in cache
            CM-->>C: Return path
        else Env not set
            CM->>CF: Check config file
            
            alt Config has path
                CF-->>CM: Config path
                CM->>CM: Validate path
                CM->>CA: Store in cache
                CM-->>C: Return path
            else Config empty
                CM->>AD: Auto-detect
                AD-->>CM: Detected path
                CM->>CA: Store in cache
                CM-->>C: Return path
            end
        end
    end
```

## Directory Resolution

How directories are resolved:

```mermaid
flowchart TD
    START([Directory Requested]) --> TYPE{Directory Type?}
    
    TYPE -->|"Output"| OUT["Check --output flag<br/>→ ENV: FACTORY_OUTPUT<br/>→ Config: default_output<br/>→ ./output"]
    
    TYPE -->|"Templates"| TMP["Check --templates flag<br/>→ ENV: FACTORY_TEMPLATES<br/>→ Config: templates_dir<br/>→ ./templates"]
    
    TYPE -->|"Knowledge"| KNW["Check --knowledge flag<br/>→ ENV: FACTORY_KNOWLEDGE<br/>→ Config: knowledge_dir<br/>→ ./knowledge"]
    
    TYPE -->|"Cache"| CAC["ENV: FACTORY_CACHE<br/>→ Config: cache_dir<br/>→ ~/.factory/cache"]
    
    OUT & TMP & KNW & CAC --> RESOLVE["Resolve absolute path"]
    RESOLVE --> CREATE{Exists?}
    CREATE -->|"No"| MKDIR["Create directory"]
    CREATE -->|"Yes"| RETURN["Return path"]
    MKDIR --> RETURN
```

## Environment Variable Interpolation

How nested variables are expanded:

```mermaid
flowchart TB
    subgraph Input["Input Value"]
        I["${HOME}/.factory/cache"]
    end
    
    subgraph Process["Interpolation Process"]
        P1["Detect ${...} pattern"]
        P2["Extract variable name"]
        P3["Lookup variable value"]
        P4["Substitute in string"]
        P5["Handle nested ${...}"]
    end
    
    subgraph Output["Output Value"]
        O["/Users/john/.factory/cache"]
    end
    
    Input --> Process --> Output
    
    subgraph Example["Examples"]
        E1["${HOME}/projects → /Users/john/projects"]
        E2["${PROJECT_ROOT}/src → /code/myproject/src"]
        E3["${CONDA_PREFIX}/bin/python → /opt/conda/bin/python"]
    end
```

## Configuration Validation

How configuration values are validated:

```mermaid
flowchart TD
    VAL([Validate Configuration]) --> PATH{Path value?}
    
    PATH -->|"Yes"| P_CHECK["Check path exists"]
    P_CHECK --> P_OK{Exists?}
    P_OK -->|"No"| P_WARN["Warning: Path not found"]
    P_OK -->|"Yes"| P_EXEC{Executable?}
    P_EXEC -->|"No"| E_WARN["Warning: Not executable"]
    P_EXEC -->|"Yes"| VALID["Valid ✓"]
    
    PATH -->|"No"| TYPE{Value type?}
    TYPE -->|"Boolean"| B_CHECK["Parse as boolean"]
    TYPE -->|"Number"| N_CHECK["Parse as number"]
    TYPE -->|"String"| S_CHECK["Validate string"]
    
    B_CHECK & N_CHECK & S_CHECK --> VALID
```

## Configuration Override Flow

How overrides are applied:

```mermaid
flowchart TB
    subgraph Sources["Override Sources"]
        CLI["Command-line flags<br/>(highest)"]
        ENV["Environment variables"]
        LOCAL["local.json<br/>(user-specific)"]
        PROJECT["settings.json<br/>(project)"]
        DEFAULT["defaults.json<br/>(lowest)"]
    end
    
    subgraph Merge["Merge Process"]
        M1["Start with defaults"]
        M2["Layer project settings"]
        M3["Apply local overrides"]
        M4["Apply environment"]
        M5["Apply CLI flags"]
    end
    
    subgraph Result["Final Configuration"]
        R["Fully resolved config"]
    end
    
    Sources --> Merge --> Result
```
