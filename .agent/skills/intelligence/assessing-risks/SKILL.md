---
agents:
- none
category: general
description: Quantitative and Industrial risk assessment with VaR, drawdown analysis,
  SLA breach forecasting, and process reliability metrics.
knowledge:
- none
name: assessing-risks
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Risk Assessment & Prognosis

Perform quantitative and qualitative risk analysis. This skill covers both financial risk (VaR, Sharpe) and Industrial risk (SLA breaches, throughput bottlenecks).

## Process

1. **Review Context**: Determine if the risk is Financial, Operational, or Technical.
2. **Select Methodology**: Use statistical methods for large datasets; use heuristic analysis for process risks.
3. **Generate Report**: Produce a structured `RiskReport` with actionable mitigations.

### Step 1: Financial Risk Metrics (Quantitative)

Compute standard risk metrics for time-series data.

```python
import numpy as np
import pandas as pd
from scipy import stats

def compute_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Compute 95% Value-at-Risk."""
    return -returns.quantile(1 - confidence)

def compute_sharpe(returns: pd.Series, rf=0.0) -> float:
    """Annualized Sharpe Ratio (252 periods)."""
    return (returns.mean() - rf/252) / returns.std() * np.sqrt(252)
```

### Step 2: Industrial Risk (Operational)

Analyze process data for potential SLA breaches or bottlenecks.

```python
def analyze_sla_risk(
    actual_uph: float,
    target_uph: float,
    remaining_volume: int,
    remaining_hours: float
) -> dict:
    """Assess risk of failing to meet shipment deadline."""
    needed_uph = remaining_volume / remaining_hours
    gap = needed_uph - actual_uph
    risk_level = "High" if gap > actual_uph * 0.2 else "Low"

    return {
        "risk_level": risk_level,
        "needed_uph": needed_uph,
        "current_gap": gap,
        "mitigation": "Increase labor allocation" if risk_level == "High" else "Monitor"
    }
```

### Step 3: Predictive Anomaly Detection

Use Z-scores to identify extreme operational risks.

```python
def detect_operational_outliers(df, column='processing_time'):
    z_scores = stats.zscore(df[column])
    critical_risks = df[np.abs(z_scores) > 3]
    return critical_risks
```

## Best Practices

- **Contextualize**: A 5% dip is "High Risk" for an equity fund but "Normal Variance" for picker UPH.
- **Duality**: Always report Risk Magnitude alongside Probability.
- **Actionability**: Every identified risk MUST have a corresponding mitigation strategy.

## References

- `.agent/knowledge/risk-management.json`
- `.agent/knowledge/risk-management-patterns.json`
- `.agent/knowledge/quantitative-theory.json`

## When to Use
Use this when requested to perform "Risk Analysis", "SLA Verification", or "Stress Testing".


## Prerequisites

- Access to relevant project documentation
- Environmental awareness of the target stack
