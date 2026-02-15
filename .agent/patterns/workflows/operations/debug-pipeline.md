# Debug Pipeline Workflow

## Overview

Systematic workflow for debugging CI/CD pipeline failures. This workflow demonstrates the Cursor Agent Factory workflow system architecture with phases, decision points, escalation paths, and learning hooks.

**Version:** 1.0.0  
**Created:** 2026-01-31  
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../../../../docs/setup/configuration.md).

## Trigger Conditions

This workflow is activated when:

- CI/CD pipeline reports failure
- Test suite fails locally or in CI
- User mentions "pipeline failing", "tests broken", "CI red"
- GitHub Actions workflow fails
- Pre-commit hook reports errors

**Trigger Examples:**
- "The CI is failing, can you fix it?"
- "Debug the pipeline failure"
- "Tests are broken after my last commit"
- "Fix the GitHub Actions error"

## Phases

### Phase 1: Error Detection

**Description:** Parse error logs and identify the failure type and location.

**Entry Criteria:** Error reported or CI failure detected  
**Exit Criteria:** Error classified and located

#### Step 1.1: Gather Error Information

**Description:** Collect all available error information from logs and outputs.

**Actions:**
- Check CI/CD logs for failure output
- Parse error messages and stack traces
- Identify the failing test or step
- Note any timeout or resource issues

**MCP Tools:**
- `github-getWorkflowRuns`: Fetch CI workflow status
- `github-getWorkflowRunLogs`: Get detailed logs
- `git-log`: Check recent commits

**Skills:**
- `pipeline-error-fix`: Error categorization

**Knowledge:**
- `workflow-patterns.json`: Debugging patterns

**Outputs:**
- Raw error output
- Identified failure point

**Is Mandatory:** Yes

---

#### Step 1.2: Classify Error Type

**Description:** Categorize the error for appropriate handling.

**Actions:**
- Match error against known patterns
- Determine severity (critical, major, minor)
- Identify if it's test, code, or config issue

**Error Type Classification:**

| Pattern | Type | Severity |
|---------|------|----------|
| `SyntaxError`, `IndentationError` | Syntax | Critical |
| `ImportError`, `ModuleNotFoundError` | Import | Critical |
| `AssertionError` | Test Failure | Major |
| `TimeoutError`, "timed out" | Timeout | Major |
| `ValidationError` | Schema | Major |
| `RuntimeError` | Runtime | Varies |

**Outputs:**
- Error classification
- Severity assessment
- Initial hypothesis

**Is Mandatory:** Yes

---

### Phase 2: Root Cause Analysis

**Description:** Investigate the error to identify the underlying cause.

**Entry Criteria:** Error classified  
**Exit Criteria:** Root cause hypothesis formed with evidence

#### Step 2.1: Trace Error Origin

**Description:** Follow the error to its source.

**Actions:**
- Parse stack trace to find origin
- Identify the file and line number
- Read surrounding code context

**MCP Tools:**
- `filesystem-read_file`: Read source files

**Skills:**
- `grounding`: Verify code assumptions

**Outputs:**
- Source file identification
- Error context (10-20 lines around error)

**Is Mandatory:** Yes

---

#### Step 2.2: Identify Recent Changes

**Description:** Check what changed recently that might have caused the issue.

**Actions:**
- Review git log for recent commits
- Check diff for relevant files
- Identify who made changes and when

**MCP Tools:**
- `git-log`: View commit history
- `git-diff`: Compare changes

**Outputs:**
- Relevant commits list
- Change summary

**Is Mandatory:** Yes

---

#### Step 2.3: Form Hypothesis

**Description:** Develop a theory for what caused the failure.

**Actions:**
- Correlate changes with error
- Consider timing and dependencies
- Formulate testable hypothesis

**Outputs:**
- Root cause hypothesis
- Evidence supporting hypothesis
- Confidence level (high/medium/low)

**Is Mandatory:** Yes

---

### Phase 3: Resolution Strategy

**Description:** Determine the best approach to fix the issue.

**Entry Criteria:** Root cause identified  
**Exit Criteria:** Fix approach selected

#### Step 3.1: Evaluate Fix Options

**Description:** Consider different ways to resolve the issue.

**Actions:**
- Identify possible fixes
- Assess risk of each option
- Consider side effects

**Options Assessment:**

| Option Type | When to Use | Risk Level |
|-------------|-------------|------------|
| Direct Fix | Clear single-point change | Low |
| Refactor | Design flaw evident | Medium |
| New Test | Test was wrong | Low |
| Revert | Recent change broke it | Low |
| Skip/Disable | Flaky or blocking | Medium |

**Outputs:**
- List of fix options
- Recommended approach
- Risk assessment

**Is Mandatory:** Yes

---

### Phase 4: Implementation

**Description:** Apply the selected fix.

**Entry Criteria:** Fix approach selected  
**Exit Criteria:** Changes made and initial test passes

#### Step 4.1: Implement Fix

**Description:** Make the necessary code changes.

**Actions:**
- Make minimal required changes
- Follow existing code style
- Add comments if non-obvious
- Preserve existing behavior where possible

**Skills:**
- `tdd`: If writing new tests

**Outputs:**
- Modified files
- Description of changes

**Is Mandatory:** Yes

---

#### Step 4.2: Local Verification

**Description:** Test the fix locally before broader verification.

**Actions:**
- Run the specific failing test
- Check for obvious regressions
- Verify the error is resolved

**Commands:**
```bash
# Run specific failing test
pytest tests/path/to/test.py::TestClass::test_method -v

# Run related tests
pytest tests/path/to/ -v --tb=short
```

**Outputs:**
- Test results
- Pass/fail status

**Is Mandatory:** Yes

---

### Phase 5: Verification

**Description:** Comprehensive verification that the fix works and doesn't break anything.

**Entry Criteria:** Local verification passed  
**Exit Criteria:** Full test suite passes

#### Step 5.1: Run Full Test Suite

**Description:** Execute all tests to check for regressions.

**Actions:**
- Run complete test suite
- Check all categories pass
- Note any warnings

**Commands:**
```bash
# Full test suite
pytest tests/ -v --tb=short

# With coverage
pytest tests/ -v --cov=. --cov-report=term-missing
```

**Outputs:**
- Full test results
- Coverage report (optional)
- Regression check

**Is Mandatory:** Yes

---

#### Step 5.2: Validate Fix

**Description:** Confirm the fix addresses the original issue properly.

**Actions:**
- Verify original error no longer occurs
- Check fix is minimal and clean
- Ensure no new warnings introduced

**Outputs:**
- Validation confirmation
- Any remaining concerns

**Is Mandatory:** Yes

---

### Phase 6: Learning

**Description:** Capture lessons from this debugging session for future improvement.

**Entry Criteria:** Fix verified (or escalated)  
**Exit Criteria:** Lessons documented

#### Step 6.1: Capture Pattern

**Description:** Document the failure pattern for future reference.

**Actions:**
- Classify the error type
- Note what made it hard/easy to debug
- Identify prevention measures

**Pattern Template:**
```json
{
  "error_type": "AssertionError",
  "category": "sync_drift",
  "symptoms": ["CI failure", "count mismatch"],
  "root_cause": "Artifact counts not synced",
  "fix_approach": "Run sync script",
  "prevention": "Pre-commit hook",
  "time_to_resolve": "5 minutes"
}
```

**Outputs:**
- Pattern classification
- Prevention recommendation

**Is Mandatory:** Yes

---

#### Step 6.2: Update Knowledge

**Description:** Add learnings to the knowledge base.

**Actions:**
- Update debug-patterns.json if new pattern
- Add to test suite if gap found
- Document for team

**Knowledge:**
- `debug-patterns.json`: Pattern storage

**Outputs:**
- Knowledge update
- Recommendation for process improvement

**Is Mandatory:** No (but recommended)

---

## Decision Points

### Decision: Direct Fix vs Alternative

**Condition:** After root cause analysis

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| Clear single-point fix | Implementation | Minimal risk |
| Test is wrong, not code | Write new test | Fix test, keep code |
| Design flaw | Refactor needed | Larger change |
| Unknown/complex | Escalate | Need human input |

---

### Decision: Tests Pass?

**Condition:** After implementation

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| All pass | Verification | Proceed |
| Original still fails | Re-analyze | Fix didn't work |
| New failures | Investigate | Regression |
| Flaky | Stabilize first | Reliability |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Can't identify root cause | Provide analysis so far | User |
| Fix requires major refactor | Document options | User + Team |
| Security issue found | Flag immediately | User + Security |
| External dependency broken | Document workaround | User |
| Multiple valid approaches | Present trade-offs | User |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| End of Phase 1 | Error type distribution | Improve error handling |
| End of Phase 2 | Root cause categories | Code review focus |
| End of Phase 4 | Fix success rate | Strategy refinement |
| End of Phase 6 | Resolution patterns | Training, automation |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Debug Log | Console output | Real-time status |
| Fix Commit | Git repository | Applied changes |
| Pattern Entry | `knowledge/debug-patterns.json` | Future reference |
| Recommendation | Summary output | Process improvement |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| CI logs unavailable | Ask user to paste error |
| MCP server missing | Use fallback tools |
| Cannot reproduce locally | Document environment diff |
| Fix causes new failures | Revert and re-analyze |
| Multiple unrelated failures | Triage and prioritize |

---

## Example Session

```
User: Fix the pipeline failure

Agent:
━━━ PHASE 1: Error Detection ━━━
Fetching CI logs from GitHub Actions...
Found failure in: test_artifacts_are_currently_synced

Error: AssertionError - Out of sync: ['Count: 34 -> 43']
Classification: Sync Drift (Major)

━━━ PHASE 2: Root Cause Analysis ━━━
Checking recent commits...
- 5 commits added new skills
- sync_artifacts.py not run

Hypothesis: README counts out of sync with actual files
Confidence: HIGH

━━━ PHASE 3: Resolution Strategy ━━━
Option: Run sync script (Low risk)
Proceeding with direct fix...

━━━ PHASE 4: Implementation ━━━
Running: python scripts/validation/sync_artifacts.py --sync
Updated: README.md (4 count fields)

━━━ PHASE 5: Verification ━━━
Running tests...
Result: 483 passed ✅

━━━ PHASE 6: Learning ━━━
Pattern: Sync drift after artifact addition
Prevention: Verify pre-commit hook runs sync

✨ Pipeline fixed!
```

---

## Related Artifacts

- **Agent**: `.cursor/agents/debug-conductor.md`
- **Skill**: `.cursor/skills/pipeline-error-fix/SKILL.md`
- **Knowledge**: `knowledge/workflow-patterns.json`
- **Entities**: `knowledge/workflow-entities.json`
