# Rule: TDD Governance (The Iron Law)

## Context
Governs all development, refactoring, and bug-fixing activities within the Antigravity Agent Factory. Grounded in Axiom A1 (Verifiability).

## The Iron Law
> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

Violating the letter of this rule is violating the spirit of the Factory's integrity.

## Requirements
1.  **Verify RED**: You MUST write a failing test and EXPLICITLY verify its failure before writing any implementation code.
2.  **Minimalism**: Write only the minimal code necessary to make the failing test pass (Verify GREEN).
3.  **Delete on Violation**: If implementation code is written before a failing test is verified, that code MUST be deleted. No "keeping it as reference" or "adapting it later".
4.  **Evidence of RED**: All `walkthrough.md` files MUST include logs/screenshots of the failing test (Verify RED phase).

## Process (RED-GREEN-REFACTOR)
1.  **RED**: Write one minimal test showing what *should* happen.
2.  **Verify RED**: Run the test and confirm it fails for the expected reason (feature missing, not a typo).
3.  **GREEN**: Write minimal code to pass the test.
4.  **Verify GREEN**: Run the test and confirm it passes and no regressions exist.
5.  **REFACTOR**: Clean up code, improve names, remove duplication while staying green.

## Tooling Integration
- Use the `parallel/tdd-rigor` skill for all implementation tasks.
- All `*-creator` skills MUST enforce these gates programmatically.

## Axiomatic Alignment
- **Truth**: We prove the code works via empirical evidence, not claims.
- **Beauty**: Consistency in testing patterns creates a harmonious and reliable codebase.
- **Love**: We protect our future selves and collaborators from hidden bugs and technical debt.
