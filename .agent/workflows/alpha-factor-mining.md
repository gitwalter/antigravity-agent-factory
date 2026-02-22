---
## Overview

version: 1.0.0
description: Step-by-step guide for finding and testing new predictive features (technical, fundamental, alternative).
---

# Alpha Factor Mining

This workflow defines the systematic process for identifying, testing, and validating new predictive factors (Alpha) before they are integrated into the factory's trading intelligence patterns.

**Version:** 1.0.0
**Note**: All mining activities must align with `trading-governance.md`.

## Steps

### 1. Feature Hypothesis
- **Action**: State the theoretical reason why a feature should predict price action.
- **Example**: "Put/Call ratio spikes predict short-term reversals due to extreme fear."

### 2. Data Acquisition
- **Action**: Fetch primary (Price/Volume) and secondary (Sentiment/Financials) data.
- **Check**: Ensure no look-ahead bias in feature calculation.
- Example: `mcp_local-faiss-mcp_ingest_document(path="data/raw/sentiment_v2.csv")`

### 3. Feature Transformation
- **Action**: Apply normalization or scaling.
- **Methods**: z-score, Min-Max, or Log-Returns.

### 4. Correlation Analysis
- **Action**: Check correlation of the new factor with existing factors in `trading-intelligence-patterns.json`.
- **Threshold**: pass if Absolute Correlation < 0.7.

### 5. IC (Information Coefficient) Testing
- **Action**: Calculate the Rank Correlation between the factor and future n-period returns.
- **pass if**: Mean IC > 0.02 and IC IR (Information Ratio) > 0.5.

### 6. Strategy Simulation
- **Action**: Run a simple long/short quintile backtest on the factor.
- **Metric**: Sharpe Ratio must be stable across multiple market regimes.

### 7. Factory Registration
- **Action**: Add the validated factor to `trading-intelligence-patterns.json` with its math and validation results.

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
