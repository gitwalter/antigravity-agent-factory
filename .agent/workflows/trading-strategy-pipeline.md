---
## Overview

description: End-to-end workflow for developing, validating, and deploying algorithmic trading strategies. Covers hypothesis forma...
---

# Trading Strategy Pipeline

End-to-end workflow for developing, validating, and deploying algorithmic trading strategies. Covers hypothesis formation, backtesting, statistical validation, paper trading, and live deployment approval.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** quantitative-trading, financial-ai-agents

## Trigger Conditions

This workflow is activated when:

- New trading strategy proposed
- Strategy needs validation
- Backtest requested
- Live deployment approval needed

**Trigger Examples:**
- "Test my momentum strategy"
- "Backtest the mean reversion algorithm"
- "Validate strategy for live trading"
- "Deploy strategy to paper trading"

## Steps

### 1. Hypothesis Formation
- **Task**: Define the economic or behavioral intuition for the strategy.
- **Goal**: Document the "Alpha Source" (e.g., "Overreaction to earnings misses in high-growth tech").
- **Constraint**: Must align with `trading-governance.md` section 4.

### 2. Prepare & Clean Data
- **Task**: Fetch historical OHLCV data.
- **Check**: Audit for survivorship bias (use delisted tickers if available).
- **Normalize**: Ensure splits and dividends are properly accounted for.

### 3. Strategy Implementation
- **Task**: Vectorize the signal logic using pandas/numpy or TA-Lib.
- **Rule**: Keep parameters < 5 to avoid overfitting (P1_OVERFITTING).

### 4. Backtest Execution
- **Task**: Run initial simulation with realistic slippage (0.1%) and commissions.
- **Output**: Equity curve, Drawdown chart, and Sharpe Ratio.

### 5. Robustness Testing (Walk-Forward)
- **Task**: Divide data into 5 segments (Anchored or Rolling).
- **Validation**: Pass if out-of-sample Sharpe > 1.2.

### 6. Bias & Decay Check
- **Task**: Compare 1st half of backtest vs 2nd half.
- **Goal**: Identify factor decay or regime sensitivity.

### 7. Deployment Approval
- **Task**: Package metrics and equity curve.
- **Decision**: Promote to "Skill" if all `trading-governance.md` gates are passed.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
