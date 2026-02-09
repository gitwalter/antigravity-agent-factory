---
description: Build algorithmic trading strategies with backtesting, technical indicators, and fundamental data
---

# Algo Trading

Build algorithmic trading strategies with backtesting, technical indicators, and fundamental data

## 
# Algorithmic Trading Skill

Build production-ready trading systems with proper backtesting, risk management, and data integration.

## 
# Algorithmic Trading Skill

Build production-ready trading systems with proper backtesting, risk management, and data integration.

## Process
### Step 1: Data Acquisition

```python
import yfinance as yf

# Single asset
df = yf.download("SPY", start="2020-01-01", end="2024-01-01")
df.columns = [c.lower() for c in df.columns]

# Multiple assets
data = yf.download(["SPY", "QQQ", "IWM"], start="2020-01-01")
```

### Step 2: Calculate Technical Indicators

```python
import pandas_ta as ta

# Add indicators
df['sma_20'] = ta.sma(df['close'], length=20)
df['rsi'] = ta.rsi(df['close'], length=14)
df['macd'] = ta.macd(df['close'])['MACD_12_26_9']
df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
df['bbands'] = ta.bbands(df['close'], length=20, std=2)
```

### Step 3: Generate Signals

```python
# Example: MA Crossover
fast_ma = df['close'].rolling(10).mean()
slow_ma = df['close'].rolling(50).mean()

signals = pd.Series(0, index=df.index)
signals[fast_ma > slow_ma] = 1   # Long
signals[fast_ma < slow_ma] = -1  # Short
```

### Step 4: Backtest

**VectorBT (fast, vectorized):**
```python
import vectorbt as vbt

entries = signals.diff() == 1
exits = signals.diff() == -1

portfolio = vbt.Portfolio.from_signals(
    df['close'],
    entries,
    exits,
    init_cash=100_000,
    fees=0.001
)
print(portfolio.stats())
```

**Backtrader (object-oriented):**
```python
import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SMA(period=20)
    
    def next(self):
        if self.data.close > self.sma:
            self.buy()
        elif self.data.close < self.sma:
            self.close()
```

### Step 5: Fetch Fundamental Data

```python
ticker = yf.Ticker("AAPL")

# Financial statements
income_stmt = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cashflow

# Key ratios from info
info = ticker.info
pe_ratio = info.get('trailingPE')
roe = info.get('returnOnEquity')
debt_to_equity = info.get('debtToEquity')
```

### Step 6: Risk Metrics

```python
from knowledge.quantitative-finance import sharpe_ratio, max_drawdown

returns = df['close'].pct_change()
sharpe = np.sqrt(252) * returns.mean() / returns.std()
max_dd = (df['close'] / df['close'].expanding().max() - 1).min()
```

```python
import yfinance as yf

# Single asset
df = yf.download("SPY", start="2020-01-01", end="2024-01-01")
df.columns = [c.lower() for c in df.columns]

# Multiple assets
data = yf.download(["SPY", "QQQ", "IWM"], start="2020-01-01")
```

```python
import pandas_ta as ta

# Add indicators
df['sma_20'] = ta.sma(df['close'], length=20)
df['rsi'] = ta.rsi(df['close'], length=14)
df['macd'] = ta.macd(df['close'])['MACD_12_26_9']
df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
df['bbands'] = ta.bbands(df['close'], length=20, std=2)
```

```python
# Example: MA Crossover
fast_ma = df['close'].rolling(10).mean()
slow_ma = df['close'].rolling(50).mean()

signals = pd.Series(0, index=df.index)
signals[fast_ma > slow_ma] = 1   # Long
signals[fast_ma < slow_ma] = -1  # Short
```

```python
import vectorbt as vbt

entries = signals.diff() == 1
exits = signals.diff() == -1

portfolio = vbt.Portfolio.from_signals(
    df['close'],
    entries,
    exits,
    init_cash=100_000,
    fees=0.001
)
print(portfolio.stats())
```

```python
import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SMA(period=20)
    
    def next(self):
        if self.data.close > self.sma:
            self.buy()
        elif self.data.close < self.sma:
            self.close()
```

```python
ticker = yf.Ticker("AAPL")

# Financial statements
income_stmt = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cashflow

# Key ratios from info
info = ticker.info
pe_ratio = info.get('trailingPE')
roe = info.get('returnOnEquity')
debt_to_equity = info.get('debtToEquity')
```

```python
from knowledge.quantitative-finance import sharpe_ratio, max_drawdown

returns = df['close'].pct_change()
sharpe = np.sqrt(252) * returns.mean() / returns.std()
max_dd = (df['close'] / df['close'].expanding().max() - 1).min()
```

## What Gets Created
| File | Purpose |
|------|---------|
| `strategies/` | Strategy implementations |
| `indicators/` | Custom indicator calculations |
| `data/` | Data fetching and caching |
| `backtest/` | Backtesting engine and reports |
| `risk/` | Position sizing and risk management |

## Strategy Categories
| Category | Use When |
|----------|----------|
| **Momentum** | Assets trending, ADX > 25 |
| **Mean Reversion** | Range-bound markets, low volatility |
| **Statistical Arbitrage** | Pairs trading, factor models |
| **Machine Learning** | Non-linear patterns, feature engineering |

## Key Technical Indicators
| Indicator | Category | Use |
|-----------|----------|-----|
| SMA/EMA | Trend | Direction, support/resistance |
| RSI | Momentum | Overbought/oversold |
| MACD | Trend/Momentum | Crossover signals |
| Bollinger Bands | Volatility | Mean reversion entries |
| ATR | Volatility | Stop loss sizing |
| VWAP | Volume | Institutional benchmark |
| Ichimoku | Trend | Multi-component analysis |

## Fundamental Data Sources
| Source | Data Type | Cost |
|--------|-----------|------|
| yfinance | OHLCV, Financials | Free |
| Alpha Vantage | OHLCV, Fundamentals | Free tier |
| SEC EDGAR | Filings | Free |
| Polygon.io | Real-time | $29+/mo |

## Backtesting Best Practices
1. **Walk-forward validation** - Prevent overfitting
2. **Include transaction costs** - Realistic P&L
3. **Out-of-sample testing** - Validate on unseen data
4. **Monte Carlo simulation** - Assess robustness
5. **Parameter stability** - Avoid curve fitting

## Anti-Patterns to Avoid
| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Curve fitting | Fails live | Walk-forward validation |
| Survivorship bias | Overstated returns | Point-in-time data |
| Look-ahead bias | Unrealistic backtest | Strict data alignment |
| Ignoring costs | Unprofitable live | Include slippage + commissions |

## Fallback Procedures
| Issue | Solution |
|-------|----------|
| yfinance rate limited | Cache data locally |
| No fundamental data | Use technical-only strategy |
| Backtest fails | Check data alignment |
| Poor Sharpe ratio | Review strategy logic |

## Related Artifacts
- **Knowledge**: `knowledge/trading-patterns.json`
- **Knowledge**: `knowledge/quantitative-finance.json`
- **Knowledge**: `knowledge/risk-management.json`
- **Templates**: `templates/trading/`
- **Blueprint**: `blueprints/quantitative-trading/`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: yfinance, pandas-ta, vectorbt, backtrader, scipy, numpy
> - Knowledge: trading-patterns.json, quantitative-finance.json, risk-management.json
