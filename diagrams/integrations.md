# Integration Architecture

This document visualizes how the Factory integrates with external systems including MCP servers, PM backends, and development tools.

## Quick Reference

```mermaid
flowchart LR
    F[Factory] --> M[MCP Servers]
    F --> P[PM Backends]
    F --> T[Dev Tools]
    F --> S[Society Verification]
```

## Integration Overview

Complete integration landscape:

```mermaid
flowchart TB
    subgraph Factory["Antigravity Agent Factory"]
        CORE["Core System"]
    end

    subgraph MCP["MCP Servers"]
        M1["SAP Docs"]
        M2["DeepWiki"]
        M3["Atlassian"]
        M4["Custom MCPs"]
    end

    subgraph PM["PM Backends"]
        P1["Jira"]
        P2["GitHub Issues"]
        P3["Linear"]
        P4["Local JSON"]
    end

    subgraph Tools["Development Tools"]
        T1["Git"]
        T2["Docker"]
        T3["Cloud Providers"]
        T4["CI/CD Systems"]
    end

    subgraph Verify["Verification"]
        V1["Society System"]
        V2["Lean 4 Proofs"]
    end

    CORE <--> MCP
    CORE <--> PM
    CORE <--> Tools
    CORE <--> Verify
```

## MCP Server Integration

How MCP servers are discovered and used:

```mermaid
flowchart TB
    subgraph Discovery["MCP Discovery"]
        D1["Read .cursor/mcp.json"]
        D2["Parse server definitions"]
        D3["Validate connections"]
    end

    subgraph Catalog["MCP Catalog"]
        C1["mcp-servers-catalog.json"]
        C2["Available servers"]
        C3["Capabilities map"]
    end

    subgraph Usage["MCP Usage"]
        U1["Agent invokes MCP tool"]
        U2["MCP server responds"]
        U3["Agent processes result"]
    end

    Discovery --> Catalog --> Usage
```

## MCP Server Configuration

Configuration structure:

```mermaid
flowchart TB
    subgraph ConfigFile[".cursor/mcp.json"]
        subgraph Server["Server Definition"]
            S1["name: server-name"]
            S2["command: executable path"]
            S3["args: [arguments]"]
            S4["env: {environment vars}"]
        end

        subgraph Types["Server Types"]
            T1["stdio: Local process"]
            T2["sse: HTTP streaming"]
            T3["websocket: WebSocket"]
        end
    end

    subgraph Example["Example Configuration"]
        E1["sap-docs-server"]
        E2["deepwiki-server"]
        E3["atlassian-server"]
    end
```

## PM Backend Abstraction

Project management backend architecture:

```mermaid
flowchart TB
    subgraph Interface["PM Interface"]
        I1["create_issue()"]
        I2["update_issue()"]
        I3["get_issues()"]
        I4["transition_issue()"]
        I5["add_comment()"]
    end

    subgraph Backends["Backend Implementations"]
        subgraph Jira["Jira Backend"]
            J1["REST API calls"]
            J2["Authentication"]
            J3["Field mapping"]
        end

        subgraph GitHub["GitHub Backend"]
            G1["GraphQL API"]
            G2["Token auth"]
            G3["Label mapping"]
        end

        subgraph Linear["Linear Backend"]
            L1["GraphQL API"]
            L2["API key auth"]
            L3["Status mapping"]
        end

        subgraph Local["Local Backend"]
            LC1["JSON file storage"]
            LC2["No auth required"]
            LC3["Simple schema"]
        end
    end

    Interface --> Backends
```

## PM Backend Selection

How the right backend is selected:

```mermaid
flowchart TD
    START([PM Operation Requested]) --> CHECK{Configuration exists?}

    CHECK -->|"No"| DEFAULT["Use local JSON backend"]
    CHECK -->|"Yes"| TYPE{Backend type?}

    TYPE -->|"jira"| JIRA["Initialize Jira client"]
    TYPE -->|"github"| GH["Initialize GitHub client"]
    TYPE -->|"linear"| LIN["Initialize Linear client"]
    TYPE -->|"local"| LOC["Initialize local storage"]

    JIRA & GH & LIN & LOC --> AUTH["Authenticate"]
    AUTH --> READY["Backend ready"]
```

## Git Integration

Git operations and workflows:

```mermaid
flowchart TB
    subgraph GitOps["Git Operations"]
        subgraph Safe["Safe Operations"]
            S1["status"]
            S2["diff"]
            S3["log"]
            S4["branch --list"]
        end

        subgraph Protected["Protected Operations"]
            P1["commit (on request)"]
            P2["push (on request)"]
            P3["branch create"]
        end

        subgraph Dangerous["Dangerous Operations"]
            D1["push --force (warn)"]
            D2["reset --hard (warn)"]
            D3["branch -D (warn)"]
        end
    end

    subgraph Safety["Safety Rules"]
        R1["Never auto-commit"]
        R2["Never force push to main"]
        R3["Always show diff first"]
    end

    GitOps --> Safety
```

## Society Verification Integration

How lib/society integrates:

```mermaid
flowchart TB
    subgraph Society["Society Verification System"]
        subgraph EventStore["Event Store"]
            ES1["Immutable events"]
            ES2["Hash chain"]
            ES3["Signatures"]
        end

        subgraph Verifiers["Axiom Verifiers"]
            V1["A0SDGVerifier"]
            V2["A1LoveVerifier"]
            V3["A2TruthVerifier"]
            V4["A3BeautyVerifier"]
            V5["A4GuardianVerifier"]
            V6["A5MemoryVerifier"]
        end

        subgraph Contracts["Agent Contracts"]
            C1["Capabilities"]
            C2["Obligations"]
            C3["Prohibitions"]
        end
    end

    subgraph Integration["Factory Integration"]
        I1["Agent actions logged"]
        I2["Axiom compliance verified"]
        I3["Trust scores maintained"]
    end

    Society --> Integration
```

## External Tool Integration

Development tool integrations:

```mermaid
flowchart TB
    subgraph Tools["Development Tools"]
        subgraph Docker["Docker"]
            D1["Container management"]
            D2["Image building"]
            D3["Compose orchestration"]
        end

        subgraph Cloud["Cloud Providers"]
            C1["AWS (boto3)"]
            C2["GCP (google-cloud)"]
            C3["Azure (azure-sdk)"]
        end

        subgraph CICD["CI/CD"]
            CI1["GitHub Actions"]
            CI2["GitLab CI"]
            CI3["Jenkins"]
        end
    end

    subgraph ToolConfig["Tool Configuration"]
        TC1["Path resolution"]
        TC2["Environment setup"]
        TC3["Credential management"]
    end

    Tools --> ToolConfig
```

## Authentication Flow

How external services are authenticated:

```mermaid
sequenceDiagram
    participant F as Factory
    participant CM as Credential Manager
    participant ENV as Environment
    participant KR as Keyring
    participant SVC as External Service

    F->>CM: Get credentials for service

    CM->>ENV: Check environment variable
    alt Env has credential
        ENV-->>CM: Credential value
    else Env empty
        CM->>KR: Check secure keyring
        alt Keyring has credential
            KR-->>CM: Credential value
        else Keyring empty
            CM-->>F: Prompt user
            F-->>CM: User provides credential
            CM->>KR: Store securely
        end
    end

    CM-->>F: Return credential
    F->>SVC: Authenticate with credential
    SVC-->>F: Authentication result
```

## MCP Tool Invocation

How MCP tools are called:

```mermaid
sequenceDiagram
    participant A as Agent
    participant MC as MCP Client
    participant MS as MCP Server
    participant EXT as External Resource

    A->>MC: Call MCP tool
    MC->>MC: Validate parameters
    MC->>MS: Send tool request

    MS->>MS: Process request
    MS->>EXT: Fetch external data
    EXT-->>MS: External data
    MS->>MS: Format response

    MS-->>MC: Tool response
    MC-->>A: Processed result
```

## Integration Error Handling

How integration errors are handled:

```mermaid
flowchart TD
    ERR([Integration Error]) --> TYPE{Error Type?}

    TYPE -->|"Auth failure"| AUTH["Re-authenticate"]
    TYPE -->|"Network error"| NET["Retry with backoff"]
    TYPE -->|"Rate limit"| RATE["Wait and retry"]
    TYPE -->|"Not found"| NF["Report missing resource"]
    TYPE -->|"Permission"| PERM["Request permission"]

    AUTH --> RETRY{Retry successful?}
    NET --> RETRY
    RATE --> RETRY

    RETRY -->|"Yes"| SUCCESS["Continue operation"]
    RETRY -->|"No"| FAIL["Report failure to user"]

    NF --> FAIL
    PERM --> FAIL
```

## Integration Configuration

Configuration for integrations:

```mermaid
flowchart TB
    subgraph Config["Integration Configuration"]
        subgraph MCP_Config["MCP Configuration"]
            MC1[".cursor/mcp.json"]
            MC2["Server definitions"]
            MC3["Environment variables"]
        end

        subgraph PM_Config["PM Configuration"]
            PM1["settings.json pm section"]
            PM2["Backend type"]
            PM3["Connection details"]
        end

        subgraph Tool_Config["Tool Configuration"]
            TC1["tools.json"]
            TC2["Path overrides"]
            TC3["Version requirements"]
        end
    end
```

## Webhook Integration

Event-driven integrations:

```mermaid
flowchart TB
    subgraph Triggers["Webhook Triggers"]
        T1["GitHub webhook"]
        T2["Jira webhook"]
        T3["CI/CD callback"]
    end

    subgraph Handler["Webhook Handler"]
        H1["Validate signature"]
        H2["Parse payload"]
        H3["Route to handler"]
        H4["Execute action"]
    end

    subgraph Actions["Triggered Actions"]
        A1["Start workflow"]
        A2["Update status"]
        A3["Generate report"]
        A4["Notify team"]
    end

    Triggers --> Handler --> Actions
```

## Integration Health Monitoring

Monitoring integration health:

```mermaid
flowchart TB
    subgraph Monitoring["Health Monitoring"]
        M1["Periodic health checks"]
        M2["Connection testing"]
        M3["Response time tracking"]
    end

    subgraph Status["Integration Status"]
        S1["Healthy: All connections OK"]
        S2["Degraded: Some issues"]
        S3["Unhealthy: Critical failure"]
    end

    subgraph Alerts["Alerting"]
        A1["Log warnings"]
        A2["Notify user"]
        A3["Fallback to alternatives"]
    end

    Monitoring --> Status --> Alerts
```
