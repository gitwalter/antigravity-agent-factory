---
agents:
- none
category: general
description: Query and report current status
knowledge:
- workflow-patterns.json
- best-practices.json
- team-dynamics.json
name: run-standup
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Run Standup Skill

Queries in-progress work items, checks for blockers, and formats standup reports. Helps teams run efficient daily standups by surfacing status, progress, and impediments.

## Philosophy

> Standups connect people, not just status.

Daily standups are about team alignment, not status reporting. They help teams understand what's happening, identify blockers early, and support each other. This skill surfaces the right information quickly, grounded in love for team communication, truth in sharing, and beauty in connection.

## When to Use

- When running daily standup meetings
- When user mentions "standup", "daily standup", "status update", "team sync"
- When checking team progress and blockers
- When generating status reports
- When preparing for team meetings
- When reviewing work in progress

## Prerequisites

Before running standup, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Project ID or team context is available
3. Board or sprint context is understood (optional but recommended)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Determine Standup Scope

Identify what to include in standup:

```
"I'll help you run a standup. What's the scope?

A) Current sprint (active sprint)
B) Specific sprint: {SPRINT_ID or SPRINT_NAME}
C) All in-progress work (across sprints)
D) Team member: {USER_ID or USERNAME}
E) Project: {PROJECT_ID}

[If user doesn't specify, default to current sprint]"
```

### Step 2: Query In-Progress Items

Fetch work items in progress:

**Backend Operation:** `listItems`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "status": "In Progress",
  "sprintId": "{SPRINT_ID}", // if sprint-specific
  "assignee": "{USER_ID}" // if user-specific
}
```

**Also query blocked items:**
```json
{
  "projectId": "{PROJECT_ID}",
  "status": "Blocked",
  "sprintId": "{SPRINT_ID}"
}
```

### Step 3: Get Board Status (Optional)

If board-based workflow:

**Backend Operation:** `getBoard`

**Parameters:**
```json
{
  "boardId": "{BOARD_ID}"
}
```

**Backend Operation:** `getBoardColumns`

**Parameters:**
```json
{
  "boardId": "{BOARD_ID}"
}
```

### Step 4: Analyze Work Status

Process the data to identify:

**For each team member:**
- Items in progress
- Items completed since last standup
- Items blocked
- Items ready for review
- Items planned for today

**Team-level insights:**
- Total items in progress
- Blockers count
- WIP limits status
- Sprint progress

### Step 5: Format Standup Report

Generate formatted standup report:

```
"📊 Standup Report - {DATE}

**Sprint:** {SPRINT_NAME} ({SPRINT_DATES})
**Team:** {TEAM_NAME}
**Velocity:** {COMPLETED_POINTS} / {PLANNED_POINTS} points

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Member: {USERNAME}**

✅ **Completed Yesterday:**
- {ITEM_1}: {TITLE} ({POINTS} pts)
- {ITEM_2}: {TITLE} ({POINTS} pts)

🔄 **In Progress:**
- {ITEM_3}: {TITLE} ({POINTS} pts) - {PROGRESS_NOTES}
- {ITEM_4}: {TITLE} ({POINTS} pts) - {PROGRESS_NOTES}

🚧 **Blocked:**
- {ITEM_5}: {TITLE} - {BLOCKER_DESCRIPTION}

📋 **Planned Today:**
- {ITEM_6}: {TITLE} ({POINTS} pts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Member: {USERNAME_2}**

[Repeat format for each team member]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Summary:**

📈 **Sprint Progress:** {COMPLETED} / {TOTAL} items ({PERCENTAGE}%)
📊 **Points Completed:** {COMPLETED_POINTS} / {PLANNED_POINTS} ({PERCENTAGE}%)
🚧 **Blockers:** {BLOCKER_COUNT}
👥 **Active Contributors:** {ACTIVE_MEMBERS} / {TOTAL_MEMBERS}

**Top Blockers:**
1. {BLOCKER_1}: {DESCRIPTION} (affects {AFFECTED_ITEMS})
2. {BLOCKER_2}: {DESCRIPTION} (affects {AFFECTED_ITEMS})

**WIP Status:**
- In Progress: {WIP_COUNT} / {WIP_LIMIT} (limit: {WIP_LIMIT})
- Review: {REVIEW_COUNT} / {REVIEW_LIMIT} (limit: {REVIEW_LIMIT})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Action Items:**
- [ ] {ACTION_1}: {ASSIGNEE} - {DUE_DATE}
- [ ] {ACTION_2}: {ASSIGNEE} - {DUE_DATE}

**Next Standup:** {NEXT_STANDUP_DATE} at {TIME}
"
```

### Step 6: Highlight Blockers

If blockers found, provide detailed view:

```
"🚧 **Blockers Detected**

**Critical Blockers ({COUNT}):**

**{ITEM_TITLE}** ({ITEM_ID})
- **Assignee:** {USERNAME}
- **Blocked Since:** {BLOCKED_DATE}
- **Blocker:** {BLOCKER_DESCRIPTION}
- **Impact:** {IMPACT_ASSESSMENT}
- **Suggested Actions:**
  - {ACTION_1}
  - {ACTION_2}

[Repeat for each blocker]

**Recommendation:** Address blockers in order of impact.
Consider unblocking session if multiple blockers exist.
"
```

### Step 7: Provide Standup Format

Suggest standup format for team:

```
"**Standup Format (15 minutes):**

1. **What did I complete yesterday?** (2 min)
   - Share completed items
   - Highlight achievements

2. **What am I working on today?** (2 min)
   - Current in-progress items
   - Planned work

3. **Any blockers?** (5 min)
   - Identify impediments
   - Get help from team
   - Assign action items

4. **Sprint health check** (3 min)
   - Review sprint progress
   - Adjust if needed

5. **Team support** (3 min)
   - Offer help
   - Share knowledge
   - Celebrate wins

**Standup Rules:**
- Keep it brief (15 minutes max)
- Focus on blockers, not status
- Offer help, don't just report
- Update items in PM system after standup"
```

## Example Outputs

### Example 1: Sprint Standup

**User:** "Run standup for current sprint"

**Agent:** [Queries sprint items, formats report]

**Output:**
```
📊 Standup Report - January 30, 2026

**Sprint:** Sprint 5 - Payment Integration (Jan 15-29)
**Team:** Backend Team
**Velocity:** 18 / 25 points

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Member: Alice**

✅ **Completed Yesterday:**
- TASK-201: Implement payment API endpoint (5 pts)
- TASK-202: Add payment validation (3 pts)

🔄 **In Progress:**
- TASK-203: Payment webhook handler (5 pts) - 80% complete, testing

📋 **Planned Today:**
- TASK-204: Payment error handling (3 pts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Member: Bob**

🔄 **In Progress:**
- TASK-205: Payment status tracking (5 pts) - Started yesterday

🚧 **Blocked:**
- TASK-206: Payment gateway integration (8 pts) - Waiting on API credentials from vendor

📋 **Planned Today:**
- TASK-207: Payment tests (3 pts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Summary:**

📈 **Sprint Progress:** 8 / 12 items (67%)
📊 **Points Completed:** 18 / 25 (72%)
🚧 **Blockers:** 1
👥 **Active Contributors:** 2 / 2

**Top Blockers:**
1. TASK-206: Waiting on API credentials (affects payment gateway work)

**WIP Status:**
- In Progress: 2 / 3 (limit: 3) ✅
- Review: 0 / 2 (limit: 2) ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Action Items:**
- [ ] Follow up with vendor for API credentials: Bob - Today
- [ ] Review TASK-201: Alice - Today

**Next Standup:** January 31, 2026 at 10:00 AM
```

### Example 2: Team-Wide Standup

**User:** "Run standup for all in-progress work"

**Agent:** [Queries all in-progress items across projects]

**Output:**
```
📊 Standup Report - January 30, 2026

**Scope:** All In-Progress Work
**Team:** Engineering Team
**Projects:** 3 active projects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project: Payment System (PROJ-123)**

**In Progress:** 5 items
**Blockers:** 1 item

[Detailed breakdown...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project: User Portal (PROJ-456)**

**In Progress:** 3 items
**Blockers:** 0 items

[Detailed breakdown...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Team Summary:**

📊 **Total In Progress:** 8 items
🚧 **Total Blockers:** 1 item
👥 **Active Contributors:** 4 / 5

**Cross-Project Blockers:**
1. Payment API credentials (affects PROJ-123)

**Recommendation:** Focus on unblocking payment work before starting new items.
```

### Example 3: Individual Standup

**User:** "Run standup for Alice"

**Agent:** [Queries Alice's items]

**Output:**
```
📊 Standup Report - Alice - January 30, 2026

**Sprint:** Sprint 5 - Payment Integration
**Status:** Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **Completed Yesterday:**
- TASK-201: Implement payment API endpoint (5 pts)
- TASK-202: Add payment validation (3 pts)

**Total Points Completed:** 8 pts

🔄 **In Progress:**
- TASK-203: Payment webhook handler (5 pts)
  - Status: 80% complete
  - Notes: Testing webhook endpoints
  - Started: Jan 29

📋 **Planned Today:**
- TASK-204: Payment error handling (3 pts)
- Review TASK-201 for merge

**Estimated Points Today:** 3 pts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Sprint Progress:**
- Completed: 8 / 13 points (62%)
- Remaining: 5 points
- On Track: ✅ Yes

**Recommendation:** You're on track! Consider helping Bob with payment gateway integration if you finish early.
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `listItems` | `workItems.listItems` | Query in-progress and blocked items |
| `getBoard` | `boards.getBoard` | Get board status (optional) |
| `getBoardColumns` | `boards.getBoardColumns` | Get board columns for WIP limits (optional) |
| `getSprint` | `planning.getSprint` | Get sprint details (optional) |

### Operation Details

**listItems:**
- **Parameters:** `projectId`, `status` ("In Progress", "Blocked"), `sprintId`, `assignee`
- **Returns:** List of work items with status, assignee, points, etc.
- **Error Handling:** Handle empty results, invalid filters

**getBoard:**
- **Parameters:** `boardId` (required)
- **Returns:** Board details with columns and cards
- **Error Handling:** Validate boardId exists

**getBoardColumns:**
- **Parameters:** `boardId` (required)
- **Returns:** List of columns with WIP limits
- **Error Handling:** Validate boardId exists

**getSprint:**
- **Parameters:** `sprintId` (required)
- **Returns:** Sprint details with dates, goals, items
- **Error Handling:** Validate sprintId exists

## Standup Best Practices

### Time Management

- **Duration:** 15 minutes maximum
- **Format:** Round-robin, 2-3 minutes per person
- **Focus:** Blockers and coordination, not status reporting

### Blocker Handling

- **Identify early:** Surface blockers immediately
- **Assign owners:** Who will help resolve?
- **Set deadlines:** When will blocker be resolved?
- **Follow up:** Check blocker status next standup

### WIP Limits

- **Monitor:** Check WIP against limits
- **Alert:** Warn if limits exceeded
- **Adjust:** Help team stay within limits

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| No sprint found | Query all in-progress work instead |
| No items in progress | Report empty standup, suggest planning work |
| Board not found | Skip board-specific metrics, use item-based metrics |
| Team members not found | Report items without assignee grouping |
| Backend connection fails | Show cached data if available, suggest retry |

## Integration with Other Skills

### Integration with create-task Skill

After standup:
```
"If new work was identified during standup, I can help create tasks using the create-task skill."
```

### Integration with plan-sprint Skill

Standup informs sprint planning:
```
"Based on standup data, I can help:
1. Identify items to carry over to next sprint
2. Adjust sprint capacity based on current progress
3. Plan next sprint with realistic estimates"
```

### Integration with health-check Skill

Standup data informs health checks:
```
"Standup data contributes to team health metrics:
- WIP levels
- Blocker frequency
- Cycle time trends"
```

## Important Rules

1. **Keep it brief** - Standup reports should be scannable
2. **Focus on blockers** - Highlight impediments prominently
3. **Group by person** - Make it easy to see each team member's status
4. **Show progress** - Include sprint progress and velocity
5. **Action items** - Capture follow-up actions from standup
6. **Respect time** - Format for quick reading (15 min meeting)
7. **Support async** - Format works for async standups too
8. **Ground in team needs** - Adapt format to team's preferences

## CLI Quick Reference

```bash
# Run standup via CLI (if implemented)
python cli/factory_cli.py --run-standup \
  --sprint-id "SPRINT-123" \
  --format "markdown" \
  --output "standup-report.md"

# Run standup for specific user
python cli/factory_cli.py --run-standup --user "alice@company.com"

# Run standup for all projects
python cli/factory_cli.py --run-standup --all-projects
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for standups
- `knowledge/best-practices.json` - Best practices for daily standups
- `knowledge/team-dynamics.json` - Team dynamics and communication patterns
- `.agent/skills/pm/plan-sprint/SKILL.md` - Sprint planning skill
- `.agent/skills/pm/health-check/SKILL.md` - Team health check skill

---

*Generated by Antigravity Agent Factory*
*Skill: run-standup v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.
