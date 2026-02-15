# Bugfix Resolution Workflow

## Overview

Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow ensures thorough root cause analysis, proper fix implementation, and comprehensive testing.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../../../../docs/setup/configuration.md).

## Trigger Conditions

This workflow is activated when:

- Jira, GitHub, or GitLab bug ticket is mentioned
- User reports a bug or defect
- Error report requires investigation
- Test failure needs resolution

**Trigger Examples:**
- "Fix bug PROJ-123"
- "Resolve issue #456"
- "The login page is throwing an error"
- "Users are reporting data not saving"

## Phases

### Phase 1: Ticket Analysis

**Description:** Gather and analyze bug report information.

**Entry Criteria:** Bug ticket or report received  
**Exit Criteria:** Bug understood with reproduction steps

#### Step 1.1: Fetch Ticket Details

**Description:** Retrieve bug information from tracking system.

**Actions:**
- Fetch ticket from Jira/GitHub/GitLab
- Extract error description
- Identify affected components
- Note reproduction steps

**MCP Tools:**
- `atlassian-getJiraIssue`: Fetch Jira tickets
- `github-getIssue`: Fetch GitHub issues
- `gitlab-getIssue`: Fetch GitLab issues

**Outputs:**
- Ticket summary
- Error description
- Affected components
- Reproduction steps

**Is Mandatory:** Yes

---

#### Step 1.2: Classify Bug Severity

**Description:** Determine the severity and priority of the bug.

**Actions:**
- Assess user impact
- Check frequency of occurrence
- Evaluate data integrity risk
- Determine urgency

**Severity Classification:**

| Severity | Description | Response |
|----------|-------------|----------|
| Critical | System down, data loss | Immediate |
| High | Major feature broken | Same day |
| Medium | Feature degraded | Within sprint |
| Low | Minor inconvenience | Backlog |

**Outputs:**
- Severity classification
- Priority recommendation

**Is Mandatory:** Yes

---

### Phase 2: Grounding and Context

**Description:** Verify understanding of the system context.

**Entry Criteria:** Bug classified  
**Exit Criteria:** System context understood

#### Step 2.1: Ground Data Model

**Description:** Verify data structures involved in the bug.

**Actions:**
- Identify affected entities
- Verify data model assumptions
- Check relationships and constraints

**Skills:**
- `grounding`: Data model verification

**Knowledge:**
- `object-types.json`: Domain definitions

**Outputs:**
- Verified data model
- Entity relationships

**Is Mandatory:** Yes

---

#### Step 2.2: Gather Code Context

**Description:** Collect relevant code and configuration.

**Actions:**
- Identify affected files
- Read related code sections
- Check configuration
- Review recent changes

**MCP Tools:**
- `filesystem-read_file`: Read source files
- `git-log`: Check recent commits
- `git-diff`: Compare changes

**Outputs:**
- Relevant code snippets
- Recent change history
- Configuration state

**Is Mandatory:** Yes

---

### Phase 3: Root Cause Analysis

**Description:** Identify the underlying cause of the bug.

**Entry Criteria:** Context gathered  
**Exit Criteria:** Root cause identified with evidence

#### Step 3.1: Reproduce the Bug

**Description:** Confirm the bug can be reproduced.

**Actions:**
- Follow reproduction steps
- Observe actual behavior
- Compare with expected behavior
- Document reproduction evidence

**Outputs:**
- Reproduction confirmation
- Actual vs expected behavior

**Is Mandatory:** Yes

---

#### Step 3.2: Trace Error Origin

**Description:** Follow the error to its source.

**Actions:**
- Parse stack traces
- Trace data flow
- Identify the exact failure point
- Check boundary conditions

**Outputs:**
- Error origin location
- Failure point analysis

**Is Mandatory:** Yes

---

#### Step 3.3: Identify Recent Changes

**Description:** Correlate with recent code changes.

**Actions:**
- Review git history for affected files
- Check recent deployments
- Identify potentially breaking changes
- Correlate timing with bug reports

**MCP Tools:**
- `git-log`: View commit history
- `git-diff`: Compare changes

**Outputs:**
- Relevant commits
- Change correlation

**Is Mandatory:** Yes

---

#### Step 3.4: Form Hypothesis

**Description:** Develop a theory for the root cause.

**Actions:**
- Correlate evidence
- Form testable hypothesis
- Identify fix approach
- Assess confidence level

**Outputs:**
- Root cause hypothesis
- Supporting evidence
- Confidence level (high/medium/low)

**Is Mandatory:** Yes

---

### Phase 4: Fix Implementation

**Description:** Implement the bug fix.

**Entry Criteria:** Root cause identified  
**Exit Criteria:** Fix implemented with passing tests

#### Step 4.1: Create Implementation Plan

**Description:** Document the fix approach.

**Actions:**
- Define fix strategy
- Identify files to modify
- Consider side effects
- Plan test coverage

**Outputs:**
- Implementation plan (`docs/{TICKET_ID}_fix_plan.md`)

**Is Mandatory:** Yes

---

#### Step 4.2: Write Regression Test

**Description:** Create test that reproduces the bug.

**Actions:**
- Write test that fails with current code
- Test should pass after fix
- Cover edge cases

**Skills:**
- `tdd`: Test-driven development

**Outputs:**
- Regression test
- Test failure confirmation

**Is Mandatory:** Yes

---

#### Step 4.3: Implement Fix

**Description:** Apply the code fix.

**Actions:**
- Make minimal necessary changes
- Follow existing code style
- Add comments if non-obvious
- Preserve backward compatibility

**Outputs:**
- Modified code
- Fix description

**Is Mandatory:** Yes

---

#### Step 4.4: Verify Fix Locally

**Description:** Confirm fix works locally.

**Actions:**
- Run regression test (should pass)
- Run related tests
- Verify original bug is fixed
- Check for obvious regressions

**Outputs:**
- Test results
- Verification confirmation

**Is Mandatory:** Yes

---

### Phase 5: Verification

**Description:** Comprehensive verification of the fix.

**Entry Criteria:** Fix implemented and locally verified  
**Exit Criteria:** All tests pass, no regressions

#### Step 5.1: Run Full Test Suite

**Description:** Execute complete test suite.

**Actions:**
- Run all unit tests
- Run integration tests
- Check coverage metrics
- Note any warnings

**Outputs:**
- Full test results
- Coverage report

**Is Mandatory:** Yes

---

#### Step 5.2: Code Review

**Description:** Review fix for quality.

**Actions:**
- Check fix correctness
- Verify minimal change
- Assess side effects
- Confirm test coverage

**Skills:**
- `code-review`: Quality verification

**Outputs:**
- Review result
- Any required changes

**Is Mandatory:** Yes

---

### Phase 6: Completion

**Description:** Complete the fix and update tracking.

**Entry Criteria:** Fix verified  
**Exit Criteria:** Ticket closed, lessons captured

#### Step 6.1: Update Ticket

**Description:** Update the bug ticket with resolution.

**Actions:**
- Add fix description comment
- Transition ticket status
- Link related PRs or commits
- Note any follow-up items

**MCP Tools:**
- `atlassian-addCommentToJiraIssue`: Add resolution notes
- `atlassian-transitionJiraIssue`: Update status
- `github-updateIssue`: Update GitHub issue

**Outputs:**
- Updated ticket
- Resolution summary

**Is Mandatory:** Yes

---

#### Step 6.2: Capture Lessons

**Description:** Document learnings from this fix.

**Actions:**
- Classify the bug pattern
- Note what made it hard/easy
- Identify prevention measures
- Update knowledge base

**Knowledge:**
- `debug-patterns.json`: Pattern storage

**Outputs:**
- Pattern classification
- Prevention recommendation

**Is Mandatory:** No (but recommended)

---

## Decision Points

### Decision: Root Cause Confidence

**Condition:** After hypothesis formation

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| High confidence (>80%) | Implementation | Proceed with fix |
| Medium confidence (50-80%) | Seek validation | Get second opinion |
| Low confidence (<50%) | More investigation | Need more evidence |

---

### Decision: Fix Complexity

**Condition:** After implementation planning

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| Simple, isolated fix | Implement directly | Low risk |
| Complex, multiple files | Review plan first | Higher risk |
| Requires refactoring | Escalate for approval | Scope change |

---

### Decision: Tests Pass?

**Condition:** After implementation

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| All tests pass | Verification | Proceed |
| Original bug test fails | Re-analyze | Fix didn't work |
| New test failures | Investigate regression | Side effects |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Cannot reproduce bug | Request more information | Reporter |
| Root cause unclear | Provide analysis so far | Senior Developer |
| Fix requires major changes | Document options | Tech Lead |
| Security vulnerability | Flag immediately | Security Team |
| Data integrity risk | Immediate notification | Team Lead |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After Phase 1 | Bug type distribution | Improve quality |
| After Phase 3 | Root cause categories | Code review focus |
| After Phase 4 | Fix success rate | Strategy refinement |
| After Phase 6 | Resolution time | Process improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Fix Plan | `docs/{TICKET_ID}_fix_plan.md` | Implementation guide |
| Regression Test | Test directory | Prevent recurrence |
| Code Changes | Source files | Bug resolution |
| Resolution Notes | Ticket system | Documentation |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Ticket fetch fails | Ask user for bug details manually |
| Cannot reproduce | Request environment details |
| Data model unclear | Ask for confirmation |
| Fix causes regressions | Revert and re-analyze |
| Multiple valid fixes | Present options to user |

---

## Example Session

```
User: Fix bug PROJ-789 - users can't save settings

Agent:
━━━ PHASE 1: Ticket Analysis ━━━
Fetching PROJ-789 from Jira...

Bug Summary: User settings not persisting
Affected: Settings page, UserPreferences entity
Reproduction: Change setting → Save → Refresh → Setting reverted
Severity: HIGH (core functionality broken)

━━━ PHASE 2: Grounding and Context ━━━
Verifying data model...
✓ UserPreferences entity exists
✓ Settings API endpoints defined

Gathering code context...
Found: settings_service.py, user_preferences_repository.py

━━━ PHASE 3: Root Cause Analysis ━━━
Reproducing bug...
✓ Confirmed: Settings not persisting after save

Tracing error...
- API receives correct data
- Service processes correctly
- Repository commit() not called!

Recent changes:
- Commit abc123 refactored transaction handling
- Removed explicit commit() call

Hypothesis: Missing commit() after repository save
Confidence: HIGH (clear evidence)

━━━ PHASE 4: Fix Implementation ━━━
Creating fix plan...

Writing regression test...
- test_settings_persist_after_save → FAILS (expected)

Implementing fix...
Added: db.session.commit() after save operation

Running test:
- test_settings_persist_after_save → PASSES ✅

━━━ PHASE 5: Verification ━━━
Running full test suite...
Results: 234/234 passing ✅

Code review: APPROVED
- Fix is minimal and correct
- Test coverage adequate

━━━ PHASE 6: Completion ━━━
Updated PROJ-789:
- Added resolution comment
- Status: Done
- Linked commit: def456

Captured pattern:
- Type: Missing transaction commit
- Prevention: Add transaction integration tests

✨ Bug fixed!
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/bugfix-workflow.json`
- **Agent**: `.cursor/agents/debug-conductor.md`
- **Skills**: `.cursor/skills/grounding`, `.cursor/skills/pipeline-error-fix`
- **Knowledge**: `knowledge/debug-patterns.json`
