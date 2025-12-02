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

### 3. Follow the Prompts

The script will guide you through:

1. **Choose a Strategy** (5 options):
   - RSI + Bollinger Bands (Mean Reversion)
   - Combined (RSI + MACD + BB)
   - Moving Average Crossover
   - RSI Momentum
   - MACD Momentum

2. **Enter Stock Symbol**:
   - Just the symbol (e.g., `RELIANCE`, `TCS`, `INFY`)
   - No need to add `.NS` - it's added automatically

3. **Select Date Range**:
   - Press Enter for defaults (last 2 years)
   - Or specify custom dates (YYYY-MM-DD format)

4. **View Results**:
   - Performance metrics printed to terminal
   - Beautiful graphs showing equity curve, drawdown, and trades

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
  1. Backtest a stock
  2. Show popular NSE stocks
  3. Exit

Enter choice (1-3): 1

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

---

**Happy Backtesting! 🇮🇳📈**

