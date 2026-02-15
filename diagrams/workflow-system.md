# Workflow System Architecture Diagrams

This document contains the architectural diagrams for the Cursor Agent Factory Workflow System.

## Entity Relationship Diagram

Shows how workflow entities relate to each other.

```mermaid
erDiagram
    WORKFLOW ||--o{ PHASE : contains
    WORKFLOW ||--o{ TRIGGER : activatedBy
    WORKFLOW }o--o{ KNOWLEDGE : references
    WORKFLOW ||--o{ MCP_REQUIREMENT : requires
    WORKFLOW ||--o{ LEARNING_HOOK : generates

    PHASE ||--o{ STEP : contains
    PHASE ||--o{ DECISION_POINT : mayHave
    PHASE ||--o{ ESCALATION : mayTrigger

    STEP }o--|| SKILL : invokes
    STEP ||--o{ ACTION : executes
    STEP ||--o{ OUTPUT : produces
    STEP }o--o{ MCP_TOOL : uses

    DECISION_POINT ||--o{ BRANCH : contains
    BRANCH }o--|| PHASE : goesTo

    MCP_REQUIREMENT }o--|| MCP_SERVER : references
    MCP_SERVER ||--o{ MCP_TOOL : provides

    SKILL }o--o{ KNOWLEDGE : uses
    SKILL }o--o{ MCP_SERVER : mayRequire
```

## Workflow Lifecycle State Machine

Shows all possible states and transitions during workflow execution.

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Triggered: trigger_received
    Triggered --> Validating: begin_workflow

    Validating --> Initializing: context_valid
    Validating --> Failed: context_invalid

    Initializing --> Executing: state_loaded
    Initializing --> AcquiringMCP: mcp_missing

    AcquiringMCP --> Initializing: mcp_ready
    AcquiringMCP --> NeedsAuth: auth_required
    NeedsAuth --> AcquiringMCP: auth_provided
    NeedsAuth --> Failed: auth_timeout

    Executing --> StepComplete: step_finished
    StepComplete --> Executing: next_step
    StepComplete --> DecisionPoint: decision_needed
    StepComplete --> PhaseComplete: phase_finished

    DecisionPoint --> Executing: branch_selected
    DecisionPoint --> Researching: needs_info
    DecisionPoint --> Escalating: needs_human

    Researching --> DecisionPoint: info_gathered
    Researching --> Escalating: research_failed

    Escalating --> Executing: user_responded
    Escalating --> Paused: user_requested_pause
    Escalating --> Cancelled: user_cancelled

    Paused --> Executing: user_resumed
    Paused --> Cancelled: user_cancelled

    PhaseComplete --> Executing: next_phase
    PhaseComplete --> Verifying: all_phases_complete

    Verifying --> Learning: verification_passed
    Verifying --> Executing: verification_failed

    Learning --> Completed: lessons_stored

    Completed --> [*]
    Failed --> [*]
    Cancelled --> [*]
```

## MCP Server Orchestration Flow

Shows how workflows dynamically acquire and manage MCP server capabilities.

```mermaid
flowchart TB
    subgraph Detection [Capability Detection]
        A[Workflow declares MCP requirement]
        B{Server installed?}
        C{Server authenticated?}
        D[Query mcp-servers-catalog.json]
    end

    subgraph Acquisition [Capability Acquisition]
        E[Prompt user for installation]
        F[Guide authentication setup]
        G[Store credentials securely]
    end

    subgraph Activation [Runtime Management]
        H[Enable server for workflow]
        I[Use MCP tools]
        J[Disable after workflow]
        K[Maintain connection pool]
    end

    A --> B
    B -->|No| D
    D --> E
    E --> B
    B -->|Yes| C
    C -->|No| F
    F --> G
    G --> C
    C -->|Yes| H
    H --> I
    I --> J

    subgraph Fallback [Fallback Handling]
        L{Fallback defined?}
        M[Try fallback server]
        N[Continue without]
        O[Fail workflow]
    end

    B -->|Not available| L
    L -->|Yes| M
    M --> B
    L -->|No, optional| N
    L -->|No, required| O
```

## Learning Loop Architecture

Shows how workflows capture and apply learnings for continuous improvement.

```mermaid
flowchart TB
    subgraph Capture [Event Capture]
        A1[Successful Resolution]
        A2[Failed Attempt]
        A3[Novel Error Pattern]
        A4[User Correction]
    end

    subgraph Analysis [Pattern Analysis]
        B1[Extract Signature]
        B2[Classify Category]
        B3[Correlate Context]
        B4[Calculate Confidence]
    end

    subgraph Storage [Knowledge Update]
        C1[error-patterns.json]
        C2[fix-strategies.json]
        C3[lessons-learned.json]
    end

    subgraph Application [Future Application]
        D1[Pattern Matching]
        D2[Strategy Selection]
        D3[Confidence Scoring]
        D4[Autonomous Fix]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1

    B1 --> B2
    B2 --> B3
    B3 --> B4

    B4 --> C1
    B4 --> C2
    B4 --> C3

    C1 --> D1
    C2 --> D2
    C3 --> D3
    D3 --> D4

    D4 -.->|feedback| A1
    D4 -.->|feedback| A2
```

## Escalation Decision Tree

Shows how workflows decide when and how to involve humans.

```mermaid
flowchart TB
    A[Decision Point Reached]

    A --> B{Confidence >= 0.8?}
    B -->|Yes| C[Proceed Autonomously]
    B -->|No| D{Action Reversible?}

    D -->|Yes| E{Confidence >= 0.5?}
    E -->|Yes| F[Proceed with Logging]
    E -->|No| G[Escalate: Low Confidence]

    D -->|No| H{Confidence >= 0.7?}
    H -->|Yes| I[Escalate: Confirm Before Proceed]
    H -->|No| J[Escalate: Require Approval]

    C --> K[Execute Action]
    F --> K

    G --> L[Present Options to User]
    I --> L
    J --> L

    L --> M{User Decision}
    M -->|Approve| K
    M -->|Modify| N[Apply Modifications]
    N --> K
    M -->|Reject| O[Abort/Alternative]
    M -->|More Info| P[Expand Context]
    P --> L
```

## Workflow Hierarchy

Shows the structural hierarchy of workflow entities.

```mermaid
flowchart TB
    subgraph Workflow [Workflow Definition]
        W[Workflow]
        W --> T[Triggers]
        W --> C[Context]
        W --> M[MCP Requirements]
        W --> K[Knowledge]
    end

    subgraph Phases [Execution Phases]
        W --> P1[Phase 1]
        W --> P2[Phase 2]
        W --> P3[Phase N]
    end

    subgraph Steps [Phase Steps]
        P1 --> S1[Step 1]
        P1 --> S2[Step 2]
        S1 --> SK[Skill]
        S1 --> MT[MCP Tools]
        S1 --> O[Outputs]
    end

    subgraph Control [Control Flow]
        W --> DP[Decision Points]
        W --> ES[Escalations]
        W --> LH[Learning Hooks]
        DP --> BR[Branches]
    end
```

## Quick Reference

### Workflow Lifecycle

```mermaid
flowchart LR
    T[Trigger] --> I[Initialize] --> E[Execute] --> V[Verify] --> L[Learn] --> C[Complete]
```

### Entity Flow

```mermaid
flowchart LR
    W[Workflow] --> P[Phase] --> S[Step] --> SK[Skill] --> A[Action]
```

### Learning Flow

```mermaid
flowchart LR
    O[Outcome] --> C[Capture] --> S[Store] --> A[Apply]
```

## Related Documents

- **WORKFLOW_SYSTEM.md** - Conceptual architecture
- **WORKFLOW_AUTHORING.md** - Authoring guide
- **w-o-r-k-f-l-o-w-patterns.md** - Pattern catalog
