# 📘 Donchian Breakout Strategy Guide

## What Is the Donchian Breakout Strategy?

The Donchian Channel is created by **Richard Donchian** and is built using:

- **Upper Band** = Highest High over X periods
- **Lower Band** = Lowest Low over X periods
- **Middle Band** = (Upper + Lower) / 2

A **Donchian Breakout** occurs when price breaks above the upper band (bullish) or breaks below the lower band (bearish).

It is a **pure trend-following strategy** used by hedge funds and the famous **Turtle Traders**.

---

## 🎯 Core Idea

> **"When price breaks out of its recent range, a new trend may be starting."**

So you enter only when price makes a new X-day high or low, signaling momentum.

---

## 🟢 Bullish Breakout (Buy Signal)

**Buy when:**
- Price closes above the Donchian Upper Band (20-day or 55-day high)

**This means:**
Price is the highest it has been in X days → trend is starting upward.

---

## 🔴 Bearish Breakout (Sell/Short Signal)

**Sell/short when:**
- Price closes below the Donchian Lower Band (20-day or 55-day low)

**Meaning:**
Price is the lowest it has been in X days → downward trend is starting.

---

## 🔧 Typical Settings

### ✔ Fast Donchian: 20-period
- Good for **swing trading**
- More frequent signals
- Higher false breakouts in ranging markets

### ✔ Slow Donchian: 55-period
- Used by **Turtle Traders** (famous hedge fund rules)
- Better for longer-term trends
- Fewer but more reliable signals

---

## 📈 Example Strategy (20-Day Donchian)

**Buy:**
- Price closes above the 20-day high

**Exit:**
- Price closes below the 10-day low (protects profits)

This prevents large trend reversals from eating gains.

---

## 🛡 Risk Management

Donchian breakout requires **strict risk rules**:

✔ **Position size based on volatility (ATR)**
✔ **Always use a stop-loss**
✔ **Expect many small losses but few massive winners**
✔ **Works best in trending markets (not sideways markets)**

---

## 🐢 The Turtle Traders Story

In 1983, legendary commodities trader **Richard Dennis** made a bet with his partner William Eckhardt:

> "Can trading be taught, or is it an innate skill?"

To prove his point, Dennis recruited 23 people (the "Turtles") with no trading experience and taught them a simple trend-following system based on Donchian Channels.

**The Results:**
- Over the next 4 years, the Turtle Traders earned an average annual return of **80%**
- They collectively made **over $175 million**
- The experiment proved that trading discipline and a systematic approach can be learned

**The Turtle Trading Rules:**
1. Entry: Buy when price breaks above the 55-day high (or 20-day for System 1)
2. Exit: Sell when price falls below the 20-day low (or 10-day for System 1)
3. Position Sizing: Risk 2% of capital per trade based on ATR
4. Add to Winners: Pyramid up to 4 units on winning trades
5. Cut Losses Fast: Exit immediately when stop is hit

---

## 🚀 Three Strategies Implemented

### 1️⃣ **DonchianBreakoutStrategy** (Classic)

**Best for:** Long-term trend following

**Parameters:**
- `entry_period=55` (Turtle Traders default)
- `exit_period=20` (protects profits)
- `use_middle_band=True` (optional early exits)
- `atr_period=14` (volatility measurement)

**Entry:**
- Long: Price closes above 55-day high
- Short: Price closes below 55-day low

**Exit:**
- Long exit: Price closes below 20-day low
- Short exit: Price closes above 20-day high
- Optional: Exit when price crosses middle band

**Best Markets:** Strongly trending stocks (Nifty 50 large caps)

---

### 2️⃣ **AggressiveDonchianStrategy** (Fast)

**Best for:** Swing trading, volatile markets

**Parameters:**
- `entry_period=20` (faster signals)
- `exit_period=10` (quicker exits)
- `atr_period=14`
- `atr_multiplier=2.0` (ATR-based stops)

**Entry:**
- Long: Price breaks above 20-day high
- Short: Price breaks below 20-day low

**Exit:**
- ATR-based stop loss: Entry price ± (2 × ATR)
- Or exit channel breach (10-day)

**Best Markets:** Mid-cap stocks with good volatility

**Advantages:**
- More trading opportunities
- Tighter risk control with ATR stops
- Adapts to volatility automatically

---

### 3️⃣ **TurtleTradersStrategy** (Original System)

**Best for:** Replicating the famous Turtle Trading system

**Parameters:**
- `entry_period=55` (System 2)
- `exit_period=20`
- `atr_period=20` (N-value in Turtle speak)
- `risk_per_trade=0.02` (2% risk per trade)

**Entry:**
- Long: New 55-day high
- Short: New 55-day low

**Exit:**
- Long: 20-day low
- Short: 20-day high

**Position Sizing:**
- Calculates position size based on ATR (volatility)
- Risks 2% of capital per trade
- Uses "N" (ATR) as the unit of risk

**Best Markets:** Any trending market (stocks, commodities, forex)

---

## 📊 When to Use Each Strategy

| Strategy | Market Type | Trading Frequency | Risk Level | Best For |
|----------|-------------|-------------------|------------|----------|
| **Classic Donchian** | Strong trends | Low (2-5 trades/year) | Medium | Patient investors |
| **Aggressive Donchian** | Volatile | Medium (10-20 trades/year) | Higher | Active traders |
| **Turtle Traders** | Any trend | Low-Medium (3-8 trades/year) | Controlled | Systematic traders |

---

## ✅ Advantages

1. **Simple & Objective** - No subjective interpretation
2. **Trend Capturing** - Catches major market moves
3. **Self-Adjusting** - Adapts to different timeframes
4. **Proven Track Record** - Used successfully by professionals
5. **Works Across Markets** - Stocks, commodities, forex, crypto

---

## ⚠️ Disadvantages

1. **Whipsaws in Ranging Markets** - Many false breakouts
2. **Late Entry** - By nature, enters after trend has started
3. **Gives Back Profits** - Waits for trend reversal to exit
4. **Requires Discipline** - Hard to follow during losing streaks
5. **Not Ideal for Choppy Markets** - Best in trending conditions

---

## 💡 Tips for Success

### 1. **Filter by Trend Strength**
Add ADX (Average Directional Index) to confirm trend:
- Only trade when ADX > 25 (strong trend)
- Avoid trading when ADX < 20 (weak/no trend)

### 2. **Combine with Volume**
- Confirm breakouts with above-average volume
- Higher volume = more reliable breakout

### 3. **Use Multiple Timeframes**
- Weekly chart for major trend
- Daily chart for entry/exit
- Align both for best results

### 4. **Position Sizing is Critical**
- Always use ATR-based position sizing
- Smaller positions in volatile stocks
- Larger positions in stable stocks

### 5. **Avoid in Sideways Markets**
- Donchian performs poorly in ranges
- Use RSI or Bollinger Band strategies instead
- Wait for clear trend direction

### 6. **Backtest Before Trading**
- Test on your target stocks first
- Check historical performance
- Understand typical drawdown periods

---

## 🎓 How to Use in This Framework

### Option 1: Run Interactive Backtest

```bash
python run_nse_backtest.py
```

Then select:
- **Strategy 11:** Donchian Breakout (Classic 55/20)
- **Strategy 12:** Donchian Fast (Aggressive 20/10)
- **Strategy 13:** Turtle Traders (Original System)

### Option 2: Compare All Strategies

```bash
python run_nse_backtest.py
```

Choose option 2 to compare all 13 strategies including Donchian variants.

### Option 3: SIP Portfolio Optimization

```bash
python sip_strategy_optimizer.py
```

The optimizer will automatically test Donchian strategies and include them if they perform best on any stock.

---

## 📚 Example Usage

### Test on Reliance Industries

```python
from backtester import Backtester, YFinanceDataHandler
from strategies import DonchianBreakoutStrategy

# Create strategy
strategy = DonchianBreakoutStrategy(
    entry_period=55,
    exit_period=20,
    use_middle_band=True
)

# Fetch data
data_handler = YFinanceDataHandler(
    symbol="RELIANCE.NS",
    start_date="2022-01-01",
    end_date="2024-12-01"
)

# Run backtest
backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=100000,
    commission=0.0005
)

results = backtester.run()
backtester.plot_results()
```

---

## 🎯 Best Stocks for Donchian Strategy

### ✅ Good Candidates (Strong Trending Behavior)
- **Reliance Industries (RELIANCE)** - Strong long-term trends
- **TCS** - Technology leader with clear trends
- **HDFC Bank (HDFCBANK)** - Banking sector leader
- **Infosys (INFY)** - Export-driven trends
- **Asian Paints** - Consistent long-term trends

### ⚠️ Avoid (Choppy/Ranging Behavior)
- Penny stocks with erratic movements
- Stocks with frequent gap ups/downs
- Stocks in consolidation phases
- Highly manipulated small caps

---

## 📊 Expected Performance Metrics

**In Trending Markets:**
- Win Rate: 35-45% (fewer wins, but big winners)
- Average Win/Loss Ratio: 2:1 to 3:1
- Sharpe Ratio: 0.8 - 1.5
- Max Drawdown: 15-25%

**In Ranging Markets:**
- Win Rate: 25-35% (many false breakouts)
- Expect multiple small losses
- Sharpe Ratio: 0 - 0.5
- Max Drawdown: 20-30%

---

## 🔗 Related Strategies

If Donchian doesn't work well on a stock, try:

1. **RSI + Bollinger Bands** - Better for ranging markets
2. **VWAP Reversal** - Mean reversion alternative
3. **Supertrend Momentum** - Alternative trend follower
4. **Keltner Squeeze** - Breakout with volatility filter

---

## 📖 Further Reading

- **"Way of the Turtle"** by Curtis Faith (Original Turtle Trader)
- **"The Complete TurtleTrader"** by Michael Covel
- **"Trend Following"** by Michael Covel
- Original Turtle Trading Rules (available free online)

---

## 🚨 Important Disclaimers

1. **Past Performance ≠ Future Results**
2. **Always use proper position sizing**
3. **Test thoroughly before live trading**
4. **This is for educational purposes only**
5. **Consult a financial advisor before trading**

---

## ✨ Summary

The Donchian Breakout strategy is:
- ✅ **Simple** to understand and implement
- ✅ **Objective** with clear entry/exit rules
- ✅ **Proven** by the Turtle Traders' success
- ✅ **Effective** in trending markets
- ⚠️ **Requires discipline** during losing periods
- ⚠️ **Not suitable** for ranging markets

**Best Use Case:** Long-term trend following on liquid, large-cap stocks with your backtesting framework to find the best-performing variant for each stock!

---

*Happy Trading! 🚀*

