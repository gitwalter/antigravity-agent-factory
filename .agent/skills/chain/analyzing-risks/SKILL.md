---
description: Quantitative risk assessment with VaR, drawdown analysis, Sharpe ratio,
  and portfolio risk metrics
name: analyzing-risks
type: skill
---
# Risk Analysis

Quantitative risk assessment with VaR, drawdown analysis, Sharpe ratio, and portfolio risk metrics

Perform quantitative risk assessment using Value-at-Risk (VaR), drawdown analysis, Sharpe ratio, and other portfolio risk metrics. Produces structured risk reports for strategy evaluation.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Return Calculation

Compute returns from price or equity series.

```python
import numpy as np
import pandas as pd

def compute_returns(
    prices: pd.Series,
    method: str = "log",
) -> pd.Series:
    """Calculate returns from price series.

    Args:
        prices: Price or equity series.
        method: 'log' for log returns, 'simple' for simple returns.

    Returns:
        Returns series.
    """
    if method == "log":
        return np.log(prices / prices.shift(1)).dropna()
    return (prices.pct_change()).dropna()
```

### Step 2: VaR Computation

Compute Value-at-Risk using parametric or historical methods.

```python
from scipy import stats

def compute_var(
    returns: pd.Series,
    confidence: float = 0.95,
    method: str = "parametric",
) -> float:
    """Compute Value-at-Risk.

    Args:
        returns: Return series.
        confidence: Confidence level (e.g., 0.95 for 95% VaR).
        method: 'parametric' (normal) or 'historical'.

    Returns:
        VaR as negative return (loss).
    """
    if method == "parametric":
        mu, sigma = returns.mean(), returns.std()
        z = stats.norm.ppf(1 - confidence)
        return -(mu + z * sigma)
    quantile = 1 - confidence
    return -returns.quantile(quantile)
```

### Step 3: Drawdown Analysis

Calculate drawdown and related metrics.

```python
def compute_drawdown(equity: pd.Series) -> pd.DataFrame:
    """Compute drawdown series and metrics.

    Args:
        equity: Cumulative equity curve.

    Returns:
        DataFrame with drawdown, underwater, and peak columns.
    """
    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max
    return pd.DataFrame({
        "equity": equity,
        "peak": running_max,
        "drawdown": drawdown,
        "underwater_pct": drawdown * 100,
    })
```

### Step 4: Risk-Adjusted Metrics

Compute Sharpe ratio and related metrics.

```python
def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Compute annualized Sharpe ratio.

    Args:
        returns: Return series.
        risk_free_rate: Annual risk-free rate.
        periods_per_year: Trading periods per year.

    Returns:
        Annualized Sharpe ratio.
    """
    excess = returns - risk_free_rate / periods_per_year
    annualized = excess.mean() * periods_per_year
    vol = excess.std() * np.sqrt(periods_per_year)
    return annualized / vol if vol > 0 else 0.0
```

### Step 5: Risk Report

Aggregate metrics into a structured report.

```python
from dataclasses import dataclass

@dataclass
class RiskReport:
    """Structured risk analysis report."""

    var_95: float
    max_drawdown_pct: float
    sharpe_ratio: float
    cagr_pct: float

def generate_risk_report(
    equity: pd.Series,
    returns: pd.Series,
) -> RiskReport:
    """Generate comprehensive risk report."""
    dd_df = compute_drawdown(equity)
    n_years = len(equity) / 252
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (1 / n_years) - 1 if n_years > 0 else 0
    return RiskReport(
        var_95=compute_var(returns, 0.95),
        max_drawdown_pct=dd_df["drawdown"].min() * 100,
        sharpe_ratio=sharpe_ratio(returns),
        cagr_pct=cagr * 100,
    )
```

## Best Practices

- Use both parametric and historical VaR for robustness
- annualize metrics using correct periods_per_year (252 for daily)
- Validate against risk-management.json thresholds
- Report drawdown duration alongside magnitude

## References

- {directories.knowledge}/risk-management.json
- {directories.knowledge}/quantitative-finance.json
- {directories.knowledge}/trading-patterns.json

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
