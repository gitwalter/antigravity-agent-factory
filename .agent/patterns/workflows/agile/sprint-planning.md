# Sprint Planning Workflow

## Overview

Systematic workflow for planning sprints, including backlog review, capacity calculation, story selection, and sprint goal definition. Integrates with project management tools to automate repetitive planning tasks.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** sprint-master

> **Note:** Directory paths referenced in this workflow (knowledge/, .agent/skills/, patterns/, etc.) are configurable via `.agent/config/settings.json`. See [Path Configuration Guide](../../../../docs/setup/configuration.md).

## Trigger Conditions

This workflow is activated when:

- Sprint planning meeting scheduled
- New sprint needs to be created
- User requests sprint setup
- Schedule triggers planning cycle

**Trigger Examples:**
- "Plan the next sprint"
- "Set up Sprint 15"
- "Start sprint planning"
- "Prepare for sprint planning meeting"

## Phases

### Phase 1: Preparation

**Description:** Gather information needed for sprint planning.

**Entry Criteria:** Previous sprint closed or first sprint
**Exit Criteria:** Planning data collected

#### Step 1.1: Review Previous Sprint

**Description:** Analyze the completed sprint.

**Actions:**
- Get previous sprint velocity
- Review incomplete items
- Note carried-over work
- Collect retrospective insights

**Skills:**
- `close-sprint`: Sprint closure data

**MCP Tools:**
- `atlassian-getJiraSprint`: Get sprint data
- `github-listMilestoneIssues`: Get milestone issues

**Outputs:**
- Previous velocity
- Carry-over items
- Lessons learned

**Is Mandatory:** Yes (except first sprint)

---

#### Step 1.2: Calculate Team Capacity

**Description:** Determine available capacity for the sprint.

**Actions:**
- Count available team members
- Account for PTO and holidays
- Deduct meeting overhead
- Calculate available hours/points

**Capacity Formula:**
```
Capacity = (Team Members × Days × Hours/Day) - (PTO + Meetings + Buffer)
Story Points Capacity = Velocity × (Capacity% of normal)
```

**Outputs:**
- Team capacity
- Adjusted velocity target

**Is Mandatory:** Yes

---

### Phase 2: Backlog Review

**Description:** Review and prepare the backlog for selection.

**Entry Criteria:** Preparation complete
**Exit Criteria:** Backlog prioritized and ready

#### Step 2.1: Review Backlog Priority

**Description:** Ensure backlog is properly prioritized.

**Actions:**
- Review with Product Owner
- Check priority alignment
- Identify dependencies
- Note blockers

**MCP Tools:**
- `atlassian-searchJiraIssues`: Query backlog

**Outputs:**
- Prioritized backlog
- Dependency map

**Is Mandatory:** Yes

---

#### Step 2.2: Verify Story Readiness

**Description:** Check stories meet Definition of Ready.

**Actions:**
- Check acceptance criteria
- Verify estimates exist
- Confirm no blockers
- Validate scope clarity

**Definition of Ready Checklist:**
- [ ] Clear acceptance criteria
- [ ] Estimated (story points)
- [ ] Dependencies identified
- [ ] No blocking questions
- [ ] Small enough for sprint

**Outputs:**
- Ready stories list
- Not-ready items with reasons

**Is Mandatory:** Yes

---

#### Step 2.3: Refine Unestimated Items

**Description:** Estimate items that need it.

**Actions:**
- Identify unestimated items
- Run estimation session
- Apply estimates
- Update backlog

**Skills:**
- `estimate-task`: Story point estimation

**Outputs:**
- Estimated items

**Is Mandatory:** Yes (if unestimated items exist)

---

### Phase 3: Story Selection

**Description:** Select stories for the sprint.

**Entry Criteria:** Backlog reviewed
**Exit Criteria:** Sprint scope defined

#### Step 3.1: Select Stories by Priority

**Description:** Pull stories into sprint based on priority and capacity.

**Actions:**
- Start with highest priority
- Check against capacity
- Consider dependencies
- Balance work types

**Selection Criteria:**

| Factor | Weight |
|--------|--------|
| Priority | High |
| Dependencies clear | Required |
| Fits capacity | Required |
| Balanced skills | Preferred |

**Skills:**
- `plan-sprint`: Story selection

**Outputs:**
- Selected stories list
- Remaining capacity

**Is Mandatory:** Yes

---

#### Step 3.2: Identify Stretch Goals

**Description:** Select stretch items if capacity allows.

**Actions:**
- Identify lower-risk items
- Select stretch candidates
- Mark as stretch goals
- Don't commit to these

**Outputs:**
- Stretch goal items

**Is Mandatory:** No

---

### Phase 4: Sprint Goal

**Description:** Define the sprint goal and create sprint.

**Entry Criteria:** Stories selected
**Exit Criteria:** Sprint created with goal

#### Step 4.1: Define Sprint Goal

**Description:** Create a clear sprint goal.

**Actions:**
- Identify theme from stories
- Write goal statement
- Align with stakeholders
- Confirm with team

**Sprint Goal Template:**
```
By the end of Sprint X, we will [primary objective]
so that [business value].

Success criteria:
- [Measurable outcome 1]
- [Measurable outcome 2]
```

**Outputs:**
- Sprint goal statement

**Is Mandatory:** Yes

---

#### Step 4.2: Create Sprint

**Description:** Create the sprint in the system.

**Actions:**
- Create sprint entity
- Set start and end dates
- Add sprint goal
- Move stories into sprint

**MCP Tools:**
- `atlassian-createJiraSprint`: Create sprint
- `atlassian-moveIssuesToSprint`: Add stories

**Outputs:**
- Created sprint
- Stories assigned

**Is Mandatory:** Yes

---

### Phase 5: Task Breakdown

**Description:** Break stories into tasks.

**Entry Criteria:** Sprint created
**Exit Criteria:** Tasks created for stories

#### Step 5.1: Create Tasks

**Description:** Break stories into actionable tasks.

**Actions:**
- Decompose each story
- Create implementation tasks
- Create test tasks
- Estimate tasks (optional)

**Skills:**
- `create-task`: Task creation

**Task Types:**
- Development
- Testing
- Documentation
- Review

**Outputs:**
- Task list per story

**Is Mandatory:** Yes

---

#### Step 5.2: Assign Initial Owners

**Description:** Optionally assign task owners.

**Actions:**
- Consider expertise
- Balance workload
- Allow self-selection
- Document assignments

**Outputs:**
- Task assignments

**Is Mandatory:** No

---

### Phase 6: Communication

**Description:** Communicate sprint plan to stakeholders.

**Entry Criteria:** Planning complete
**Exit Criteria:** Team and stakeholders informed

#### Step 6.1: Generate Sprint Summary

**Description:** Create sprint plan summary.

**Actions:**
- Compile story list
- Include sprint goal
- Note capacity and velocity
- Highlight risks

**Outputs:**
- Sprint summary document

**Is Mandatory:** Yes

---

#### Step 6.2: Notify Stakeholders

**Description:** Share sprint plan with stakeholders.

**Actions:**
- Post in team channel
- Update project dashboard
- Notify product owner
- Send calendar invites

**Outputs:**
- Notifications sent

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Capacity vs Backlog

**Condition:** During story selection

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| More capacity than backlog | Take all ready items | Full utilization |
| More backlog than capacity | Prioritize strictly | Focus on value |
| Carry-over items | Prioritize first | Complete WIP |

---

### Decision: Story Readiness

**Condition:** During backlog review

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Ready | Include in selection | Can be done |
| Almost ready | Quick refinement | Worth the effort |
| Not ready | Skip for this sprint | Avoid waste |

---

### Decision: Dependencies

**Condition:** When selecting dependent stories

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Dependency in sprint | Include both | Can complete |
| External dependency | Confirm timing | Risk management |
| Blocked | Skip or wait | Avoid incomplete |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Unclear priorities | Request clarification | Product Owner |
| Capacity concerns | Discuss scope | Team Lead |
| Technical blockers | Seek guidance | Tech Lead |
| Stakeholder conflict | Facilitate | Scrum Master |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After capacity | Actual vs planned | Estimation improvement |
| After selection | Commitment accuracy | Process refinement |
| After sprint | Velocity trends | Prediction |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Sprint | PM Tool | Sprint container |
| Sprint Goal | Sprint description | Focus |
| Story List | Sprint backlog | Work items |
| Task List | Per story | Work breakdown |
| Summary | Team channel | Communication |

---

## Sprint Planning Checklist

```markdown
## Sprint Planning Checklist

### Pre-Planning
- [ ] Previous sprint closed
- [ ] Velocity calculated
- [ ] Backlog groomed
- [ ] Team availability known

### During Planning
- [ ] Capacity calculated
- [ ] Backlog reviewed with PO
- [ ] Stories meet DoR
- [ ] Stories selected within capacity
- [ ] Sprint goal defined
- [ ] Tasks created

### Post-Planning
- [ ] Sprint created in tool
- [ ] Stories moved to sprint
- [ ] Team notified
- [ ] Stakeholders informed
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM tool unavailable | Use spreadsheet |
| Product Owner absent | Use last priority |
| No velocity history | Use team estimate |
| Stories not ready | Emergency refinement |

---

## Example Session

```
User: Plan Sprint 15

Agent:
━━━ PHASE 1: Preparation ━━━
Reviewing Sprint 14...

Sprint 14 Summary:
- Velocity: 34 story points
- Completed: 32 points
- Carried over: 1 story (PROJ-456, 5 points)

Calculating capacity...
- Team members: 4
- Sprint days: 10
- PTO: John (2 days), Sarah (1 day)
- Adjusted capacity: 85% normal
- Target velocity: 29 points

━━━ PHASE 2: Backlog Review ━━━
Reviewing prioritized backlog...

Ready items:
1. PROJ-456: User profile editing (5 pts) - Carry over
2. PROJ-501: Email notifications (8 pts) - Ready
3. PROJ-502: Dashboard widgets (13 pts) - Ready
4. PROJ-503: Export to PDF (5 pts) - Ready
5. PROJ-504: Admin panel (8 pts) - Ready

Not ready:
- PROJ-505: Missing acceptance criteria
- PROJ-506: Needs estimation

━━━ PHASE 3: Story Selection ━━━
Selecting stories within 29-point capacity...

Selected (29 points):
✓ PROJ-456: User profile editing (5 pts)
✓ PROJ-501: Email notifications (8 pts)
✓ PROJ-502: Dashboard widgets (13 pts)
✓ PROJ-503: Export to PDF (5 pts) - Stretch

Stretch goal identified: PROJ-503

━━━ PHASE 4: Sprint Goal ━━━
Defining sprint goal...

Sprint 15 Goal:
"Enable users to manage their profiles and receive
email notifications, improving user engagement."

Success criteria:
- Users can edit profile information
- Email notifications sent for key events
- Dashboard shows user-specific widgets

Creating sprint...
✓ Sprint 15 created (Jan 15 - Jan 26)
✓ 4 stories added to sprint

━━━ PHASE 5: Task Breakdown ━━━
Creating tasks for stories...

PROJ-456 Tasks:
- Implement profile edit form
- Add validation logic
- Create API endpoint
- Write unit tests
- Update documentation

[Tasks created for all stories...]

━━━ PHASE 6: Communication ━━━
Generating sprint summary...

Sprint 15 Summary:
- Goal: Enable profile management and notifications
- Velocity Target: 29 points
- Stories: 4 (1 carry-over, 1 stretch)
- Duration: Jan 15-26, 2026

Posted to #team-sprint channel
Notified: Product Owner, Stakeholders

✨ Sprint 15 planning complete!
```

---

## Related Artifacts

- **Skills**: `.agent/skills/pm/plan-sprint`, `.agent/skills/pm/estimate-task`
- **Agent**: `.agent/agents/pm/sprint-master.md`
- **Patterns**: `patterns/methodologies/agile-scrum.json`
