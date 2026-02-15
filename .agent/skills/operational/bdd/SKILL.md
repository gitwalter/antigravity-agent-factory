---
description: Behavior-driven development with Gherkin feature files, scenario outlines,
  and step definitions
name: bdd
type: skill
---
# Bdd

Behavior-driven development with Gherkin feature files, scenario outlines, and step definitions

Implements BDD using Gherkin syntax for feature files, scenario outlines, data tables, and step definitions. Bridges stakeholder requirements with executable specifications.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Feature Writing

Write Gherkin feature files describing behavior:

```gherkin
# features/trading_signals.feature
Feature: Trading Signal Generation
  As a trading system
  I want to generate buy/sell signals
  So that positions can be managed automatically

  Scenario: Generate buy signal on momentum crossover
    Given a momentum strategy with lookback 20
    And price data with 25 bars
    When the close crosses above the 20-period SMA
    Then a buy signal of 1 should be generated

  Scenario Outline: Generate signals for different thresholds
    Given a momentum strategy with threshold <threshold>
    And price data showing <condition>
    When signals are generated
    Then the result should be <signal>
    Examples:
      | threshold | condition | signal |
      | 0.01      | 2% rise   | 1      |
      | 0.05      | 1% rise   | 0      |
```

### Step 2: Step Definitions

Implement step definitions in Python:

```python
from behave import given, when, then
import pandas as pd
import numpy as np

@given("a momentum strategy with lookback {lookback:d}")
def step_momentum_strategy(context, lookback: int) -> None:
    """Create momentum strategy with specified lookback."""
    context.strategy = MomentumStrategy(lookback=lookback)

@given("price data with {n_bars:d} bars")
def step_price_data(context, n_bars: int) -> None:
    """Create synthetic OHLCV data."""
    dates = pd.date_range("2024-01-01", periods=n_bars, freq="D")
    context.data = pd.DataFrame({
        "close": np.random.uniform(100, 110, n_bars),
    }, index=dates)

@when("the close crosses above the 20-period SMA")
def step_crosses_above(context) -> None:
    """Simulate crossover and generate signals."""
    context.signal = context.strategy.generate_signals(context.data)

@then("a buy signal of {expected:d} should be generated")
def step_assert_signal(context, expected: int) -> None:
    """Assert signal value matches expected."""
    assert context.signal.iloc[-1] == expected
```

### Step 3: Scenario Outlines

Use data tables for parameterized scenarios:

```python
@given("a momentum strategy with threshold {threshold:g}")
def step_strategy_threshold(context, threshold: float) -> None:
    """Set strategy threshold."""
    context.strategy = MomentumStrategy(threshold=threshold)

@when("signals are generated")
def step_generate(context) -> None:
    """Generate signals from context data."""
    context.result = context.strategy.generate_signals(context.data)

@then("the result should be {signal:d}")
def step_assert_result(context, signal: int) -> None:
    """Assert final signal value."""
    assert context.result.iloc[-1] == signal
```

### Step 4: Data Tables

Parse and use Gherkin data tables:

```python
@given("the following price series")
def step_price_table(context) -> None:
    """Parse table with columns: date, open, high, low, close."""
    rows = [dict(zip(context.table.headings, row)) for row in context.table]
    context.data = pd.DataFrame(rows)
    context.data["date"] = pd.to_datetime(context.data["date"])
    context.data.set_index("date", inplace=True)
```

### Step 5: Test Execution

Run BDD tests from command line:

```bash
behave features/ -t @regression
behave features/ --format json -o results.json
pytest {directories.tests}/ -k bdd  # for pytest-bdd
```

## Best Practices

- Keep scenarios short and focused
- Use scenario outlines for similar cases
- Share step definitions across features
- Tag scenarios for selective execution
- Use Background for common setup

## References

- [Behave Documentation](https://behave.readthedocs.io/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
