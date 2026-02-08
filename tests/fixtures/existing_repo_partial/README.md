# Partial Repository Fixture

This fixture represents a repository with SOME Antigravity artifacts.Used to test the PARTIAL onboarding scenario.

## Contents

- `.agentrules` - Factory-style rules
- `.agent/agents/code-reviewer.md` - Custom agent
- `.agent/skills/tdd/SKILL.md` - Custom skill- `src/` - Sample source code

## Missing (should be added)

- Other agents (test-generator, explorer)
- Other skills (bugfix-workflow, feature-workflow, grounding)
- Knowledge files
- Templates
- Workflows

## Expected Behavior

When onboarding this repository:
1. Analyzer should detect PARTIAL scenario
2. Existing agents/skills should be preserved
3. Missing components should be added
4. Conflicts should prompt user for resolution
