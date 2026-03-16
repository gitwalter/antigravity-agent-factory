---
version: 1.0.0
description: Step-by-step guide for finding and testing-agents new predictive features (technical,
  fundamental, alternative).
dashboard: true
tags:
- alpha
- factor
- mining
- standardized
---


# Alpha Factor Mining

This workflow defines the systematic process for identifying, testing-agents, and validating new predictive factors (Alpha) before they are integrated into the factory's trading intelligence patterns.

**Version:** 1.0.0
**Note**: All mining activities must align with `trading-governance.md`.

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

## Trigger Conditions
- New data source acquired.
- Fundamental regime change (e.g. Fed pivot).
- Strategy performance degradation (Sharpe < 1.0).

**Trigger Examples:**
- "Guardian, mine new alpha factors from the Put/Call ratio."
- "/alpha-factor-mining --source sentiment --target technology-sector"
- "Analyze this new data source for predictive alpha: `data/raw/sentiment_v2.csv`"


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
