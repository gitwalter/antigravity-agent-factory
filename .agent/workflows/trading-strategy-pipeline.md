---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for trading-strategy-pipeline. Standardized for
  IDX Visual Editor.
domain: universal
name: trading-strategy-pipeline
steps:
- actions:
  - '**Task**: Define the economic or behavioral intuition for the strategy.'
  - '**Constraint**: Must align with `trading-governance.md` section 4.'
  agents:
  - '@Architect'
  goal: Document the "Alpha Source" (e.g., "Overreaction to earnings misses in high-growth
    tech").
  name: Hypothesis Formation
  skills: []
  tools: []
- actions:
  - '**Task**: Fetch historical OHLCV data.'
  - '**Check**: Audit for survivorship bias (use delisted tickers if available).'
  - '**Normalize**: Ensure splits and dividends are properly accounted for.'
  agents:
  - '@Architect'
  goal: ''
  name: Prepare & Clean Data
  skills: []
  tools: []
- actions:
  - '**Task**: Vectorize the signal logic using pandas/numpy or TA-Lib.'
  - '**Rule**: Keep parameters < 5 to avoid overfitting (P1_OVERFITTING).'
  agents:
  - '@Architect'
  goal: ''
  name: Strategy Implementation
  skills: []
  tools: []
- actions:
  - '**Task**: Run initial simulation with realistic slippage (0.1%) and commissions.'
  - '**Output**: Equity curve, Drawdown chart, and Sharpe Ratio.'
  agents:
  - '@Architect'
  goal: ''
  name: Backtest Execution
  skills: []
  tools: []
- actions:
  - '**Task**: Divide data into 5 segments (Anchored or Rolling).'
  - '**Validation**: Pass if out-of-sample Sharpe > 1.2.'
  agents:
  - '@Architect'
  goal: ''
  name: Robustness Testing (Walk-Forward)
  skills: []
  tools: []
- actions:
  - '**Task**: Compare 1st half of backtest vs 2nd half.'
  agents:
  - '@Architect'
  goal: Identify factor decay or regime sensitivity.
  name: Bias & Decay Check
  skills: []
  tools: []
- actions:
  - '**Task**: Package metrics and equity curve.'
  - '**Decision**: Promote to "Skill" if all `trading-governance.md` gates are passed.'
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: Deployment Approval
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Trading Strategy Pipeline

**Version:** 1.0.0

## Overview
Antigravity workflow for researching, backtesting, and validating quantitative trading strategies. Standardized for IDX Visual Editor.

## Trigger Conditions
- New hypothesis for a market edge or "Alpha Source".
- Requirement for backtesting a trading signal against historical data.
- User request: `/trading-strategy-pipeline`.

**Trigger Examples:**
- "Execute the pipeline for a 'Mean Reversion' strategy on the S&P 500."
- "Validate the hypothesis for 'Momentum Persistence' in cryptocurrency markets."

## Phases

### 1. Hypothesis Formation
- **Goal**: Document the "Alpha Source" (e.g., "Overreaction to earnings misses in high-growth tech").
- **Agents**: `@Architect`
- **Task**: Define the economic or behavioral intuition for the strategy.
- **Constraint**: Must align with `trading-governance.md` section 4.

### 2. Prepare & Clean Data
- **Agents**: `@Architect`
- **Task**: Fetch historical OHLCV data.
- **Check**: Audit for survivorship bias (use delisted tickers if available).
- **Normalize**: Ensure splits and dividends are properly accounted for.

### 3. Strategy Implementation
- **Agents**: `@Architect`
- **Task**: Vectorize the signal logic using pandas/numpy or TA-Lib.
- **Rule**: Keep parameters < 5 to avoid overfitting (P1_OVERFITTING).

### 4. Backtest Execution
- **Agents**: `@Architect`
- **Task**: Run initial simulation with realistic slippage (0.1%) and commissions.
- **Output**: Equity curve, Drawdown chart, and Sharpe Ratio.

### 5. Robustness Testing (Walk-Forward)
- **Agents**: `@Architect`
- **Task**: Divide data into 5 segments (Anchored or Rolling).
- **Validation**: Pass if out-of-sample Sharpe > 1.2.

### 6. Bias & Decay Check
- **Goal**: Identify factor decay or regime sensitivity.
- **Agents**: `@Architect`
- **Task**: Compare 1st half of backtest vs 2nd half.

### 7. Deployment Approval
- **Agents**: `@Architect`
- **Task**: Package metrics and equity curve.
- **Decision**: Promote to "Skill" if all `trading-governance.md` gates are passed.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
