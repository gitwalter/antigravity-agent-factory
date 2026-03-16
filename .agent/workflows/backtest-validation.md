---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for backtest-validation. Standardized for IDX Visual
  Editor.
domain: universal
name: backtest-validation
steps:
- actions:
  - Identify missing candles and outliers.
  - Verify volume scaling consistency.
  agents:
  - '@Architect'
  goal: ''
  name: Data Sanitization
  skills: []
  tools: []
- actions:
  - Run parameter sweep (Grid search or Bayesian).
  - '**Warning**: Do not over-optimize. Focus on "Stability Zones."'
  agents:
  - '@Architect'
  goal: ''
  name: In-Sample Optimization
  skills: []
  tools: []
- actions:
  - Run strategy on "Seen but unused" data.
  - Pass if performance remains within 20% of In-Sample metrics.
  agents:
  - '@Architect'
  goal: ''
  name: Out-of-Sample Validation
  skills: []
  tools: []
- actions:
  - Randomize trade order 1000x to calculate Max Drawdown probability.
  - PASS if 95% Var < 15%.
  agents:
  - '@Architect'
  goal: ''
  name: Monte Carlo Simulation
  skills: []
  tools: []
- actions:
  - Compare returns vs Benchmarks (SPY, QQQ) and other factory strategies.
  - Pass if Correlation < 0.6.
  agents:
  - '@Architect'
  goal: ''
  name: Correlation Audit
  skills: []
  tools: []
- actions:
  - Generate "Fact Sheet" with Sharpe, Sortino, and Profit Factor.
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
  name: Recommendation Package
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Backtest Validation

**Version:** 1.0.0

## Overview
Antigravity workflow for backtest-validation. Standardized for IDX Visual Editor.

## Trigger Conditions
- New strategy development completed.
- Existing strategy requires re-validation against new data.
- User request: `/backtest-validation`.

**Trigger Examples:**
- "Validate the new trend-following strategy."
- "Run a backtest audit on the Mean Reversion bot."

## Phases

### 1. Data Sanitization
- **Agents**: `@Architect`
- Identify missing candles and outliers.
- Verify volume scaling consistency.

### 2. In-Sample Optimization
- **Agents**: `@Architect`
- Run parameter sweep (Grid search or Bayesian).
- **Warning**: Do not over-optimize. Focus on "Stability Zones."

### 3. Out-of-Sample Validation
- **Agents**: `@Architect`
- Run strategy on "Seen but unused" data.
- Pass if performance remains within 20% of In-Sample metrics.

### 4. Monte Carlo Simulation
- **Agents**: `@Architect`
- Randomize trade order 1000x to calculate Max Drawdown probability.
- PASS if 95% Var < 15%.

### 5. Correlation Audit
- **Agents**: `@Architect`
- Compare returns vs Benchmarks (SPY, QQQ) and other factory strategies.
- Pass if Correlation < 0.6.

### 6. Recommendation Package
- **Agents**: `@Architect`
- Generate "Fact Sheet" with Sharpe, Sortino, and Profit Factor.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
