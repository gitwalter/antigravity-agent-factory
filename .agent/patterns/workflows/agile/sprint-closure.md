# Sprint Closure Workflow

## Overview

Systematic workflow for closing sprints, including status review, velocity calculation, incomplete item handling, and retrospective facilitation. Captures lessons learned and prepares for the next sprint.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** sprint-master

## Trigger Conditions

This workflow is activated when:

- Sprint end date reached
- User requests sprint closure
- Sprint completion requested
- Schedule triggers closure

**Trigger Examples:**
- "Close Sprint 14"
- "End the current sprint"
- "Sprint completion review"
- "Wrap up the sprint"

## Phases

### Phase 1: Status Review

**Description:** Review the current state of all sprint items.

**Entry Criteria:** Sprint end date reached  
**Exit Criteria:** All items status confirmed

#### Step 1.1: Gather Sprint Items

**Description:** Collect all items in the sprint.

**Actions:**
- Query sprint backlog
- Get status of each item
- Identify completed items
- Identify incomplete items

**MCP Tools:**
- `atlassian-getJiraSprint`: Get sprint details
- `atlassian-searchJiraIssues`: Query sprint items

**Outputs:**
- Complete item list
- Status breakdown

**Is Mandatory:** Yes

---

#### Step 1.2: Verify Completions

**Description:** Confirm completed items meet Definition of Done.

**Actions:**
- Check each "Done" item
- Verify acceptance criteria met
- Confirm tests passing
- Check documentation

**Definition of Done Checklist:**
- [ ] Code complete and reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO accepted

**Outputs:**
- Verified completions
- Items needing verification

**Is Mandatory:** Yes

---

### Phase 2: Metrics Calculation

**Description:** Calculate sprint metrics and velocity.

**Entry Criteria:** Status verified  
**Exit Criteria:** Metrics calculated

#### Step 2.1: Calculate Velocity

**Description:** Compute the sprint velocity.

**Actions:**
- Sum completed story points
- Compare to commitment
- Calculate completion rate
- Track velocity trend

**Velocity Formula:**
```
Velocity = Sum of story points for completed items
Completion Rate = Completed Points / Committed Points × 100%
```

**Skills:**
- `close-sprint`: Velocity calculation

**Outputs:**
- Sprint velocity
- Completion rate
- Velocity trend

**Is Mandatory:** Yes

---

#### Step 2.2: Calculate Additional Metrics

**Description:** Compute other useful metrics.

**Actions:**
- Calculate cycle time
- Measure throughput
- Track scope changes
- Note blockers

**Metrics:**

| Metric | Formula |
|--------|---------|
| Cycle Time | Avg(Done Date - Started Date) |
| Throughput | Count of completed items |
| Scope Change | Added points - Removed points |
| Bug Rate | Bug count / Total items |

**Outputs:**
- Metric report

**Is Mandatory:** Yes

---

### Phase 3: Incomplete Items

**Description:** Handle items not completed in the sprint.

**Entry Criteria:** Metrics calculated  
**Exit Criteria:** Incomplete items addressed

#### Step 3.1: Review Incomplete Items

**Description:** Analyze why items weren't completed.

**Actions:**
- List incomplete items
- Identify blockers
- Assess remaining effort
- Categorize reasons

**Incompletion Reasons:**

| Reason | Action |
|--------|--------|
| Blocked | Document blocker |
| Underestimated | Re-estimate |
| Deprioritized | Move to backlog |
| Scope grew | Split story |

**Outputs:**
- Incomplete item analysis

**Is Mandatory:** Yes

---

#### Step 3.2: Decide Item Fate

**Description:** Determine what happens to incomplete items.

**Actions:**
- Carry over to next sprint?
- Return to backlog?
- Split into smaller items?
- Cancel if obsolete?

**Decision Matrix:**

| In Progress | Priority | Action |
|-------------|----------|--------|
| Yes | High | Carry over |
| Yes | Low | Return to backlog |
| No | High | Carry over |
| No | Low | Return to backlog |

**MCP Tools:**
- `atlassian-moveIssuesToSprint`: Move issues

**Outputs:**
- Item disposition

**Is Mandatory:** Yes

---

### Phase 4: Burndown Analysis

**Description:** Analyze the sprint burndown.

**Entry Criteria:** Items handled  
**Exit Criteria:** Burndown analyzed

#### Step 4.1: Generate Burndown

**Description:** Create burndown chart data.

**Actions:**
- Plot ideal burndown
- Plot actual burndown
- Identify deviations
- Note significant events

**Skills:**
- `generate-burndown`: Chart generation

**Outputs:**
- Burndown data
- Deviation analysis

**Is Mandatory:** Yes

---

#### Step 4.2: Identify Patterns

**Description:** Analyze burndown patterns.

**Actions:**
- Late completion clustering?
- Scope changes visible?
- Steady progress or spikes?
- Flat periods?

**Pattern Analysis:**

| Pattern | Indication |
|---------|------------|
| Late burn | Starting late |
| Flat periods | Blockers |
| Scope increase | Requirement changes |
| Early completion | Good estimation |

**Outputs:**
- Pattern analysis

**Is Mandatory:** Yes

---

### Phase 5: Retrospective

**Description:** Conduct or prepare for retrospective.

**Entry Criteria:** Burndown analyzed  
**Exit Criteria:** Retro insights captured

#### Step 5.1: Gather Feedback

**Description:** Collect team feedback.

**Actions:**
- What went well?
- What didn't go well?
- What to improve?
- Action items from last retro?

**Retrospective Format:**
```
What Went Well:
- [Team inputs]

What Didn't Go Well:
- [Team inputs]

Action Items:
- [Improvements to try]
```

**Outputs:**
- Retrospective notes

**Is Mandatory:** Yes

---

#### Step 5.2: Create Action Items

**Description:** Convert insights to actions.

**Actions:**
- Prioritize improvements
- Assign owners
- Set deadlines
- Track in next sprint

**Outputs:**
- Action item list

**Is Mandatory:** Yes

---

### Phase 6: Closure

**Description:** Officially close the sprint.

**Entry Criteria:** Retro complete  
**Exit Criteria:** Sprint closed

#### Step 6.1: Close Sprint

**Description:** Complete sprint in the system.

**Actions:**
- Mark sprint as closed
- Archive sprint data
- Update project metrics
- Prepare for next sprint

**MCP Tools:**
- `atlassian-completeJiraSprint`: Close sprint

**Outputs:**
- Closed sprint

**Is Mandatory:** Yes

---

#### Step 6.2: Generate Sprint Report

**Description:** Create comprehensive sprint report.

**Actions:**
- Compile all metrics
- Include burndown
- Summarize outcomes
- Note lessons learned

**Report Sections:**
- Executive Summary
- Completed Work
- Incomplete Work
- Metrics
- Retrospective Summary
- Action Items

**Outputs:**
- Sprint report

**Is Mandatory:** Yes

---

#### Step 6.3: Communicate Closure

**Description:** Notify stakeholders of sprint completion.

**Actions:**
- Post sprint summary
- Share with stakeholders
- Update project status
- Archive sprint channel (if applicable)

**Outputs:**
- Communications sent

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Incomplete Item Handling

**Condition:** For each incomplete item

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| In progress, high priority | Carry over | Continue momentum |
| Not started, high priority | Carry over | Still important |
| Low priority | Return to backlog | Re-prioritize |
| Obsolete | Cancel | No longer needed |

---

### Decision: Velocity Trend

**Condition:** After velocity calculation

**Options:**

| Trend | Action | Rationale |
|-------|--------|-----------|
| Improving | Continue practices | Working well |
| Declining | Investigate | Something wrong |
| Stable | Normal | Predictable |
| Erratic | Review estimation | Consistency needed |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Significant velocity drop | Root cause analysis | Team Lead |
| Many incomplete items | Process review | Scrum Master |
| Team conflict | Facilitation | Scrum Master |
| Stakeholder concerns | Communication | Product Owner |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After metrics | Velocity patterns | Forecasting |
| After retro | Improvement patterns | Process evolution |
| After closure | Sprint outcomes | Trend analysis |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Sprint Report | `docs/sprints/sprint-X-report.md` | Documentation |
| Metrics Data | PM Tool | Tracking |
| Retro Notes | Team wiki | Learning |
| Action Items | Next sprint | Improvement |

---

## Sprint Report Template

```markdown
# Sprint X Report

## Executive Summary
- **Sprint:** X (YYYY-MM-DD to YYYY-MM-DD)
- **Velocity:** XX points (YY% of commitment)
- **Status:** Completed / Partially Completed

## Completed Work
| Story | Points | Description |
|-------|--------|-------------|
| PROJ-123 | 5 | Feature description |

## Incomplete Work
| Story | Points | Reason | Disposition |
|-------|--------|--------|-------------|
| PROJ-456 | 8 | Blocked | Carry over |

## Metrics
- Velocity: XX points
- Completion Rate: YY%
- Cycle Time: Z days average
- Scope Change: +X/-Y points

## Burndown Analysis
[Chart or description]

## Retrospective Summary
### What Went Well
- [Item 1]
- [Item 2]

### What to Improve
- [Item 1]
- [Item 2]

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Improve estimation | Team | Next sprint |
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM tool unavailable | Manual calculation |
| Team unavailable | Async retro |
| Metrics incomplete | Use available data |
| Urgent next sprint | Abbreviated closure |

---

## Example Session

```
User: Close Sprint 14

Agent:
━━━ PHASE 1: Status Review ━━━
Gathering sprint items...

Sprint 14 (Jan 1-12, 2026)
- Total items: 8
- Completed: 6
- In Progress: 1
- Not Started: 1

Verifying completions...
✓ PROJ-401: API refactoring (8 pts) - Done
✓ PROJ-402: User dashboard (5 pts) - Done
✓ PROJ-403: Email templates (3 pts) - Done
✓ PROJ-404: Bug fixes (5 pts) - Done
✓ PROJ-405: Documentation (3 pts) - Done
✓ PROJ-406: Performance optimization (8 pts) - Done

Incomplete:
⚠️ PROJ-407: Admin panel (8 pts) - In Progress (80%)
⚠️ PROJ-408: Reporting module (5 pts) - Not Started

━━━ PHASE 2: Metrics Calculation ━━━
Calculating velocity...

Committed: 45 points
Completed: 32 points
Velocity: 32 points
Completion Rate: 71%

Velocity Trend (last 5 sprints):
Sprint 10: 28 pts
Sprint 11: 30 pts
Sprint 12: 35 pts
Sprint 13: 34 pts
Sprint 14: 32 pts
Average: 31.8 pts

Additional Metrics:
- Cycle Time: 4.2 days average
- Throughput: 6 items
- Scope Change: +3 points added mid-sprint
- Bug Rate: 1/8 (12.5%)

━━━ PHASE 3: Incomplete Items ━━━
Analyzing incomplete items...

PROJ-407 (Admin panel):
- Status: 80% complete
- Blocker: Waiting on design approval
- Remaining: ~2 points of work
- Recommendation: Carry over

PROJ-408 (Reporting module):
- Status: Not started
- Reason: Lower priority than bug fixes
- Recommendation: Return to backlog

━━━ PHASE 4: Burndown Analysis ━━━
Generating burndown...

Day 1:  45 pts (Ideal: 45)
Day 3:  40 pts (Ideal: 36)  ← Slow start
Day 5:  35 pts (Ideal: 27)
Day 7:  20 pts (Ideal: 18)
Day 9:  15 pts (Ideal: 9)
Day 10: 13 pts (Ideal: 0)   ← Incomplete

Pattern: Late completion clustering
- 60% of work completed in last 4 days
- Scope increase (+3 pts) on Day 4

━━━ PHASE 5: Retrospective ━━━
Gathering team feedback...

What Went Well:
- API refactoring completed ahead of schedule
- Good collaboration on performance work
- Daily standups were focused

What Didn't Go Well:
- Design approval delayed admin panel
- Scope added mid-sprint
- Started too many items in parallel

Action Items:
1. Get design approval before sprint starts
2. Limit WIP to 2 items per developer
3. Protect sprint scope after day 2

━━━ PHASE 6: Closure ━━━
Closing sprint...
✓ Sprint 14 marked as complete
✓ PROJ-407 moved to Sprint 15
✓ PROJ-408 returned to backlog

Generating report...
Created: docs/sprints/sprint-14-report.md

Communicating closure...
Posted to #team-sprint:
"Sprint 14 closed! Velocity: 32 pts. See full report."

✨ Sprint 14 closed successfully!
```

---

## Related Artifacts

- **Skills**: `.cursor/skills/pm/close-sprint`, `.cursor/skills/pm/generate-burndown`
- **Agent**: `.cursor/agents/pm/sprint-master.md`
- **Patterns**: `patterns/methodologies/agile-scrum.json`
