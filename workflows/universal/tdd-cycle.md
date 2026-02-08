# TDD Cycle Workflow

## Overview

Test-Driven Development workflow implementing the Red-Green-Refactor cycle. Guides developers through writing failing tests first, implementing minimal code to pass, and then refactoring for quality.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** test-generator

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../docs/PATH_CONFIGURATION.md).

## Trigger Conditions

This workflow is activated when:

- User requests TDD-based development
- Feature workflow chains to implementation
- User wants to write tests first
- Refactoring with test safety is needed

**Trigger Examples:**
- "Implement this using TDD"
- "Write tests first for this feature"
- "Use red-green-refactor"
- "TDD cycle for the calculator module"

## Phases

### Phase 1: Red Phase (Write Failing Test)

**Description:** Write a test that defines expected behavior before implementation.

**Entry Criteria:** Feature or behavior requirement defined  
**Exit Criteria:** Test written and confirmed failing

#### Step 1.1: Define Test Scenario

**Description:** Identify what behavior to test.

**Actions:**
- Understand the requirement
- Define the expected behavior
- Identify inputs and expected outputs
- Consider edge cases

**Outputs:**
- Test scenario description
- Expected inputs/outputs
- Edge cases list

**Is Mandatory:** Yes

---

#### Step 1.2: Write Test Structure

**Description:** Create the test with Given-When-Then structure.

**Actions:**
- Create test file if needed
- Write test function with descriptive name
- Set up test preconditions (Given)
- Define the action to test (When)
- Assert expected outcome (Then)

**Test Naming Convention:**
```
test_<behavior>_<scenario>_<expected_outcome>

Examples:
- test_add_positive_numbers_returns_sum
- test_login_invalid_password_returns_error
- test_empty_cart_checkout_raises_exception
```

**Skills:**
- `tdd`: Test structure patterns

**Outputs:**
- Test file with failing test

**Is Mandatory:** Yes

---

#### Step 1.3: Verify Test Fails

**Description:** Confirm the test fails for the right reason.

**Actions:**
- Run the test
- Verify it fails
- Confirm failure is due to missing implementation
- Ensure test is not broken

**Outputs:**
- Test failure output
- Failure reason confirmation

**Is Mandatory:** Yes

---

### Phase 2: Green Phase (Make Test Pass)

**Description:** Write minimum code to make the test pass.

**Entry Criteria:** Failing test exists  
**Exit Criteria:** Test passes with minimal implementation

#### Step 2.1: Implement Minimal Code

**Description:** Write the simplest code that makes the test pass.

**Actions:**
- Focus only on making the test pass
- Avoid premature optimization
- Don't add features not tested
- Keep implementation simple

**Important Rules:**
- Write only enough code to pass the test
- Don't anticipate future requirements
- Hard-coded values are acceptable initially
- Focus on correctness, not elegance

**Outputs:**
- Implementation code
- Test passing confirmation

**Is Mandatory:** Yes

---

#### Step 2.2: Verify Test Passes

**Description:** Confirm the test now passes.

**Actions:**
- Run the specific test
- Verify it passes
- Check no other tests broke
- Document what was implemented

**Outputs:**
- Test pass confirmation
- Related test results

**Is Mandatory:** Yes

---

### Phase 3: Refactor Phase (Improve Code)

**Description:** Improve code quality while keeping tests green.

**Entry Criteria:** Test passing  
**Exit Criteria:** Code improved, tests still passing

#### Step 3.1: Identify Refactoring Opportunities

**Description:** Find areas for improvement.

**Actions:**
- Look for duplication
- Check naming clarity
- Assess code structure
- Identify complexity

**Refactoring Candidates:**
- Duplicate code
- Long methods
- Poor naming
- Complex conditionals
- Magic numbers

**Outputs:**
- Refactoring opportunities list

**Is Mandatory:** Yes

---

#### Step 3.2: Apply Refactoring

**Description:** Improve code incrementally.

**Actions:**
- Apply one refactoring at a time
- Run tests after each change
- Maintain green tests
- Document significant changes

**Common Refactorings:**
- Extract method
- Rename variable/method
- Extract constant
- Simplify conditional
- Remove duplication

**Outputs:**
- Refactored code
- Test confirmation

**Is Mandatory:** No (skip if code is clean)

---

#### Step 3.3: Verify All Tests Pass

**Description:** Confirm refactoring didn't break anything.

**Actions:**
- Run full test suite
- Check for regressions
- Verify coverage maintained

**Outputs:**
- Full test results
- Coverage report

**Is Mandatory:** Yes

---

### Phase 4: Iterate

**Description:** Continue the cycle for additional behaviors.

**Entry Criteria:** Current cycle complete  
**Exit Criteria:** All required behaviors implemented

#### Step 4.1: Check Remaining Requirements

**Description:** Identify next behavior to implement.

**Actions:**
- Review requirements list
- Identify next test case
- Check edge cases
- Assess completeness

**Outputs:**
- Next test scenario
- Remaining requirements

**Is Mandatory:** Yes

---

#### Step 4.2: Continue or Complete

**Description:** Decide whether to continue cycling.

**Actions:**
- If more behaviors needed: Return to Phase 1
- If all done: Proceed to completion

**Outputs:**
- Decision: continue or complete

**Is Mandatory:** Yes

---

### Phase 5: Completion

**Description:** Finalize the TDD session.

**Entry Criteria:** All behaviors implemented  
**Exit Criteria:** Documentation complete

#### Step 5.1: Run Full Test Suite

**Description:** Final verification of all tests.

**Actions:**
- Run complete test suite
- Generate coverage report
- Check for warnings

**Outputs:**
- Final test results
- Coverage report

**Is Mandatory:** Yes

---

#### Step 5.2: Document Implementation

**Description:** Document what was built.

**Actions:**
- Update code documentation
- Document public APIs
- Note any limitations
- Update changelog

**Outputs:**
- Updated documentation

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Test Fails Correctly?

**Condition:** After writing test

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Fails as expected | Proceed to Green | Test is valid |
| Fails unexpectedly | Fix test | Test is broken |
| Passes (shouldn't) | Investigate | Already implemented? |

---

### Decision: Implementation Complete?

**Condition:** After each cycle

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| More behaviors needed | New Red phase | Continue TDD |
| All behaviors done | Finalize | Complete implementation |
| Edge cases remain | Continue | Cover edge cases |

---

### Decision: Refactor Needed?

**Condition:** After Green phase

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Code is clean | Skip refactor | Proceed to next cycle |
| Obvious improvements | Refactor | Improve quality |
| Major restructure needed | Plan carefully | Larger refactoring |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Test hard to write | May indicate design issue | Tech Lead |
| Too much setup | Consider mocking/refactoring | Team |
| Unclear requirements | Clarify before continuing | Product Owner |
| Coverage concerns | Discuss testing strategy | Team |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After Red | Test patterns | Template library |
| After Green | Implementation patterns | Code generation |
| After Refactor | Refactoring patterns | Guidelines |
| After Complete | Cycle metrics | Process improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Test Files | `tests/` directory | Test coverage |
| Implementation | Source directory | Feature code |
| Coverage Report | `reports/coverage/` | Quality metric |

---

## TDD Best Practices

### Test Naming

```python
def test_<unit>_<scenario>_<expected>():
    # Given (Arrange)
    # When (Act)  
    # Then (Assert)
```

### Test Structure

```python
def test_add_positive_numbers_returns_sum():
    # Given
    calculator = Calculator()
    
    # When
    result = calculator.add(2, 3)
    
    # Then
    assert result == 5
```

### Cycle Rhythm

1. **Red (30s - 2min)**: Write a small failing test
2. **Green (30s - 5min)**: Make it pass quickly
3. **Refactor (1min - 5min)**: Clean up

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Test framework not configured | Set up testing first |
| Unclear behavior | Ask for clarification |
| External dependency | Use mocks |
| Database required | Use test fixtures |

---

## Example Session

```
User: Implement a calculator add method using TDD

Agent:
━━━ PHASE 1: Red (Write Failing Test) ━━━
Defining test scenario...
- Feature: Calculator addition
- Input: Two positive numbers
- Expected: Sum of numbers

Writing test:
```python
def test_add_positive_numbers_returns_sum():
    # Given
    calc = Calculator()
    
    # When
    result = calc.add(2, 3)
    
    # Then
    assert result == 5
```

Running test...
❌ FAILED: NameError: Calculator not defined

✓ Test fails for the right reason (implementation missing)

━━━ PHASE 2: Green (Make Test Pass) ━━━
Implementing minimal code:
```python
class Calculator:
    def add(self, a, b):
        return a + b
```

Running test...
✅ PASSED

━━━ PHASE 3: Refactor ━━━
Checking for improvements...
- Code is simple and clean
- Naming is clear
- No duplication

Skipping refactor (code is clean)

Running all tests...
✅ 1/1 passed

━━━ Continue Cycle ━━━
Next test: Edge case - negative numbers

Writing test:
```python
def test_add_negative_numbers_returns_sum():
    calc = Calculator()
    result = calc.add(-2, -3)
    assert result == -5
```

Running test...
✅ PASSED (already works!)

Next test: Mixed positive and negative...
[Cycle continues...]

━━━ PHASE 5: Completion ━━━
Final test suite: 5/5 passing
Coverage: 100%

Implemented:
- Calculator.add() with full test coverage
- Handles positive, negative, and zero values

✨ TDD cycle complete!
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/tdd.json`
- **Skills**: `.cursor/skills/tdd`
- **Knowledge**: `knowledge/test-patterns.json`
