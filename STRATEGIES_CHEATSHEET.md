# Advanced Strategies Quick Reference

## Quick Import Guide

```python
from strategies import (
    # Stochastic Breakout
    StochasticBreakoutStrategy,
    AggressiveStochasticStrategy,
    
    # VWAP Reversal
    VWAPReversalStrategy,
    AggressiveVWAPStrategy,
    
    # Supertrend Momentum
    SupertrendMomentumStrategy,
    AggressiveSupertrendStrategy,
    
    # Keltner Squeeze
    KeltnerSqueezeStrategy,
    AggressiveSqueezeStrategy,
    
    # Williams Trend
    WilliamsTrendStrategy,
    AggressiveWilliamsStrategy
)
```

---

## One-Liner Strategy Descriptions

| Strategy | When to Use | One Line Description |
|----------|-------------|---------------------|
| **Stochastic Breakout** | Volatile, trending markets | Buy momentum surges with volume confirmation |
| **VWAP Reversal** | Ranging, mean-reverting markets | Buy dips below fair value with divergence |
| **Supertrend Momentum** | Strong trending markets | Ride trends with multi-indicator confirmation |
| **Keltner Squeeze** | After consolidation periods | Catch explosive breakouts from low volatility |
| **Williams Trend** | Mixed market conditions | Trade extremes with trend strength validation |

---

## Quick Setup Examples

### 1. Stochastic Breakout
```python
# Conservative
strategy = StochasticBreakoutStrategy(
    stoch_oversold=20,
    adx_threshold=25,
    volume_spike_multiplier=1.5
)

# Aggressive
strategy = AggressiveStochasticStrategy(
    stoch_oversold=25,
    adx_threshold=15,
    volume_spike_multiplier=1.2
)
```

### 2. VWAP Reversal
```python
# Conservative
strategy = VWAPReversalStrategy(
    vwap_deviation_threshold=2.0,
    rsi_oversold=30,
    volume_threshold=1.2
)

# Aggressive
strategy = AggressiveVWAPStrategy(
    vwap_deviation_threshold=0.8,
    volume_threshold=1.05
)
```

### 3. Supertrend Momentum
```python
# Conservative
strategy = SupertrendMomentumStrategy(
    atr_period=14,
    atr_multiplier=3.0,
    ema_period=20
)

# Aggressive
strategy = AggressiveSupertrendStrategy(
    atr_period=7,
    atr_multiplier=2.0,
    ema_period=10
)
```

### 4. Keltner Squeeze
```python
# Conservative
strategy = KeltnerSqueezeStrategy(
    kc_atr_multiplier=2.5,
    momentum_threshold=1.5,
    volume_threshold=1.5
)

# Aggressive
strategy = AggressiveSqueezeStrategy(
    kc_atr_multiplier=1.5,
    volume_threshold=1.15
)
```

### 5. Williams Trend
```python
# Conservative
strategy = WilliamsTrendStrategy(
    williams_oversold=-80,
    adx_strong_trend=25,
    volume_threshold=1.2
)

# Aggressive
strategy = AggressiveWilliamsStrategy(
    williams_oversold=-70,
    adx_threshold=15
)
```

---

## Standard Backtest Template

```python
from backtester.engine import BacktestEngine
import pandas as pd

# Load data
data = pd.read_csv('your_data.csv', index_col='Date', parse_dates=True)

# Choose strategy
strategy = StochasticBreakoutStrategy()  # or any other strategy

# Run backtest
engine = BacktestEngine(
    data=data,
    strategy=strategy,
    initial_capital=100000,
    commission=0.001
)

results = engine.run()

# View results
print(f"Total Return: {results['total_return']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
print(f"Total Trades: {results['total_trades']}")
```

---

## Parameter Tuning Tips

### Increase Trade Frequency
- Lower oversold/overbought thresholds
- Reduce volume requirements
- Shorten indicator periods
- Lower ADX thresholds

### Decrease Trade Frequency (More Selective)
- Raise oversold/overbought thresholds
- Increase volume requirements
- Lengthen indicator periods
- Raise ADX thresholds

### Reduce Risk
- Tighten stop losses
- Lower position sizes
- Require more confirmations
- Increase ADX thresholds for trend strength

### Increase Returns (More Risk)
- Wider stop losses
- Larger position sizes
- Fewer confirmations required
- Use aggressive variants

---

## Common Parameter Ranges

| Parameter | Conservative | Balanced | Aggressive |
|-----------|-------------|----------|-----------|
| **Stochastic Oversold** | 15 | 20 | 25-30 |
| **RSI Oversold** | 25 | 30 | 35-40 |
| **ADX Threshold** | 25+ | 20 | 15 |
| **Volume Multiplier** | 1.5x | 1.3x | 1.1-1.2x |
| **ATR Multiplier** | 3.0 | 2.5 | 2.0 |
| **VWAP Deviation** | 2.0% | 1.5% | 0.8-1.0% |

---

## Market Condition Guide

### Trending Market (Use Trend Following)
✓ **Supertrend Momentum**  
✓ **Williams Trend** (with high ADX)  
⚠ VWAP Reversal (less effective)

### Ranging Market (Use Mean Reversion)
✓ **VWAP Reversal**  
✓ **Keltner Squeeze** (for breakout attempts)  
⚠ Supertrend Momentum (whipsaws)

### Volatile Market (Use Breakouts)
✓ **Stochastic Breakout**  
✓ **Keltner Squeeze**  
⚠ Mean reversion strategies (risk of trending)

### Low Volatility (Use Squeeze)
✓ **Keltner Squeeze**  
⚠ All others (few signals)

---

## Risk Management Essentials

### Position Sizing
```python
# Risk 1% of capital per trade
risk_per_trade = 0.01
stop_loss_pct = 0.02  # 2% stop loss

position_size = (capital * risk_per_trade) / stop_loss_pct
```

### Stop Loss Recommendations
- **Stochastic Breakout**: 2-3% below entry
- **VWAP Reversal**: Below recent low or 1.5%
- **Supertrend**: Use Supertrend line as stop
- **Keltner Squeeze**: Below Keltner lower band
- **Williams Trend**: 2-3% or below recent swing low

### Profit Targets
- **Mean Reversion**: Target VWAP or Bollinger mid-band
- **Trend Following**: Trailing stop or opposite signal
- **Breakout**: 1.5-2x risk or next resistance level

---

## Testing Workflow

1. **Load Data**: Historical OHLCV data
2. **Pick Strategy**: Based on market condition
3. **Set Parameters**: Start with defaults
4. **Run Backtest**: Test on historical data
5. **Analyze Results**: Check all metrics
6. **Optimize**: Tune parameters carefully
7. **Validate**: Test on out-of-sample data
8. **Paper Trade**: Real-time testing
9. **Go Live**: Start with small positions

---

## Performance Metrics Guide

| Metric | Good | Acceptable | Poor |
|--------|------|-----------|------|
| **Sharpe Ratio** | > 1.5 | 0.8 - 1.5 | < 0.8 |
| **Win Rate** | > 55% | 45-55% | < 45% |
| **Max Drawdown** | < 15% | 15-25% | > 25% |
| **Profit Factor** | > 1.5 | 1.2-1.5 | < 1.2 |
| **Avg Win/Loss** | > 1.5 | 1.0-1.5 | < 1.0 |

---

## Common Mistakes to Avoid

❌ **Over-optimization** - Fitting too closely to historical data  
❌ **Ignoring commissions** - Not accounting for transaction costs  
❌ **Too many indicators** - Analysis paralysis  
❌ **No risk management** - Trading without stops  
❌ **Wrong market condition** - Using trend strategy in range  
❌ **Position sizing** - Risking too much per trade  
❌ **No validation** - Not testing out-of-sample  
❌ **Emotional trading** - Not following the system  

---

## Files Reference

- **Strategy Files**: `strategies/` folder
- **Examples**: `examples/advanced_strategies_example.py`
- **Full Guide**: `ADVANCED_STRATEGIES_GUIDE.md`
- **This Cheatsheet**: `STRATEGIES_CHEATSHEET.md`

---

## Quick Command to Test All

```bash
# Run the example file
python examples/advanced_strategies_example.py
```

This will:
- Generate sample data
- Test each strategy
- Compare all strategies
- Save results to CSV

---

**Remember**: Past performance ≠ Future results. Always backtest, validate, and paper trade before going live! 📈

