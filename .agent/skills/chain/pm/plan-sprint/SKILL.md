---
agents:
- none
category: general
description: Pull stories into sprint
knowledge:
- workflow-patterns.json
- best-practices.json
- team-dynamics.json
name: plan-sprint
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Plan Sprint Skill

Reviews backlog, checks team capacity, pulls stories into sprint, and creates sprint structure. Helps teams plan realistic sprints that balance ambition with achievability.

## Philosophy

> Sprint planning balances commitment with capacity.

Sprint planning is a collaborative process where teams commit to achievable work. It requires understanding capacity, prioritizing value, and ensuring work is appropriately sized. This skill supports teams in creating sprints grounded in love for realistic planning, truth in capacity assessment, and beauty in commitment.

## When to Use

- When planning a new sprint
- When user mentions "sprint planning", "plan sprint", "sprint", "iteration"
- During sprint planning meetings
- When reviewing backlog for sprint inclusion
- When adjusting sprint scope
- When creating sprint structure

## Prerequisites

Before planning sprint, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Project ID is available
3. Backlog has stories ready for planning
4. Team capacity is understood (or will be gathered)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Determine Sprint Context

Identify sprint planning context:

```
"I'll help you plan a sprint. Let me understand the context:

**Sprint Type:**
A) New sprint (create new)
B) Adjust existing sprint: {SPRINT_ID or SPRINT_NAME}
C) Next sprint in sequence

**Project:** {PROJECT_ID}
**Team:** {TEAM_NAME}

**Sprint Duration:**
- 1 week
- 2 weeks (most common)
- 3 weeks
- 4 weeks
- Custom: {DAYS} days

**Sprint Dates:**
- Start: {START_DATE}
- End: {END_DATE}
"
```

### Step 2: Review Backlog

Query backlog items ready for planning:

**Backend Operation:** `listItems`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "status": "Backlog",
  "type": "story"
}
```

**Also check for unestimated items:**
```json
{
  "projectId": "{PROJECT_ID}",
  "status": "Backlog",
  "estimate": null
}
```

**Format backlog review:**

```
"📋 **Backlog Review**

**Total Stories:** {TOTAL_COUNT}
**Estimated Stories:** {ESTIMATED_COUNT}
**Unestimated Stories:** {UNESTIMATED_COUNT}

**Stories Ready for Planning:**

**High Priority:**
- {STORY_1}: {TITLE} ({POINTS} pts) - {PRIORITY_REASON}
- {STORY_2}: {TITLE} ({POINTS} pts) - {PRIORITY_REASON}

**Medium Priority:**
- {STORY_3}: {TITLE} ({POINTS} pts)
- {STORY_4}: {TITLE} ({POINTS} pts)

**Low Priority:**
- {STORY_5}: {TITLE} ({POINTS} pts)
- {STORY_6}: {TITLE} ({POINTS} pts)

**⚠️ Unestimated Stories:**
- {STORY_7}: {TITLE} - Needs estimation
- {STORY_8}: {TITLE} - Needs estimation

**Total Points Available:** {TOTAL_POINTS} pts
"
```

### Step 3: Check Team Capacity

Determine team capacity:

```
"**Team Capacity Assessment**

**Team Members:** {TEAM_SIZE}
**Sprint Duration:** {DURATION} weeks

**Individual Capacity:**
- {MEMBER_1}: {CAPACITY} pts (available {DAYS} days)
- {MEMBER_2}: {CAPACITY} pts (available {DAYS} days)
- {MEMBER_3}: {CAPACITY} pts (available {DAYS} days)

**Team Velocity (Last 3 Sprints):**
- Sprint {N-2}: {POINTS} pts
- Sprint {N-1}: {POINTS} pts
- Sprint {N}: {POINTS} pts
- **Average:** {AVG_POINTS} pts

**Recommended Capacity:** {RECOMMENDED_POINTS} pts
(Based on {AVG_POINTS} avg velocity with {BUFFER}% buffer)

**Capacity Factors:**
- Holidays: {HOLIDAY_COUNT} days
- Time off: {TIME_OFF_COUNT} days
- Other commitments: {COMMITMENT_POINTS} pts
"
```

**Backend Operation:** `getVelocity`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "sprintCount": 3
}
```

### Step 4: Select Stories for Sprint

Help team select stories:

```
"**Story Selection**

**Recommended Capacity:** {CAPACITY} pts

**Selected Stories ({CURRENT_POINTS} pts):**

✅ {STORY_1}: {TITLE} ({POINTS} pts)
✅ {STORY_2}: {TITLE} ({POINTS} pts)
✅ {STORY_3}: {TITLE} ({POINTS} pts)

**Remaining Capacity:** {REMAINING} pts

**Available Stories:**
- {STORY_4}: {TITLE} ({POINTS} pts) - Fits ✅
- {STORY_5}: {TITLE} ({POINTS} pts) - Too large ⚠️
- {STORY_6}: {TITLE} ({POINTS} pts) - Fits ✅

**Recommendations:**
- Add {STORY_4} to reach {NEW_TOTAL} pts
- Consider breaking down {STORY_5} if needed
- Leave {BUFFER} pts buffer for unexpected work

Would you like to:
A) Add more stories
B) Remove stories
C) Finalize sprint with current selection
D) Adjust capacity
"
```

### Step 5: Create Sprint

If new sprint, create it:

**Backend Operation:** `createSprint`

**Parameters:**
```json
{
  "name": "{SPRINT_NAME}",
  "startDate": "{START_DATE}",
  "endDate": "{END_DATE}",
  "projectId": "{PROJECT_ID}",
  "goal": "{SPRINT_GOAL}"
}
```

**Expected Response:**
```json
{
  "id": "{SPRINT_ID}",
  "name": "{SPRINT_NAME}",
  "startDate": "{START_DATE}",
  "endDate": "{END_DATE}",
  "projectId": "{PROJECT_ID}",
  "goal": "{SPRINT_GOAL}",
  "status": "Planning"
}
```

### Step 6: Add Stories to Sprint

Add selected stories to sprint:

**Backend Operation:** `addToSprint`

**For each selected story:**
```json
{
  "sprintId": "{SPRINT_ID}",
  "itemId": "{STORY_ID}"
}
```

**Track additions:**
- Successfully added: {COUNT}
- Failed: {FAILED_ITEMS}

### Step 7: Set Sprint Goal

Define sprint goal:

```
"**Sprint Goal**

What is the primary goal for this sprint?

**Sprint Goal:**
{GOAL_DESCRIPTION}

**Success Criteria:**
- {CRITERION_1}
- {CRITERION_2}
- {CRITERION_3}

**Key Deliverables:**
- {DELIVERABLE_1}
- {DELIVERABLE_2}
"
```

### Step 8: Confirm and Summarize

Present planned sprint:

```
"✅ Sprint planned successfully!

**Sprint Details:**
- **ID:** {SPRINT_ID}
- **Name:** {SPRINT_NAME}
- **Dates:** {START_DATE} to {END_DATE}
- **Duration:** {DURATION} weeks
- **Goal:** {SPRINT_GOAL}

**Sprint Contents:**
- **Stories:** {STORY_COUNT} stories
- **Total Points:** {TOTAL_POINTS} pts
- **Team Capacity:** {CAPACITY} pts
- **Utilization:** {PERCENTAGE}%

**Stories:**
{STORY_LIST}

**Team Members:**
{TEAM_MEMBER_LIST}

**Next Steps:**
1. Review sprint: {BACKEND_URL}
2. Break down stories into tasks (use create-task skill)
3. Assign work to team members
4. Start sprint on {START_DATE}
5. Run daily standups (use run-standup skill)

**Sprint Planning Checklist:**
- [x] Sprint created
- [x] Stories selected
- [x] Stories added to sprint
- [x] Sprint goal defined
- [ ] Stories broken into tasks
- [ ] Tasks assigned to team members
- [ ] Sprint kickoff scheduled

Sprint is ready to start!"
```

## Example Outputs

### Example 1: New Sprint Planning

**User:** "Plan a new 2-week sprint for PROJ-123"

**Agent:** [Reviews backlog, checks capacity, creates sprint]

**Output:**
```
✅ Sprint planned successfully!

**Sprint Details:**
- **ID:** SPRINT-789
- **Name:** Sprint 6 - Payment Integration Phase 2
- **Dates:** February 3, 2026 to February 14, 2026
- **Duration:** 2 weeks
- **Goal:** Complete payment processing integration and testing

**Sprint Contents:**
- **Stories:** 5 stories
- **Total Points:** 23 pts
- **Team Capacity:** 25 pts
- **Utilization:** 92%

**Stories:**
- STORY-101: Payment gateway integration (8 pts)
- STORY-102: Payment validation (5 pts)
- STORY-103: Payment error handling (3 pts)
- STORY-104: Payment webhooks (5 pts)
- STORY-105: Payment tests (2 pts)

**Team Members:**
- Alice (8 pts capacity)
- Bob (8 pts capacity)
- Charlie (9 pts capacity)

**Next Steps:**
1. Review sprint: https://company.atlassian.net/browse/SPRINT-789
2. Break down stories into tasks
3. Assign work to team members
4. Start sprint on February 3, 2026
```

### Example 2: Sprint Adjustment

**User:** "Add STORY-106 to current sprint"

**Agent:** [Checks sprint capacity, adds story]

**Output:**
```
✅ Story added to sprint!

**Sprint:** Sprint 6 - Payment Integration Phase 2
**Story Added:** STORY-106: Payment refunds (5 pts)

**Updated Sprint:**
- **Stories:** 6 stories
- **Total Points:** 28 pts
- **Team Capacity:** 25 pts
- **Utilization:** 112% ⚠️

**⚠️ Warning:** Sprint is over capacity!
- Current: 28 pts
- Capacity: 25 pts
- Over by: 3 pts

**Recommendations:**
- Remove a smaller story (e.g., STORY-105: 2 pts)
- Extend sprint by 1-2 days
- Reduce scope of a story
- Accept risk and plan to carry over

Would you like to adjust the sprint?
```

### Example 3: Capacity-Based Planning

**User:** "Plan sprint with 20 point capacity"

**Agent:** [Selects stories to fit capacity]

**Output:**
```
✅ Sprint planned successfully!

**Sprint Details:**
- **ID:** SPRINT-790
- **Name:** Sprint 7 - User Portal Enhancements
- **Dates:** February 17, 2026 to February 28, 2026
- **Duration:** 2 weeks
- **Goal:** Improve user portal usability and performance

**Sprint Contents:**
- **Stories:** 4 stories
- **Total Points:** 20 pts
- **Team Capacity:** 20 pts
- **Utilization:** 100%

**Stories Selected:**
- STORY-201: User profile improvements (5 pts)
- STORY-202: Portal performance optimization (8 pts)
- STORY-203: Mobile responsiveness (5 pts)
- STORY-204: Accessibility improvements (2 pts)

**Stories Not Selected (for next sprint):**
- STORY-205: Portal redesign (13 pts) - Too large, consider breaking down
- STORY-206: Advanced search (5 pts) - Lower priority

**Next Steps:**
1. Review sprint: https://linear.app/team/sprint/790
2. Break down stories into tasks
3. Start sprint on February 17, 2026
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `listItems` | `workItems.listItems` | Query backlog stories |
| `getVelocity` | `metrics.getVelocity` | Get team velocity for capacity planning |
| `createSprint` | `planning.createSprint` | Create new sprint |
| `addToSprint` | `planning.addToSprint` | Add stories to sprint |
| `getSprint` | `planning.getSprint` | Get sprint details (for adjustments) |
| `listSprints` | `planning.listSprints` | List sprints (for context) |

### Operation Details

**listItems:**
- **Parameters:** `projectId`, `status` ("Backlog"), `type` ("story"), `estimate`
- **Returns:** List of stories with estimates
- **Error Handling:** Handle empty backlog, unestimated items

**getVelocity:**
- **Parameters:** `projectId` (required), `sprintCount` (optional, default 3)
- **Returns:** Velocity metrics with average, trend
- **Error Handling:** Handle insufficient history, use defaults

**createSprint:**
- **Parameters:** `name` (required), `startDate`, `endDate` (required), `projectId` (required), `goal`
- **Returns:** Created sprint with ID
- **Error Handling:** Validate dates, check for overlapping sprints

**addToSprint:**
- **Parameters:** `sprintId` (required), `itemId` (required)
- **Returns:** Updated sprint
- **Error Handling:** Validate sprintId exists, itemId exists, sprint is not closed

## Sprint Planning Best Practices

### Capacity Planning

- **Use historical velocity** - Average of last 3 sprints
- **Account for time off** - Reduce capacity for holidays/vacation
- **Include buffer** - 10-20% buffer for unexpected work
- **Consider team changes** - Adjust for new/leaving members

### Story Selection

- **Prioritize value** - Select highest value stories first
- **Balance size** - Mix of small, medium, and large stories
- **Consider dependencies** - Ensure dependencies are met
- **Include testing** - Don't forget testing and documentation

### Sprint Goals

- **Single focus** - One clear goal per sprint
- **Measurable** - Define success criteria
- **Achievable** - Goal should be realistic
- **Valuable** - Goal should deliver value to stakeholders

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Backlog is empty | Suggest creating stories first (use create-story skill) |
| No velocity history | Use team capacity estimate, suggest tracking velocity |
| Stories unestimated | Warn user, suggest estimating first (use estimate-task skill) |
| Sprint creation fails | Show error, suggest checking dates and project ID |
| Story addition fails | Continue with other stories, note failures |
| Over capacity | Warn user, suggest removing stories or extending sprint |

## Integration with Other Skills

### Integration with create-story Skill

Before planning:
```
"If backlog is empty, I can help create stories using the create-story skill."
```

### Integration with estimate-task Skill

During planning:
```
"If stories are unestimated, I can help estimate them using the estimate-task skill before adding to sprint."
```

### Integration with create-task Skill

After planning:
```
"After planning, I can help break down stories into tasks using the create-task skill."
```

### Integration with run-standup Skill

During sprint:
```
"During the sprint, use run-standup skill to track progress and identify blockers."
```

### Integration with close-sprint Skill

After sprint:
```
"After sprint ends, use close-sprint skill to calculate velocity and plan next sprint."
```

## Important Rules

1. **Respect capacity** - Don't overcommit, use historical velocity
2. **Prioritize value** - Select highest value stories first
3. **Ensure estimation** - Stories should be estimated before planning
4. **Set clear goals** - Define sprint goal and success criteria
5. **Balance size** - Mix story sizes for flexibility
6. **Account for time off** - Reduce capacity for holidays/vacation
7. **Include buffer** - Leave 10-20% buffer for unexpected work
8. **Ground in reality** - Plan achievable sprints, not aspirational ones

## CLI Quick Reference

```bash
# Plan sprint via CLI (if implemented)
python cli/factory_cli.py --plan-sprint \
  --project-id "PROJ-123" \
  --duration "2_weeks" \
  --start-date "2026-02-03" \
  --capacity "25"

# Add story to sprint
python cli/factory_cli.py --add-to-sprint \
  --sprint-id "SPRINT-789" \
  --story-id "STORY-101"

# List sprint stories
python cli/factory_cli.py --list-sprint-stories --sprint-id "SPRINT-789"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for sprint planning
- `knowledge/best-practices.json` - Best practices for sprint planning
- `knowledge/team-dynamics.json` - Team dynamics and capacity planning
- `.agent/skills/pm/create-story/SKILL.md` - Story creation skill
- `.agent/skills/pm/estimate-task/SKILL.md` - Story estimation skill
- `.agent/skills/pm/close-sprint/SKILL.md` - Sprint closure skill

---

*Generated by Antigravity Agent Factory*
*Skill: plan-sprint v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.
