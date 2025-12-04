# Trade Levels Guide (Entry, Target, Stop Loss)

## Overview

The NSE backtesting system now displays **real-world trading levels** for each trade:
- **Entry Price**: Price at which you enter the trade
- **Target Price**: Take profit level (2:1 reward-to-risk ratio)
- **Stop Loss**: Exit level to limit losses (2% risk)
- **Exit Price**: Actual exit price achieved
- **Outcome**: Whether target was hit, stop was hit, or other exit

This helps you understand risk management and set realistic expectations for live trading.

---

## How Trade Levels are Calculated

### Default Settings
- **Risk per trade**: 2% of entry price
- **Reward-to-Risk Ratio**: 2:1 (4% target for 2% risk)

### For BUY Trades

```
Entry Price:   ₹1,000
Stop Loss:     ₹1,000 × (1 - 0.02) = ₹980   (-2%)
Target Price:  ₹1,000 × (1 + 0.04) = ₹1,040 (+4%)
```

### For SELL/SHORT Trades

```
Entry Price:   ₹1,000
Stop Loss:     ₹1,000 × (1 + 0.02) = ₹1,020 (+2%)
Target Price:  ₹1,000 × (1 - 0.04) = ₹960   (-4%)
```

---

## Trade Outcomes

The system categorizes each completed trade into one of three outcomes:

### 🎯 Target Hit
- Exit price reached or exceeded the target price
- Best case scenario - full profit realized
- Example: Entry ₹1,000, Target ₹1,040, Exit ₹1,045

### 🛑 Stop Hit  
- Exit price hit the stop loss level
- Loss was limited to predefined risk
- Example: Entry ₹1,000, Stop ₹980, Exit ₹975

### 📤 Other Exit
- Exited for reasons other than target/stop
- Could be profitable or loss
- Example: Strategy signal, end of test period, etc.

---

## Using Trade Levels in Real Trading

### Step 1: Entry Signal
When your backtest shows a BUY signal:
```
Entry Date: 2025-04-07
Entry Price: ₹1,161.06
```

**Action**: Place a buy order at or near ₹1,161

### Step 2: Set Stop Loss
```
Stop Loss: ₹1,137.84 (-2%)
```

**Action**: Place a stop-loss order at ₹1,138

### Step 3: Set Target
```
Target: ₹1,207.51 (+4%)
```

**Action**: Place a limit sell order at ₹1,207 (or use alerts)

### Step 4: Monitor
Track the trade and let your orders work automatically.

---

## Reading the Trade Details Report

### Example Output

```
Trade #2  🎯
─────────────────────────────────────────
Entry:  2025-04-07  @  ₹1,161.06
Target:                    ₹1,207.51  (+4.0%)
Stop:                      ₹1,137.84  (-2.0%)
Exit:   2025-04-21  @  ₹1,290.35  ✅
P&L:                       ₹  129.28  (+11.13%)
```

### What This Means

- **Entry Date**: April 7, 2025
- **Entry Price**: ₹1,161.06
- **Target**: ₹1,207.51 (profit target 4% above entry)
- **Stop**: ₹1,137.84 (stop loss 2% below entry)
- **Exit Date**: April 21, 2025 (14 days later)
- **Exit Price**: ₹1,290.35
- **Outcome**: 🎯 Target hit (and exceeded!)
- **P&L**: ₹129.28 profit = **11.13% return**

---

## Trade Statistics

At the bottom of each report, you'll see outcome distribution:

```
Trade Outcomes:
🎯 Target Hit: 1 (25.0%)    ← 25% of trades hit target
🛑 Stop Hit:   0 (0.0%)     ← 0% hit stop loss
📤 Other Exit: 3 (75.0%)    ← 75% exited for other reasons
```

### What to Look For

**Good Strategy Indicators:**
- High target hit rate (>30%)
- Low stop hit rate (<40%)
- Positive P&L on "Other Exit" trades
- Win rate > 50%

**Warning Signs:**
- High stop hit rate (>60%)
- Negative average P&L
- Win rate < 40%

---

## Running with Trade Levels

### Interactive Mode

```bash
python run_nse_backtest.py
```

Select any strategy, enter a stock symbol, and the report will automatically show trade levels.

### Test Script

```bash
python test_nse_with_levels.py
```

Quick test on RELIANCE stock to see trade levels in action.

---

## Customizing Risk Parameters

You can adjust risk/reward settings in `run_nse_backtest.py`:

```python
def calculate_trade_levels(entry_price, direction, 
                          risk_reward_ratio=2.0,  # Change this
                          risk_pct=0.02):          # Or this
```

### Examples

**Conservative (1.5:1 ratio, 1.5% risk)**
```python
risk_reward_ratio=1.5
risk_pct=0.015
```
- Stop: -1.5%
- Target: +2.25%

**Aggressive (3:1 ratio, 3% risk)**
```python
risk_reward_ratio=3.0
risk_pct=0.03
```
- Stop: -3%
- Target: +9%

---

## Real-World Application Example

### Scenario: Trading RELIANCE with RSI+BB Strategy

**1. Run Backtest**
```bash
python run_nse_backtest.py
# Choose: 1 (RSI + Bollinger Bands)
# Stock: RELIANCE
# Date range: Last 1 year
```

**2. Review Results**
```
Total Return:     16.07%
Total Trades:     4
Win Rate:         100.00%
```

**3. Check Latest Trade**
```
Trade #4
Entry:  2025-10-06  @  ₹1,375.00
Target:                ₹1,430.00  (+4.0%)
Stop:                  ₹1,347.50  (-2.0%)
```

**4. If Signal Occurs Today**
- **BUY**: ₹1,375
- **Set Stop Loss**: ₹1,347.50
- **Set Target**: ₹1,430
- **Risk**: ₹27.50 per share (2%)
- **Reward**: ₹55 per share (4%)

**5. Position Sizing (₹10,000 capital)**
- Capital at risk: ₹10,000 × 2% = ₹200
- Risk per share: ₹27.50
- Shares to buy: ₹200 ÷ ₹27.50 = **7 shares**
- Investment: 7 × ₹1,375 = ₹9,625

---

## Advanced: Trailing Stops

If a trade moves in your favor beyond the target:

**Example:**
```
Entry:   ₹1,000
Target:  ₹1,040 (hit!)
Current: ₹1,060
```

**Option 1**: Book profit at target (₹1,040)
**Option 2**: Trail stop to entry (₹1,000) - risk-free trade
**Option 3**: Trail stop to 2% below current (₹1,039)

---

## Comparing Strategies

When you use **Option 2** (Compare all strategies), you'll see trade levels for the best strategy:

```bash
python run_nse_backtest.py
# Choose: 2 (Compare all strategies)
# Stock: TCS
```

The system will:
1. Test all 13 strategies
2. Find the best performer
3. Show detailed trade levels for that strategy

---

## Tips for Live Trading

### ✅ Do's
1. **Always set stop loss** before entering
2. **Stick to the plan** - don't move stops against you
3. **Track actual vs backtest** - keep a trading journal
4. **Use proper position sizing** - risk only 1-2% per trade
5. **Consider slippage** - real prices may differ slightly

### ❌ Don'ts
1. **Don't skip the stop loss** - it protects your capital
2. **Don't chase trades** - wait for proper entry
3. **Don't overtrade** - quality > quantity
4. **Don't ignore commissions** - they add up
5. **Don't trade without backtest** - know your edge

---

## Understanding Risk:Reward Ratio

The 2:1 ratio means:

```
For every ₹100 you risk, you aim to make ₹200

Win Rate needed to breakeven: 33.3%
With 50% win rate: Expected return = +16.7%
With 60% win rate: Expected return = +40%
```

**Why 2:1 is popular:**
- Allows for win rate < 50%
- Realistic targets
- Good risk management
- Proven in many strategies

---

## Troubleshooting

### "No trades executed"
- Strategy didn't generate signals in this period
- Try longer date range or different stock
- Check if stock has enough volatility

### "All trades hit stop loss"
- Market conditions don't favor this strategy
- Consider different strategy or stock
- May need parameter optimization

### "Targets never hit"
- Risk:reward ratio may be too aggressive
- Try 1.5:1 or 1:1 ratio
- Check if stop loss is too tight

---

## Next Steps

1. **Backtest multiple stocks** to find best opportunities
2. **Compare strategies** to find what works for each stock
3. **Paper trade** first before using real money
4. **Track results** and compare with backtest
5. **Adjust parameters** based on your risk tolerance

---

## Support & Resources

- **Main Guide**: `README.md`
- **Strategy Guide**: `STRATEGIES_CHEATSHEET.md`
- **Quick Start**: `QUICK_START_NSE_STRATEGIES.md`
- **Example Scripts**: `examples/` directory

---

## Summary

Trade levels transform backtesting from theory to practice by showing:
- **Exact entry prices** from historical data
- **Calculated risk levels** (stop loss)
- **Profit targets** (take profit)
- **Actual outcomes** for each trade
- **Risk management** in action

This bridges the gap between backtesting and live trading, giving you actionable insights for real market execution.

---

**Happy Trading! 📈**

