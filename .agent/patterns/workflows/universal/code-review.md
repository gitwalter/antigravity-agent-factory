# Code Review Workflow

## Overview

Comprehensive workflow for performing structured code reviews covering correctness, style, design, performance, security, and maintainability. Generates actionable feedback with severity ratings and clear recommendations.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** code-reviewer

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../../../../docs/setup/configuration.md).

## Trigger Conditions

This workflow is activated when:

- Pull request is created or updated
- User requests code review
- Pre-merge review is required
- Code audit is needed

**Trigger Examples:**
- "Review this pull request"
- "Check my code for issues"
- "Do a code review on the changes"
- "PR #123 needs review"

## Phases

### Phase 1: Context Gathering

**Description:** Understand the change context and scope.

**Entry Criteria:** Code changes identified for review
**Exit Criteria:** Change context fully understood

#### Step 1.1: Fetch Change Details

**Description:** Retrieve the code changes to review.

**Actions:**
- Fetch PR or diff information
- Identify affected files
- Determine change scope
- Retrieve related tickets/specs

**MCP Tools:**
- `github-getPullRequest`: Fetch PR details
- `github-getPullRequestDiff`: Get diff content
- `gitlab-getMergeRequest`: Fetch MR details

**Outputs:**
- Change summary
- Affected files list
- Related context

**Is Mandatory:** Yes

---

#### Step 1.2: Understand Change Purpose

**Description:** Identify what the changes are meant to accomplish.

**Actions:**
- Read PR description
- Check linked tickets
- Understand business context
- Note the intended behavior change

**Outputs:**
- Purpose statement
- Expected behavior changes
- Success criteria

**Is Mandatory:** Yes

---

#### Step 1.3: Detect Style Guide

**Description:** Identify the applicable coding standards.

**Actions:**
- Check .cursorrules for style guide
- Review .editorconfig settings
- Analyze existing code patterns
- Identify framework conventions

**Outputs:**
- Applicable style guide
- Formatting rules

**Is Mandatory:** Yes

---

### Phase 2: Correctness Review

**Description:** Verify the code does what it should do.

**Entry Criteria:** Context understood
**Exit Criteria:** Correctness issues identified

#### Step 2.1: Logic Verification

**Description:** Check the logical correctness of the code.

**Actions:**
- Trace execution paths
- Verify business logic implementation
- Check edge cases handling
- Validate input/output contracts

**Checks:**
- Logic correctness
- Edge case handling
- Null/undefined handling
- Boundary conditions

**Outputs:**
- Correctness issues list
- Logic verification notes

**Is Mandatory:** Yes

---

#### Step 2.2: Error Handling Review

**Description:** Verify error handling completeness.

**Actions:**
- Check exception handling
- Verify error propagation
- Validate error messages
- Check recovery mechanisms

**Checks:**
- Exception handling completeness
- Error message quality
- Graceful degradation
- Resource cleanup on error

**Outputs:**
- Error handling issues
- Improvement suggestions

**Is Mandatory:** Yes

---

### Phase 3: Style and Formatting

**Description:** Check adherence to coding standards.

**Entry Criteria:** Style guide identified
**Exit Criteria:** Style issues documented

#### Step 3.1: Naming Convention Review

**Description:** Verify naming conventions are followed.

**Actions:**
- Check variable naming
- Check function/method naming
- Check class/type naming
- Check file naming

**Checks:**
- Descriptive and meaningful names
- Consistent naming patterns
- Language convention adherence
- Abbreviation usage

**Outputs:**
- Naming issues list

**Is Mandatory:** Yes

---

#### Step 3.2: Formatting Review

**Description:** Check code formatting consistency.

**Actions:**
- Check indentation
- Verify line length
- Check whitespace usage
- Verify import organization

**Outputs:**
- Formatting issues list

**Is Mandatory:** Yes

---

### Phase 4: Design Review

**Description:** Evaluate architectural and design decisions.

**Entry Criteria:** Correctness verified
**Exit Criteria:** Design issues identified

#### Step 4.1: Architecture Assessment

**Description:** Review structural design decisions.

**Actions:**
- Assess component boundaries
- Check separation of concerns
- Verify abstraction levels
- Review dependency structure

**Checks:**
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- Appropriate abstraction
- Loose coupling

**Knowledge:**
- `design-patterns.json`: Pattern reference

**Outputs:**
- Design concerns
- Refactoring suggestions

**Is Mandatory:** Yes

---

#### Step 4.2: API Design Review

**Description:** Review interface and API design.

**Actions:**
- Check API consistency
- Verify naming conventions
- Assess usability
- Review documentation

**Outputs:**
- API design feedback

**Is Mandatory:** Yes

---

### Phase 5: Performance Review

**Description:** Identify performance concerns.

**Entry Criteria:** Design reviewed
**Exit Criteria:** Performance issues identified

#### Step 5.1: Algorithm Complexity

**Description:** Assess computational complexity.

**Actions:**
- Analyze time complexity
- Analyze space complexity
- Check for nested loops
- Identify optimization opportunities

**Checks:**
- O(n²) or worse algorithms
- Unnecessary iterations
- Memory allocation patterns

**Outputs:**
- Complexity assessment
- Optimization suggestions

**Is Mandatory:** Yes

---

#### Step 5.2: Resource Usage

**Description:** Check resource utilization patterns.

**Actions:**
- Check database query efficiency
- Verify connection management
- Assess memory usage
- Review caching opportunities

**Checks:**
- N+1 query patterns
- Connection leaks
- Memory leaks
- Caching candidates

**Outputs:**
- Resource usage concerns

**Is Mandatory:** Yes

---

### Phase 6: Security Review

**Description:** Check for security vulnerabilities.

**Entry Criteria:** Performance reviewed
**Exit Criteria:** Security issues identified

#### Step 6.1: Security Vulnerability Scan

**Description:** Perform security vulnerability assessment.

**Actions:**
- Check input validation
- Verify authentication/authorization
- Scan for injection vulnerabilities
- Check data exposure risks

**Skills:**
- `security-audit`: Security analysis

**Knowledge:**
- `security-checklist.json`: Security patterns

**Checks:**
- SQL/NoSQL injection
- XSS vulnerabilities
- CSRF protection
- Authentication bypass
- Data leakage

**Outputs:**
- Security issues (with severity)

**Is Mandatory:** Yes

---

### Phase 7: Maintainability Review

**Description:** Assess long-term maintainability.

**Entry Criteria:** Security reviewed
**Exit Criteria:** Maintainability concerns identified

#### Step 7.1: Code Clarity

**Description:** Assess code readability and clarity.

**Actions:**
- Evaluate readability
- Check comment quality
- Assess code organization
- Verify documentation

**Checks:**
- Self-documenting code
- Comment appropriateness
- Function length and complexity
- Cognitive complexity

**Outputs:**
- Clarity concerns
- Documentation suggestions

**Is Mandatory:** Yes

---

#### Step 7.2: Test Coverage

**Description:** Assess test coverage quality.

**Actions:**
- Check test existence
- Verify test quality
- Assess edge case coverage
- Review test naming

**Outputs:**
- Test coverage assessment
- Missing test suggestions

**Is Mandatory:** Yes

---

### Phase 8: Report Generation

**Description:** Compile findings into structured feedback.

**Entry Criteria:** All reviews complete
**Exit Criteria:** Review report generated

#### Step 8.1: Compile Review Report

**Description:** Generate comprehensive review report.

**Actions:**
- Aggregate all findings
- Prioritize by severity
- Group by category
- Generate actionable feedback

**Outputs:**
- Review report (`docs/code_review_report.md`)

**Is Mandatory:** Yes

---

#### Step 8.2: Determine Approval Status

**Description:** Make approval recommendation.

**Actions:**
- Evaluate critical issues count
- Consider high-severity issues
- Assess overall quality
- Make recommendation

**Approval Criteria:**

| Condition | Decision |
|-----------|----------|
| No critical/high issues | APPROVE |
| Minor issues only | APPROVE with comments |
| Critical issues exist | REQUEST CHANGES |
| Major design concerns | REQUEST CHANGES |

**Outputs:**
- Approval status
- Required actions

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Severity Assessment

**Condition:** For each issue found

**Options:**

| Severity | Criteria | Blocking |
|----------|----------|----------|
| Critical | Security flaw, data loss risk | Yes |
| High | Major bug, performance issue | Yes |
| Medium | Code quality, minor bugs | No |
| Low | Style, preference | No |

---

### Decision: Review Outcome

**Condition:** After all phases complete

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| All critical fixed | APPROVE | Ready to merge |
| Open critical issues | REQUEST CHANGES | Must be fixed |
| Only style issues | APPROVE with comments | Non-blocking |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Security vulnerability | Immediate flag | Security Team |
| Architecture concern | Request discussion | Tech Lead |
| Breaking change | Confirm intent | Author |
| Complex logic | Request explanation | Author |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After Phase 2 | Common correctness issues | Training |
| After Phase 5 | Performance patterns | Guidelines |
| After Phase 6 | Security findings | Checklist updates |
| After Phase 8 | Review outcomes | Process improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Review Report | `docs/code_review_report.md` | Detailed findings |
| PR Comment | Pull request | Summary and status |
| Issue List | Inline comments | Specific feedback |

---

## Review Report Format

```markdown
# Code Review Report

## Summary
- **Files Reviewed:** {count}
- **Lines Changed:** +{added} / -{removed}
- **Issues Found:** {total} ({critical} critical, {high} high)
- **Recommendation:** APPROVE | REQUEST CHANGES | COMMENT

## Critical Issues
{Must be fixed before merge}

## High Priority Issues
{Should be fixed before merge}

## Suggestions
{Nice to have improvements}

## Positive Observations
{What was done well}

## Questions for Author
{Clarifications needed}
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Style guide not found | Infer from existing code |
| Context unclear | Ask for related ticket |
| Security assessment needed | Invoke security-audit skill |
| Large changeset | Focus on critical paths |

---

## Example Session

```
User: Review PR #234 for the user settings feature

Agent:
━━━ PHASE 1: Context Gathering ━━━
Fetching PR #234...

Summary: Add user settings persistence
Files changed: 5 (+234/-45)
Related: PROJ-789

Understanding purpose...
- Implements settings save/load functionality
- Adds new API endpoints
- Updates database schema

Style guide: Google Python Style (from .cursorrules)

━━━ PHASE 2: Correctness Review ━━━
Checking logic...
✓ Business logic correct
✓ Edge cases handled
⚠️ Missing null check on line 45 of settings_service.py

Error handling...
⚠️ Generic exception catch on line 78

━━━ PHASE 3: Style and Formatting ━━━
Naming conventions...
✓ Consistent naming
⚠️ Variable 'x' not descriptive (line 23)

Formatting...
✓ Consistent formatting

━━━ PHASE 4: Design Review ━━━
Architecture...
✓ Good separation of concerns
✓ Appropriate abstraction

API design...
✓ RESTful conventions followed

━━━ PHASE 5: Performance Review ━━━
Complexity...
✓ O(n) operations appropriate
⚠️ Potential N+1 query on line 112

Resource usage...
✓ Connections properly managed

━━━ PHASE 6: Security Review ━━━
Invoking security-audit skill...
✓ Input validation present
✓ Authorization checks correct
✓ No injection vulnerabilities

━━━ PHASE 7: Maintainability Review ━━━
Code clarity...
✓ Well-documented functions
⚠️ Complex function could be split (line 89-145)

Test coverage...
✓ Unit tests present
⚠️ Missing integration test for error path

━━━ PHASE 8: Report Generation ━━━

# Code Review Report

## Summary
- Files Reviewed: 5
- Lines Changed: +234 / -45
- Issues Found: 6 (0 critical, 1 high, 5 medium)
- Recommendation: APPROVE WITH COMMENTS

## High Priority Issues
1. **N+1 Query** (settings_repository.py:112)
   - Category: Performance
   - Suggestion: Use eager loading for related settings

## Suggestions
1. Add null check (settings_service.py:45)
2. Specific exception handling (settings_service.py:78)
3. Rename variable 'x' (settings_controller.py:23)
4. Split complex function (settings_service.py:89-145)
5. Add integration test for error path

## Positive Observations
- Clean code structure
- Good documentation
- Comprehensive unit tests

✅ APPROVED with comments
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/code-review.json`
- **Skills**: `.cursor/skills/security-audit`, `.cursor/skills/grounding`
- **Knowledge**: `knowledge/design-patterns.json`, `knowledge/security-checklist.json`
