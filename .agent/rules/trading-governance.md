# Trading Governance & Standards

This document defines the mandatory safety and statistical standards for all trading agents, skills, and workflows within the Antigravity Agent Factory.

## 1. Safety Axioms (Circuit Breakers)

All trading agents MUST adhere to these safety principles to prevent catastrophic losses:

- **A1_MAX_DRAWDOWN**: No strategy shall be deployed to live trading if its historical maximum drawdown exceeds 25% without explicit risk-governor override.
- **A2_STOP_LOSS**: All trade recommendations MUST include a hard stop-loss based on volatility (e.g., 2*ATR) or a fixed percentage.
- **A3_POSITION_LIMIT**: Single position exposure MUST NOT exceed 10% of the total portfolio value.
- **A4_LIQUIDITY_CHECK**: Agents must verify that the average daily volume of the asset is at least 100x the intended position size.

## 2. Statistical Validation Requirements

Before a strategy can be promoted to a "Skill," it must pass these statistical hurdles:

- **Sharpe Ratio**: > 1.2 on out-of-sample data.
- **Win Rate**: > 45% (for momentum) or > 55% (for mean reversion).
- **Min Trade Count**: > 100 trades to ensure statistical significance.
- **Profit Factor**: > 1.5.

## 3. Backtesting Protocol

- **Walk-Forward Analysis**: Mandatory for all strategy validations to detect over-fitting.
- **Data Integrity**: Agents must check for look-ahead bias and survivorship bias in the data source.
- **Slippage & Commission**: Backtests MUST include realistic estimates for slippage (e.g., 0.1% per trade) and commission fees.

## 4. Alpha Promotion Workflow

To add a new predictive factor to `trading-intelligence-patterns.json`, the following must be documented:
1. **Economic Intuition**: Why should this factor work?
2. **Correlation Check**: Is this factor redundant with existing factors in the factory?
3. **Decay Analysis**: How has the factor performed in the most recent 6 months?

## 5. Anti-Patterns to Avoid

- **P1_OVERFITTING**: Using more than 5 parameters for a simple technical strategy.
- **P2_CHERRY_PICKING**: Validating a strategy only on "bull market" periods.
- **P3_CORRELATION_IGNORE**: Assuming diversification while holding 10 highly correlated tech stocks.
