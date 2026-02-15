# Backlog Refinement Workflow

## Overview

Systematic workflow for maintaining a healthy product backlog through prioritization, estimation, story refinement, and readiness verification. Ensures the backlog is always ready for sprint planning.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** product-owner

## Trigger Conditions

This workflow is activated when:

- Weekly refinement session scheduled
- User requests backlog grooming
- New items need estimation
- Pre-planning preparation needed

**Trigger Examples:**
- "Refine the backlog"
- "Groom user stories"
- "Prepare backlog for planning"
- "Estimate new stories"

## Phases

### Phase 1: Backlog Review

**Description:** Analyze current backlog state.

**Entry Criteria:** Refinement triggered
**Exit Criteria:** Backlog state understood

#### Step 1.1: Inventory Backlog

**Description:** Get overview of backlog items.

**Actions:**
- Count total items
- Identify unestimated items
- Find items without acceptance criteria
- Note stale items

**MCP Tools:**
- `atlassian-searchJiraIssues`: Query backlog

**Query:**
```
Project = X AND Type = Story AND Sprint IS EMPTY
ORDER BY Rank ASC
```

**Outputs:**
- Backlog inventory
- Health metrics

**Is Mandatory:** Yes

---

#### Step 1.2: Assess Backlog Health

**Description:** Evaluate backlog quality.

**Actions:**
- Calculate ready percentage
- Identify gaps
- Note aging items
- Check priority distribution

**Health Indicators:**

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Ready % | >60% | 40-60% | <40% |
| Unestimated | <20% | 20-40% | >40% |
| Stale (>30 days) | <10% | 10-25% | >25% |

**Skills:**
- `health-check`: Backlog health

**Outputs:**
- Health assessment

**Is Mandatory:** Yes

---

### Phase 2: Priority Review

**Description:** Review and adjust item priorities.

**Entry Criteria:** Backlog inventoried
**Exit Criteria:** Priorities validated

#### Step 2.1: Review Top Items

**Description:** Ensure top items are correctly prioritized.

**Actions:**
- Review top 20 items
- Validate priority order
- Check business value alignment
- Identify re-prioritization needs

**Priority Factors:**

| Factor | Weight |
|--------|--------|
| Business value | High |
| Dependencies | High |
| Risk/Uncertainty | Medium |
| Effort | Medium |
| Stakeholder request | Medium |

**Outputs:**
- Validated priorities
- Recommended changes

**Is Mandatory:** Yes

---

#### Step 2.2: Apply Priority Changes

**Description:** Update priorities based on review.

**Actions:**
- Discuss with Product Owner
- Reorder items
- Update rankings
- Document rationale

**MCP Tools:**
- `atlassian-updateJiraIssue`: Update priority

**Outputs:**
- Updated priorities

**Is Mandatory:** Yes (if changes needed)

---

### Phase 3: Story Refinement

**Description:** Improve story quality and clarity.

**Entry Criteria:** Priorities set
**Exit Criteria:** Stories refined

#### Step 3.1: Review Acceptance Criteria

**Description:** Ensure stories have clear acceptance criteria.

**Actions:**
- Check each top story
- Add missing AC
- Clarify vague AC
- Verify testability

**Good Acceptance Criteria:**
- Specific and measurable
- Testable
- Reflects user value
- Complete coverage

**AC Template:**
```
Given [precondition]
When [action]
Then [expected result]
```

**Outputs:**
- Refined acceptance criteria

**Is Mandatory:** Yes

---

#### Step 3.2: Clarify Story Details

**Description:** Add missing information to stories.

**Actions:**
- Fill in description gaps
- Add technical notes
- Document assumptions
- Link related items

**Story Quality Checklist:**
- [ ] Clear user story format
- [ ] Business value stated
- [ ] Acceptance criteria complete
- [ ] Dependencies noted
- [ ] Attachments/mockups linked

**Outputs:**
- Improved story details

**Is Mandatory:** Yes

---

#### Step 3.3: Split Large Stories

**Description:** Break down stories that are too large.

**Actions:**
- Identify stories >13 points
- Find natural split points
- Create child stories
- Maintain traceability

**Splitting Strategies:**

| Strategy | Example |
|----------|---------|
| By workflow step | "Search → Filter → Sort" |
| By data type | "Users → Groups → Permissions" |
| By operation | "Create → Read → Update → Delete" |
| By user type | "Admin → User → Guest" |

**Skills:**
- `create-story`: Story creation

**Outputs:**
- Split stories

**Is Mandatory:** Yes (for large stories)

---

### Phase 4: Estimation

**Description:** Estimate unestimated items.

**Entry Criteria:** Stories refined
**Exit Criteria:** Top items estimated

#### Step 4.1: Identify Unestimated Items

**Description:** Find items needing estimates.

**Actions:**
- Query unestimated items
- Prioritize by backlog rank
- Focus on top items first
- Note estimation blockers

**Outputs:**
- Items to estimate

**Is Mandatory:** Yes

---

#### Step 4.2: Conduct Estimation

**Description:** Estimate story points.

**Actions:**
- Present story to team
- Discuss complexity
- Apply estimation technique
- Record estimate

**Estimation Techniques:**

| Technique | Best For |
|-----------|----------|
| Planning Poker | Team estimation |
| T-Shirt Sizing | Quick relative sizing |
| Reference Stories | Comparison-based |
| Affinity Mapping | Large batches |

**Story Point Scale:**
```
1 - Trivial (hours)
2 - Small (day)
3 - Medium (2-3 days)
5 - Large (week)
8 - Very Large (multiple people)
13 - Epic-sized (should split)
```

**Skills:**
- `estimate-task`: Estimation patterns

**Outputs:**
- Story point estimates

**Is Mandatory:** Yes

---

### Phase 5: Readiness Check

**Description:** Verify items are ready for sprint.

**Entry Criteria:** Estimation complete
**Exit Criteria:** Ready items identified

#### Step 5.1: Apply Definition of Ready

**Description:** Check each item against DoR.

**Actions:**
- Check acceptance criteria
- Verify estimate exists
- Confirm no blockers
- Validate scope clarity

**Definition of Ready:**
- [ ] Story in standard format
- [ ] Acceptance criteria defined
- [ ] Story points estimated
- [ ] Dependencies identified
- [ ] No blocking questions
- [ ] Small enough for sprint
- [ ] Mockups/specs attached

**Outputs:**
- Readiness status per item

**Is Mandatory:** Yes

---

#### Step 5.2: Calculate Ready Sprint Coverage

**Description:** Ensure enough ready items for sprints.

**Actions:**
- Sum ready story points
- Compare to velocity
- Calculate sprint coverage
- Identify gaps

**Coverage Calculation:**
```
Ready Points = Sum of ready story points
Sprint Coverage = Ready Points / Avg Velocity
Target: 2-3 sprints of ready items
```

**Outputs:**
- Sprint coverage metric

**Is Mandatory:** Yes

---

### Phase 6: Documentation

**Description:** Document refinement outcomes.

**Entry Criteria:** Readiness verified
**Exit Criteria:** Documentation complete

#### Step 6.1: Update Backlog Status

**Description:** Record refinement changes.

**Actions:**
- Update item statuses
- Record decisions
- Note action items
- Update metrics

**Outputs:**
- Updated backlog

**Is Mandatory:** Yes

---

#### Step 6.2: Generate Refinement Report

**Description:** Create summary of refinement session.

**Actions:**
- Summarize changes
- List refined items
- Note remaining work
- Calculate health improvement

**Report Contents:**
- Items refined
- Estimates added
- Stories split
- Priority changes
- Health before/after

**Outputs:**
- Refinement report

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Story Size

**Condition:** During estimation

**Options:**

| Size | Action | Rationale |
|------|--------|-----------|
| ≤8 points | Accept | Fits in sprint |
| >8 points | Split | Too large |
| Unknown | Spike first | Need research |

---

### Decision: Priority Conflict

**Condition:** Multiple high-priority items

**Options:**

| Situation | Action |
|-----------|--------|
| Clear business value | Prioritize by value |
| Dependencies | Prioritize enablers |
| Stakeholder tie | Escalate to PO |

---

### Decision: Refinement Depth

**Condition:** How much to refine

**Options:**

| Backlog Position | Refinement Level |
|------------------|------------------|
| Top 10 | Full detail |
| 11-25 | AC and estimate |
| 26+ | Basic description |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Priority conflict | Request decision | Product Owner |
| Missing requirements | Request clarification | Business Analyst |
| Technical uncertainty | Request spike | Tech Lead |
| Resource question | Discuss capacity | Scrum Master |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After estimation | Accuracy metrics | Calibration |
| After refinement | Time spent | Efficiency |
| After sprint | Actual vs estimate | Improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Refined Backlog | PM Tool | Sprint planning |
| Refinement Report | Team wiki | Documentation |
| Health Metrics | Dashboard | Tracking |

---

## Refinement Report Template

```markdown
# Backlog Refinement Report - YYYY-MM-DD

## Summary
- Duration: X minutes
- Participants: [list]
- Items Reviewed: N
- Items Refined: N

## Backlog Health
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Ready % | 45% | 65% | 60% |
| Estimated % | 70% | 90% | 80% |
| Sprint Coverage | 1.5 | 2.5 | 2.0 |

## Items Refined

### Newly Estimated
| Item | Points | Notes |
|------|--------|-------|
| PROJ-501 | 5 | Straightforward |
| PROJ-502 | 8 | Complex logic |

### Acceptance Criteria Added
- PROJ-503: Added 5 AC
- PROJ-504: Clarified 3 AC

### Stories Split
- PROJ-505 → PROJ-505a (5 pts) + PROJ-505b (5 pts)

### Priority Changes
- PROJ-506: Moved up (stakeholder request)
- PROJ-507: Moved down (dependency)

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Clarify PROJ-508 scope | PO | Tomorrow |
| Technical spike for PROJ-509 | Dev | This sprint |

## Next Refinement
- Date: YYYY-MM-DD
- Focus: [specific areas]
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PO unavailable | Focus on estimation |
| Team unavailable | Async estimation |
| Tool unavailable | Spreadsheet backup |
| Time constraint | Focus on top items |

---

## Example Session

```
User: Refine the backlog

Agent:
━━━ PHASE 1: Backlog Review ━━━
Inventorying backlog...

Backlog Summary:
- Total items: 45
- Estimated: 32 (71%)
- Ready: 20 (44%)
- Stale (>30 days): 5 (11%)

Health Assessment:
⚠️ Ready percentage below target (44% vs 60%)
✓ Estimated percentage good (71%)
✓ Stale items acceptable (11%)

━━━ PHASE 2: Priority Review ━━━
Reviewing top 20 items...

Priority Issues Found:
1. PROJ-520 (dependency) should be before PROJ-518
2. PROJ-525 (stakeholder request) needs re-prioritization

Recommended Changes:
- Move PROJ-520 to position 3
- Move PROJ-525 to position 8

Applying priority changes...
✓ Priorities updated

━━━ PHASE 3: Story Refinement ━━━
Reviewing acceptance criteria...

Items Missing AC:
- PROJ-521: No acceptance criteria
- PROJ-522: Vague criteria
- PROJ-523: Incomplete criteria

Adding/Improving AC...

PROJ-521: User Profile Settings
Added AC:
- Given a logged-in user, When they access profile page, Then they see current settings
- Given current settings displayed, When user updates email, Then email is validated
- Given valid email, When user saves, Then settings are persisted

[Similar for PROJ-522, PROJ-523...]

Large Stories Identified:
- PROJ-524: 21 points (too large)

Splitting PROJ-524...
Created:
- PROJ-524a: User search (5 pts)
- PROJ-524b: Search filters (8 pts)
- PROJ-524c: Search results pagination (5 pts)

━━━ PHASE 4: Estimation ━━━
Identifying unestimated items...

Unestimated (Top 20): 5 items

Conducting estimation...

| Item | Complexity | Points |
|------|------------|--------|
| PROJ-526 | Simple CRUD | 3 |
| PROJ-527 | Integration | 5 |
| PROJ-528 | Complex logic | 8 |
| PROJ-529 | UI component | 3 |
| PROJ-530 | API endpoint | 2 |

✓ All top 20 items now estimated

━━━ PHASE 5: Readiness Check ━━━
Applying Definition of Ready...

| Item | AC | Estimate | Blockers | Ready |
|------|-----|----------|----------|-------|
| PROJ-501 | ✓ | ✓ | None | ✅ |
| PROJ-502 | ✓ | ✓ | None | ✅ |
| PROJ-503 | ✓ | ✓ | Design | ❌ |
| ... | | | | |

Ready Items: 28
Ready Points: 89
Sprint Coverage: 2.8 sprints ✓

━━━ PHASE 6: Documentation ━━━

# Backlog Refinement Report

## Summary
Items Reviewed: 25
Items Refined: 15
New Estimates: 5
Stories Split: 1

## Health Improvement
| Metric | Before | After |
|--------|--------|-------|
| Ready % | 44% | 62% |
| Estimated % | 71% | 89% |
| Coverage | 1.5 | 2.8 |

## Action Items
1. @designer: Complete mockup for PROJ-503
2. @dev: Spike for PROJ-535 complexity

Report saved to team wiki.

✨ Refinement complete!
```

---

## Related Artifacts

- **Skills**: `.cursor/skills/pm/create-story`, `.cursor/skills/pm/estimate-task`
- **Agent**: `.cursor/agents/pm/product-owner.md`
- **Patterns**: `patterns/methodologies/agile-scrum.json`
