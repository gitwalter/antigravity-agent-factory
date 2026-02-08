# Quality Gate Workflow

## Overview

Automated quality gate workflow that enforces code quality standards before merge. Runs comprehensive checks including linting, testing, coverage, security scanning, and code review to ensure only high-quality code enters the codebase.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** code-reviewer

## Trigger Conditions

This workflow is activated when:

- Pull request is opened or updated
- Pre-merge check is requested
- CI/CD pipeline runs quality checks
- User requests quality validation

**Trigger Examples:**
- "Run quality checks on this PR"
- "Check if PR #123 is ready to merge"
- "Validate code quality"
- "Pre-merge check"

## Phases

### Phase 1: Static Analysis

**Description:** Run static code analysis tools.

**Entry Criteria:** Code changes identified  
**Exit Criteria:** All static analysis complete

#### Step 1.1: Lint Check

**Description:** Run linting tools for code style.

**Actions:**
- Detect language and framework
- Run appropriate linter
- Collect lint errors and warnings
- Generate lint report

**Tools by Language:**

| Language | Linter |
|----------|--------|
| Python | ruff, pylint |
| TypeScript | ESLint |
| Java | Checkstyle |
| Rust | clippy |
| Go | golangci-lint |

**Outputs:**
- Lint results
- Error count
- Warning count

**Pass Criteria:** Zero errors (warnings allowed)

**Is Mandatory:** Yes

---

#### Step 1.2: Type Check

**Description:** Run type checking where applicable.

**Actions:**
- Detect type system
- Run type checker
- Collect type errors

**Tools by Language:**

| Language | Type Checker |
|----------|-------------|
| Python | mypy |
| TypeScript | tsc |
| Java | javac |

**Outputs:**
- Type check results
- Error list

**Pass Criteria:** Zero type errors

**Is Mandatory:** Yes

---

#### Step 1.3: Format Check

**Description:** Verify code formatting.

**Actions:**
- Run formatter in check mode
- Identify formatting violations
- Report differences

**Tools by Language:**

| Language | Formatter |
|----------|-----------|
| Python | black, ruff format |
| TypeScript | Prettier |
| Java | google-java-format |
| Rust | rustfmt |

**Outputs:**
- Formatting check results
- Files needing formatting

**Pass Criteria:** All files properly formatted

**Is Mandatory:** Yes

---

### Phase 2: Test Execution

**Description:** Run test suites and collect results.

**Entry Criteria:** Static analysis passed  
**Exit Criteria:** All tests executed

#### Step 2.1: Unit Tests

**Description:** Execute unit test suite.

**Actions:**
- Run unit tests
- Collect test results
- Generate coverage data
- Identify failures

**Test Frameworks:**

| Language | Framework |
|----------|-----------|
| Python | pytest |
| TypeScript | Vitest, Jest |
| Java | JUnit 5 |
| Rust | cargo test |

**Outputs:**
- Test results
- Pass/fail counts
- Failure details

**Pass Criteria:** All unit tests pass

**Is Mandatory:** Yes

---

#### Step 2.2: Integration Tests

**Description:** Execute integration test suite.

**Actions:**
- Run integration tests
- Check external dependencies
- Collect results

**Outputs:**
- Integration test results
- Pass/fail counts

**Pass Criteria:** All integration tests pass

**Is Mandatory:** Yes

---

#### Step 2.3: Coverage Analysis

**Description:** Analyze test coverage.

**Actions:**
- Calculate line coverage
- Calculate branch coverage
- Identify uncovered code
- Compare with thresholds

**Coverage Thresholds:**

| Metric | Minimum | Target |
|--------|---------|--------|
| Line Coverage | 70% | 85% |
| Branch Coverage | 60% | 75% |
| New Code Coverage | 80% | 90% |

**Outputs:**
- Coverage report
- Coverage percentage
- Uncovered lines

**Pass Criteria:** Coverage meets minimum thresholds

**Is Mandatory:** Yes

---

### Phase 3: Security Scanning

**Description:** Perform security vulnerability scans.

**Entry Criteria:** Tests passed  
**Exit Criteria:** Security scan complete

#### Step 3.1: Dependency Scan

**Description:** Scan dependencies for vulnerabilities.

**Actions:**
- Identify dependencies
- Check vulnerability databases
- Assess severity
- Report findings

**Tools:**
- Python: `safety`, `pip-audit`
- Node: `npm audit`
- Java: `dependency-check`

**Outputs:**
- Vulnerability list
- Severity ratings
- Remediation suggestions

**Pass Criteria:** No high/critical vulnerabilities

**Is Mandatory:** Yes

---

#### Step 3.2: Secret Scan

**Description:** Check for exposed secrets.

**Actions:**
- Scan for API keys
- Check for passwords
- Identify tokens
- Report findings

**Patterns Checked:**
- AWS keys
- API tokens
- Database passwords
- Private keys
- JWT secrets

**Outputs:**
- Secret findings
- File locations

**Pass Criteria:** No secrets detected

**Is Mandatory:** Yes

---

#### Step 3.3: SAST (Static Application Security Testing)

**Description:** Static security analysis of code.

**Actions:**
- Scan for injection vulnerabilities
- Check authentication patterns
- Analyze data handling
- Report security issues

**Skills:**
- `security-audit`: Security patterns

**Knowledge:**
- `security-checklist.json`: Security patterns

**Outputs:**
- Security issues
- Severity ratings

**Pass Criteria:** No critical security issues

**Is Mandatory:** Yes

---

### Phase 4: Code Review

**Description:** Automated code review checks.

**Entry Criteria:** Security scans passed  
**Exit Criteria:** Code review complete

#### Step 4.1: Complexity Analysis

**Description:** Analyze code complexity.

**Actions:**
- Calculate cyclomatic complexity
- Identify complex functions
- Check method length
- Report violations

**Thresholds:**

| Metric | Warning | Error |
|--------|---------|-------|
| Cyclomatic Complexity | > 10 | > 15 |
| Method Length | > 50 lines | > 100 lines |
| File Length | > 300 lines | > 500 lines |

**Outputs:**
- Complexity metrics
- Violations list

**Pass Criteria:** No error-level violations

**Is Mandatory:** Yes

---

#### Step 4.2: Design Pattern Check

**Description:** Check for anti-patterns.

**Actions:**
- Detect code smells
- Identify anti-patterns
- Check design principles
- Report issues

**Checks:**
- God classes
- Long parameter lists
- Duplicate code
- Circular dependencies

**Knowledge:**
- `design-patterns.json`: Pattern reference

**Outputs:**
- Anti-pattern findings
- Improvement suggestions

**Pass Criteria:** No critical anti-patterns

**Is Mandatory:** Yes

---

### Phase 5: Gate Decision

**Description:** Make the final quality gate decision.

**Entry Criteria:** All checks complete  
**Exit Criteria:** Gate decision rendered

#### Step 5.1: Aggregate Results

**Description:** Compile all check results.

**Actions:**
- Collect all phase results
- Calculate overall score
- Identify blockers
- Generate summary

**Outputs:**
- Aggregated report
- Pass/fail status
- Blocking issues list

**Is Mandatory:** Yes

---

#### Step 5.2: Render Decision

**Description:** Make final gate decision.

**Actions:**
- Evaluate all criteria
- Apply decision rules
- Generate recommendation
- Create report

**Decision Matrix:**

| All Passed | Minor Issues | Major Issues | Critical Issues |
|------------|--------------|--------------|-----------------|
| PASS | PASS with notes | FAIL | FAIL |

**Outputs:**
- Gate decision (PASS/FAIL)
- Decision rationale
- Required actions

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Static Analysis Result

**Condition:** After Phase 1

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| All checks pass | Continue | Proceed to tests |
| Lint errors only | Fail fast | Fix before testing |
| Type errors | Fail fast | Fix before testing |

---

### Decision: Test Failure

**Condition:** After Phase 2

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| All tests pass | Continue | Proceed to security |
| Test failures | Fail | Must fix tests |
| Coverage below threshold | Fail | Need more tests |

---

### Decision: Security Issues

**Condition:** After Phase 3

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| No security issues | Continue | Proceed to review |
| Critical/High issues | Fail | Security risk |
| Medium/Low issues | Continue with notes | Track for later |

---

### Decision: Final Gate

**Condition:** After Phase 5

**Options:**

| Result | Action |
|--------|--------|
| PASS | Allow merge |
| PASS with notes | Allow merge, track items |
| FAIL | Block merge, list issues |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Critical security issue | Immediate block | Security Team |
| Flaky tests | Flag for investigation | Test Owner |
| Coverage drop | Block with explanation | Developer |
| Complex failure | Provide analysis | Tech Lead |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After lint | Common lint issues | Documentation |
| After tests | Failure patterns | Test improvement |
| After security | Vulnerability types | Training |
| After gate | Pass/fail rates | Process improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Quality Report | PR comment | Summary |
| Lint Report | `reports/lint.xml` | Details |
| Coverage Report | `reports/coverage/` | Coverage data |
| Security Report | `reports/security.json` | Vulnerabilities |

---

## Quality Gate Summary Format

```
╔══════════════════════════════════════════════════════════╗
║                    QUALITY GATE REPORT                    ║
╠══════════════════════════════════════════════════════════╣
║ Status: ✅ PASSED / ❌ FAILED                             ║
╠══════════════════════════════════════════════════════════╣
║ Static Analysis                                          ║
║   Lint:        ✅ 0 errors, 3 warnings                   ║
║   Types:       ✅ No errors                              ║
║   Format:      ✅ All files formatted                    ║
╠══════════════════════════════════════════════════════════╣
║ Tests                                                    ║
║   Unit:        ✅ 156/156 passed                         ║
║   Integration: ✅ 23/23 passed                           ║
║   Coverage:    ✅ 87% (threshold: 70%)                   ║
╠══════════════════════════════════════════════════════════╣
║ Security                                                 ║
║   Dependencies: ✅ No vulnerabilities                    ║
║   Secrets:      ✅ No secrets detected                   ║
║   SAST:         ✅ No critical issues                    ║
╠══════════════════════════════════════════════════════════╣
║ Code Quality                                             ║
║   Complexity:   ✅ Within limits                         ║
║   Design:       ⚠️ 1 minor issue                        ║
╠══════════════════════════════════════════════════════════╣
║ Decision: ✅ APPROVED FOR MERGE                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Linter not available | Skip with warning |
| Tests timeout | Retry once, then fail |
| External service down | Use cached results if available |
| Coverage tool fails | Use estimated coverage |

---

## Example Session

```
User: Run quality gate on PR #456

Agent:
━━━ PHASE 1: Static Analysis ━━━
Running linter (ruff)...
✅ Lint: 0 errors, 2 warnings

Running type checker (mypy)...
✅ Types: No errors

Checking formatting (black)...
✅ Format: All files properly formatted

━━━ PHASE 2: Test Execution ━━━
Running unit tests...
✅ Unit tests: 234/234 passed

Running integration tests...
✅ Integration tests: 45/45 passed

Analyzing coverage...
✅ Coverage: 82% (threshold: 70%)
   Lines: 85%
   Branches: 78%
   New code: 91%

━━━ PHASE 3: Security Scanning ━━━
Scanning dependencies...
✅ No known vulnerabilities

Scanning for secrets...
✅ No secrets detected

Running SAST...
✅ No critical issues
⚠️ 1 medium: Possible timing attack (auth.py:45)

━━━ PHASE 4: Code Review ━━━
Analyzing complexity...
✅ All functions within limits

Checking design patterns...
✅ No anti-patterns detected

━━━ PHASE 5: Gate Decision ━━━
Aggregating results...

╔══════════════════════════════════════════════════════════╗
║                    QUALITY GATE REPORT                    ║
╠══════════════════════════════════════════════════════════╣
║ Status: ✅ PASSED                                         ║
╠══════════════════════════════════════════════════════════╣
║ All checks passed with 1 note:                           ║
║ - SAST: Review timing in auth.py:45 (medium)             ║
╠══════════════════════════════════════════════════════════╣
║ Decision: ✅ APPROVED FOR MERGE                          ║
╚══════════════════════════════════════════════════════════╝

✅ Quality gate PASSED - ready to merge
```

---

## Related Artifacts

- **Skills**: `.cursor/skills/security-audit`, `.cursor/skills/code-review`
- **Knowledge**: `knowledge/design-patterns.json`, `knowledge/security-checklist.json`
- **Patterns**: `patterns/enforcement/quality-enforcement.json`
