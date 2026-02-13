---
description: Validate trading strategies with walk-forward analysis, Monte Carlo simulation,
  and robustness checks
name: backtesting-validation
type: skill
---
# Backtesting Validation

Validate trading strategies with walk-forward analysis, Monte Carlo simulation, and robustness checks

Validate trading strategies using historical backtests, walk-forward analysis, Monte Carlo simulation, and parameter sensitivity checks. Produces robustness reports for deployment decisions.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Historical Backtest

Run in-sample backtest with backtrader.

```python
import backtrader as bt
import pandas as pd

class SimpleStrategy(bt.Strategy):
    """Minimal strategy for backtest validation."""

    def __init__(self) -> None:
        self.sma = bt.indicators.SMA(self.data.close, period=20)

    def next(self) -> None:
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.close()

def run_backtest(data: pd.DataFrame) -> bt.Strategy:
    """Execute historical backtest.

    Args:
        data: OHLCV DataFrame with DatetimeIndex.

    Returns:
        Strategy instance with results.
    """
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SimpleStrategy)
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.broker.setcash(100000.0)
    cerebro.run()
    return cerebro
```

### Step 2: Walk-Forward Analysis

Split data into train/test windows and validate out-of-sample.

```python
import numpy as np

def walk_forward_split(
    data: pd.DataFrame,
    train_pct: float = 0.7,
    n_splits: int = 5,
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """Generate train/test splits for walk-forward validation.

    Args:
        data: Full OHLCV dataset.
        train_pct: Proportion used for training.
        n_splits: Number of expanding window splits.

    Returns:
        List of (train, test) DataFrame tuples.
    """
    n = len(data)
    splits = []
    for i in range(1, n_splits + 1):
        train_end = int(n * train_pct * (i / n_splits))
        test_end = min(train_end + int(n * 0.2), n)
        splits.append((data.iloc[:train_end], data.iloc[train_end:test_end]))
    return splits
```

### Step 3: Monte Carlo Simulation

Simulate path-dependence and trade order effects.

```python
def monte_carlo_returns(
    returns: pd.Series,
    n_simulations: int = 1000,
    horizon: int = 252,
) -> np.ndarray:
    """Bootstrap Monte Carlo simulation of returns.

    Args:
        returns: Historical return series.
        n_simulations: Number of simulated paths.
        horizon: Simulation horizon in periods.

    Returns:
        Array of shape (n_simulations, horizon).
    """
    rng = np.random.default_rng()
    sims = rng.choice(returns.values, size=(n_simulations, horizon), replace=True)
    return sims
```

### Step 4: Parameter Sensitivity

Vary parameters and record performance.

```python
from dataclasses import dataclass

@dataclass
class SensitivityResult:
    """Result of parameter sensitivity run."""
    params: dict
    total_return: float
    sharpe: float
    max_dd: float

def parameter_sensitivity(
    data: pd.DataFrame,
    param_grid: dict[str, list],
) -> list[SensitivityResult]:
    """Run backtest across parameter grid.

    Args:
        data: OHLCV data.
        param_grid: Dict of param name -> list of values.

    Returns:
        List of SensitivityResult for each combination.
    """
    results = []
    # Implement grid search over param_grid
    return results
```

### Step 5: Robustness Report

Aggregate validation metrics into a report.

```python
def generate_robustness_report(
    oos_returns: list[float],
    mc_final_equity: np.ndarray,
) -> dict:
    """Generate strategy robustness report.

    Args:
        oos_returns: Out-of-sample returns from walk-forward.
        mc_final_equity: Final equity from Monte Carlo paths.

    Returns:
        Report dict with metrics.
    """
    return {
        "oos_mean_return": np.mean(oos_returns),
        "oos_std": np.std(oos_returns),
        "mc_median_equity": np.median(mc_final_equity),
        "mc_5pct_equity": np.percentile(mc_final_equity, 5),
    }
```

## Best Practices

- Reserve at least 20% of data for out-of-sample validation
- Use multiple Monte Carlo seeds for reproducibility
- Document parameter ranges in trading-patterns.json
- Run unit tests for strategy logic before backtest

## References

- {directories.knowledge}/trading-patterns.json
- {directories.knowledge}/quantitative-finance.json
- {directories.knowledge}/test-patterns.json

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
