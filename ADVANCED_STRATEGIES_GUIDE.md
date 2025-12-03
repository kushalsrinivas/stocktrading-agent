# Advanced Trading Strategies Guide

This guide covers the 5 new aggressive trading strategies designed with primary and confirmation indicators for well-informed trading decisions.

## Overview

Each strategy follows a multi-indicator approach:

- **Primary Indicator**: Main signal generator
- **Confirmation Indicators**: 1-2 additional filters to validate the signal
- **Aggressive Parameters**: Tuned for higher trade frequency and faster signals

All strategies come in two variants:

1. **Standard Version**: Balanced aggression with multiple confirmations
2. **Aggressive Version**: Ultra-fast signals with looser conditions

---

## 1. Stochastic Breakout Strategy

**File**: `strategies/stochastic_breakout.py`

### Strategy Type

Breakout/Momentum - Captures momentum shifts with volatility confirmation

### Indicators

- **Primary**: Stochastic Oscillator (%K and %D)
- **Confirmation 1**: Volume Spike (volume > MA \* multiplier)
- **Confirmation 2**: ADX (Average Directional Index for trend strength)

### Logic

**Buy Signal**:

- Stochastic %K crosses above oversold level (20)
- Volume shows significant spike above average (30%+)
- ADX indicates strong trend forming (> 20)

**Sell Signal**:

- Stochastic %K crosses below overbought level (80)
- OR ADX weakens significantly (trend exhaustion)

### Key Parameters

```python
StochasticBreakoutStrategy(
    stoch_period=14,           # Lookback for stochastic
    stoch_oversold=20,         # Buy threshold
    stoch_overbought=80,       # Sell threshold
    adx_threshold=20,          # Minimum trend strength
    volume_spike_multiplier=1.3 # Volume confirmation
)
```

### Use Cases

- Best in trending markets with clear momentum
- Effective for capturing breakouts after consolidation
- Works well with volatile stocks/assets

---

## 2. VWAP Reversal Strategy

**File**: `strategies/vwap_reversal.py`

### Strategy Type

Mean Reversion - Buys dips with divergence confirmation

### Indicators

- **Primary**: VWAP (Volume Weighted Average Price)
- **Confirmation 1**: RSI Divergence Detection
- **Confirmation 2**: Volume Analysis

### Logic

**Buy Signal**:

- Price deviates significantly below VWAP (1.5%+)
- Bullish RSI divergence detected (price lower lows, RSI higher lows)
- Volume confirms participation (10%+ above average)

**Sell Signal**:

- Price reaches VWAP (mean reversion target)
- Bearish RSI divergence appears
- OR RSI shows overbought conditions

### Key Parameters

```python
VWAPReversalStrategy(
    vwap_deviation_threshold=1.5,  # % below VWAP to trigger
    rsi_period=14,                 # RSI calculation period
    divergence_lookback=10,        # Bars to scan for divergence
    volume_threshold=1.1           # Volume confirmation
)
```

### Use Cases

- Excellent for intraday mean reversion trades
- Works best in ranging/choppy markets
- Ideal for buying dips in strong stocks

---

## 3. Supertrend Momentum Strategy

**File**: `strategies/supertrend_momentum.py`

### Strategy Type

Trend Following - Rides strong trends aggressively

### Indicators

- **Primary**: Supertrend (ATR-based trend indicator)
- **Confirmation 1**: MACD Histogram (momentum acceleration)
- **Confirmation 2**: EMA Slope (trend direction)

### Logic

**Buy Signal**:

- Supertrend flips from bearish to bullish
- MACD histogram is positive and accelerating
- Price is above fast EMA (20) with upward slope

**Sell Signal**:

- Supertrend flips from bullish to bearish
- OR MACD histogram turns negative
- OR price breaks below EMA with downward slope

### Key Parameters

```python
SupertrendMomentumStrategy(
    atr_period=10,              # ATR calculation period
    atr_multiplier=2.5,         # Supertrend sensitivity
    macd_fast=12,               # MACD fast period
    macd_slow=26,               # MACD slow period
    ema_period=20               # Trend confirmation EMA
)
```

### Use Cases

- Perfect for strong trending markets
- Captures major moves with momentum confirmation
- Great for swing trading positions

---

## 4. Keltner Channel Squeeze Strategy

**File**: `strategies/keltner_squeeze.py`

### Strategy Type

Breakout/Volatility - Catches explosive moves after consolidation

### Indicators

- **Primary**: Keltner Channels (ATR-based bands)
- **Confirmation 1**: Bollinger Band Width (volatility measure)
- **Confirmation 2**: Momentum Oscillator (ROC)

### Logic

**Buy Signal**:

- Volatility squeeze detected (Bollinger Bands inside Keltner Channels)
- Price breaks out above Keltner upper band
- Momentum oscillator shows positive direction
- Volume surge confirms breakout

**Sell Signal**:

- Price falls back below Keltner middle (failed breakout)
- OR momentum reverses significantly
- OR extreme volatility expansion (profit taking)

### Key Parameters

```python
KeltnerSqueezeStrategy(
    kc_period=20,               # Keltner Channel period
    kc_atr_multiplier=2.0,      # KC band width
    bb_period=20,               # Bollinger Band period
    bb_std=2.0,                 # BB standard deviations
    momentum_threshold=1.0,     # Minimum momentum %
    volume_threshold=1.3        # Volume surge requirement
)
```

### Use Cases

- Exceptional for capturing volatility expansions
- Works after periods of consolidation
- Ideal for breakout traders

---

## 5. Williams %R Trend Catcher

**File**: `strategies/williams_trend.py`

### Strategy Type

Momentum/Trend - Aggressive reversal and continuation plays

### Indicators

- **Primary**: Williams %R (momentum oscillator)
- **Confirmation 1**: ADX (trend strength)
- **Confirmation 2**: Volume Moving Average

### Logic

**Buy Signal**:

- Williams %R shows extreme oversold (< -80)
- ADX confirms strong trend forming (> 20)
- Volume is above moving average
- Price momentum confirms reversal

**Sell Signal**:

- Williams %R shows extreme overbought (> -20)
- OR ADX weakens significantly
- OR volume dries up with weakening momentum

### Key Parameters

```python
WilliamsTrendStrategy(
    williams_period=14,         # Williams %R period
    williams_oversold=-80,      # Oversold threshold
    williams_overbought=-20,    # Overbought threshold
    adx_strong_trend=20,        # Strong trend threshold
    volume_threshold=1.1        # Volume confirmation
)
```

### Use Cases

- Great for catching reversals at extremes
- Works in both trending and ranging markets
- Good for momentum-based entries

---

## Strategy Comparison

| Strategy            | Type            | Market Condition | Trade Frequency | Risk Level  |
| ------------------- | --------------- | ---------------- | --------------- | ----------- |
| Stochastic Breakout | Momentum        | Trending         | Medium          | Medium-High |
| VWAP Reversal       | Mean Reversion  | Ranging/Choppy   | High            | Medium      |
| Supertrend Momentum | Trend Following | Strong Trends    | Low-Medium      | Medium      |
| Keltner Squeeze     | Breakout        | Consolidation    | Low             | High        |
| Williams %R         | Momentum/Trend  | Mixed            | Medium-High     | Medium-High |

---

## Testing Your Strategies

### Basic Usage Example

```python
from strategies import (
    StochasticBreakoutStrategy,
    VWAPReversalStrategy,
    SupertrendMomentumStrategy,
    KeltnerSqueezeStrategy,
    WilliamsTrendStrategy
)
from backtester.engine import BacktestEngine
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv', index_col='Date', parse_dates=True)

# Choose a strategy
strategy = StochasticBreakoutStrategy()

# Run backtest
engine = BacktestEngine(
    data=data,
    strategy=strategy,
    initial_capital=100000,
    commission=0.001
)

results = engine.run()
print(results)
```

### Testing All Strategies

```python
strategies = [
    ("Stochastic Breakout", StochasticBreakoutStrategy()),
    ("VWAP Reversal", VWAPReversalStrategy()),
    ("Supertrend Momentum", SupertrendMomentumStrategy()),
    ("Keltner Squeeze", KeltnerSqueezeStrategy()),
    ("Williams Trend", WilliamsTrendStrategy())
]

for name, strategy in strategies:
    print(f"\nTesting {name}...")
    engine = BacktestEngine(data=data, strategy=strategy, initial_capital=100000)
    results = engine.run()
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
```

---

## Optimization Tips

### 1. Parameter Tuning

- Start with default parameters
- Use historical data to optimize key thresholds
- Be careful not to overfit to past data

### 2. Risk Management

- Always use stop losses
- Consider position sizing based on volatility
- Don't risk more than 1-2% per trade

### 3. Market Conditions

- Test strategies in different market conditions
- Some strategies work better in trends, others in ranges
- Consider combining multiple strategies for diversification

### 4. Volume Analysis

- All strategies use volume confirmation
- Higher volume = more reliable signals
- Low volume breakouts often fail

### 5. Time Frames

- Test on multiple time frames
- Shorter time frames = more signals but more noise
- Longer time frames = fewer but higher quality signals

---

## Aggressive Variants

Each strategy includes an aggressive variant with:

- Lower confirmation thresholds
- Shorter indicator periods
- Higher trade frequency
- Increased risk/reward potential

Access them with the `Aggressive` prefix:

```python
from strategies import (
    AggressiveStochasticStrategy,
    AggressiveVWAPStrategy,
    AggressiveSupertrendStrategy,
    AggressiveSqueezeStrategy,
    AggressiveWilliamsStrategy
)
```

---

## Next Steps

1. **Backtest**: Test each strategy on historical data
2. **Compare**: See which strategies work best for your assets
3. **Optimize**: Fine-tune parameters for your specific needs
4. **Combine**: Consider portfolio approaches using multiple strategies
5. **Paper Trade**: Test in real-time before risking real money

---

## Notes

- These strategies are designed to be aggressive for active trading
- Always backtest thoroughly before live trading
- Past performance does not guarantee future results
- Consider transaction costs and slippage in real trading
- Use proper risk management and position sizing

Happy Trading! 🚀
