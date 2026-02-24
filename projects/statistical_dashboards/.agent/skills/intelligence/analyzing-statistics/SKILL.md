---
description: Statistical analysis, predictive modeling, and automated insight generation
name: analyzing-statistics
type: skill
---
# Statistical Analysis & Data Science Mastery

This skill provides comprehensive agentic guidance for industrial-grade data science, statistical modeling, and automated insight generation within the Antigravity ecosystem.

## Process

Follow these procedures to implement the capability:

## When to Use

This skill should be used when completing tasks related to analyzing statistics.

## 🔬 Statistical Foundations

### 1. Correct Application of Statistics
- **Descriptive**: Use `Pandas` and `DataManager.get_summary_stats` for initial posture analysis (Mean vs. Median for skewed warehouse data).
- **Inference**: Apply Hypothesis Testing (T-tests, Chi-square) to verify if operation changes (e.g., new conveyor speed) are statistically significant using `AnalysisManager.run_hypothesis_test`.
- **Distributions**: Detect and handle non-normal distributions using Log/Box-Cox transformations via `NumPy` before spectral or linear modeling.

### 2. Outlier & Anomaly Management
- Use **IQR (Interquartile Range)** for robust outlier detection in noisy IoT streams.
- Use **Z-score** for detecting deviations in standardized performance metrics (e.g., UPH variance).

## 🤖 Data Science & Machine Learning

### 1. Predictive Modeling (Prognosis)
- **Linear/Logistic Regression**: Use for trend forecasting and probability modeling (e.g., probability of an SLA breach).
- **Clustering (K-Means)**: Group warehouse bins or associates into "Performance Tiers" for targeted coaching or slotting optimization.
- **Validation**: Always report $R^2$, MSE, and P-values to ensure model reliability.

### 2. Tool Integration Patterns
- **Pandas**: Prioritize vectorized operations (`df.apply`, `df.groupby`) to handle building-scale datasets efficiently.
- **Visuals**:
    - **Matplotlib**: Deep-dive static plots for publication/reports.
    - **Plotly/Altair**: Interactive drill-down dashboards in Streamlit (e.g., Bin Density Heatmaps).

## 🧠 LLM-Augmented Analysis
- **Narrative Generation**: Extract statistical artifacts (coefficients, cluster centroids) and feed them to LLM APIs (OpenAI/Anthropic) to produce management-ready summaries.
- **Automated Interpretation**: Use LLMs to explain *why* a correlation might exist based on the business domain (e.g., "The correlation between shelf height and UPH suggests ergonomic fatigue").

## Best Practices
- **Workflow First**: Start with `/eda`, move to `/strategy-development` or `/warehouse-analytics`, and finalize with an Executive Summary.
- **Grounding**: Ensure all AI-generated insights are anchored to specific calculated metrics ($R^2$, P-value) to avoid hallucinated trends.
- **Reproducibility**: Save all models and data snapshots to the `Project` database to allow analysts to audit the decision logic.


## Prerequisites

- Access to relevant project documentation
- Environmental awareness of the target stack
