# Feature Development Workflow

## Overview

Comprehensive workflow for developing new features from specifications through to completion. This workflow orchestrates requirements analysis, architecture design, TDD-based implementation, code review, and documentation.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** workflow-architect

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../../../../docs/setup/configuration.md).

## Trigger Conditions

This workflow is activated when:

- Confluence page or specification is referenced
- GitHub/GitLab issue for new feature is mentioned
- User requests "implement feature", "new feature", "develop functionality"
- Feature request ticket is mentioned

**Trigger Examples:**
- "Implement the user authentication feature from CONF-123"
- "Develop the payment processing module"
- "Create the API endpoint described in the spec"
- "Build the dashboard feature from issue #456"

## Phases

### Phase 1: Requirements Analysis

**Description:** Gather and analyze feature requirements from specifications.

**Entry Criteria:** Feature request or specification reference received
**Exit Criteria:** Requirements documented and understood

#### Step 1.1: Fetch Specifications

**Description:** Retrieve the feature specification from the source.

**Actions:**
- Fetch Confluence page or GitHub issue
- Parse requirements document
- Extract acceptance criteria
- Identify stakeholders and context

**MCP Tools:**
- `atlassian-getConfluencePage`: Fetch Confluence specifications
- `github-getIssue`: Fetch GitHub issues
- `gitlab-getIssue`: Fetch GitLab issues

**Outputs:**
- Raw specification content
- Extracted requirements list
- Acceptance criteria

**Is Mandatory:** Yes

---

#### Step 1.2: Analyze Requirements

**Description:** Break down requirements into actionable items.

**Actions:**
- Identify functional requirements
- Identify non-functional requirements
- Map dependencies and constraints
- Clarify ambiguities with stakeholders

**Skills:**
- `grounding`: Verify data models and domain concepts

**Outputs:**
- Structured requirements document
- Dependency map
- Questions for clarification

**Is Mandatory:** Yes

---

### Phase 2: Architecture Design

**Description:** Design the technical architecture for the feature.

**Entry Criteria:** Requirements analyzed and understood
**Exit Criteria:** Architecture documented and approved

#### Step 2.1: Ground Data Model

**Description:** Verify all data structures before design begins.

**Actions:**
- Identify entities and relationships
- Verify against existing data models
- Document new entities required

**Skills:**
- `grounding`: Verify data model accuracy

**Knowledge:**
- `object-types.json`: Domain object definitions

**Outputs:**
- Validated data model
- Entity relationship diagram

**Is Mandatory:** Yes

---

#### Step 2.2: Create Architecture Document

**Description:** Document the high-level solution design.

**Actions:**
- Define component structure
- Specify interfaces and contracts
- Document integration points
- Consider scalability and performance

**Outputs:**
- Architecture document (`docs/{FEATURE_NAME}_architecture.md`)
- Component diagram

**Is Mandatory:** Yes

---

#### Step 2.3: Create Technical Specification

**Description:** Create detailed technical design.

**Actions:**
- Define API contracts
- Specify data schemas
- Document error handling
- Define security requirements

**Outputs:**
- Technical specification (`docs/{FEATURE_NAME}_technical_spec.md`)

**Is Mandatory:** Yes

---

### Phase 3: Test-Driven Development

**Description:** Implement the feature using TDD methodology.

**Entry Criteria:** Architecture approved
**Exit Criteria:** All tests pass, code implemented

#### Step 3.1: Create Test Plan

**Description:** Define comprehensive test strategy.

**Actions:**
- Define unit test scenarios
- Define integration test scenarios
- Create test data requirements
- Set coverage targets

**Skills:**
- `tdd`: Test-driven development patterns

**Outputs:**
- Test plan document (`docs/{FEATURE_NAME}_test_plan.md`)

**Is Mandatory:** Yes

---

#### Step 3.2: Write Failing Tests (Red Phase)

**Description:** Write tests that define expected behavior.

**Actions:**
- Create unit tests for core functionality
- Create integration tests for interfaces
- Verify tests fail as expected

**Skills:**
- `tdd`: Red-Green-Refactor cycle

**Outputs:**
- Test files
- Test failure report

**Is Mandatory:** Yes

---

#### Step 3.3: Implement Code (Green Phase)

**Description:** Write minimum code to pass tests.

**Actions:**
- Implement functionality
- Follow coding standards
- Use appropriate design patterns

**Skills:**
- `code-templates`: Code generation patterns

**Outputs:**
- Implementation code
- Passing test results

**Is Mandatory:** Yes

---

#### Step 3.4: Refactor

**Description:** Improve code quality while maintaining tests.

**Actions:**
- Remove duplication
- Improve naming and structure
- Optimize performance
- Ensure all tests still pass

**Outputs:**
- Refactored code
- Clean code metrics

**Is Mandatory:** No

---

### Phase 4: Code Review

**Description:** Review implementation for quality and correctness.

**Entry Criteria:** Implementation complete with passing tests
**Exit Criteria:** Code review approved

#### Step 4.1: Invoke Code Review

**Description:** Perform comprehensive code review.

**Actions:**
- Check correctness and logic
- Verify style compliance
- Review security implications
- Assess maintainability

**Skills:**
- `code-review`: Code review patterns
- `security-audit`: Security checks

**Outputs:**
- Code review report
- Required changes list

**Is Mandatory:** Yes

---

### Phase 5: Documentation

**Description:** Create comprehensive documentation for the feature.

**Entry Criteria:** Code review approved
**Exit Criteria:** Documentation complete

#### Step 5.1: Generate Documentation

**Description:** Create user and developer documentation.

**Actions:**
- Generate API documentation
- Create usage examples
- Update README if needed
- Create changelog entry

**Outputs:**
- API documentation
- Usage guide
- Changelog entry

**Is Mandatory:** Yes

---

### Phase 6: Integration

**Description:** Integrate feature and update tracking systems.

**Entry Criteria:** Documentation complete
**Exit Criteria:** Feature integrated and ticket updated

#### Step 6.1: Integration Testing

**Description:** Run full integration test suite.

**Actions:**
- Run integration tests
- Verify no regressions
- Check performance metrics

**Outputs:**
- Integration test results
- Performance report

**Is Mandatory:** Yes

---

#### Step 6.2: Update Tracking Systems

**Description:** Update tickets and documentation.

**Actions:**
- Update Jira/GitHub issue status
- Add implementation notes
- Link related documentation

**MCP Tools:**
- `atlassian-transitionJiraIssue`: Update Jira status
- `atlassian-addCommentToJiraIssue`: Add implementation notes
- `github-updateIssue`: Update GitHub issue

**Outputs:**
- Updated ticket
- Implementation summary

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Requirements Clear?

**Condition:** After requirements analysis

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| Requirements clear and complete | Architecture Design | Proceed with design |
| Requirements ambiguous | Escalate to stakeholder | Need clarification |
| Requirements conflict with existing system | Escalate to architect | Design decision needed |

---

### Decision: Architecture Approved?

**Condition:** After architecture design

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| Architecture approved | TDD Implementation | Proceed with development |
| Major concerns raised | Revise architecture | Address concerns |
| Significant scope change | Re-analyze requirements | Requirements changed |

---

### Decision: Code Review Outcome

**Condition:** After code review

**Options:**

| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| Approved | Documentation | Proceed to documentation |
| Changes requested (minor) | Address and re-review | Fix issues |
| Changes requested (major) | Revisit implementation | Significant rework needed |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Requirements unclear | Present questions | Product Owner / Stakeholder |
| Architecture conflicts | Present options | Technical Lead / Architect |
| Security concerns | Flag immediately | Security Team |
| Performance concerns | Document trade-offs | Technical Lead |
| Scope creep detected | Document and confirm | Product Owner |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After Phase 1 | Requirement patterns | Improve specification templates |
| After Phase 3 | Test coverage metrics | Refine TDD practices |
| After Phase 4 | Review feedback patterns | Improve code quality |
| After Phase 6 | Feature completion metrics | Estimation improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Architecture Document | `docs/{FEATURE_NAME}_architecture.md` | Design reference |
| Technical Specification | `docs/{FEATURE_NAME}_technical_spec.md` | Implementation guide |
| Test Plan | `docs/{FEATURE_NAME}_test_plan.md` | Testing strategy |
| Implementation Code | Source directories | Feature functionality |
| API Documentation | `docs/api/` | Developer reference |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Specification fetch fails | Ask user to provide requirements manually |
| Data model cannot be verified | Ask user for confirmation |
| Tests cannot be created | Document manual test plan |
| Integration tests fail | Isolate and debug, escalate if needed |
| MCP server unavailable | Use manual fallback procedures |

---

## Example Session

```
User: Implement the user profile feature from CONF-456

Agent:
━━━ PHASE 1: Requirements Analysis ━━━
Fetching Confluence page CONF-456...

Requirements extracted:
- User can view and edit profile information
- Profile includes: name, email, avatar, preferences
- Changes require email verification
- Profile accessible via REST API

Acceptance Criteria:
- [ ] GET /api/profile returns user data
- [ ] PUT /api/profile updates user data
- [ ] Email changes trigger verification flow
- [ ] Avatar upload supports JPG/PNG up to 5MB

━━━ PHASE 2: Architecture Design ━━━
Grounding data model...
✓ User entity exists with required fields
✓ Email verification flow exists

Creating architecture document...
Created: docs/user-profile_architecture.md

━━━ PHASE 3: TDD Implementation ━━━
Writing failing tests...
- test_get_profile_returns_user_data
- test_update_profile_validates_input
- test_email_change_triggers_verification

Running tests: 0/15 passing (expected)

Implementing code...
Running tests: 15/15 passing ✅

━━━ PHASE 4: Code Review ━━━
Invoking code-review skill...

Review Result: APPROVED
- No critical issues
- 2 minor suggestions applied
- Security checks passed

━━━ PHASE 5: Documentation ━━━
Generated API documentation
Updated README.md
Created changelog entry

━━━ PHASE 6: Integration ━━━
Running integration tests: 45/45 passing ✅
Updated CONF-456: Status → Done

✨ Feature complete!
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/feature-workflow.json`
- **Skills**: `.cursor/skills/grounding`, `.cursor/skills/tdd`, `.cursor/skills/code-templates`
- **Knowledge**: `knowledge/object-types.json`
- **Documentation**: `docs/WORKFLOW_AUTHORING.md`
