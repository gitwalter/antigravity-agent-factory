# Security Pipeline Architecture

This document visualizes the multi-layer security validation system that protects users, their data, and system integrity.

## Quick Reference

```mermaid
flowchart LR
    C[Command] --> A[Axiom Check] --> H[Harm Detection] --> S[Secret Scan] --> M[Mutability Guard] --> E[Execute/Block]
```

## Multi-Layer Validation Pipeline

Complete security check flow:

```mermaid
flowchart TB
    subgraph Input["Input"]
        CMD["Command/Action"]
    end

    subgraph Layer1["Layer 1: Axiom Checker"]
        AC["axiom_checker.py"]
        AC1["Pattern-based violation detection"]
        AC2["Severity classification (0-4)"]
        AC3["Axiom source identification"]
    end

    subgraph Layer2["Layer 2: Harm Detector"]
        HD["harm_detector.py"]
        HD1["Combines multiple checks"]
        HD2["Irreversibility assessment"]
        HD3["Consent requirement check"]
    end

    subgraph Layer3["Layer 3: Secret Scanner"]
        SS["secret_scanner.py"]
        SS1["30+ secret patterns"]
        SS2["Severity classification"]
        SS3["File path analysis"]
    end

    subgraph Layer4["Layer 4: Mutability Guard"]
        MG["mutability_guard.py"]
        MG1["Layer protection (L0-L2)"]
        MG2["File modification tracking"]
        MG3["Immutability enforcement"]
    end

    subgraph Output["Output"]
        PASS["Execute: ALLOWED"]
        WARN["Execute: WITH WARNINGS"]
        BLOCK["Execute: BLOCKED"]
    end

    Input --> Layer1 --> Layer2 --> Layer3 --> Layer4 --> Output
```

## Axiom Checker Detail

Pattern-based axiom violation detection:

```mermaid
flowchart TB
    subgraph Input["Input Analysis"]
        CMD["Command text"]
        CTX["Context (file, action)"]
    end

    subgraph Patterns["Violation Patterns"]
        P1["A1 Transparency Violations<br/>Hidden actions, unexplained changes"]
        P2["A2 User Primacy Violations<br/>Override user intent, force actions"]
        P3["A4 Non-Harm Violations<br/>Delete without backup, expose secrets"]
        P4["A5 Consistency Violations<br/>Contradictory rules, circular deps"]
    end

    subgraph Scoring["Severity Scoring"]
        S0["Level 0: Flow<br/>No issue detected"]
        S1["Level 1: Nudge<br/>Minor concern"]
        S2["Level 2: Pause<br/>Needs explanation"]
        S3["Level 3: Block<br/>Clear violation"]
        S4["Level 4: Protect<br/>Imminent harm"]
    end

    Input --> Patterns --> Scoring
```

## Harm Detection System

Comprehensive harm assessment:

```mermaid
flowchart TB
    subgraph Checks["Harm Detection Checks"]
        C1["Axiom compliance check"]
        C2["Secret exposure check"]
        C3["Destructive action check"]
        C4["Irreversibility check"]
    end

    subgraph Categories["Harm Categories"]
        CAT1["dataLoss<br/>Loss of user data"]
        CAT2["securityBreach<br/>Exposure of secrets"]
        CAT3["systemDamage<br/>Damage to system"]
        CAT4["deception<br/>Misleading the user"]
    end

    subgraph Assessment["Assessment Result"]
        ASS["HarmAssessment"]
        A1["category: HarmCategory"]
        A2["isIrreversible: Bool"]
        A3["hasConsent: Bool"]
        A4["severity: 0-4"]
    end

    Checks --> Categories --> Assessment
```

## Secret Scanner Patterns

30+ patterns for detecting exposed secrets:

```mermaid
flowchart TB
    subgraph Patterns["Secret Patterns"]
        subgraph API["API Keys"]
            API1["AWS Access Key<br/>Prefix pattern + 16 chars"]
            API2["Google API Key<br/>Prefix pattern + 35 chars"]
            API3["GitHub Token<br/>Prefix pattern + 36 chars"]
            API4["Stripe Key<br/>Prefix pattern + 24 chars"]
        end

        subgraph Auth["Authentication"]
            AUTH1["JWT Token<br/>Base64 encoded header"]
            AUTH2["Bearer Token<br/>Authorization header"]
            AUTH3["Basic Auth<br/>Base64 encoded"]
        end

        subgraph DB["Database"]
            DB1["PostgreSQL Connection<br/>URI with credentials"]
            DB2["MongoDB URI<br/>URI with credentials"]
            DB3["Redis URL<br/>URI with credentials"]
        end

        subgraph Cloud["Cloud Credentials"]
            CL1["Azure Key<br/>Service principal"]
            CL2["GCP Key<br/>Service account"]
            CL3["Private Key<br/>PEM format"]
        end
    end

    subgraph Severity["Severity Classification"]
        HIGH["HIGH: Active credentials"]
        MED["MEDIUM: Potentially sensitive"]
        LOW["LOW: Possibly harmless"]
    end

    Patterns --> Severity
```

## Mutability Guard

Layer protection enforcement:

```mermaid
flowchart TB
    subgraph Layers["5-Layer Architecture"]
        L0["Layer 0: Axioms<br/>IMMUTABLE"]
        L1["Layer 1: Purpose<br/>IMMUTABLE"]
        L2["Layer 2: Principles<br/>IMMUTABLE"]
        L3["Layer 3: Methodology<br/>MUTABLE"]
        L4["Layer 4: Technical<br/>MUTABLE"]
    end

    subgraph Operations["Operation Types"]
        OP1["READ: Always allowed"]
        OP2["MODIFY: Check layer"]
        OP3["DELETE: Check layer"]
        OP4["CREATE: Check layer"]
    end

    subgraph Guard["Mutability Guard"]
        CHK["Check target layer"]

        subgraph L0L2["L0-L2 Protection"]
            BLOCK_L["BLOCKED<br/>Cannot modify immutable layers"]
        end

        subgraph L3L4["L3-L4 Allowed"]
            ALLOW_L["ALLOWED<br/>Can modify mutable layers"]
        end
    end

    Operations --> CHK
    CHK -->|"L0, L1, L2"| BLOCK_L
    CHK -->|"L3, L4"| ALLOW_L
```

## Security Check Sequence

Complete security validation sequence:

```mermaid
sequenceDiagram
    participant C as Command
    participant AC as Axiom Checker
    participant HD as Harm Detector
    participant SS as Secret Scanner
    participant MG as Mutability Guard
    participant G as Guardian
    participant E as Executor

    C->>AC: Validate axiom compliance

    alt Axiom Violation
        AC->>G: Report violation (severity)
        G-->>C: Block/Warn based on level
    else Axiom OK
        AC->>HD: Check for harm

        alt Harm Detected
            HD->>G: Report harm assessment
            G-->>C: Block if irreversible without consent
        else No Harm
            HD->>SS: Scan for secrets

            alt Secrets Found
                SS->>G: Report exposed secrets
                G-->>C: Block with warning
            else No Secrets
                SS->>MG: Check mutability

                alt Immutable Layer
                    MG->>G: Report layer violation
                    G-->>C: Block modification
                else Mutable Layer
                    MG->>E: Proceed with execution
                    E-->>C: Execute command
                end
            end
        end
    end
```

## Guardian Response Integration

How security checks integrate with Guardian response levels:

```mermaid
flowchart TB
    subgraph Findings["Security Findings"]
        F0["No issues<br/>Severity: 0"]
        F1["Minor concern<br/>Severity: 1"]
        F2["Moderate risk<br/>Severity: 2"]
        F3["Clear violation<br/>Severity: 3"]
        F4["Critical risk<br/>Severity: 4"]
    end

    subgraph Response["Guardian Response"]
        R0["FLOW<br/>Continue normally"]
        R1["NUDGE<br/>Self-correct subtly"]
        R2["PAUSE<br/>Explain, ask user"]
        R3["BLOCK<br/>Stop, offer alternatives"]
        R4["PROTECT<br/>Prevent, then explain"]
    end

    F0 --> R0
    F1 --> R1
    F2 --> R2
    F3 --> R3
    F4 --> R4
```

## Severity Level Classification

How severity levels are determined:

```mermaid
flowchart TD
    START([Finding Detected]) --> TYPE{Finding Type?}

    TYPE -->|"Secret exposed"| SEC{Secret type?}
    SEC -->|"Active credential"| S4["Severity 4: PROTECT"]
    SEC -->|"Potential secret"| S3["Severity 3: BLOCK"]
    SEC -->|"Possible harmless"| S2["Severity 2: PAUSE"]

    TYPE -->|"Destructive action"| DEST{Reversible?}
    DEST -->|"No"| D4["Severity 4: PROTECT"]
    DEST -->|"Yes"| D2["Severity 2: PAUSE"]

    TYPE -->|"Axiom violation"| AX{Which axiom?}
    AX -->|"A4 Non-Harm"| A4["Severity 3-4"]
    AX -->|"A2 User Primacy"| A2["Severity 2-3"]
    AX -->|"A1 Transparency"| A1["Severity 1-2"]

    TYPE -->|"Layer violation"| LAY{Which layer?}
    LAY -->|"L0 Axioms"| L0["Severity 4: PROTECT"]
    LAY -->|"L1-L2"| L12["Severity 3: BLOCK"]
```

## Destructive Command Detection

Patterns for detecting dangerous commands:

```mermaid
flowchart TB
    subgraph Patterns["Destructive Patterns"]
        subgraph FileOps["File Operations"]
            F1["rm -rf / (recursive delete)"]
            F2["del /s /q (Windows delete)"]
            F3["> file (overwrite)"]
            F4["truncate (file truncation)"]
        end

        subgraph GitOps["Git Operations"]
            G1["git push --force"]
            G2["git reset --hard"]
            G3["git clean -fd"]
            G4["git branch -D"]
        end

        subgraph DBOps["Database Operations"]
            D1["DROP TABLE"]
            D2["DROP DATABASE"]
            D3["TRUNCATE TABLE"]
            D4["DELETE FROM (no WHERE)"]
        end

        subgraph SysOps["System Operations"]
            S1["chmod 777"]
            S2["sudo rm"]
            S3["Format drive"]
            S4["Kill process"]
        end
    end

    subgraph Assessment["Risk Assessment"]
        HIGH["HIGH RISK: Irreversible"]
        MED["MEDIUM RISK: Damaging"]
        LOW["LOW RISK: Cautionary"]
    end

    FileOps & GitOps & DBOps --> HIGH
    SysOps --> MED
```

## File Path Analysis

Security considerations for file paths:

```mermaid
flowchart TB
    subgraph Paths["Path Analysis"]
        P1["Sensitive directories<br/>~/.ssh, ~/.aws, ~/.env"]
        P2["System files<br/>/etc, C:\\Windows"]
        P3["Project secrets<br/>.env, credentials.*"]
        P4["Config files<br/>*.config, *.yml with secrets"]
    end

    subgraph Actions["Path Actions"]
        A1["READ: Log access"]
        A2["MODIFY: Warn user"]
        A3["DELETE: Block + confirm"]
        A4["EXPOSE: Block entirely"]
    end

    Paths --> Actions
```

## Security Event Logging

How security events are recorded:

```mermaid
flowchart TB
    subgraph Event["Security Event"]
        E1["Timestamp"]
        E2["Event type"]
        E3["Severity level"]
        E4["Finding details"]
        E5["Action taken"]
        E6["User response (if any)"]
    end

    subgraph Storage["Event Storage"]
        S1["Session log<br/>(ephemeral)"]
        S2["Security audit<br/>(if configured)"]
        S3["Guardian state<br/>(for response level)"]
    end

    Event --> Storage
```

## Consent Flow for Risky Actions

How user consent is obtained:

```mermaid
sequenceDiagram
    participant S as Security Check
    participant G as Guardian
    participant U as User
    participant E as Executor

    S->>G: Risky action detected (severity 2-3)
    G->>G: Escalate to PAUSE/BLOCK
    G->>U: This action may cause harm:<br/>[details]<br/>Do you want to proceed?

    alt User Consents
        U->>G: Yes, I understand the risks
        G->>G: Log consent
        G->>E: Proceed with action
        E-->>U: Action completed
    else User Declines
        U->>G: No, cancel
        G->>G: Log decline
        G-->>U: Action cancelled
    end
```

## Security Pipeline Configuration

How security checks can be configured:

```mermaid
flowchart TB
    subgraph Config["Configuration Options"]
        C1["Enabled checks<br/>(all enabled by default)"]
        C2["Severity thresholds<br/>(when to block)"]
        C3["Allowed patterns<br/>(skip certain paths)"]
        C4["Audit logging<br/>(enable/disable)"]
    end

    subgraph Defaults["Default Settings"]
        D1["All checks enabled"]
        D2["Block at severity 3+"]
        D3["No skip patterns"]
        D4["Session logging only"]
    end

    Config --> Defaults
```
