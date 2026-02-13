---
description: Design and implement algorithmic trading strategies with entry/exit rules,
  position sizing, and risk parameters
name: trading-strategy
type: skill
---
# Trading Strategy

Design and implement algorithmic trading strategies with entry/exit rules, position sizing, and risk parameters

Design and implement algorithmic trading strategies with explicit entry/exit rules, position sizing logic, and risk parameter configuration. Follows a structured process from hypothesis to executable signal generation.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Strategy Hypothesis

Formulate a testable market hypothesis with clear entry/exit criteria.

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class StrategyHypothesis:
    """Documented strategy hypothesis for validation.

    Attributes:
        name: Strategy identifier.
        logic: Market hypothesis description.
        entry_condition: When to enter positions.
        exit_condition: When to exit positions.
    """
    name: str
    logic: str
    entry_condition: str
    exit_condition: str

hypothesis = StrategyHypothesis(
    name="ema_crossover",
    logic="Price trending above short EMA signals momentum",
    entry_condition="Close > EMA(9) and EMA(9) crosses above EMA(21)",
    exit_condition="Close < EMA(9) or stop-loss hit",
)
```

### Step 2: Rule Definition

Translate the hypothesis into explicit, testable rules.

```python
import pandas as pd
import pandas_ta as ta

def define_ema_rules(
    data: pd.DataFrame,
    fast: int = 9,
    slow: int = 21,
) -> tuple[pd.Series, pd.Series]:
    """Generate EMA crossover signals.

    Args:
        data: OHLCV DataFrame with 'close' column.
        fast: Fast EMA period.
        slow: Slow EMA period.

    Returns:
        Tuple of (entry_signal, exit_signal) Series.
    """
    ema_fast = ta.ema(data["close"], length=fast)
    ema_slow = ta.ema(data["close"], length=slow)
    entry_signal = (data["close"] > ema_fast) & (ema_fast > ema_slow)
    exit_signal = data["close"] < ema_fast
    return entry_signal, exit_signal
```

### Step 3: Signal Generation

Produce executable buy/sell signals from the rules.

```python
import numpy as np

def generate_signals(
    data: pd.DataFrame,
    entry: pd.Series,
    exit_signal: pd.Series,
) -> pd.Series:
    """Convert rules to -1/0/1 signal series.

    Args:
        data: OHLCV DataFrame.
        entry: Boolean entry trigger.
        exit_signal: Boolean exit trigger.

    Returns:
        Signal series: 1=buy, -1=sell, 0=hold.
    """
    signals = pd.Series(0, index=data.index)
    position = 0
    for i in range(1, len(data)):
        if entry.iloc[i] and position <= 0:
            signals.iloc[i] = 1
            position = 1
        elif exit_signal.iloc[i] and position >= 0:
            signals.iloc[i] = -1
            position = -1
    return signals
```

### Step 4: Position Sizing

Apply position sizing based on risk parameters.

```python
def calculate_position_size(
    capital: float,
    price: float,
    risk_pct: float = 0.02,
    atr: float | None = None,
) -> int:
    """Compute position size using risk-based sizing.

    Args:
        capital: Available capital.
        price: Current price.
        risk_pct: Max risk per trade (e.g., 0.02 = 2%).
        atr: ATR for volatility-based sizing (optional).

    Returns:
        Number of shares to trade.
    """
    risk_amount = capital * risk_pct
    stop_distance = (atr * 2) if atr else price * 0.02
    size = int(risk_amount / stop_distance) if stop_distance > 0 else 0
    return min(size, int(capital * 0.1 / price))  # Max 10% of capital
```

### Step 5: Risk Limits

Enforce risk limits and constraints.

```python
@dataclass
class RiskLimits:
    """Risk parameter configuration for strategy."""

    max_position_pct: float = 0.10
    max_drawdown_pct: float = 0.15
    max_daily_loss_pct: float = 0.05
    stop_loss_pct: float = 0.02

    def validate_position(
        self,
        position_value: float,
        total_capital: float,
    ) -> bool:
        """Check if position is within limits."""
        return position_value / total_capital <= self.max_position_pct
```

## Best Practices

- Document every entry/exit rule in code and in knowledge files
- Use risk-based position sizing instead of fixed shares
- Validate rules against trading-patterns.json before implementation
- Include stop-loss and take-profit logic in rule definition
- Test signals on historical data before backtesting

## References

- {directories.knowledge}/trading-patterns.json
- {directories.knowledge}/quantitative-finance.json
- {directories.knowledge}/risk-management.json

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
