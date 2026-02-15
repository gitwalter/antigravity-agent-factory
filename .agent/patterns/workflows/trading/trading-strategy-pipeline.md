# Trading Strategy Pipeline Workflow

## Overview

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

## Phases

### Phase 1: Hypothesis Formation

**Description:** Define the trading hypothesis and expected behavior.

**Entry Criteria:** Strategy idea exists
**Exit Criteria:** Hypothesis documented

#### Step 1.1: Document Strategy

**Actions:**
- Define market hypothesis
- Specify entry/exit rules
- Document position sizing
- Set risk parameters

**Strategy Template:**
```
Hypothesis: [Market inefficiency to exploit]
Entry: [Conditions to enter trade]
Exit: [Conditions to exit trade]
Position Size: [Sizing methodology]
Risk Limits: [Maximum risk parameters]
```

**Skills:**
- `trading-strategy`: Strategy patterns

**Outputs:**
- Strategy specification

**Is Mandatory:** Yes

---

### Phase 2: Backtesting

**Description:** Test strategy on historical data.

**Entry Criteria:** Strategy documented
**Exit Criteria:** Backtest results available

#### Step 2.1: Prepare Data

**Actions:**
- Load historical data
- Handle missing values
- Adjust for splits/dividends
- Verify data quality

#### Step 2.2: Run Backtest

**Actions:**
- Execute strategy on historical data
- Calculate P&L
- Track all trades
- Measure performance metrics

**Skills:**
- `backtesting-validation`: Validation patterns

**Key Metrics:**

| Metric | Minimum | Good |
|--------|---------|------|
| Sharpe Ratio | 1.0 | >1.5 |
| Sortino Ratio | 1.5 | >2.0 |
| Max Drawdown | <20% | <10% |
| Win Rate | 40% | >50% |

**Outputs:**
- Backtest report
- Trade log

**Is Mandatory:** Yes

---

### Phase 3: Statistical Validation

**Description:** Verify results are statistically significant.

**Entry Criteria:** Backtest complete
**Exit Criteria:** Statistical validation passed

#### Step 3.1: Bias Detection

**Actions:**
- Check look-ahead bias
- Verify survivorship bias
- Detect overfitting
- Check data snooping

**Bias Checks:**

| Bias | Detection Method |
|------|-----------------|
| Look-ahead | Point-in-time data verification |
| Survivorship | Include delisted securities |
| Overfitting | Out-of-sample testing |
| Selection | Multiple testing correction |

#### Step 3.2: Walk-Forward Analysis

**Actions:**
- Split into training/test periods
- Re-optimize on rolling windows
- Calculate out-of-sample performance
- Verify parameter stability

**Outputs:**
- Validation report
- Confidence level

**Is Mandatory:** Yes

---

### Phase 4: Paper Trading

**Description:** Test strategy in real-time with simulated money.

**Entry Criteria:** Statistical validation passed
**Exit Criteria:** Paper trading period complete

#### Step 4.1: Deploy to Paper

**Actions:**
- Deploy to paper trading environment
- Monitor execution
- Track real-time performance
- Compare to backtest

**Paper Trading Requirements:**
- Minimum duration: 30 days
- Minimum trades: 50
- Real market conditions
- Simulated slippage

**Outputs:**
- Paper trading results
- Execution quality metrics

**Is Mandatory:** Yes

---

### Phase 5: Live Approval

**Description:** Human approval gate for live deployment.

**Entry Criteria:** Paper trading successful
**Exit Criteria:** Approval decision made

#### Step 5.1: Prepare Approval Package

**Actions:**
- Compile all test results
- Document risk limits
- Define kill switch criteria
- Prepare monitoring plan

**Approval Criteria:**

| Metric | Requirement |
|--------|-------------|
| Sharpe (paper) | >80% of backtest |
| Max Drawdown | Within limits |
| Execution Quality | <0.5% slippage |
| Consistency | No major divergence |

#### Step 5.2: Human Review

**Actions:**
- Present to risk committee
- Address questions
- Document decision
- Set monitoring schedule

**Decision:**
- APPROVED: Ready for live
- CONDITIONAL: Fix issues first
- REJECTED: Back to development

**Outputs:**
- Approval decision
- Deployment constraints

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Backtest Quality

| Condition | Action |
|-----------|--------|
| Metrics meet thresholds | Proceed to validation |
| Metrics marginal | Optimize strategy |
| Metrics poor | Revise hypothesis |

### Decision: Live Deployment

| Condition | Action |
|-----------|--------|
| All gates passed | Deploy with limits |
| Paper underperforms | Extend paper period |
| Significant issues | Return to development |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Data unavailable | Use alternative data source |
| Backtest fails | Check data quality first |
| Paper trading system down | Use broker demo account |
| Approval delayed | Extend paper trading |
| Live issues detected | Automatic kill switch |

---

## Escalation Paths

| Trigger | Escalate To |
|---------|-------------|
| Risk limit breach | Risk Manager |
| Regulatory concern | Compliance |
| System failure | Operations |
| Market anomaly | Trading Desk |

---

## Example Session

```
User: Validate my momentum strategy for live trading

Agent:
━━━ PHASE 1: Hypothesis Formation ━━━
Strategy: 20-day momentum with RSI filter
Entry: Price > 20-day high, RSI < 70
Exit: 5% trailing stop or RSI > 80
Position Size: 2% per trade
Risk Limit: 10% max portfolio drawdown

━━━ PHASE 2: Backtesting ━━━
Period: 2020-2024 (5 years)
Universe: S&P 500

Results:
- Total Return: 187%
- Sharpe Ratio: 1.8 ✓
- Sortino Ratio: 2.3 ✓
- Max Drawdown: 12% ✓
- Win Rate: 54%
- Total Trades: 342

━━━ PHASE 3: Statistical Validation ━━━
Bias Checks:
✓ No look-ahead bias detected
✓ Survivorship bias accounted for
✓ Overfitting test passed (IS/OOS ratio: 0.85)

Walk-Forward Analysis:
- 5 periods tested
- Consistent performance
- Parameter stability verified

Confidence: HIGH (p-value < 0.01)

━━━ PHASE 4: Paper Trading ━━━
Deploying to paper trading...

After 45 days:
- Return: 8.2%
- Sharpe: 1.6 (89% of backtest) ✓
- Max Drawdown: 4.2%
- Trades: 28
- Avg Slippage: 0.3% ✓

━━━ PHASE 5: Live Approval ━━━
Preparing approval package...

Recommendation: APPROVED FOR LIVE

Constraints:
- Initial allocation: $100,000
- Max position: 2%
- Daily loss limit: 2%
- Kill switch: 5% monthly loss

Monitoring: Daily performance review

✨ Strategy approved for live trading!
```

---

## Related Artifacts

- **Skills**: `patterns/skills/trading-strategy.json`, `patterns/skills/risk-analysis.json`
- **Knowledge**: `knowledge/trading-patterns.json`
