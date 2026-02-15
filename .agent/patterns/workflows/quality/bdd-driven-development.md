# BDD-Driven Development Workflow

## Overview

Behavior-Driven Development workflow that starts with stakeholder-readable Gherkin scenarios and translates them into executable tests. Emphasizes collaboration between business, development, and QA through the Three Amigos process.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** test-generator

## Trigger Conditions

This workflow is activated when:

- User requests BDD-style development
- Feature file or Gherkin scenario is provided
- Stakeholder-readable specifications needed
- Behavior-first approach requested

**Trigger Examples:**
- "Implement this feature using BDD"
- "Write Gherkin scenarios for user login"
- "Create feature files for the checkout process"
- "BDD for the payment module"

## Phases

### Phase 1: Three Amigos Discovery

**Description:** Collaborative session to understand and define behavior.

**Entry Criteria:** Feature or requirement identified
**Exit Criteria:** Shared understanding of behavior

#### Step 1.1: Gather Stakeholders

**Description:** Identify perspectives needed for feature definition.

**Actions:**
- Identify business representative (what)
- Identify developer (how)
- Identify tester (what if)
- Schedule discovery session

**Roles:**

| Role | Focus | Questions |
|------|-------|-----------|
| Business | Value | Why is this needed? |
| Developer | Implementation | How will this work? |
| Tester | Quality | What could go wrong? |

**Outputs:**
- Participant list
- Session agenda

**Is Mandatory:** Yes

---

#### Step 1.2: Define Examples

**Description:** Use concrete examples to illustrate behavior.

**Actions:**
- Discuss happy path scenarios
- Explore edge cases
- Identify error conditions
- Document examples

**Example Format:**
```
Given [context/precondition]
When [action/event]
Then [expected outcome]
```

**Outputs:**
- Example scenarios
- Edge cases list
- Error conditions

**Is Mandatory:** Yes

---

### Phase 2: Feature File Creation

**Description:** Write Gherkin feature files from examples.

**Entry Criteria:** Examples defined
**Exit Criteria:** Feature file complete

#### Step 2.1: Write Feature Description

**Description:** Create the feature file header.

**Actions:**
- Write feature name
- Describe the value proposition
- Identify stakeholder benefit
- Set feature context

**Feature Template:**
```gherkin
Feature: <Feature Name>
  As a <role>
  I want <capability>
  So that <benefit>
```

**Outputs:**
- Feature file header

**Is Mandatory:** Yes

---

#### Step 2.2: Write Scenarios

**Description:** Convert examples to Gherkin scenarios.

**Actions:**
- Write Given steps (context)
- Write When steps (action)
- Write Then steps (outcome)
- Add scenario outlines for data variations

**Scenario Template:**
```gherkin
Scenario: <Descriptive name>
  Given <precondition>
  And <additional context>
  When <action>
  Then <expected result>
  And <additional verification>
```

**Skills:**
- `bdd`: Gherkin patterns

**Outputs:**
- Complete scenarios

**Is Mandatory:** Yes

---

#### Step 2.3: Add Background and Hooks

**Description:** Extract common setup and add hooks.

**Actions:**
- Identify repeated Given steps
- Create Background section
- Add tags for filtering
- Document dependencies

**Background Template:**
```gherkin
Background:
  Given <common setup step>
  And <another common step>
```

**Outputs:**
- Optimized feature file

**Is Mandatory:** No

---

### Phase 3: Step Definition Creation

**Description:** Implement step definitions for scenarios.

**Entry Criteria:** Feature file complete
**Exit Criteria:** Step definitions implemented

#### Step 3.1: Generate Step Stubs

**Description:** Create placeholder step definitions.

**Actions:**
- Parse feature file
- Generate step function stubs
- Match regex patterns
- Organize by feature

**Framework Examples:**

| Framework | Language | Decorator |
|-----------|----------|-----------|
| behave | Python | `@given`, `@when`, `@then` |
| Cucumber | Java | `@Given`, `@When`, `@Then` |
| Cucumber.js | TypeScript | `Given`, `When`, `Then` |

**Outputs:**
- Step definition stubs

**Is Mandatory:** Yes

---

#### Step 3.2: Implement Step Definitions

**Description:** Fill in step definition logic.

**Actions:**
- Implement Given steps (setup)
- Implement When steps (actions)
- Implement Then steps (assertions)
- Handle step parameters

**Implementation Pattern:**
```python
@given('a user with email "{email}"')
def step_user_with_email(context, email):
    context.user = User(email=email)

@when('the user logs in with password "{password}"')
def step_user_logs_in(context, password):
    context.result = context.user.login(password)

@then('the login should be successful')
def step_login_successful(context):
    assert context.result.success is True
```

**Outputs:**
- Implemented step definitions

**Is Mandatory:** Yes

---

#### Step 3.3: Run Feature Tests

**Description:** Execute feature file tests.

**Actions:**
- Run BDD test suite
- Collect results
- Identify failures
- Generate report

**Outputs:**
- Test results
- Failure details

**Is Mandatory:** Yes

---

### Phase 4: TDD Implementation

**Description:** Implement underlying functionality using TDD.

**Entry Criteria:** Step definitions calling production code
**Exit Criteria:** All scenarios passing

#### Step 4.1: Translate to Unit Tests

**Description:** Create unit tests from BDD scenarios.

**Actions:**
- Identify unit-level tests needed
- Create focused unit tests
- Map to BDD scenarios
- Maintain traceability

**Skills:**
- `test-translation`: BDD to TDD translation

**Outputs:**
- Unit tests with BDD traceability

**Is Mandatory:** Yes

---

#### Step 4.2: Implement Production Code

**Description:** Write code to pass both unit and BDD tests.

**Actions:**
- Follow TDD Red-Green-Refactor
- Implement feature logic
- Run unit tests
- Run BDD tests

**Outputs:**
- Production code
- Passing tests

**Is Mandatory:** Yes

---

#### Step 4.3: Verify All Scenarios Pass

**Description:** Confirm all BDD scenarios are green.

**Actions:**
- Run full BDD suite
- Verify all scenarios pass
- Generate living documentation
- Update status

**Outputs:**
- All scenarios passing
- Living documentation

**Is Mandatory:** Yes

---

### Phase 5: Living Documentation

**Description:** Generate stakeholder-readable documentation.

**Entry Criteria:** All scenarios passing
**Exit Criteria:** Documentation generated

#### Step 5.1: Generate Documentation

**Description:** Create living documentation from feature files.

**Actions:**
- Parse feature files
- Generate HTML report
- Include test results
- Link to source

**Documentation Tools:**
- behave: `behave --format=html`
- Cucumber: Cucumber Reports
- SpecFlow: Living Doc

**Outputs:**
- Living documentation
- Test execution report

**Is Mandatory:** Yes

---

#### Step 5.2: Share with Stakeholders

**Description:** Distribute documentation to stakeholders.

**Actions:**
- Publish documentation
- Notify stakeholders
- Collect feedback
- Update if needed

**Outputs:**
- Published documentation
- Stakeholder feedback

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Scenario Clarity

**Condition:** After scenario writing

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Scenarios clear | Proceed | Ready for implementation |
| Business unclear | Clarify with stakeholder | Need input |
| Technical unclear | Developer review | Need design |

---

### Decision: Step Reuse

**Condition:** When implementing steps

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Step exists | Reuse | DRY principle |
| Similar step | Parameterize | Flexibility |
| New step | Create | New behavior |

---

### Decision: Test Strategy

**Condition:** After step definitions

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Unit tests sufficient | BDD only | Simple feature |
| Complex logic | Add unit tests | Thorough coverage |
| Integration needed | Add integration tests | End-to-end |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Unclear acceptance criteria | Clarify | Product Owner |
| Technical complexity | Design session | Tech Lead |
| Test infrastructure issues | Support | DevOps |
| Conflicting requirements | Prioritize | Stakeholders |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After Phase 1 | Good example patterns | Templates |
| After Phase 2 | Gherkin patterns | Style guide |
| After Phase 3 | Step definition patterns | Reuse library |
| After Phase 5 | Documentation feedback | Improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Feature Files | `features/` | Specifications |
| Step Definitions | `features/steps/` | Test implementation |
| Living Docs | `docs/features/` | Stakeholder documentation |
| Test Report | `reports/bdd/` | Execution results |

---

## Gherkin Best Practices

### Feature Structure

```gherkin
@tag1 @tag2
Feature: User Authentication
  As a registered user
  I want to log into the system
  So that I can access my account

  Background:
    Given the system is available
    And I am on the login page

  @happy-path
  Scenario: Successful login with valid credentials
    Given I have a registered account with email "user@example.com"
    When I enter email "user@example.com" and password "valid123"
    And I click the login button
    Then I should be logged in successfully
    And I should see the dashboard

  @error-case
  Scenario: Failed login with invalid password
    Given I have a registered account with email "user@example.com"
    When I enter email "user@example.com" and password "wrong"
    And I click the login button
    Then I should see error message "Invalid credentials"

  @data-driven
  Scenario Outline: Login with various credentials
    When I enter email "<email>" and password "<password>"
    And I click the login button
    Then I should see "<result>"

    Examples:
      | email              | password | result              |
      | valid@example.com  | correct  | dashboard           |
      | invalid@example.com| correct  | User not found      |
      | valid@example.com  | wrong    | Invalid credentials |
```

### Step Definition Patterns

```python
# features/steps/auth_steps.py
from behave import given, when, then

@given('I have a registered account with email "{email}"')
def step_registered_account(context, email):
    context.user = create_test_user(email=email)

@when('I enter email "{email}" and password "{password}"')
def step_enter_credentials(context, email, password):
    context.login_page.enter_email(email)
    context.login_page.enter_password(password)

@when('I click the login button')
def step_click_login(context):
    context.result = context.login_page.click_login()

@then('I should be logged in successfully')
def step_login_success(context):
    assert context.result.success is True
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| BDD framework not installed | Install and configure |
| Step definition missing | Generate stub |
| Scenario ambiguous | Clarify with stakeholder |
| Test data unavailable | Create fixtures |

---

## Example Session

```
User: Create BDD scenarios for user registration

Agent:
━━━ PHASE 1: Three Amigos Discovery ━━━
Understanding the feature...

Feature: User Registration
- Business value: Enable new users to create accounts
- Key stakeholder: Marketing (user acquisition)

Defining examples:
1. Happy path: Valid registration
2. Edge case: Duplicate email
3. Edge case: Invalid email format
4. Edge case: Weak password

━━━ PHASE 2: Feature File Creation ━━━
Writing feature file:

```gherkin
Feature: User Registration
  As a new user
  I want to create an account
  So that I can access the platform

  Background:
    Given I am on the registration page

  @happy-path
  Scenario: Successful registration with valid details
    Given no user exists with email "new@example.com"
    When I enter name "John Doe"
    And I enter email "new@example.com"
    And I enter password "StrongP@ss123"
    And I click register
    Then I should see "Registration successful"
    And I should receive a confirmation email

  @error-case
  Scenario: Registration fails with existing email
    Given a user exists with email "existing@example.com"
    When I enter name "John Doe"
    And I enter email "existing@example.com"
    And I enter password "StrongP@ss123"
    And I click register
    Then I should see "Email already registered"

  @validation
  Scenario: Registration fails with weak password
    When I enter name "John Doe"
    And I enter email "new@example.com"
    And I enter password "weak"
    And I click register
    Then I should see "Password too weak"
```

Created: features/user_registration.feature

━━━ PHASE 3: Step Definition Creation ━━━
Generating step stubs...

```python
@given('I am on the registration page')
def step_on_registration_page(context):
    context.page = RegistrationPage()

@given('no user exists with email "{email}"')
def step_no_user_exists(context, email):
    ensure_user_not_exists(email)

@when('I enter name "{name}"')
def step_enter_name(context, name):
    context.page.enter_name(name)
```

Implementing step definitions...
Created: features/steps/registration_steps.py

Running scenarios...
❌ 3 scenarios (3 undefined)

━━━ PHASE 4: TDD Implementation ━━━
Implementing registration logic using TDD...

[TDD cycle for User.register()]
[TDD cycle for EmailValidator()]
[TDD cycle for PasswordStrength()]

Running scenarios again...
✅ 3 scenarios (3 passed)

━━━ PHASE 5: Living Documentation ━━━
Generating documentation...

Created: docs/features/user_registration.html

Living documentation available at:
- 3 scenarios documented
- 100% passing
- Updated: 2026-02-02

✨ BDD implementation complete!
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/bdd.json`
- **Skills**: `.cursor/skills/bdd`, `.cursor/skills/test-translation`
- **Knowledge**: `knowledge/test-traceability.json`
