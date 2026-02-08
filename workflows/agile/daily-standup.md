# Daily Standup Workflow

## Overview

Automated workflow for facilitating daily standup meetings, including status collection, blocker identification, and action item tracking. Keeps standups focused and time-boxed while ensuring important information surfaces.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** sprint-master

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../docs/PATH_CONFIGURATION.md).

## Trigger Conditions

This workflow is activated when:

- Scheduled standup time
- User requests standup
- Team status query
- Morning check-in

**Trigger Examples:**
- "Run standup"
- "What's the team status?"
- "Daily standup"
- "Morning check-in"

## Phases

### Phase 1: Status Collection

**Description:** Gather current work status from team and tools.

**Entry Criteria:** Standup triggered  
**Exit Criteria:** Status data collected

#### Step 1.1: Query Active Work

**Description:** Get current in-progress items.

**Actions:**
- Query in-progress items
- Identify assignees
- Check last update time
- Note stale items

**MCP Tools:**
- `atlassian-searchJiraIssues`: Query sprint items
- `github-listIssues`: Get assigned issues

**Query:**
```
Sprint = currentSprint() AND Status = "In Progress"
```

**Outputs:**
- In-progress items list
- Assignee mapping

**Is Mandatory:** Yes

---

#### Step 1.2: Get Recent Completions

**Description:** Identify items completed since last standup.

**Actions:**
- Query recently completed items
- Check completion time
- Note cycle time
- Identify accomplishments

**Query:**
```
Sprint = currentSprint() AND Status = "Done" 
AND Updated >= -24h
```

**Outputs:**
- Recently completed items
- Team accomplishments

**Is Mandatory:** Yes

---

#### Step 1.3: Identify Blockers

**Description:** Find blocked items and issues.

**Actions:**
- Query blocked items
- Check blocker labels
- Review comments for blocks
- Note blocker age

**Blocker Indicators:**
- Status = "Blocked"
- Label contains "blocked"
- No progress in 24+ hours
- Comments mention waiting

**Outputs:**
- Blocked items
- Blocker details

**Is Mandatory:** Yes

---

### Phase 2: Status Formatting

**Description:** Format status information for standup.

**Entry Criteria:** Status collected  
**Exit Criteria:** Report formatted

#### Step 2.1: Format Per-Person Status

**Description:** Organize status by team member.

**Actions:**
- Group items by assignee
- Format yesterday's work
- Format today's plan
- Note blockers per person

**Per-Person Format:**
```
**[Name]**
✅ Yesterday: [completed items]
🔄 Today: [planned items]
🚫 Blockers: [if any]
```

**Outputs:**
- Formatted per-person status

**Is Mandatory:** Yes

---

#### Step 2.2: Create Standup Summary

**Description:** Generate overall standup summary.

**Actions:**
- Compile team summary
- Highlight accomplishments
- Surface all blockers
- Note sprint progress

**Summary Format:**
```
📊 Sprint Progress: X of Y points (Z%)
✅ Completed Today: N items
🔄 In Progress: N items
🚫 Blocked: N items (require attention)
```

**Outputs:**
- Standup summary

**Is Mandatory:** Yes

---

### Phase 3: Blocker Resolution

**Description:** Address and track blockers.

**Entry Criteria:** Blockers identified  
**Exit Criteria:** Blockers documented with actions

#### Step 3.1: Analyze Blockers

**Description:** Understand each blocker.

**Actions:**
- Categorize blocker type
- Identify resolution owner
- Estimate impact
- Suggest resolution

**Blocker Categories:**

| Category | Example | Resolution |
|----------|---------|------------|
| External | Waiting on vendor | Follow up |
| Internal | Need design review | Schedule |
| Technical | Build failing | Debug |
| Resource | Need access | Request |

**Outputs:**
- Blocker analysis

**Is Mandatory:** Yes (if blockers exist)

---

#### Step 3.2: Create Action Items

**Description:** Create actions to resolve blockers.

**Actions:**
- Define specific action
- Assign owner
- Set due date
- Add to tracking

**Action Format:**
```
Action: [What needs to happen]
Owner: [Who will do it]
Due: [When it should be done]
Related: [Blocked item]
```

**Outputs:**
- Action items

**Is Mandatory:** Yes (if blockers exist)

---

### Phase 4: Communication

**Description:** Share standup results.

**Entry Criteria:** Status formatted  
**Exit Criteria:** Team informed

#### Step 4.1: Post Standup Report

**Description:** Share standup summary.

**Actions:**
- Post to team channel
- Tag relevant people
- Highlight urgent items
- Include action items

**Skills:**
- `run-standup`: Report formatting

**Outputs:**
- Posted standup

**Is Mandatory:** Yes

---

#### Step 4.2: Track Metrics

**Description:** Track standup metrics over time.

**Actions:**
- Log completion rate
- Track blocker trends
- Note velocity progress
- Update burndown

**Metrics Tracked:**
- Daily velocity
- Blocker count
- WIP count
- Cycle time

**Outputs:**
- Updated metrics

**Is Mandatory:** No

---

## Decision Points

### Decision: Blocker Severity

**Condition:** For each blocker

**Options:**

| Severity | Criteria | Action |
|----------|----------|--------|
| Critical | Blocks multiple people | Immediate escalation |
| High | Blocks one person, high priority | Same-day resolution |
| Medium | Impacts progress | Track and resolve |
| Low | Minor inconvenience | Note and continue |

---

### Decision: Standup Format

**Condition:** Based on team size and context

**Options:**

| Situation | Format |
|-----------|--------|
| Small team (<5) | Full round-robin |
| Large team (>8) | Focus on blockers |
| Remote team | Async + summary |
| Hybrid | Summary with sync for blockers |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Critical blocker | Immediate notification | Team Lead |
| Stale item (>3 days) | Check-in with assignee | Scrum Master |
| Sprint at risk | Flag for action | Product Owner |
| Resource conflict | Facilitate resolution | Team Lead |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| Daily | Blocker patterns | Process improvement |
| Weekly | Velocity trends | Sprint prediction |
| Sprint end | Standup effectiveness | Format optimization |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Standup Report | Team channel | Communication |
| Action Items | Task tracker | Follow-up |
| Metrics | Dashboard | Tracking |

---

## Standup Report Template

```markdown
# Daily Standup - YYYY-MM-DD

## 📊 Sprint Progress
**Sprint X** - Day Y of Z
Progress: XX/YY points (ZZ%)
Burndown: On Track / At Risk / Behind

## 👥 Team Status

### Alice
✅ Yesterday: Completed user login API
🔄 Today: Starting password reset feature
🚫 Blockers: None

### Bob
✅ Yesterday: Fixed validation bug
🔄 Today: Continuing dashboard widgets
🚫 Blockers: Waiting on design mockup

### Carol
✅ Yesterday: Code review for PR #234
🔄 Today: Database migration script
🚫 Blockers: Need DB admin access

## 🚫 Blockers Requiring Action

| Blocker | Impact | Owner | Action Needed |
|---------|--------|-------|---------------|
| Design mockup | Dashboard blocked | @designer | ETA? |
| DB admin access | Migration blocked | @devops | Grant access |

## ✅ Completed Since Yesterday
- PROJ-123: User login API
- PROJ-124: Validation bug fix

## 📈 Key Metrics
- Velocity today: 13 pts
- WIP items: 5
- Cycle time avg: 3.2 days
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Tool unavailable | Manual status collection |
| Team members absent | Async update request |
| No updates | Check if items stale |
| Time constraint | Focus on blockers only |

---

## Example Session

```
User: Run standup

Agent:
━━━ PHASE 1: Status Collection ━━━
Querying active work...

In Progress (5 items):
- PROJ-501: Dashboard widgets (Bob) - 3 days
- PROJ-502: Password reset (Alice) - 1 day
- PROJ-503: DB migration (Carol) - 2 days
- PROJ-504: API documentation (Dave) - 1 day
- PROJ-505: Bug fixes (Eve) - 1 day

Recently Completed (2 items):
- PROJ-500: User login API (Alice) - Completed yesterday
- PROJ-499: Validation fix (Bob) - Completed yesterday

Blocked Items (2 items):
- PROJ-501: Waiting on design mockup (2 days)
- PROJ-503: Needs DB admin access (1 day)

━━━ PHASE 2: Status Formatting ━━━

# Daily Standup - 2026-02-02

## 📊 Sprint Progress
**Sprint 15** - Day 3 of 10
Progress: 18/45 points (40%)
Burndown: On Track ✓

## 👥 Team Status

### Alice
✅ Yesterday: Completed user login API (PROJ-500)
🔄 Today: Password reset feature (PROJ-502)
🚫 Blockers: None

### Bob
✅ Yesterday: Fixed validation bug (PROJ-499)
🔄 Today: Dashboard widgets (PROJ-501)
🚫 Blockers: Waiting on design mockup (2 days)

### Carol
✅ Yesterday: Started DB migration
🔄 Today: Continue DB migration (PROJ-503)
🚫 Blockers: Need DB admin access

### Dave
✅ Yesterday: Drafted API docs
🔄 Today: Complete API documentation (PROJ-504)
🚫 Blockers: None

### Eve
✅ Yesterday: Triaged bug reports
🔄 Today: Bug fixes (PROJ-505)
🚫 Blockers: None

━━━ PHASE 3: Blocker Resolution ━━━

## 🚫 Blockers Requiring Action

1. **Dashboard design mockup** (2 days old)
   - Blocking: PROJ-501 (Bob)
   - Impact: Medium - not on critical path
   - Action: @designer please provide ETA
   - Owner: Design team

2. **DB admin access** (1 day old)
   - Blocking: PROJ-503 (Carol)
   - Impact: High - migration needed for sprint goal
   - Action: @devops please grant access to staging DB
   - Owner: DevOps

━━━ PHASE 4: Communication ━━━

Posted to #team-sprint:

📊 **Daily Standup - Feb 2**

Sprint 15 Progress: 40% (18/45 pts) ✓ On Track

✅ Completed: 2 items
🔄 In Progress: 5 items
🚫 Blocked: 2 items ⚠️

**Action Items:**
1. @designer - Dashboard mockup ETA?
2. @devops - DB access for Carol

Full report: [link]

✨ Standup complete!
```

---

## Related Artifacts

- **Skills**: `.cursor/skills/pm/run-standup`, `.cursor/skills/pm/health-check`
- **Agent**: `.cursor/agents/pm/sprint-master.md`
- **Patterns**: `patterns/methodologies/agile-scrum.json`
