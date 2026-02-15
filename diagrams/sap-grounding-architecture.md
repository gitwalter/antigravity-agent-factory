# SAP Grounding Architecture Diagrams

This document provides detailed diagrams of the SAP-specific grounding system, including the 5-layer architecture and specialized skill hierarchy.

## 5-Layer Grounding Architecture

The grounding system uses a tiered approach for verification, starting with fast cached lookups and escalating to more thorough verification:

```mermaid
flowchart TB
    subgraph Query["Grounding Query"]
        Q["Verify: Does table BSEG have field DMBTR?"]
    end

    subgraph L1["Layer 1: Knowledge Cache"]
        L1D["knowledge/*.json"]
        L1C["Instant lookup"]
        L1R["HIGH confidence"]
    end

    subgraph L2["Layer 2: SAP Documentation"]
        L2D["SAP Help Portal (MCP)"]
        L2C["Fast lookup"]
        L2R["HIGH confidence"]
    end

    subgraph L3["Layer 3: Reference Repositories"]
        L3D["abap-cheat-sheets, code samples"]
        L3C["DeepWiki MCP"]
        L3R["MEDIUM confidence"]
    end

    subgraph L4["Layer 4: Project Specifications"]
        L4D["Confluence, Excel mappings"]
        L4C["Atlassian MCP"]
        L4R["HIGH project-specific"]
    end

    subgraph L5["Layer 5: Strawberry Verification"]
        L5D["Two-pass verification"]
        L5C["Hallucination detection"]
        L5R["Final verification"]
    end

    Q --> L1
    L1 -->|"Not found"| L2
    L2 -->|"Not found"| L3
    L3 -->|"Not found"| L4
    L4 --> L5

    L1 -->|"Found"| RESULT
    L2 -->|"Found"| RESULT
    L3 -->|"Found"| RESULT
    L4 -->|"Found"| L5

    L5 --> RESULT["Grounding Result"]

    style L1 fill:#c8e6c9
    style L2 fill:#a5d6a7
    style L3 fill:#fff9c4
    style L4 fill:#ffcc80
    style L5 fill:#ce93d8
    style RESULT fill:#e3f2fd
```

## SAP Grounding Skill Hierarchy

The SAP grounding coordinator delegates to specialized skills based on artifact type:

```mermaid
flowchart TB
    subgraph Coordinator["sap-grounding (Coordinator)"]
        COORD["Analyzes artifact type<br/>Routes to specialist"]
    end

    subgraph DDIC["Data Dictionary"]
        DDIC_S["ddic-grounding"]
        DDIC_A["Tables, structures,<br/>data elements, domains"]
    end

    subgraph CDS["Core Data Services"]
        CDS_S["cds-grounding"]
        CDS_A["CDS views, annotations,<br/>access control (DCL)"]
    end

    subgraph RAP["RESTful ABAP"]
        RAP_S["rap-grounding"]
        RAP_A["Behavior definitions,<br/>actions, validations"]
    end

    subgraph OO["ABAP OO"]
        OO_S["class-grounding"]
        OO_A["Classes, interfaces,<br/>exception classes"]
    end

    subgraph FM["Function Modules"]
        FM_S["function-grounding"]
        FM_A["Function modules,<br/>BAPIs, RFCs"]
    end

    subgraph API["APIs"]
        API_S["api-grounding"]
        API_A["OData services,<br/>service bindings"]
    end

    COORD --> DDIC_S
    COORD --> CDS_S
    COORD --> RAP_S
    COORD --> OO_S
    COORD --> FM_S
    COORD --> API_S

    DDIC_S --> DDIC_A
    CDS_S --> CDS_A
    RAP_S --> RAP_A
    OO_S --> OO_A
    FM_S --> FM_A
    API_S --> API_A

    style Coordinator fill:#e3f2fd
    style DDIC fill:#c8e6c9
    style CDS fill:#a5d6a7
    style RAP fill:#fff9c4
    style OO fill:#ffcc80
    style FM fill:#ce93d8
    style API fill:#f48fb1
```

## Complete SAP Skill Map

```mermaid
flowchart TB
    subgraph Core["Core Skills"]
        SAP["sap-grounding"]
        STRAW["strawberry-verification"]
    end

    subgraph Technical["Technical Grounding"]
        DDIC["ddic-grounding"]
        CDS["cds-grounding"]
        RAP["rap-grounding"]
        CLASS["class-grounding"]
        FUNC["function-grounding"]
        API["api-grounding"]
    end

    subgraph Support["Support Grounding"]
        ENH["enhancement-grounding"]
        MSG["message-grounding"]
        AUTH["authorization-grounding"]
        MAP["mapping-grounding"]
        EXIST["existence-grounding"]
        FIORI["fiori-grounding"]
    end

    SAP --> DDIC
    SAP --> CDS
    SAP --> RAP
    SAP --> CLASS
    SAP --> FUNC
    SAP --> API
    SAP --> ENH
    SAP --> MSG
    SAP --> AUTH
    SAP --> MAP
    SAP --> EXIST
    SAP --> FIORI

    DDIC --> STRAW
    CDS --> STRAW
    RAP --> STRAW
    CLASS --> STRAW
    FUNC --> STRAW
    API --> STRAW

    style Core fill:#e3f2fd
    style Technical fill:#e8f5e9
    style Support fill:#fff3e0
```

## SAP Artifact Verification Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Agent as Grounding Agent
    participant Coord as sap-grounding
    participant Spec as Specialist Skill
    participant Cache as Knowledge Cache
    participant Docs as SAP Documentation
    participant Verify as strawberry-verification

    Dev->>Agent: Create BAPI wrapper for BAPI_USER_GET_DETAIL
    Agent->>Coord: Verify BAPI exists

    Coord->>Spec: Route to function-grounding
    Spec->>Cache: Check function-catalog.json

    alt Found in cache
        Cache-->>Spec: Return cached signature
    else Not in cache
        Spec->>Docs: Search SAP Help Portal
        Docs-->>Spec: Return documentation
        Spec->>Cache: Cache for future
    end

    Spec->>Verify: Verify with Strawberry
    Verify->>Verify: Scrubbed test
    Verify->>Verify: Full test
    Verify-->>Spec: VERIFIED

    Spec-->>Coord: Verification complete
    Coord-->>Agent: Grounding result
    Agent-->>Dev: Proceed with verified parameters
```

## MCP Server Integration

```mermaid
flowchart LR
    subgraph Skills["Grounding Skills"]
        S1["ddic-grounding"]
        S2["cds-grounding"]
        S3["class-grounding"]
        S4["mapping-grounding"]
    end

    subgraph MCP["MCP Servers"]
        subgraph SAP["sap-documentation"]
            SAP_T1["search"]
            SAP_T2["fetch"]
            SAP_T3["sap_help_search"]
        end

        subgraph ATL["atlassian"]
            ATL_T1["getConfluencePage"]
            ATL_T2["searchConfluenceUsingCql"]
            ATL_T3["getJiraIssue"]
        end

        subgraph DW["deepwiki"]
            DW_T1["ask_question"]
            DW_T2["read_wiki_contents"]
        end
    end

    S1 --> SAP
    S2 --> SAP
    S3 --> SAP
    S3 --> DW
    S4 --> ATL

    style Skills fill:#e3f2fd
    style MCP fill:#e8f5e9
```

## Grounding Result Format

```mermaid
flowchart TB
    subgraph Report["Grounding Verification Report"]
        ID["Verification ID: UUID<br/>Timestamp: ISO-8601"]

        subgraph Metrics["Metrics"]
            M1["Total Artifacts: N"]
            M2["Verified HIGH: X"]
            M3["Verified MEDIUM: Y"]
            M4["Unverified: Z"]
            M5["Issues: W"]
        end

        subgraph Strawberry["Strawberry Status"]
            SS["PASSED / WARNING / FAILED"]
        end

        subgraph Rec["Recommendation"]
            R["PROCEED / PROCEED_WITH_WARNINGS / STOP / ASK_USER"]
        end

        REASON["Reason: Detailed explanation"]
    end

    ID --> Metrics --> Strawberry --> Rec --> REASON

    style Report fill:#f5f5f5
    style Metrics fill:#e3f2fd
    style Strawberry fill:#f3e5f5
    style Rec fill:#e8f5e9
```

## Release Contract Verification (C0/C1/C2)

```mermaid
flowchart TD
    subgraph Input["Object to Verify"]
        OBJ["CL_* / IF_* / TA* / etc."]
    end

    subgraph Check["existence-grounding"]
        C1["Check TADIR entry"]
        C2["Check release contract"]
        C3["Check ABAP Cloud compatibility"]
    end

    subgraph Status["Release Status"]
        C0["C0: Not Released<br/>⚠ Use at own risk"]
        C1S["C1: Released for Key Users<br/>◐ Limited use"]
        C2S["C2: Released for All<br/>✓ Safe to use"]
        DEP["Deprecated<br/>✗ Avoid using"]
    end

    subgraph Action["Action"]
        OK["✓ Proceed"]
        WARN["⚠ Proceed with warning"]
        ALT["🔄 Find alternative"]
        STOP["✗ Do not use"]
    end

    OBJ --> C1 --> C2 --> C3

    C3 --> C0 --> WARN
    C3 --> C1S --> WARN
    C3 --> C2S --> OK
    C3 --> DEP --> ALT

    style C0 fill:#fff9c4
    style C1S fill:#ffcc80
    style C2S fill:#c8e6c9
    style DEP fill:#ef9a9a
```

## Example: DDIC Grounding Flow

```mermaid
flowchart TB
    subgraph Request["Verification Request"]
        REQ["Verify: BSEG-DMBTR exists<br/>and is CURR type"]
    end

    subgraph Process["ddic-grounding Process"]
        S1["Step 1: Check ddic-catalog.json"]
        S2["Step 2: Search SAP Help Portal"]
        S3["Step 3: Verify field properties"]
        S4["Step 4: Check data element"]
        S5["Step 5: Verify domain"]
    end

    subgraph Evidence["Evidence Collected"]
        E1["S0: BSEG is transparent table"]
        E2["S1: DMBTR field exists"]
        E3["S2: Type DMBTR (data element)"]
        E4["S3: Domain BAPICURR, CURR(23,2)"]
    end

    subgraph Verify["Strawberry Verification"]
        V1["Scrub: {TABLE}-{FIELD} of type {TYPE}"]
        V2["Full: BSEG-DMBTR of type CURR"]
        V3["Result: VERIFIED ✓"]
    end

    subgraph Output["Grounding Result"]
        OUT["Structure: BSEG<br/>Field: DMBTR<br/>Verified: ✓<br/>Source: SAP Help Portal"]
    end

    REQ --> S1
    S1 -->|"Not in cache"| S2
    S2 --> S3 --> S4 --> S5

    S2 --> E1
    S3 --> E2
    S4 --> E3
    S5 --> E4

    E1 --> V1
    E2 --> V1
    E3 --> V1
    E4 --> V1

    V1 --> V2 --> V3 --> OUT

    style Request fill:#e3f2fd
    style Process fill:#fff3e0
    style Evidence fill:#e8f5e9
    style Verify fill:#f3e5f5
    style Output fill:#c8e6c9
```
