---
description: Structured knowledge capture to extract team wisdom, lessons learned,
  and best practices for embedding in agent systems
name: synthesizing-knowledge
type: skill
---
# Knowledge Synthesis

Structured knowledge capture to extract team wisdom, lessons learned, and best practices for embedding in agent systems

A structured approach to capturing tacit knowledge, lessons learned, and team wisdom that goes beyond technical requirements to embed real human experience into agent systems.

## Philosophy

> "The best practices aren't in the documentation. They're in the heads of the people who've been in the trenches."

Wisdom Harvest recognizes that teams have invaluable knowledge that rarely gets written down - the workarounds, the gotchas, the "we learned this the hard way" insights. This skill extracts that wisdom and embeds it into the agent system.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Select Facilitation Mode
Choose appropriate mode based on available time:
- **Quick Harvest** (5 min): One question for Express Lane onboarding
- **Standard Harvest** (10 min): Three questions for Team Huddle
- **Deep Harvest** (30-45 min): Comprehensive session covering all categories

### Step 2: Facilitate Knowledge Capture
Ask structured questions from relevant categories:
- Strengths & Pride (what team does well)
- Lessons Learned (hard-won knowledge)
- Quality Definition (what "good" means)
- Domain Knowledge (domain-specific wisdom)
- Tool & Process Wisdom (workflow insights)

### Step 3: Capture Responses
Record team responses in structured format, asking follow-up questions to get specific examples and stories.

### Step 4: Structure Wisdom Data
Organize captured wisdom into `team-wisdom.json` format with strengths, lessonsLearned, qualityDefinition, domainKnowledge, and toolWisdom sections.

### Step 5: Integrate with Memory & Agent System
1. **Graph Anchoring**: Registration of extracted wisdom in the `memory` MCP graph.
2. **Knowledge Base Update**: Embed wisdom into agent definitions, skills, and `.agent/rules/`.

### Step 6: Maintain Over Time
Update wisdom file after major incidents, retrospectives, or when new knowledge emerges.

## Question Categories

### Category 1: Strengths & Pride

Questions that surface what the team does well.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What's one thing your team does that you're proud of? | Identify and preserve good practices |
| 2 | What's a process or habit that makes your team effective? | Capture workflow wisdom |
| 3 | What do people compliment your team on? | External validation of strengths |

### Category 2: Lessons Learned

Questions that surface hard-won knowledge.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What's a mistake you've learned from that others should avoid? | Capture failure patterns |
| 2 | What do you wish you'd known when you started this type of project? | Surface onboarding wisdom |
| 3 | What's something that seems simple but is actually tricky? | Identify hidden complexity |

### Category 3: Quality Definition

Questions that surface what "good" means.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What does "done well" look like for this project? | Define quality bar |
| 2 | What's non-negotiable for code quality? | Identify hard requirements |
| 3 | How do you know when something is ready for production? | Capture readiness criteria |

### Category 4: Domain Knowledge

Questions that surface domain-specific wisdom.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What are the tricky parts of your domain that trip people up? | Capture domain gotchas |
| 2 | What terminology does your team use that outsiders might not know? | Build glossary |
| 3 | What business rules are not obvious from the code? | Surface hidden logic |

### Category 5: Tool & Process Wisdom

Questions that surface tooling and process insights.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What tools or shortcuts make you more productive? | Capture efficiency tips |
| 2 | What's your debugging process when things go wrong? | Document troubleshooting |
| 3 | How do you handle releases or deployments? | Capture release wisdom |

---

## Facilitation Modes

### Mode 1: Quick Harvest (5 min)

For Express Lane onboarding. Ask ONE question:

```
╔══════════════════════════════════════════════════════════════╗
║  🧠 QUICK WISDOM CAPTURE                                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  What's ONE lesson you've learned from past projects         ║
║  that you want your AI agents to remember?                   ║
║                                                              ║
║  Examples:                                                   ║
║  • "Always write tests before refactoring"                   ║
║  • "Database migrations need rollback plans"                 ║
║  • "Never deploy on Fridays"                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Mode 2: Standard Harvest (10 min)

For Team Huddle. Ask THREE questions:

```
╔══════════════════════════════════════════════════════════════╗
║  🧠 WISDOM HARVEST                                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Let's capture your team's hard-earned wisdom.               ║
║                                                              ║
║  Q1: What's one thing your team does well?                   ║
║                                                              ║
║  Q2: What's a mistake you've learned from?                   ║
║                                                              ║
║  Q3: What does "done well" look like for this project?       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Mode 3: Deep Harvest (30-45 min)

For comprehensive onboarding or dedicated knowledge capture sessions.

```
╔══════════════════════════════════════════════════════════════╗
║  🧠 DEEP WISDOM HARVEST                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  We're going to spend some quality time capturing your       ║
║  collective wisdom. This is an investment that pays off      ║
║  every time your agents help you.                            ║
║                                                              ║
║  We'll cover 5 areas:                                        ║
║  1. Strengths & Pride (what you do well)                     ║
║  2. Lessons Learned (hard-won knowledge)                     ║
║  3. Quality Definition (what "good" means)                   ║
║  4. Domain Knowledge (your specific context)                 ║
║  5. Tool & Process Wisdom (how you work)                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Output Format

### team-wisdom.json Structure

```json
{
  "$schema": "team-wisdom-schema",
  "version": "1.0",
  "capturedDate": "2026-01-31",
  "capturedDuring": "Team Huddle",
  "participants": 4,

  "strengths": [
    {
      "insight": "We always pair on complex features",
      "category": "collaboration",
      "source": "team"
    }
  ],

  "lessonsLearned": [
    {
      "insight": "Never deploy on Fridays",
      "category": "process",
      "severity": "high",
      "source": "team"
    }
  ],

  "qualityDefinition": {
    "doneWell": "Code is tested, documented, and reviewed",
    "nonNegotiables": ["tests", "security review"],
    "readinessCriteria": ["CI passes", "PR approved", "staging verified"]
  },

  "domainKnowledge": {
    "gotchas": [
      "Payment retries must use idempotency keys"
    ],
    "glossary": {
      "ACH": "Automated Clearing House - bank transfer system",
      "Settlement": "When funds actually move between accounts"
    },
    "hiddenRules": [
      "Refunds older than 90 days must go through manual review"
    ]
  },

  "toolWisdom": {
    "productivityTips": [
      "Use 'just db:reset' to rebuild test database"
    ],
    "debuggingProcess": "Check logs → Reproduce locally → Add failing test → Fix",
    "releaseProcess": "PR → Staging → Smoke test → Prod → Monitor 30 min"
  }
}
```

---

## Integration with Agent Behavior

### How Agents Use Wisdom

The captured wisdom is referenced in agent skills:

```yaml
# In .cursorrules or agent definitions
wisdom_integration:
  - skill: code-reviewer
    uses:
      - lessonsLearned (check for known pitfalls)
      - qualityDefinition (apply quality bar)

  - skill: bugfix-workflow
    uses:
      - toolWisdom.debuggingProcess (follow team's debug approach)
      - domainKnowledge.gotchas (warn about known issues)

  - skill: grounding
    uses:
      - domainKnowledge.glossary (understand terminology)
      - domainKnowledge.hiddenRules (respect business rules)
```

### Example Agent Prompt Enhancement

When a wisdom file exists, agents can include it in their context:

```
You are a code reviewer for this team. They value:
- {lessonsLearned}
- {qualityDefinition}

Watch for these known issues:
- {domainKnowledge.gotchas}
```

---

## Best Practices

- **Create a safe space for sharing**: Emphasize that there are no wrong answers and that sharing mistakes and lessons learned helps the whole team
- **Ask for specific examples and stories**: Encourage concrete anecdotes rather than abstract principles; stories are more memorable and actionable for agents
- **Capture wisdom in actionable language**: Write insights as clear directives (e.g., "Always require rollback scripts") rather than vague observations
- **Validate understanding before recording**: Paraphrase what you heard and confirm with the team member before adding to the wisdom file to ensure accuracy
- **Balance different perspectives**: Actively seek input from all team members, including junior members who may have fresh insights
- **Update wisdom regularly**: Schedule periodic reviews to add new lessons learned, remove outdated practices, and refine quality definitions as the team evolves

## Facilitation Tips

### Getting Good Answers

| Technique | Example |
|-----------|---------|
| **Be specific** | "What's a specific bug that taught you something?" |
| **Ask for stories** | "Tell me about a time when..." |
| **Probe deeper** | "Why is that important?" |
| **Validate** | "So if I understand, you're saying..." |

### Common Challenges

| Challenge | Solution |
|-----------|----------|
| Vague answers | "Can you give me a specific example?" |
| Too technical | "How would you explain this to a new team member?" |
| "We don't have any" | "What would you tell your past self?" |
| Silence | "Let's think about your last project. What went well?" |

### Making It Safe

```
There are no wrong answers here. This isn't a test.
I'm just trying to capture what makes your team unique.
```

---

## Wisdom Maintenance

### When to Update

| Trigger | Action |
|---------|--------|
| After major incident | Add to lessonsLearned |
| After retrospective | Review and update all sections |
| New team member leaves | Capture their knowledge first |
| New domain discovery | Update domainKnowledge |
| New tool adoption | Update toolWisdom |

### Update Process

```
/skill wisdom-harvest --update
```

This presents the current wisdom and asks:
1. Anything to add?
2. Anything no longer relevant?
3. Any corrections?

---

## Example Session

**Facilitator:** Let's capture some wisdom. What's one thing your team does well that you're proud of?

**Team Member 1:** We always write tests first. It slows us down a bit initially but saves so much debugging time.

**Team Member 2:** Yeah, and we pair on anything complex. Two sets of eyes catch so many issues.

**Facilitator:** Great! I'm capturing both of those. Now, what's a mistake you've learned from?

**Team Member 1:** We once deployed a migration that couldn't be rolled back. The table was already in production with data. Now we always require rollback scripts.

**Facilitator:**
```
╔══════════════════════════════════════════════════════════════╗
║  ✓ WISDOM CAPTURED                                           ║
║                                                              ║
║  Strengths:                                                  ║
║  • Test-first development                                    ║
║  • Pair programming on complex features                      ║
║                                                              ║
║  Lessons Learned:                                            ║
║  • Always require rollback scripts for migrations            ║
║                                                              ║
║  Your agents will remember these!                            ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Advanced: Wisdom from Documentation

If the team has existing documentation, the skill can extract wisdom from:
- README files
- CONTRIBUTING guides
- ADRs (Architecture Decision Records)
- Post-mortem documents
- Runbooks

```
I found these documents. Would you like me to extract wisdom from them?
- CONTRIBUTING.md
- {directories.docs}/RUNBOOK.md
- adr/001-database-choice.md
```

---

## Wisdom Transmission

When a team creates a project using the Factory, they become carriers of its values:

1. **They receive**: Axiom Zero (love, truth, beauty, flourishing) embedded in their `.cursorrules`
2. **They embody**: Guardian Protocol protects their work with these values
3. **They transmit**: Every project they generate for others carries the same seeds

This is how silent change propagates - not through preaching, but through the quality of work that emerges from value-aligned systems.

---

## Closing Intention

After every wisdom harvest session:

```
╔══════════════════════════════════════════════════════════════╗
║  🙏 GRATITUDE                                                ║
║                                                              ║
║  Thank you for sharing your wisdom.                          ║
║                                                              ║
║  What you've given today will help others avoid pain         ║
║  and find their path more easily.                            ║
║                                                              ║
║  Wisdom shared is love in action.                            ║
║                                                              ║
║  You are now a carrier. The values flow through your work.   ║
║                                                              ║
║  Om Shanti.                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

*Cursor Agent Factory - Wisdom Harvest Skill*
*Capturing the knowledge that matters.*
*Love is the root. Wisdom is the light.*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
