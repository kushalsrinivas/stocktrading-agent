# How to Run NSE Backtesting

## Quick Start

### 1. Activate Virtual Environment

```bash
cd /Users/kushalsrinivas/apps/stocktrading
source venv/bin/activate
```

### 2. Run the Interactive Script

```bash
python run_nse_backtest.py
```

### 3. Choose Your Mode

**Option 1: Test Single Strategy**
- Choose from 5 strategies
- Customize date range
- See detailed results and graphs

**Option 2: Compare All Strategies** ⭐ (Recommended!)
- Tests all 5 strategies automatically
- Fixed 1-year period from today
- Side-by-side comparison table
- Shows best performing strategy
- Option to view detailed graphs for winner

**Option 3: Show Popular Stocks**
- Lists common NSE stocks to test

### 4. Follow the Prompts

**For Option 1 (Single Strategy)**:
1. Choose a Strategy (1-5)
2. Enter Stock Symbol (e.g., `RELIANCE`, `TCS`)
3. Select Date Range (or use defaults)
4. View results and graphs

**For Option 2 (Compare All)** ⭐:
1. Enter Stock Symbol (e.g., `RELIANCE`, `TCS`)
2. Wait while all 5 strategies are tested
3. View comparison table
4. Optionally see detailed graphs for best strategy

## Example Session

```
$ python run_nse_backtest.py

======================================================================
   NSE STOCK BACKTESTING - MULTIPLE STRATEGIES
======================================================================

💰 Initial Capital: ₹10,000
📈 Commission: 0.05% (typical discount broker)
======================================================================

Options:
  1. Backtest a stock (choose strategy)
  2. Compare all strategies on a stock (1 year)
  3. Show popular NSE stocks
  4. Exit

Enter choice (1-4): 1

📊 Available Strategies:

   1. RSI + Bollinger Bands (Mean Reversion)
      • Buy: Price at lower BB + RSI oversold
      • Sell: Price at middle BB or RSI overbought

   2. Combined (RSI + MACD + Bollinger Bands)
      • Buy: All indicators confirm oversold
      • Sell: Any indicator signals overbought

   3. Moving Average Crossover
      • Buy: Fast MA crosses above slow MA
      • Sell: Fast MA crosses below slow MA

   4. RSI Momentum
      • Buy: RSI crosses above oversold level
      • Sell: RSI crosses above overbought level

   5. MACD Momentum
      • Buy: MACD crosses above signal line
      • Sell: MACD crosses below signal line

   Choose strategy (1-5): 1

📝 Enter NSE Stock Details:

Stock Symbol (e.g., RELIANCE, TCS, INFY): RELIANCE

📅 Date Range:
   Press Enter for default (last 2 years)
   Start Date (YYYY-MM-DD) [default: 2 years ago]: 
   End Date (YYYY-MM-DD) [default: today]: 

======================================================================
🔍 Fetching data for RELIANCE...
📊 Strategy: RSI + Bollinger Bands
======================================================================

Fetching data for RELIANCE.NS from 2022-12-03 to 2024-12-03...
Fetched 495 bars of data
⚙️  Running backtest...

[Results and graphs will be displayed]
```

### Option 2: Compare All Strategies (NEW! ⭐)

This mode automatically tests **all 5 strategies** on the same stock over the **last 1 year** and gives you a comprehensive comparison table!

```
Enter choice (1-4): 2

📝 Enter Stock Symbol to Compare All Strategies:

Stock Symbol (e.g., RELIANCE, TCS, INFY): TCS

======================================================================
🔄 COMPARING ALL STRATEGIES ON TCS
📅 Period: 2023-12-03 to 2024-12-03 (Last 1 Year)
======================================================================

✅ Data fetched successfully

Testing: RSI + Bollinger Bands...
--------------------------------------------------
✅ Completed - Return: 12.50%

Testing: Combined Strategy...
--------------------------------------------------
✅ Completed - Return: 8.30%

Testing: MA Crossover...
--------------------------------------------------
✅ Completed - Return: 15.20%

Testing: RSI Momentum...
--------------------------------------------------
✅ Completed - Return: 10.80%

Testing: MACD Momentum...
--------------------------------------------------
✅ Completed - Return: 11.40%

====================================================================================================
   STRATEGY COMPARISON FOR TCS
   Period: 2023-12-03 to 2024-12-03
   Initial Capital: ₹10,000
====================================================================================================

📊 PERFORMANCE SUMMARY:

                    Strategy  Total Return (%)  Sharpe Ratio  Max Drawdown (%)  ...
             MA Crossover               15.20          1.85            -12.30  ...
  RSI + Bollinger Bands               12.50          1.62             -8.50  ...
         MACD Momentum               11.40          1.45            -10.20  ...
          RSI Momentum               10.80          1.38             -9.80  ...
      Combined Strategy                8.30          1.15            -11.50  ...

====================================================================================================

🏆 HIGHLIGHTS:

   Best Return:        MA Crossover
                       15.20% return
                       Final Value: ₹11,520.00

   Best Risk-Adjusted: MA Crossover
                       Sharpe Ratio: 1.85

   Lowest Drawdown:    RSI + Bollinger Bands
                       Max Drawdown: -8.50%

   Most Active:        RSI Momentum
                       24 trades

====================================================================================================

💡 RECOMMENDATIONS:

   ✅ 5 out of 5 strategies were profitable

   Top 3 Strategies by Return:
   🥇 MA Crossover: 15.20% (Sharpe: 1.85)
   🥈 RSI + Bollinger Bands: 12.50% (Sharpe: 1.62)
   🥉 MACD Momentum: 11.40% (Sharpe: 1.45)

   📈 Average Trading Frequency: 18.4 trades/year

   ✅ 5 strategies have good risk-adjusted returns (Sharpe > 1)

====================================================================================================

📊 View detailed results for best strategy? (y/n): y

[Shows full backtest with graphs for the best performing strategy]
```


## Strategy Descriptions

### 1. RSI + Bollinger Bands ⭐ (Recommended for ₹10k)

**Best for**: Mean reversion trading, catching oversold bounces

**Entry Logic**:
- Price touches lower Bollinger Band (2 std dev)
- RSI confirms oversold condition (< 40)

**Exit Logic**:
- Price reaches middle Bollinger Band (take profit)
- OR RSI shows overbought (> 70)

**Good for**: Volatile stocks, short-term trades

---

### 2. Combined Strategy

**Best for**: Confirmation-based trading

**Entry Logic**:
- RSI oversold (< 30)
- MACD bullish crossover
- Price at lower Bollinger Band
- ALL conditions must be met

**Exit Logic**:
- ANY indicator shows sell signal

**Good for**: Conservative traders, lower frequency trades

---

### 3. Moving Average Crossover

**Best for**: Trend following

**Entry Logic**:
- 50-day MA crosses above 200-day MA (Golden Cross)

**Exit Logic**:
- 50-day MA crosses below 200-day MA (Death Cross)

**Good for**: Long-term trending stocks, less frequent trades

---

### 4. RSI Momentum

**Best for**: Momentum trading

**Entry Logic**:
- RSI crosses above 30 (oversold level)

**Exit Logic**:
- RSI crosses above 70 (overbought level)

**Good for**: Active trading, multiple signals

---

### 5. MACD Momentum

**Best for**: Trend confirmation

**Entry Logic**:
- MACD line crosses above signal line

**Exit Logic**:
- MACD line crosses below signal line

**Good for**: Medium-term trends

## Tips for ₹10,000 Capital

### 1. Choose Liquid Stocks
- Nifty 50 stocks are best
- Better execution, lower spreads

### 2. Consider Stock Price
- With ₹10k, you might only afford 1-2 shares of expensive stocks
- Consider mid-cap stocks for more flexibility

### 3. Commission Impact
- 0.05% commission on ₹10k = ₹5 per trade
- Avoid strategies with too many trades

### 4. Best Strategies for Small Capital
- **RSI + Bollinger Bands** - Good trade frequency
- **RSI Momentum** - Frequent signals
- Avoid MA Crossover (too infrequent for small capital)

## Popular NSE Stocks to Test

### Affordable (< ₹500/share)
- `ITC` - ₹400-450
- `SBIN` - ₹600-700
- `WIPRO` - ₹400-500
- `INFY` - ₹1400-1600

### Mid-Range (₹500-2000)
- `AXISBANK` - ₹1000-1200
- `ICICIBANK` - ₹900-1100
- `HDFCBANK` - ₹1500-1700

### High-Value (> ₹2000)
- `RELIANCE` - ₹2400-2800
- `TCS` - ₹3500-4000
- `BAJFINANCE` - ₹6000-7000

**Note**: With ₹10k capital and commission, you might only buy 1-3 shares of expensive stocks

## Understanding the Results

### Key Metrics

**Total Return (%)**: 
- Positive = Profit
- > 10% = Good
- > 20% = Excellent

**Sharpe Ratio**:
- > 1 = Good risk-adjusted returns
- > 2 = Excellent
- < 0 = Strategy lost money

**Max Drawdown (%)**:
- Maximum peak-to-trough decline
- Lower is better
- -20% means at worst, portfolio dropped 20%

**Win Rate (%)**:
- Percentage of profitable trades
- > 50% = More wins than losses
- < 50% = More losses (but can still be profitable if wins are big)

**Total Trades**:
- How many round trips (buy + sell)
- Too few (< 5) = Results not significant
- Too many (> 50) = High commission impact

## Troubleshooting

### No Trades Executed
**Problem**: Strategy shows 0 trades

**Solutions**:
1. Increase date range (try 3-5 years)
2. Try a different stock
3. Choose more active strategy (RSI Momentum, MACD)
4. Stock price might be too high for ₹10k

### Poor Performance
**Problem**: Negative returns

**Solutions**:
1. Not all stocks work with all strategies
2. Try different date ranges
3. Test multiple stocks
4. Some strategies work better in trending vs ranging markets

### "ModuleNotFoundError"
**Problem**: Can't import backtester

**Solutions**:
```bash
# Make sure you're in the right directory
cd /Users/kushalsrinivas/apps/stocktrading

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run from project root
python run_nse_backtest.py
```

## Next Steps

1. **Test Multiple Stocks**: Try the same strategy on 5-10 different stocks
2. **Compare Strategies**: Run all 5 strategies on your favorite stock
3. **Optimize Date Range**: Test different time periods
4. **Track Results**: Keep a log of which strategies work on which stocks
5. **Paper Trade**: Before real money, paper trade your best strategy

## Advanced Usage

### From Python Script

```python
from backtester import Backtester, YFinanceDataHandler
from strategies.rsi_bb_strategy import RSIBollingerStrategy

# Setup
data = YFinanceDataHandler("RELIANCE.NS", "2022-01-01", "2024-12-01")
strategy = RSIBollingerStrategy()

# Run
backtester = Backtester(data, strategy, initial_capital=10000, commission=0.0005)
results = backtester.run()
backtester.plot_results()

# Access metrics
print(f"Return: {results['metrics']['Total Return (%)']:.2f}%")
print(f"Sharpe: {results['metrics']['Sharpe Ratio']:.2f}")
```

## Why Use "Compare All Strategies" Mode? ⭐

### Benefits:

1. **Save Time**: Test all 5 strategies in one go (vs. running 5 times manually)
2. **Apples-to-Apples**: All strategies tested on exact same data period
3. **Clear Winner**: Instantly see which strategy works best for that stock
4. **Comprehensive View**: Compare return, Sharpe ratio, drawdown, win rate
5. **Smart Recommendations**: Get actionable insights automatically

### Best Use Cases:

✅ **Finding the right strategy for a stock**
- Test RELIANCE with all strategies
- See which one performs best
- Use that strategy going forward

✅ **Quick stock screening**
- Test multiple stocks one by one
- Find which stocks work well with these strategies
- Build a watchlist

✅ **Strategy validation**
- See if a strategy consistently performs
- Test on multiple stocks
- Build confidence before live trading

### Workflow Example:

```bash
# 1. Test TCS with all strategies
Choose option 2 → Enter "TCS" → See results

# 2. Test RELIANCE with all strategies
Choose option 2 → Enter "RELIANCE" → See results

# 3. Test INFY with all strategies
Choose option 2 → Enter "INFY" → See results

# Result: You now know which strategy works best for each stock!
```

### Reading the Comparison Table:

**Key Columns**:
- **Total Return (%)**: Higher is better (positive = profit)
- **Sharpe Ratio**: > 1 is good, > 2 is excellent
- **Max Drawdown (%)**: Closer to 0 is better (less negative)
- **Win Rate (%)**: > 50% means more wins than losses
- **Total Trades**: Frequency of trading

**🥇 Best Return**: Highest profit
**⚖️ Best Risk-Adjusted**: Best Sharpe ratio (profit per unit of risk)
**🛡️ Lowest Drawdown**: Most stable (smallest losses)
**📈 Most Active**: Most trades (good if you want action)

### Tips:

1. **Run comparison first** - See overview before diving deep
2. **View detailed graphs** - For best strategy only (saves time)
3. **Test multiple stocks** - See which strategies are consistent
4. **Note the date range** - 1 year is good for most strategies
5. **Check trade count** - < 5 trades may not be significant

---

**Happy Backtesting! 🇮🇳📈**

