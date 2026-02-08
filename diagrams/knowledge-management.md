# Knowledge Management Architecture

This document visualizes the knowledge file structure, evolution system, and query patterns that power the Factory's domain knowledge.

## Quick Reference

```mermaid
flowchart LR
    S[Sources] --> A[Aggregate] --> M[Merge] --> K[Knowledge Files]
    K --> Q[Query] --> R[Results]
```

## Knowledge File Structure

Organization of the 89+ knowledge files:

```mermaid
flowchart TB
    subgraph Knowledge["knowledge/ Directory"]
        subgraph Stack["Stack-Specific (40+)"]
            S1["fastapi-patterns.json"]
            S2["nextjs-patterns.json"]
            S3["spring-patterns.json"]
            S4["dotnet-patterns.json"]
            S5["..."]
        end
        
        subgraph AI["AI/Agent Patterns (15+)"]
            A1["langchain-patterns.json"]
            A2["langgraph-patterns.json"]
            A3["crewai-patterns.json"]
            A4["agent-coordination.json"]
            A5["..."]
        end
        
        subgraph Integration["Integration Patterns (10+)"]
            I1["sap-cap-patterns.json"]
            I2["sap-rap-patterns.json"]
            I3["mcp-servers-catalog.json"]
            I4["..."]
        end
        
        subgraph Meta["Factory Metadata (10+)"]
            M1["skill-catalog.json"]
            M2["stack-capabilities.json"]
            M3["workflow-patterns.json"]
            M4["..."]
        end
    end
```

## Knowledge File Schema

Structure of individual knowledge files:

```mermaid
classDiagram
    class KnowledgeFile {
        +String id
        +String name
        +String description
        +String version
        +Array~Pattern~ patterns
        +Object metadata
    }
    
    class Pattern {
        +String id
        +String name
        +String description
        +String category
        +Object implementation
        +Array~String~ tags
        +Number confidence
    }
    
    class Implementation {
        +String language
        +String code
        +Array~String~ dependencies
        +Object configuration
    }
    
    KnowledgeFile --> Pattern : contains
    Pattern --> Implementation : has
```

## Knowledge Evolution Architecture

How knowledge is automatically updated from sources:

```mermaid
flowchart TB
    subgraph Sources["Update Sources"]
        GH["GitHub<br/>Repository changes"]
        PY["PyPI<br/>Package updates"]
        NP["NPM<br/>Node packages"]
        DOC["Documentation<br/>Official docs"]
        COM["Community<br/>Blog posts, tutorials"]
    end
    
    subgraph Evolution["Knowledge Evolution Agent"]
        subgraph Adapters["Source Adapters"]
            GA["GitHub Adapter"]
            PA["PyPI Adapter"]
            NA["NPM Adapter"]
            DA["Docs Adapter"]
            CA["Community Adapter"]
        end
        
        AGG["Aggregator<br/>Deduplicate, normalize"]
        PRI["Priority Scorer<br/>Rank by importance"]
        VAL["Validator<br/>Check for conflicts"]
    end
    
    subgraph Output["Update Output"]
        UPD["Pending Updates"]
        NOT["User Notification"]
        MRG["Merge Engine"]
    end
    
    Sources --> Adapters
    Adapters --> AGG --> PRI --> VAL --> Output
```

## Update Aggregation Flow

How updates from multiple sources are combined:

```mermaid
flowchart TB
    subgraph Incoming["Incoming Updates"]
        U1["Update from GitHub"]
        U2["Update from PyPI"]
        U3["Update from Docs"]
    end
    
    subgraph Dedup["Deduplication"]
        D1["Compare by content hash"]
        D2["Merge similar updates"]
        D3["Keep highest confidence"]
    end
    
    subgraph Priority["Priority Scoring"]
        P1["Source trust level"]
        P2["Update recency"]
        P3["User relevance"]
        P4["Breaking change flag"]
    end
    
    subgraph Ranking["Final Ranking"]
        R["Priority Queue<br/>Highest first"]
    end
    
    Incoming --> Dedup --> Priority --> Ranking
```

## Merge Strategies

How conflicting updates are resolved:

```mermaid
flowchart TB
    subgraph Conflict["Conflict Detected"]
        C1["Existing: version A"]
        C2["Incoming: version B"]
    end
    
    subgraph Strategies["Merge Strategies"]
        S1["BALANCED<br/>Merge both, prefer incoming for new fields"]
        S2["INCOMING<br/>Replace with incoming entirely"]
        S3["EXISTING<br/>Keep existing, ignore incoming"]
        S4["USER_DECIDE<br/>Present options to user"]
    end
    
    subgraph Decision["Strategy Selection"]
        D1["Breaking change? → USER_DECIDE"]
        D2["Non-breaking update? → BALANCED"]
        D3["User customization exists? → EXISTING"]
        D4["Fresh install? → INCOMING"]
    end
    
    Conflict --> Decision --> Strategies
```

## Query Flow

How agents query knowledge files:

```mermaid
sequenceDiagram
    participant A as Agent
    participant S as Skill
    participant K as Knowledge Manager
    participant F as Knowledge Files
    participant C as Cache
    
    A->>S: Execute skill
    S->>K: Query for pattern
    
    K->>C: Check cache
    alt Cache Hit
        C-->>K: Cached result
    else Cache Miss
        K->>F: Load relevant files
        F-->>K: File contents
        K->>K: Filter by query
        K->>C: Update cache
    end
    
    K-->>S: Query results
    S-->>A: Pattern applied
```

## Knowledge Query Patterns

Common query types and their resolution:

```mermaid
flowchart TB
    subgraph Queries["Query Types"]
        Q1["By ID<br/>Exact pattern lookup"]
        Q2["By Tag<br/>Find all with tag"]
        Q3["By Category<br/>Filter by category"]
        Q4["Semantic<br/>Natural language search"]
    end
    
    subgraph Resolution["Resolution Method"]
        R1["Direct index lookup"]
        R2["Tag index scan"]
        R3["Category filter"]
        R4["Embedding similarity"]
    end
    
    subgraph Result["Result Format"]
        RES["Array of matching patterns<br/>Sorted by relevance"]
    end
    
    Q1 --> R1 --> RES
    Q2 --> R2 --> RES
    Q3 --> R3 --> RES
    Q4 --> R4 --> RES
```

## Agent-Skill-Knowledge Relationship

How components interact with knowledge:

```mermaid
flowchart TB
    subgraph Agents["Agents"]
        A1["requirements-architect"]
        A2["stack-builder"]
        A3["template-generator"]
    end
    
    subgraph Skills["Skills"]
        S1["stack-configuration"]
        S2["template-generation"]
        S3["pattern-feedback"]
    end
    
    subgraph Knowledge["Knowledge Files"]
        K1["stack-capabilities.json"]
        K2["fastapi-patterns.json"]
        K3["workflow-patterns.json"]
    end
    
    A1 -->|"uses"| S1
    A2 -->|"uses"| S1 & S2
    A3 -->|"uses"| S2
    
    S1 -->|"queries"| K1
    S2 -->|"queries"| K2
    S3 -->|"updates"| K1 & K2 & K3
```

## Knowledge Versioning

How knowledge file versions are managed:

```mermaid
flowchart TB
    subgraph Versioning["Version Management"]
        V1["Version in file metadata"]
        V2["Changelog in comments"]
        V3["Git history for full audit"]
    end
    
    subgraph Compatibility["Compatibility"]
        C1["Schema version check"]
        C2["Backward compatibility"]
        C3["Migration scripts if needed"]
    end
    
    subgraph Rollback["Rollback Capability"]
        R1["Git revert for any version"]
        R2["User can reject updates"]
        R3["Backup before merge"]
    end
    
    Versioning --> Compatibility --> Rollback
```

## Conflict Detection and Resolution

Detailed conflict handling:

```mermaid
flowchart TD
    START([Merge Initiated]) --> CHECK{Conflict exists?}
    
    CHECK -->|No| MERGE["Direct merge"]
    CHECK -->|Yes| ANALYZE["Analyze conflict type"]
    
    ANALYZE --> TYPE{Conflict Type?}
    
    TYPE -->|"Value differs"| VAL["Compare values"]
    TYPE -->|"Structure differs"| STR["Compare schemas"]
    TYPE -->|"Deleted vs Modified"| DEL["Deletion conflict"]
    
    VAL --> USER_CUSTOM{User customization?}
    USER_CUSTOM -->|Yes| PRESERVE["Preserve user value"]
    USER_CUSTOM -->|No| INCOMING["Use incoming value"]
    
    STR --> MIGRATION["Generate migration"]
    DEL --> ASK["Ask user"]
    
    PRESERVE & INCOMING & MIGRATION & ASK --> COMPLETE([Merge Complete])
```

## Knowledge Evolution Supervisor-Worker

Detailed architecture of the evolution system:

```mermaid
flowchart TB
    subgraph Supervisor["Knowledge Evolution Agent"]
        SCHED["Scheduler<br/>Periodic checks"]
        COORD["Coordinator<br/>Dispatch to workers"]
        AGG["Aggregator<br/>Collect results"]
        MERGE["Merger<br/>Apply updates"]
    end
    
    subgraph Workers["Source Adapter Workers"]
        subgraph GitHub["GitHub Adapter"]
            GH1["Watch repositories"]
            GH2["Detect changes"]
            GH3["Extract patterns"]
        end
        
        subgraph PyPI["PyPI Adapter"]
            PY1["Check package versions"]
            PY2["Fetch changelogs"]
            PY3["Update dependencies"]
        end
        
        subgraph NPM["NPM Adapter"]
            NP1["Monitor packages"]
            NP2["Check security advisories"]
            NP3["Update versions"]
        end
    end
    
    SCHED --> COORD
    COORD -->|"dispatch"| GitHub & PyPI & NPM
    GitHub & PyPI & NPM -->|"results"| AGG
    AGG --> MERGE
```

## Subscription-Based Filtering

How users can customize knowledge updates:

```mermaid
flowchart TB
    subgraph Subscriptions["User Subscriptions"]
        S1["Stack subscriptions<br/>(Python, TypeScript, etc.)"]
        S2["Framework subscriptions<br/>(FastAPI, Next.js, etc.)"]
        S3["Domain subscriptions<br/>(AI, Blockchain, SAP, etc.)"]
    end
    
    subgraph Filter["Update Filter"]
        F1["Match against subscriptions"]
        F2["Filter by relevance"]
        F3["Prioritize by usage"]
    end
    
    subgraph Delivery["Update Delivery"]
        D1["Immediate: Breaking changes"]
        D2["Batched: Regular updates"]
        D3["Deferred: Low priority"]
    end
    
    Subscriptions --> Filter --> Delivery
```

## Knowledge Cache Architecture

Caching for performance:

```mermaid
flowchart TB
    subgraph Cache["Cache Layers"]
        L1["L1: In-memory<br/>Current session"]
        L2["L2: File index<br/>Quick lookup"]
        L3["L3: Full files<br/>Disk storage"]
    end
    
    subgraph Invalidation["Cache Invalidation"]
        I1["TTL-based expiry"]
        I2["Change detection"]
        I3["Manual refresh"]
    end
    
    subgraph Query["Query Resolution"]
        Q["Query received"]
        Q --> L1
        L1 -->|miss| L2
        L2 -->|miss| L3
        L3 --> L2 --> L1
    end
```

## Knowledge File Categories

Complete categorization:

```mermaid
flowchart LR
    subgraph Categories["Knowledge Categories"]
        C1["Stack Patterns<br/>Language/framework specific"]
        C2["Agent Patterns<br/>AI agent architectures"]
        C3["Integration Patterns<br/>External system integration"]
        C4["Workflow Patterns<br/>Development methodologies"]
        C5["Security Patterns<br/>Security best practices"]
        C6["Factory Metadata<br/>Factory configuration"]
    end
    
    subgraph Examples["Examples"]
        E1["fastapi-patterns.json<br/>nextjs-patterns.json"]
        E2["langchain-patterns.json<br/>agent-coordination.json"]
        E3["sap-cap-patterns.json<br/>mcp-servers-catalog.json"]
        E4["workflow-patterns.json<br/>agile-patterns.json"]
        E5["security-patterns.json<br/>authentication-patterns.json"]
        E6["skill-catalog.json<br/>stack-capabilities.json"]
    end
    
    C1 --> E1
    C2 --> E2
    C3 --> E3
    C4 --> E4
    C5 --> E5
    C6 --> E6
```

## Knowledge Quality Metrics

How knowledge quality is measured:

```mermaid
flowchart TB
    subgraph Metrics["Quality Metrics"]
        M1["Freshness<br/>Last update date"]
        M2["Usage<br/>Query frequency"]
        M3["Accuracy<br/>User feedback"]
        M4["Completeness<br/>Coverage score"]
        M5["Consistency<br/>Cross-file validation"]
    end
    
    subgraph Actions["Quality Actions"]
        A1["Flag stale knowledge"]
        A2["Prioritize updates"]
        A3["Deprecate unused"]
        A4["Request contributions"]
    end
    
    M1 & M2 & M3 & M4 & M5 --> Actions
```
