---
agents:
- workflow-quality-specialist
- system-architecture-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for alpha-factor-mining. Standardized for IDX Visual
  Editor.
domain: universal
name: alpha-factor-mining
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - State the theoretical reason for the feature.
  agents:
  - system-architecture-specialist
  goal: Define the theoretical basis for a new predictive feature.
  name: Hypothesis & Hypothesis Generation
  skills:
  - designing-ai-systems
  - alpha-factor-mining
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Fetch Price/Volume and Sentiment data.
  - Apply z-score or Min-Max normalization.
  agents:
  - project-operations-specialist
  goal: Fetch and normalize primary and secondary data without look-ahead bias.
  name: Data Acquisition & Transformation
  skills:
  - fetch-external-data
  - alpha-factor-mining
  tools:
  - mcp_fetch_fetch
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Check correlation with existing factors.
  - Calculate Rank Correlation (IC) and IC IR.
  agents:
  - workflow-quality-specialist
  goal: Verify factor uniqueness and predictive power (Information Coefficient).
  name: Correlation & IC Testing
  skills:
  - evaluation-optimizer
  - alpha-factor-mining
  tools:
  - python-interpreter
- actions:
  - '**Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Run long/short quintile backtest.
  - Add to `trading-intelligence-patterns.json`.
  - New data source acquired.
  - Fundamental regime change (e.g. Fed pivot).
  - Strategy performance degradation (Sharpe < 1.0).
  - '"Guardian, mine new alpha factors from the Put/Call ratio."'
  - '"/alpha-factor-mining --source sentiment --target technology-sector"'
  - '"Analyze this new data source for predictive alpha: `data/raw/sentiment_v2.csv`"'
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - system-architecture-specialist
  - knowledge-operations-specialist
  goal: Validate stability across regimes and register in the intelligence library.
  name: Simulation & Registration
  skills:
  - strategy-development
  - generating-documentation
  tools:
  - python-interpreter
  - write_to_file
tags: []
type: sequential
version: 1.0.0
---

# Alpha Factor Mining

**Version:** 1.0.0

## Overview
This workflow governs the systematic discovery, validation, and registration of predictive features (alpha factors) for quantitative trading strategies.

## Trigger Conditions
- New data source acquired.
- Fundamental regime change (e.g. Fed pivot).
- Strategy performance degradation (Sharpe < 1.0).

**Trigger Examples:**
- "Guardian, mine new alpha factors from the Put/Call ratio."
- "/alpha-factor-mining --source sentiment --target technology-sector"
- "Analyze this new data source for predictive alpha: `data/raw/sentiment_v2.csv`"

## Phases

### Phase 1: Hypothesis & Hypothesis Generation
- **Goal**: Define the theoretical basis for a new predictive feature.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, alpha-factor-mining
- **Tools**: mcp_memory_search_nodes
- **Actions**:
- State the theoretical reason for the feature.

### Phase 2: Data Acquisition & Transformation
- **Goal**: Fetch and normalize primary and secondary data without look-ahead bias.
- **Agents**: `project-operations-specialist`
- **Skills**: fetch-external-data, alpha-factor-mining
- **Tools**: mcp_fetch_fetch, write_to_file
- **Actions**:
- Fetch Price/Volume and Sentiment data.
- Apply z-score or Min-Max normalization.

### Phase 3: Correlation & IC Testing
- **Goal**: Verify factor uniqueness and predictive power (Information Coefficient).
- **Agents**: `workflow-quality-specialist`
- **Skills**: evaluation-optimizer, alpha-factor-mining
- **Tools**: python-interpreter
- **Actions**:
- Check correlation with existing factors.
- Calculate Rank Correlation (IC) and IC IR.

### Phase 4: Simulation & Registration
- **Goal**: Validate stability across regimes and register in the intelligence library.
- **Agents**: `system-architecture-specialist`, `knowledge-operations-specialist`
- **Skills**: strategy-development, generating-documentation
- **Tools**: python-interpreter, write_to_file
- **Actions**:
- Run long/short quintile backtest.
- Add to `trading-intelligence-patterns.json`.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

## Best Practices
- Always split data into in-sample and out-of-sample sets for backtesting.
- Account for transaction costs and slippage in all simulations.
- Ensure factor definitions are robust to different market regimes.

## Related
- [/trading-strategy-pipeline](file:///.agent/workflows/trading-strategy-pipeline.md)
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
