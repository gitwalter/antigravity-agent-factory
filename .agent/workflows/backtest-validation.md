---
## Overview

description: Strategy backtesting workflow with walk-forward analysis and Monte Carlo simulation. Covers data preparation, backtes...
---

# Backtest Validation

Strategy backtesting workflow with walk-forward analysis and Monte Carlo simulation. Covers data preparation, backtest execution, statistical validation, and robustness checks.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** quantitative-trading, algo-trading

## Trigger Conditions

This workflow is activated when:

- Strategy backtest requested
- Walk-forward validation needed
- Monte Carlo simulation required
- Pre-live validation

**Trigger Examples:**
- "Backtest this strategy"
- "Run walk-forward analysis"
- "Run Monte Carlo simulation"
- "Validate strategy before paper trading"

## Steps

### 1. Data Sanitization
- Identify missing candles and outliers.
- Verify volume scaling consistency.

### 2. In-Sample Optimization
- Run parameter sweep (Grid search or Bayesian).
- **Warning**: Do not over-optimize. Focus on "Stability Zones."

### 3. Out-of-Sample Validation
- Run strategy on "Seen but unused" data.
- Pass if performance remains within 20% of In-Sample metrics.

### 4. Monte Carlo Simulation
- Randomize trade order 1000x to calculate Max Drawdown probability.
- PASS if 95% Var < 15%.

### 5. Correlation Audit
- Compare returns vs Benchmarks (SPY, QQQ) and other factory strategies.
- Pass if Correlation < 0.6.

### 6. Recommendation Package
- Generate "Fact Sheet" with Sharpe, Sortino, and Profit Factor.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
