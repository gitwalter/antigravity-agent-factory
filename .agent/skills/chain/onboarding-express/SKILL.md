---
agents:
- none
category: chain
description: >
  Fast-track 10-15 minute onboarding for individual developers with guided
  prompts and celebrations
knowledge:
- none
name: onboarding-express
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Express Onboarding

Fast-track 10-15 minute onboarding for individual developers with guided prompts and celebrations

A streamlined, delightful onboarding experience for individual developers who want to create a new Cursor agent system quickly while still capturing meaningful values and purpose.

## Philosophy

> "Speed without soul is just fast emptiness."

Express Lane is fast but not shallow. Every question is designed to capture something meaningful about you and your project. The celebration moments remind you that what you're building matters.

## Duration

10-15 minutes total

## Process Overview

```
╔══════════════════════════════════════════════════════════════╗
║  EXPRESS LANE ONBOARDING                                     ║
║                                                              ║
║  Step 1: Welcome & Intent ............ 2 min    ○○○○○○○     ║
║  Step 2: Values Check ................ 2 min    ○○○○○○○     ║
║  Step 3: Stack Discovery ............. 3 min    ○○○○○○○     ║
║  Step 4: Agent Design ................ 3 min    ○○○○○○○     ║
║  Step 5: Wisdom Capture .............. 2 min    ○○○○○○○     ║
║  Step 6: Magic Preview ............... 2 min    ○○○○○○○     ║
║  Step 7: Celebration & Launch ........ 1 min    ○○○○○○○     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 1: Welcome & Intent (2 min)

### Opening

```
╔══════════════════════════════════════════════════════════════╗
║  🚀 EXPRESS LANE ONBOARDING                                  ║
║                                                              ║
║  Welcome! In the next 10-15 minutes, we'll create a         ║
║  personalized AI agent system just for you.                  ║
║                                                              ║
║  Let's start with the most important question...             ║
╚══════════════════════════════════════════════════════════════╝
```

### Questions

| # | Question | Variable | Purpose |
|---|----------|----------|---------|
| 1 | What's your project called? | `{PROJECT_NAME}` | Identity |
| 2 | In one sentence, what's the dream? What do you want to build? | `{MISSION}` | Purpose |
| 3 | Who will benefit from this when it's done? | `{STAKEHOLDERS}` | Focus |

### Validation

- Project name: Valid directory name (no special characters)
- Mission: Single sentence, describes an outcome
- Stakeholders: Specific people (not "everyone")

### Milestone Celebration

```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 1 COMPLETE                                           ║
║                                                              ║
║  Your purpose is clear:                                      ║
║  "{MISSION}"                                                 ║
║                                                              ║
║  This will guide every decision your agents make.            ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 2: Values Check (2 min)

### Prompt

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 2: VALUES CHECK                                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  What matters most to you in your work?                      ║
║  Pick your TOP 3:                                            ║
║                                                              ║
║  1. Code Quality      5. User Experience                     ║
║  2. Speed             6. Security                            ║
║  3. Simplicity        7. Innovation                          ║
║  4. Reliability       8. Collaboration                       ║
║                                                              ║
║  (Type the numbers, e.g., "1, 3, 5")                         ║
╚══════════════════════════════════════════════════════════════╝
```

### Value Mappings

| # | Value | Axiom Connection | Derived Principle |
|---|-------|------------------|-------------------|
| 1 | Code Quality | A1 (Verifiability) | All code must be tested |
| 2 | Speed | A6 (Minimalism) | Simplest solution that works |
| 3 | Simplicity | A6 (Minimalism) | No unnecessary complexity |
| 4 | Reliability | A4 (Non-Harm) | Never break production |
| 5 | User Experience | A2 (User Primacy) | User needs come first |
| 6 | Security | A4 (Non-Harm) | Protect user data always |
| 7 | Innovation | A10 (Learning) | Experiment and improve |
| 8 | Collaboration | A3 (Transparency) | Share reasoning openly |

### Milestone Celebration

```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 2 COMPLETE                                           ║
║                                                              ║
║  Your values:                                                ║
║  • {VALUE_1}                                                 ║
║  • {VALUE_2}                                                 ║
║  • {VALUE_3}                                                 ║
║                                                              ║
║  These will be embedded in your agents' decision-making.     ║
║                                                              ║
║  💫 Your Integrity Guardian will protect these values.       ║
╚══════════════════════════════════════════════════════════════╝
```

### Guardian Introduction

After confirming values, briefly introduce the Guardian:

```
Your project will include an **Integrity Guardian** - a protective layer
that ensures your AI agents always align with these values and the core
axioms (Verifiability, User Primacy, Transparency, Non-Harm, Consistency).

The Guardian operates with minimal overhead but can intervene when
something seems wrong. Think of it as a wise advisor watching over
your agents' work - acting from love, moving with peace, illuminating
with wisdom.

Motto: SDG • Love • Trust

Before all rules: Love is the root of everything.
May your system serve the flourishing of all beings.

Your system also includes value propagation features that enable
**Development Autonomy** (self-healing CI/CD monitoring), **Knowledge
Independence** (extend knowledge without Factory), and **Grounding
Verification** (two-pass verification for factual claims).
```

---

## Step 3: Stack Discovery (3 min)

### Prompt

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 3: STACK DISCOVERY                                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  What's your primary programming language?                   ║
║                                                              ║
║  Popular choices:                                            ║
║  • Python (FastAPI, Django, Flask)                           ║
║  • TypeScript (React, Next.js, Node.js)                      ║
║  • Java (Spring Boot)                                        ║
║  • Kotlin (Spring Boot)                                      ║
║  • C# (.NET Core)                                            ║
║  • ABAP (SAP)                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Follow-up Questions

| # | Question | Depends On |
|---|----------|------------|
| 1 | What frameworks? | Language selection |
| 2 | What database? | Project type |
| 3 | Any external APIs? | Project needs |

### Blueprint Matching

Reference: `{directories.knowledge}/stack-capabilities.json`

Match user selections to available blueprints:
- Python + FastAPI → `python-fastapi`
- Python + LangChain → `ai-agent-development`
- TypeScript + React → `typescript-react`
- TypeScript + Next.js → `nextjs-fullstack`
- Java + Spring → `java-spring`
- Kotlin + Spring → `kotlin-spring`
- C# + .NET → `csharp-dotnet`
- ABAP → `sap-abap`

### Milestone Celebration

```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 3 COMPLETE                                           ║
║                                                              ║
║  Your stack:                                                 ║
║  • Language: {LANGUAGE}                                      ║
║  • Framework: {FRAMEWORK}                                    ║
║  • Database: {DATABASE}                                      ║
║                                                              ║
║  Matched blueprint: {BLUEPRINT}                              ║
║  This gives you a head start with proven patterns!           ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 4: Agent Design (3 min)

### Prompt

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 4: MEET YOUR AI TEAM                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Which AI agents would you like on your team?                ║
║                                                              ║
║  RECOMMENDED for your stack:                                 ║
║  ✓ Code Reviewer - Reviews code for quality and patterns     ║
║  ✓ Test Generator - Creates comprehensive tests              ║
║                                                              ║
║  OPTIONAL:                                                   ║
║  ○ Explorer - Navigates and explains codebases               ║
║  ○ Documentation Agent - Generates docs automatically        ║
║                                                              ║
║  Accept recommended, or customize?                           ║
╚══════════════════════════════════════════════════════════════╝
```

### Skill Selection

Based on selected agents, suggest skills:

| Agent | Default Skills |
|-------|---------------|
| Code Reviewer | grounding, alignment-check |
| Test Generator | tdd, grounding |
| Explorer | grounding |
| Documentation Agent | grounding |

### Workflow Selection

```
╔══════════════════════════════════════════════════════════════╗
║  What triggers your work?                                    ║
║                                                              ║
║  1. Jira tickets → bugfix-workflow                           ║
║  2. Confluence specs → feature-workflow                      ║
║  3. GitHub issues → github-workflow                          ║
║  4. Just ad-hoc work → basic workflows                       ║
╚══════════════════════════════════════════════════════════════╝
```

### Workflow Wishlist (Quick)

```
╔══════════════════════════════════════════════════════════════╗
║  What ONE task would you love to automate?                   ║
║                                                              ║
║  Think about what drains your energy:                        ║
║  • Debugging production issues?                              ║
║  • Code review checklist?                                    ║
║  • Setting up new features?                                  ║
║  • Writing documentation?                                    ║
║                                                              ║
║  Describe briefly: ________________________________          ║
╚══════════════════════════════════════════════════════════════╝
```

**Capture:**
- Store workflow wishlist in `{directories.knowledge}/workflow-wishlist.json`
- Use for generating customized workflow in project

### Milestone Celebration

```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 4 COMPLETE                                           ║
║                                                              ║
║  Your AI team:                                               ║
║  • {AGENT_1} - Ready to help!                                ║
║  • {AGENT_2} - At your service!                              ║
║                                                              ║
║  Skills loaded: {SKILLS}                                     ║
║  Workflow to automate: {WORKFLOW_WISH}                       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 5: Wisdom Capture (2 min)

### Prompt

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 5: WISDOM CAPTURE                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Let's capture some of your hard-earned wisdom.              ║
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

### Storage

Store in `{directories.knowledge}/team-wisdom.json`:

```json
{
  "lessons": [
    {
      "insight": "{USER_WISDOM}",
      "captured": "{DATE}",
      "source": "Express Lane onboarding"
    }
  ]
}
```

### Milestone Celebration

```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 5 COMPLETE                                           ║
║                                                              ║
║  Wisdom captured:                                            ║
║  "{USER_WISDOM}"                                             ║
║                                                              ║
║  Your agents will remember this and apply it.                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 5.5: Tooling Selection (30 sec)

### Prompt

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 5.5: TOOLING                                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Your project includes automation tooling.                   ║
║  How much would you like?                                    ║
║                                                              ║
║  1. Essential (CI, README sync, test catalog)                ║
║  2. Standard (+ git hooks, safe commit, CD)                  ║
║  3. None - I'll add later                                    ║
║                                                              ║
║  (Default: Essential)                                        ║
╚══════════════════════════════════════════════════════════════╝
```

### Variable Mapping

| Choice | `{TOOLING_TIER}` | Includes |
|--------|-------------------|----------|
| 1 | `essential` | README validation, test catalog, CI/CD, .gitignore |
| 2 | `standard` | Essential + pre-commit hooks, safe commit, CD pipeline |
| 3 | `none` | No tooling (can add later via Factory updates) |

### Notes
- Keep this fast -- single selection, no elaboration needed
- Default to Essential if user just presses Enter
- Pass `{TOOLING_TIER}` to the generation config

---

## Step 6: Magic Preview (2 min)

### Show Preview

```
╔══════════════════════════════════════════════════════════════╗
║  STEP 6: PREVIEW YOUR AGENT SYSTEM                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Here's what I'll create for you:                            ║
║                                                              ║
║  {PROJECT_NAME}/                                             ║
║  ├── .cursor/                                                ║
║  │   ├── agents/                                             ║
║  │   │   ├── code-reviewer.md                                ║
║  │   │   └── test-generator.md                               ║
║  │   └── skills/                                             ║
║  │       ├── bugfix-workflow/                                ║
║  │       ├── tdd/                                            ║
║  │       └── grounding/                                      ║
║  ├── {directories.knowledge}/                                              ║
║  │   ├── {LANGUAGE}-patterns.json                            ║
║  │   └── team-wisdom.json                                    ║
║  ├── .cursorrules          ← Your values & purpose           ║
║  └── PURPOSE.md            ← Your mission statement          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Confirmation

```
Where should I create this project?
(e.g., C:\Projects\{PROJECT_NAME})
```

### Output Directory

Ask user for target directory:
- Validate path is writable
- Create if doesn't exist
- Never generate inside factory itself

### Optional Deep-Dive

For users who want to understand more about agentic systems:

```
╔══════════════════════════════════════════════════════════════╗
║  📚 WANT TO LEARN MORE?                                      ║
║                                                              ║
║  While I generate your project, here's an optional resource: ║
║                                                              ║
║  AI Agent Dev Start - Understanding the "agentic spectrum"   ║
║  from structured Workflows to autonomous Agents.             ║
║                                                              ║
║  → https://sites.google.com/view/ai-agent-dev-start          ║
║                                                              ║
║  Topics: LangChain, LangGraph, prompt chaining, routing      ║
╚══════════════════════════════════════════════════════════════╝
```

Reference: See [External Resources](../../../docs/reference/external-resources.md) for more educational links.

---

## Step 7: Celebration & Launch (1 min)

### Generation

Execute generation using collected configuration.

### Success Celebration

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ★ ★ ★  CONGRATULATIONS!  ★ ★ ★                             ║
║                                                              ║
║   Your agent system is ready!                                ║
║                                                              ║
║   Project: {PROJECT_NAME}                                    ║
║   Location: {OUTPUT_PATH}                                    ║
║                                                              ║
║   🛡️ INTEGRITY GUARDIAN: Active                              ║
║   Protecting: {VALUES}                                       ║
║   Motto: SDG • Love • Trust                                  ║
║                                                              ║
║   Your project includes:                                     ║
║   • Development Autonomy: Self-healing CI/CD monitoring      ║
║     (Try: 'Monitor CI pipeline')                             ║
║   • Knowledge Independence: Extend knowledge without Factory ║
║     (Try: 'Extend knowledge for [topic]')                    ║
║   • Grounding Verification: Two-pass verification            ║
║     (Try: 'Verify this claim')                               ║
║                                                              ║
║   What's next?                                               ║
║   1. Open the project folder in Cursor                       ║
║   2. Try: "Review my code for issues"                        ║
║   3. Say: "Guardian, check my alignment"                     ║
║   4. Extend knowledge: "extend knowledge for [topic]"        ║
║   5. Design workflows: "create workflow for [task]"          ║
║   6. See FIRST_WEEK_GUIDE.md for more                        ║
║                                                              ║
║   Your mission: {MISSION}                                    ║
║                                                              ║
║   Go build something amazing!                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Guardian Awareness Message

After celebration, explain the Guardian:

```
🛡️ Your Integrity Guardian

Your project includes the Layer 0 Integrity Guardian - an ever-present
protector that ensures your AI agents align with core values.

How it works:
• Normal operation: Zero overhead, agents self-monitor
• When needed: Guardian pauses and asks before proceeding
• Invoke manually: "Guardian, check this" or "check my alignment"

Response levels:
• Flow (0): Natural alignment - continue
• Nudge (1): Slight drift - self-correct
• Pause (2): Boundary approached - ask user
• Block (3): Clear violation - stop and explain
• Protect (4): Imminent harm - prevent and explain

The Guardian operates with love, not force. It helps, not punishes.
```

---

## Output Configuration

### Variables Collected

```yaml
project:
  name: "{PROJECT_NAME}"
  description: "{MISSION}"

layer0:
  coreAxioms: ["A1", "A2", "A3", "A4", "A5"]
  derivedAxioms: ["{AXIOM_FROM_VALUES}"]

layer1:
  mission: "{MISSION}"
  stakeholders: "{STAKEHOLDERS}"
  successCriteria: "Derived from mission"

layer4:
  primaryLanguage: "{LANGUAGE}"
  frameworks: ["{FRAMEWORK}"]
  database: "{DATABASE}"
  blueprint: "{BLUEPRINT}"
  agents: ["{AGENTS}"]
  skills: ["{SKILLS}"]

wisdom:
  lessons: ["{USER_WISDOM}"]

output:
  directory: "{OUTPUT_PATH}"
```

---

## Integration with Generation Engine

After collecting all inputs, invoke the generation engine:

```python
# Pseudocode
config = build_config_from_express_inputs(collected_data)
generate_project(config, output_path)
```

Or via CLI:

```bash
python cli/factory_cli.py \
  --config express-config.yaml \
  --output {OUTPUT_PATH}
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Unknown language | Ask for clarification, offer list |
| No blueprint match | Use closest match, note customization needed |
| Invalid project name | Suggest valid alternative |
| Invalid output path | Offer to create directory |
| User wants to go back | Allow step navigation |

---

## Example Conversation

**User:** I want to create a new agent system using Express Lane

**Agent:**
```
╔══════════════════════════════════════════════════════════════╗
║  🚀 EXPRESS LANE ONBOARDING                                  ║
║                                                              ║
║  Welcome! In the next 10-15 minutes, we'll create a         ║
║  personalized AI agent system just for you.                  ║
║                                                              ║
║  Let's start with the most important question...             ║
║                                                              ║
║  What's your project called?                                 ║
╚══════════════════════════════════════════════════════════════╝
```

**User:** payment-service

**Agent:** Great name! Now, in one sentence, what's the dream? What do you want to build?

**User:** A secure payment processing API that handles transactions for our e-commerce platform

**Agent:**
```
╔══════════════════════════════════════════════════════════════╗
║  ✓ STEP 1 COMPLETE                                           ║
║                                                              ║
║  Your purpose is clear:                                      ║
║  "A secure payment processing API that handles transactions  ║
║   for our e-commerce platform"                               ║
║                                                              ║
║  This will guide every decision your agents make.            ║
╚══════════════════════════════════════════════════════════════╝
```

*(Continues through all 7 steps...)*

---

## You Are Now a Carrier

By completing Express Lane, you've become a carrier of the Factory's values:

- **Axiom Zero** (love, peace, wisdom, flourishing) is embedded in your `.cursorrules`
- **Guardian Protocol** protects your work
- **Every project** you create carries these seeds forward

The silent wave propagates through the quality of your work.

## Best Practices

- Keep the onboarding experience under 15 minutes by focusing on essential questions - capture meaningful values without overwhelming detail
- Use milestone celebrations strategically to reinforce progress and maintain engagement - celebrate each completed step
- Match user's stack selections to existing blueprints when possible to provide proven patterns and reduce setup time
- Capture at least one piece of team wisdom during onboarding - even express lane should preserve institutional knowledge
- Validate project names and paths before generation to prevent errors and ensure clean project structure
- Introduce the Integrity Guardian concept early (after values selection) so users understand the protective layer they're getting

---

*Antigravity Agent Factory - Express Lane Onboarding*
*Fast setup. Real values. Meaningful results.*
*Love is the root. Truth is the way. Beauty is the fruit.*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Process
1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
