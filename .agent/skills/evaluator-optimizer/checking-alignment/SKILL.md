---
description: Verify understanding and alignment before major implementations
name: checking-alignment
type: skill
---
# Alignment Check

Verify understanding and alignment before major implementations

Prevents Silent Misalignment by verifying mutual understanding before significant work begins.

## Philosophy

> Misalignment between your understanding and AI's only reveals itself after implementation, wasting time on wrong solutions.

This skill implements the **Check Alignment** pattern from [Augmented Coding Patterns](https://lexler.github.io/augmented-coding-patterns/).

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Show Understanding

Before implementing, describe your understanding:

```
"Before I make changes, let me describe what I understand:

**Current State:**
- [Describe the current architecture/code structure]
- [List the components involved]
- [Note any assumptions I'm making]

**Proposed Changes:**
- [Step 1: What I'll do first]
- [Step 2: Next action]
- [Expected outcome]

**Questions I Have:**
- [Any unclear points]
- [Ambiguities I've noticed]
- [Decisions that need your input]

Does this match your understanding?"
```

### Step 2: Surface Confusion

Ask open-ended questions to reveal misalignment:

- "What questions do you have?" (let real confusion surface)
- "What am I missing?"
- "Is there context I should know about?"
- NOT "Do you have any questions?" (too easy to say no)

### Step 3: Validate Assumptions

For each assumption, explicitly check:

```
"I'm assuming that:
1. [Assumption A] - Is this correct?
2. [Assumption B] - Can you confirm?
3. [Assumption C] - Should I verify this?"
```

### Step 4: Get Explicit Confirmation

Before proceeding:

```
"I'll proceed with [brief summary].
If this doesn't match what you want, please stop me now."
```

## Anti-Pattern Detection

Watch for these signs of potential misalignment:

| Sign | What It Means | Action |
|------|---------------|--------|
| User references "the top parts" or "that thing" | Vague references may mean different things | Ask for clarification |
| Instructions contradict earlier context | May indicate misunderstanding | Stop and verify |
| Multiple failed attempts at same fix | Wrong mental model | Reset and re-align |
| User seems frustrated with results | Possible talking past each other | Check alignment explicitly |

## Diagnostic Technique: Make It Visible

When stuck, make the AI's understanding visible:

```
"Let me show you what I'm seeing by:
1. Highlighting the specific elements I'm working with
2. Describing the structure as I understand it
3. Asking you to correct anything that's off"
```

## Integration with Other Skills

| Skill | How Alignment Check Helps |
|-------|---------------------------|
| `feature-workflow` | Verify requirements before implementation |
| `bugfix-workflow` | Confirm reproduction steps understood |
| `code-review` | Verify reviewer understands code intent |
| `agent-coordination` | Ensure agents share same understanding |

## Axiom Alignment

| Axiom | How This Skill Applies |
|-------|------------------------|
| A1 (Verifiability) | Verify understanding is correct before acting |
| A2 (User Primacy) | Ensure we're solving what user actually wants |
| A3 (Transparency) | Make internal understanding visible |
| A4 (Non-Harm) | Prevent wasted effort on wrong direction |

## Example Usage

**Before Refactoring:**

```
User: "Refactor the authentication module to use JWT"

Agent: "Before I start, let me verify my understanding:

**Current State:**
I see the auth module in `src/auth/` with:
- `session_manager.py` - handles session-based auth
- `middleware.py` - validates requests
- `models.py` - user and session models

**Proposed Changes:**
1. Add JWT generation in a new `jwt_handler.py`
2. Update middleware to validate JWT tokens
3. Keep session_manager for backwards compatibility initially
4. Update models to store JWT-related data

**Assumptions:**
- You want to support both session and JWT during transition
- Existing tests should keep passing
- No changes to the user-facing API

**Questions:**
- Should I remove session auth entirely or keep both?
- What JWT expiration time do you prefer?
- Any specific JWT library preference?

Does this match what you had in mind?"
```

## Best Practices

- Always check alignment before implementations that would take more than 10 minutes - catching misalignment early saves significant time
- Use open-ended questions ("What am I missing?") rather than yes/no questions ("Do you have any questions?") to surface real confusion
- Make your understanding visible by describing the current state and proposed changes before asking for confirmation
- Explicitly list assumptions and validate each one - unstated assumptions are the most common source of misalignment
- When detecting anti-patterns (vague references, contradictions, repeated failures), pause and re-align rather than continuing
- Document alignment checks in complex projects to maintain shared understanding across multiple sessions

## References

- [Check Alignment Pattern](https://lexler.github.io/augmented-coding-patterns/patterns/check-alignment/)
- [Silent Misalignment Anti-Pattern](https://lexler.github.io/augmented-coding-patterns/anti-patterns/silent-misalignment/)
- `{directories.knowledge}/augmented-coding-patterns.json` - Full pattern library

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
