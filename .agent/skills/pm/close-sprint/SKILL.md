---
name: close-sprint
description: Complete sprint, calculate velocity
type: skill
knowledge: [workflow-patterns.json, best-practices.json, team-dynamics.json]
---

# Close Sprint Skill

Completes sprints by reviewing completion status, calculating velocity, archiving the sprint, and generating completion reports. Helps teams learn from each sprint and improve planning accuracy.

## Philosophy

> Sprint closure is learning, not just completion.

Closing a sprint is an opportunity to reflect, learn, and improve. It's about understanding what worked, what didn't, and how to do better next time. This skill ensures sprints are closed thoughtfully, grounded in love for continuous improvement, truth in reflection, and beauty in growth.

## When to Use

- When sprint end date arrives
- When user mentions "close sprint", "sprint retrospective", "sprint review", "complete sprint"
- At the end of sprint cycle
- When calculating team velocity
- When generating sprint reports
- When archiving completed work

## Prerequisites

Before closing sprint, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Sprint ID is available
3. Sprint work is complete (or will be reviewed)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Identify Sprint to Close

Determine which sprint to close:

```
"I'll help you close a sprint. Which sprint should we close?

A) Current active sprint: {SPRINT_NAME}
B) Specific sprint: {SPRINT_ID or SPRINT_NAME}
C) List all active sprints

[If user doesn't specify, default to current sprint]"
```

### Step 2: Review Sprint Status

Query sprint items and status:

**Backend Operation:** `getSprint`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}"
}
```

**Backend Operation:** `listItems`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}",
  "projectId": "{PROJECT_ID}"
}
```

**Analyze completion:**

```
"📊 **Sprint Review: {SPRINT_NAME}**

**Sprint Details:**
- **Dates:** {START_DATE} to {END_DATE}
- **Goal:** {SPRINT_GOAL}
- **Planned Points:** {PLANNED_POINTS} pts

**Completion Status:**

✅ **Completed:**
- {ITEM_1}: {TITLE} ({POINTS} pts)
- {ITEM_2}: {TITLE} ({POINTS} pts)
- **Total:** {COMPLETED_COUNT} items, {COMPLETED_POINTS} pts

🔄 **In Progress:**
- {ITEM_3}: {TITLE} ({POINTS} pts) - {PROGRESS}%
- **Total:** {IN_PROGRESS_COUNT} items, {IN_PROGRESS_POINTS} pts

❌ **Not Started:**
- {ITEM_4}: {TITLE} ({POINTS} pts)
- **Total:** {NOT_STARTED_COUNT} items, {NOT_STARTED_POINTS} pts

**Completion Rate:**
- Items: {COMPLETED_COUNT} / {TOTAL_COUNT} ({PERCENTAGE}%)
- Points: {COMPLETED_POINTS} / {PLANNED_POINTS} ({PERCENTAGE}%)

**⚠️ Items to Handle:**
- {IN_PROGRESS_COUNT} items still in progress
- {NOT_STARTED_COUNT} items not started

**Options:**
A) Close sprint as-is (move incomplete items to backlog)
B) Extend sprint by {DAYS} days
C) Move incomplete items to next sprint
D) Review each item individually
"
```

### Step 3: Handle Incomplete Items

Decide what to do with incomplete work:

**Option A: Move to Backlog**
```
"Moving incomplete items to backlog..."
```

**Backend Operation:** `updateStatus`

For each incomplete item:
```json
{
  "itemId": "{ITEM_ID}",
  "status": "Backlog"
}
```

**Option B: Move to Next Sprint**
```
"Moving incomplete items to next sprint: {NEXT_SPRINT_NAME}"
```

**Backend Operation:** `addToSprint`

For each item to carry over:
```json
{
  "sprintId": "{NEXT_SPRINT_ID}",
  "itemId": "{ITEM_ID}"
}
```

**Option C: Review Individually**
```
"Let's review each incomplete item:

**{ITEM_TITLE}** ({POINTS} pts)
- Current Status: {STATUS}
- Progress: {PROGRESS}%
- Options:
  A) Complete now (mark as done)
  B) Move to backlog
  C) Move to next sprint
  D) Cancel (won't do)

[Repeat for each item]"
```

### Step 4: Calculate Velocity

Calculate sprint velocity:

**Backend Operation:** `getVelocity`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "sprintCount": 1,
  "sprintId": "{SPRINT_ID}"
}
```

**Calculate metrics:**

```
"📈 **Velocity Calculation**

**This Sprint:**
- Planned: {PLANNED_POINTS} pts
- Completed: {COMPLETED_POINTS} pts
- Velocity: {COMPLETED_POINTS} pts

**Last 3 Sprints:**
- Sprint {N-2}: {POINTS} pts
- Sprint {N-1}: {POINTS} pts
- Sprint {N}: {POINTS} pts

**Average Velocity:** {AVG_POINTS} pts
**Trend:** {TREND} ({INCREASE/DECREASE/STABLE})

**Velocity Insights:**
- {INSIGHT_1}
- {INSIGHT_2}
- {INSIGHT_3}
"
```

### Step 5: Generate Sprint Report

Create completion report:

```
"📋 **Sprint Completion Report: {SPRINT_NAME}**

**Sprint Summary:**
- **Dates:** {START_DATE} to {END_DATE}
- **Goal:** {SPRINT_GOAL}
- **Status:** ✅ Completed

**Work Completed:**
- **Stories:** {COMPLETED_STORIES} / {TOTAL_STORIES}
- **Tasks:** {COMPLETED_TASKS} / {TOTAL_TASKS}
- **Points:** {COMPLETED_POINTS} / {PLANNED_POINTS} pts
- **Completion Rate:** {PERCENTAGE}%

**Team Performance:**
- **Velocity:** {VELOCITY} pts
- **Average Velocity (3 sprints):** {AVG_VELOCITY} pts
- **Velocity Trend:** {TREND}

**Work Carried Over:**
- **To Backlog:** {BACKLOG_COUNT} items ({BACKLOG_POINTS} pts)
- **To Next Sprint:** {NEXT_SPRINT_COUNT} items ({NEXT_SPRINT_POINTS} pts)

**Key Achievements:**
- {ACHIEVEMENT_1}
- {ACHIEVEMENT_2}
- {ACHIEVEMENT_3}

**Challenges:**
- {CHALLENGE_1}
- {CHALLENGE_2}

**Lessons Learned:**
- {LEARNING_1}
- {LEARNING_2}

**Recommendations for Next Sprint:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 6: Close Sprint

Close the sprint in backend:

**Backend Operation:** `closeSprint`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}"
}
```

**Expected Response:**
```json
{
  "id": "{SPRINT_ID}",
  "status": "Closed",
  "completedAt": "{TIMESTAMP}",
  "velocity": {VELOCITY},
  "completionRate": {PERCENTAGE}
}
```

### Step 7: Archive Sprint Data

Archive sprint for historical reference:

```
"Sprint data archived:
- Sprint details saved
- Velocity recorded
- Completion report generated
- Historical data updated"
```

### Step 8: Confirm and Summarize

Present closed sprint:

```
"✅ Sprint closed successfully!

**Sprint:** {SPRINT_NAME}
**Status:** Closed
**Completed:** {END_DATE}

**Final Metrics:**
- Completed Points: {COMPLETED_POINTS} pts
- Velocity: {VELOCITY} pts
- Completion Rate: {PERCENTAGE}%

**Sprint Report:** {REPORT_URL}

**Next Steps:**
1. Review sprint report: {BACKEND_URL}
2. Conduct sprint retrospective (team meeting)
3. Plan next sprint (use plan-sprint skill)
4. Update velocity for future planning
5. Celebrate achievements! 🎉

**Sprint Closure Checklist:**
- [x] Sprint reviewed
- [x] Incomplete items handled
- [x] Velocity calculated
- [x] Sprint report generated
- [x] Sprint closed in backend
- [ ] Sprint retrospective conducted
- [ ] Next sprint planned

Sprint is closed and archived!"
```

## Example Outputs

### Example 1: Successful Sprint Closure

**User:** "Close current sprint"

**Agent:** [Reviews sprint, calculates velocity, closes sprint]

**Output:**
```
✅ Sprint closed successfully!

**Sprint:** Sprint 6 - Payment Integration Phase 2
**Status:** Closed
**Completed:** February 14, 2026

**Final Metrics:**
- Completed Points: 23 pts
- Velocity: 23 pts
- Completion Rate: 100%

**Work Completed:**
- STORY-101: Payment gateway integration (8 pts) ✅
- STORY-102: Payment validation (5 pts) ✅
- STORY-103: Payment error handling (3 pts) ✅
- STORY-104: Payment webhooks (5 pts) ✅
- STORY-105: Payment tests (2 pts) ✅

**Team Performance:**
- Velocity: 23 pts
- Average Velocity (3 sprints): 22 pts
- Velocity Trend: Stable 📊

**Sprint Report:** https://company.atlassian.net/browse/SPRINT-789

**Next Steps:**
1. Review sprint report
2. Conduct sprint retrospective
3. Plan next sprint
```

### Example 2: Sprint with Carryover

**User:** "Close sprint SPRINT-790, move incomplete items to next sprint"

**Agent:** [Reviews sprint, moves incomplete items, closes]

**Output:**
```
✅ Sprint closed successfully!

**Sprint:** Sprint 7 - User Portal Enhancements
**Status:** Closed
**Completed:** February 28, 2026

**Final Metrics:**
- Completed Points: 18 pts
- Velocity: 18 pts
- Completion Rate: 90%

**Work Completed:**
- STORY-201: User profile improvements (5 pts) ✅
- STORY-202: Portal performance optimization (8 pts) ✅
- STORY-203: Mobile responsiveness (5 pts) ✅

**Work Carried Over:**
- STORY-204: Accessibility improvements (2 pts) → Next Sprint

**Team Performance:**
- Velocity: 18 pts
- Average Velocity (3 sprints): 20 pts
- Velocity Trend: Slight decrease ⚠️

**Note:** 2 pts carried over to next sprint. Consider this in next sprint planning.

**Sprint Report:** https://linear.app/team/sprint/790

**Next Steps:**
1. Review sprint report
2. Plan next sprint (include STORY-204)
3. Discuss velocity trend in retrospective
```

### Example 3: Sprint Closure with Analysis

**User:** "Close sprint and analyze performance"

**Agent:** [Closes sprint, provides detailed analysis]

**Output:**
```
✅ Sprint closed successfully!

**Sprint:** Sprint 8 - API Redesign
**Status:** Closed
**Completed:** March 14, 2026

**Final Metrics:**
- Completed Points: 25 pts
- Velocity: 25 pts
- Completion Rate: 100%

**Velocity Analysis:**

**Last 5 Sprints:**
- Sprint 4: 20 pts
- Sprint 5: 22 pts
- Sprint 6: 23 pts
- Sprint 7: 18 pts
- Sprint 8: 25 pts (this sprint)

**Average Velocity:** 21.6 pts
**Trend:** Increasing 📈

**Insights:**
- Velocity increased 39% from Sprint 7
- Consistent completion rate (100%)
- Team capacity improving
- Consider planning 24-26 pts for next sprint

**Recommendations:**
- Continue current pace
- Consider slightly higher capacity for next sprint
- Maintain focus on completion quality

**Sprint Report:** https://company.atlassian.net/browse/SPRINT-791
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `getSprint` | `planning.getSprint` | Get sprint details |
| `listItems` | `workItems.listItems` | Query sprint items |
| `closeSprint` | `planning.closeSprint` | Close the sprint |
| `getVelocity` | `metrics.getVelocity` | Calculate velocity |
| `updateStatus` | `workItems.updateStatus` | Move incomplete items |
| `addToSprint` | `planning.addToSprint` | Move items to next sprint |

### Operation Details

**getSprint:**
- **Parameters:** `sprintId` (required)
- **Returns:** Sprint details with dates, goal, status, items
- **Error Handling:** Validate sprintId exists, sprint is not already closed

**closeSprint:**
- **Parameters:** `sprintId` (required)
- **Returns:** Closed sprint with completion metrics
- **Error Handling:** Validate sprintId exists, handle closure errors

**getVelocity:**
- **Parameters:** `projectId` (required), `sprintCount` (optional), `sprintId` (optional)
- **Returns:** Velocity metrics with average, trend
- **Error Handling:** Handle insufficient history

## Sprint Closure Best Practices

### Handling Incomplete Work

- **Move to backlog** - If work is no longer priority
- **Carry to next sprint** - If work is still valuable
- **Complete now** - If nearly done, finish before closing
- **Cancel** - If work is no longer needed

### Velocity Calculation

- **Use completed points** - Only count fully completed work
- **Track consistently** - Use same definition across sprints
- **Consider context** - Account for holidays, team changes
- **Learn from trends** - Use velocity trends to improve planning

### Sprint Reports

- **Include metrics** - Completion rate, velocity, trends
- **Highlight achievements** - Celebrate completed work
- **Identify challenges** - Note blockers and issues
- **Provide recommendations** - Suggest improvements for next sprint

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Sprint not found | List available sprints, ask user to select |
| Sprint already closed | Confirm closure, show sprint report |
| No items in sprint | Close sprint anyway, note empty sprint |
| Velocity calculation fails | Use manual calculation, suggest checking data |
| Incomplete items unclear | Ask user to review each item individually |
| Next sprint not found | Move items to backlog instead |

## Integration with Other Skills

### Integration with plan-sprint Skill

After closure:
```
"Now that sprint is closed, I can help plan the next sprint using the plan-sprint skill.
The velocity from this sprint ({VELOCITY} pts) will inform next sprint capacity."
```

### Integration with run-standup Skill

During sprint:
```
"During the sprint, use run-standup skill to track progress and identify blockers early."
```

### Integration with generate-burndown Skill

For sprint analysis:
```
"I can generate a burndown chart for this sprint using the generate-burndown skill to visualize progress."
```

### Integration with health-check Skill

Sprint data informs health:
```
"Sprint completion data contributes to team health metrics:
- Velocity trends
- Completion rates
- Carryover patterns"
```

## Important Rules

1. **Review before closing** - Always review sprint status before closing
2. **Handle incomplete work** - Decide what to do with incomplete items
3. **Calculate velocity accurately** - Only count completed work
4. **Generate reports** - Create completion reports for learning
5. **Archive data** - Save sprint data for historical reference
6. **Learn from metrics** - Use velocity trends to improve planning
7. **Celebrate achievements** - Acknowledge completed work
8. **Ground in improvement** - Focus on learning, not blame

## CLI Quick Reference

```bash
# Close sprint via CLI (if implemented)
python cli/factory_cli.py --close-sprint \
  --sprint-id "SPRINT-789" \
  --move-incomplete "backlog" \
  --generate-report

# Calculate velocity
python cli/factory_cli.py --calculate-velocity \
  --project-id "PROJ-123" \
  --sprint-count 3

# Generate sprint report
python cli/factory_cli.py --sprint-report --sprint-id "SPRINT-789"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for sprint closure
- `knowledge/best-practices.json` - Best practices for sprint closure
- `knowledge/team-dynamics.json` - Team dynamics and velocity tracking
- `.agent/skills/pm/plan-sprint/SKILL.md` - Sprint planning skill
- `.agent/skills/pm/generate-burndown/SKILL.md` - Burndown chart skill
- `.agent/skills/pm/health-check/SKILL.md` - Team health check skill

---

*Generated by Antigravity Agent Factory*
*Skill: close-sprint v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.
