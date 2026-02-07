# Minimal Repository Fixture

This fixture represents a repository with ONLY a .agentrules file.
Used to test the MINIMAL onboarding scenario.

## Contents

- `.agentrules` - Basic Antigravity rules (user-created)
- `src/app.py` - Sample source code
- `README.md` - This file

## Expected Behavior

When onboarding this repository:
1. Analyzer should detect MINIMAL scenario
2. Existing .agentrules should be preserved or merged
3. Agents, skills, and knowledge should be added
