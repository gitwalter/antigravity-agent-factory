# Quality Gates Architecture

This document visualizes the 5-phase quality validation pipeline that ensures code quality, security, and adherence to standards.

## Quick Reference

```mermaid
flowchart LR
    S[Static Analysis] --> T[Tests] --> SEC[Security] --> R[Review] --> G[Gate Decision]
```

## 5-Phase Quality Pipeline

Complete quality validation flow:

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Static Analysis"]
        L["Linting"]
        TC["Type Checking"]
        F["Formatting"]
    end
    
    subgraph Phase2["Phase 2: Test Execution"]
        UT["Unit Tests"]
        IT["Integration Tests"]
        COV["Coverage Analysis"]
    end
    
    subgraph Phase3["Phase 3: Security Scanning"]
        DEP["Dependency Audit"]
        SAST["Static Application Security"]
        SEC["Secret Detection"]
    end
    
    subgraph Phase4["Phase 4: Code Review"]
        CX["Complexity Analysis"]
        PAT["Pattern Compliance"]
        DOC["Documentation Check"]
    end
    
    subgraph Phase5["Phase 5: Gate Decision"]
        AGG["Aggregate Results"]
        THRESH["Apply Thresholds"]
        DEC{Decision}
    end
    
    Phase1 --> Phase2 --> Phase3 --> Phase4 --> Phase5
    
    DEC -->|"All pass"| PASS["PASS: Proceed"]
    DEC -->|"Warnings"| WARN["WARN: Review needed"]
    DEC -->|"Failures"| FAIL["FAIL: Block"]
```

## Phase 1: Static Analysis

Detailed static analysis checks:

```mermaid
flowchart TB
    subgraph Linting["Linting"]
        L1["Python: ruff, pylint"]
        L2["JavaScript: eslint"]
        L3["TypeScript: eslint + tsc"]
        L4["Go: golangci-lint"]
    end
    
    subgraph TypeCheck["Type Checking"]
        T1["Python: mypy, pyright"]
        T2["TypeScript: tsc --noEmit"]
        T3["Flow types"]
    end
    
    subgraph Formatting["Formatting"]
        F1["Python: black, isort"]
        F2["JavaScript: prettier"]
        F3["Go: gofmt"]
    end
    
    subgraph Output["Phase 1 Output"]
        O1["Error count"]
        O2["Warning count"]
        O3["Files processed"]
        O4["Pass/Fail status"]
    end
    
    Linting & TypeCheck & Formatting --> Output
```

## Phase 2: Test Execution

Test execution and coverage:

```mermaid
flowchart TB
    subgraph UnitTests["Unit Tests"]
        UT1["pytest (Python)"]
        UT2["jest (JavaScript)"]
        UT3["go test (Go)"]
        UT4["JUnit (Java)"]
    end
    
    subgraph IntegrationTests["Integration Tests"]
        IT1["API tests"]
        IT2["Database tests"]
        IT3["Service integration"]
    end
    
    subgraph Coverage["Coverage Analysis"]
        C1["Line coverage"]
        C2["Branch coverage"]
        C3["Function coverage"]
        
        subgraph Thresholds["Coverage Thresholds"]
            TH1["Minimum: 80%"]
            TH2["Target: 90%"]
            TH3["Critical paths: 95%"]
        end
    end
    
    subgraph Output["Phase 2 Output"]
        O1["Tests passed/failed"]
        O2["Coverage percentage"]
        O3["Uncovered lines"]
        O4["Flaky test detection"]
    end
    
    UnitTests & IntegrationTests --> Coverage --> Output
```

## Phase 3: Security Scanning

Security validation checks:

```mermaid
flowchart TB
    subgraph DependencyAudit["Dependency Audit"]
        D1["npm audit"]
        D2["pip-audit"]
        D3["snyk test"]
        D4["Dependabot alerts"]
    end
    
    subgraph SAST["Static Application Security"]
        S1["Bandit (Python)"]
        S2["ESLint security rules"]
        S3["Semgrep"]
        S4["SonarQube"]
    end
    
    subgraph SecretDetection["Secret Detection"]
        SEC1["git-secrets"]
        SEC2["trufflehog"]
        SEC3["Factory secret scanner"]
    end
    
    subgraph Output["Phase 3 Output"]
        O1["Vulnerability count"]
        O2["Severity breakdown"]
        O3["Remediation advice"]
        O4["CVE references"]
    end
    
    DependencyAudit & SAST & SecretDetection --> Output
```

## Phase 4: Code Review

Automated code review checks:

```mermaid
flowchart TB
    subgraph Complexity["Complexity Analysis"]
        CX1["Cyclomatic complexity"]
        CX2["Cognitive complexity"]
        CX3["Function length"]
        CX4["File length"]
    end
    
    subgraph Patterns["Pattern Compliance"]
        P1["Naming conventions"]
        P2["Project structure"]
        P3["Import ordering"]
        P4["Design pattern usage"]
    end
    
    subgraph Documentation["Documentation Check"]
        D1["Docstring coverage"]
        D2["README completeness"]
        D3["API documentation"]
        D4["Changelog updates"]
    end
    
    subgraph Output["Phase 4 Output"]
        O1["Complexity scores"]
        O2["Pattern violations"]
        O3["Doc coverage %"]
        O4["Review recommendations"]
    end
    
    Complexity & Patterns & Documentation --> Output
```

## Phase 5: Gate Decision

Aggregation and final decision:

```mermaid
flowchart TD
    subgraph Inputs["Phase Results"]
        I1["Phase 1: Static Analysis"]
        I2["Phase 2: Tests"]
        I3["Phase 3: Security"]
        I4["Phase 4: Review"]
    end
    
    subgraph Aggregation["Result Aggregation"]
        AGG["Combine all results"]
        WEIGHT["Apply weights"]
        SCORE["Calculate overall score"]
    end
    
    subgraph Thresholds["Threshold Application"]
        TH1["Critical failures: Any = FAIL"]
        TH2["Security high: Any = FAIL"]
        TH3["Coverage: Below 80% = WARN"]
        TH4["Complexity: Above threshold = WARN"]
    end
    
    subgraph Decision["Gate Decision"]
        DEC{Score check}
        PASS["PASS<br/>All thresholds met"]
        WARN["WARN<br/>Non-critical issues"]
        FAIL["FAIL<br/>Critical issues found"]
    end
    
    Inputs --> Aggregation --> Thresholds --> DEC
    DEC -->|"Score >= 90"| PASS
    DEC -->|"Score 70-89"| WARN
    DEC -->|"Score < 70"| FAIL
```

## Decision Matrix

Gate decision based on check results:

```mermaid
flowchart TB
    subgraph Matrix["Decision Matrix"]
        subgraph Critical["Critical Checks (Must Pass)"]
            C1["Tests pass"]
            C2["No high-severity security issues"]
            C3["No exposed secrets"]
            C4["Type checking passes"]
        end
        
        subgraph NonCritical["Non-Critical Checks (Warn)"]
            N1["Coverage below target"]
            N2["Linting warnings"]
            N3["Complexity above threshold"]
            N4["Documentation gaps"]
        end
    end
    
    subgraph Outcomes["Outcomes"]
        O1["All critical pass, all non-critical pass → PASS"]
        O2["All critical pass, some non-critical fail → WARN"]
        O3["Any critical fail → FAIL"]
    end
    
    Critical & NonCritical --> Outcomes
```

## Learning Hook Integration

How quality feedback feeds into learning:

```mermaid
flowchart TB
    subgraph QualityResults["Quality Gate Results"]
        R1["Passed checks"]
        R2["Failed checks"]
        R3["Remediation taken"]
    end
    
    subgraph Learning["Learning System"]
        L1["Capture patterns"]
        L2["Identify recurring issues"]
        L3["Propose improvements"]
    end
    
    subgraph Memory["Memory Storage"]
        M1["Successful patterns"]
        M2["Common failure modes"]
        M3["Effective remediation"]
    end
    
    subgraph Application["Future Application"]
        A1["Proactive warnings"]
        A2["Suggested fixes"]
        A3["Pattern enforcement"]
    end
    
    QualityResults --> Learning --> Memory --> Application
```

## Escalation Paths

Different failure types and their resolution:

```mermaid
flowchart TD
    FAIL([Quality Gate Failure]) --> TYPE{Failure Type?}
    
    TYPE -->|"Test failure"| TEST["Fix failing tests"]
    TYPE -->|"Security issue"| SEC["Address vulnerability"]
    TYPE -->|"Coverage drop"| COV["Add more tests"]
    TYPE -->|"Complexity"| CX["Refactor code"]
    
    TEST --> RERUN["Re-run quality gate"]
    SEC --> RERUN
    COV --> RERUN
    CX --> RERUN
    
    RERUN --> CHECK{Pass now?}
    CHECK -->|"Yes"| PROCEED["Proceed with merge"]
    CHECK -->|"No"| ESCALATE["Escalate to human review"]
```

## Quality Metrics Dashboard

Key metrics tracked:

```mermaid
flowchart TB
    subgraph Metrics["Key Quality Metrics"]
        subgraph Health["Health Indicators"]
            H1["Test pass rate"]
            H2["Coverage trend"]
            H3["Security score"]
        end
        
        subgraph Trends["Trend Metrics"]
            T1["Quality over time"]
            T2["Debt accumulation"]
            T3["Fix rate"]
        end
        
        subgraph Alerts["Alert Thresholds"]
            A1["Coverage dropping"]
            A2["Complexity increasing"]
            A3["Security issues rising"]
        end
    end
```

## Quality Gate Configuration

Configurable thresholds:

```mermaid
flowchart TB
    subgraph Config["Quality Gate Configuration"]
        subgraph Coverage["Coverage Thresholds"]
            COV1["Minimum: 80%"]
            COV2["New code: 90%"]
            COV3["Critical paths: 95%"]
        end
        
        subgraph Complexity["Complexity Limits"]
            CX1["Cyclomatic: max 10"]
            CX2["Cognitive: max 15"]
            CX3["Function lines: max 50"]
        end
        
        subgraph Security["Security Levels"]
            SEC1["Critical: Block"]
            SEC2["High: Block"]
            SEC3["Medium: Warn"]
            SEC4["Low: Info"]
        end
    end
    
    subgraph Override["Override Options"]
        O1["Skip checks (with justification)"]
        O2["Temporary exceptions"]
        O3["Project-specific thresholds"]
    end
```

## CI/CD Integration

Quality gates in CI/CD pipeline:

```mermaid
sequenceDiagram
    participant D as Developer
    participant PR as Pull Request
    participant CI as CI Pipeline
    participant QG as Quality Gate
    participant M as Merge
    
    D->>PR: Create/Update PR
    PR->>CI: Trigger pipeline
    
    CI->>QG: Run Phase 1 (Static)
    QG-->>CI: Results
    
    CI->>QG: Run Phase 2 (Tests)
    QG-->>CI: Results
    
    CI->>QG: Run Phase 3 (Security)
    QG-->>CI: Results
    
    CI->>QG: Run Phase 4 (Review)
    QG-->>CI: Results
    
    CI->>QG: Phase 5 (Decision)
    
    alt Gate Passes
        QG-->>CI: PASS
        CI-->>PR: Green status
        PR->>M: Ready to merge
    else Gate Fails
        QG-->>CI: FAIL
        CI-->>PR: Red status + details
        PR-->>D: Fix required
    end
```

## Workflow Pattern Integration

Quality gate workflow definition:

```mermaid
flowchart TB
    subgraph Workflow["quality-gate.md Workflow"]
        subgraph Phases["Phases"]
            PH1["phase: static-analysis"]
            PH2["phase: test-execution"]
            PH3["phase: security-scan"]
            PH4["phase: code-review"]
            PH5["phase: gate-decision"]
        end
        
        subgraph Steps["Steps per Phase"]
            S1["entry_criteria"]
            S2["actions"]
            S3["exit_criteria"]
            S4["on_failure"]
        end
        
        subgraph Hooks["Learning Hooks"]
            H1["on_success: capture pattern"]
            H2["on_failure: log issue"]
            H3["on_remediation: learn fix"]
        end
    end
    
    Phases --> Steps --> Hooks
```
