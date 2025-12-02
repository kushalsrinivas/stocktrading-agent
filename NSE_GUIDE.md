# NSE Stock Trading Guide

This guide shows you how to backtest strategies on NSE (National Stock Exchange of India) stocks.

## Quick Start

### 1. Basic NSE Stock Backtest

```python
from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover

# Use .NS suffix for NSE stocks
data_handler = YFinanceDataHandler(
    symbol="RELIANCE.NS",  # Reliance Industries
    start_date="2020-01-01",
    end_date="2023-12-31"
)

strategy = MovingAverageCrossover(short_window=50, long_window=200)

backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=1000000,  # 10 Lakh INR
    commission=0.0005,  # 0.05% (typical Indian brokerage)
    slippage=0.0005
)

results = backtester.run()
backtester.plot_results()
```

### 2. Run NSE Examples

```bash
python examples/nse_example.py
```

## NSE Stock Ticker Format

All NSE stocks need the `.NS` suffix:

| Company | Symbol | Yahoo Finance Ticker |
|---------|--------|---------------------|
| Reliance Industries | RELIANCE | `RELIANCE.NS` |
| TCS | TCS | `TCS.NS` |
| Infosys | INFY | `INFY.NS` |
| HDFC Bank | HDFCBANK | `HDFCBANK.NS` |
| ICICI Bank | ICICIBANK | `ICICIBANK.NS` |
| ITC | ITC | `ITC.NS` |
| Wipro | WIPRO | `WIPRO.NS` |
| Bajaj Finance | BAJFINANCE | `BAJFINANCE.NS` |
| Maruti Suzuki | MARUTI | `MARUTI.NS` |
| Asian Paints | ASIANPAINT | `ASIANPAINT.NS` |
| Larsen & Toubro | LT | `LT.NS` |
| HCL Tech | HCLTECH | `HCLTECH.NS` |
| Axis Bank | AXISBANK | `AXISBANK.NS` |
| Bharti Airtel | BHARTIARTL | `BHARTIARTL.NS` |
| State Bank of India | SBIN | `SBIN.NS` |
| Titan Company | TITAN | `TITAN.NS` |
| UltraTech Cement | ULTRACEMCO | `ULTRACEMCO.NS` |
| Sun Pharma | SUNPHARMA | `SUNPHARMA.NS` |
| Tech Mahindra | TECHM | `TECHM.NS` |
| Tata Motors | TATAMOTORS | `TATAMOTORS.NS` |

## NSE-Specific Considerations

### 1. Initial Capital (in INR)

```python
backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=1000000,  # 10 Lakh INR
)
```

Common amounts:
- ₹1,00,000 (1 Lakh) - Small account
- ₹10,00,000 (10 Lakh) - Medium account
- ₹1,00,00,000 (1 Crore) - Large account

### 2. Commission Rates

Typical Indian brokerage rates:

```python
backtester = Backtester(
    # ...
    commission=0.0005,  # 0.05% - Discount brokers (Zerodha, Upstox)
    # commission=0.001,  # 0.1% - Traditional brokers
    # commission=0.0003, # 0.03% - Ultra-low cost
)
```

### 3. Market Hours

NSE trading hours: 9:15 AM to 3:30 PM IST (Monday-Friday)

When using daily data, this is automatically handled by Yahoo Finance.

### 4. Circuit Limits

NSE has circuit limits (typically ±10% or ±20% depending on stock). The backtest doesn't enforce these automatically, but be aware they exist in real trading.

## Popular NSE Indices

You can also backtest on indices:

| Index | Ticker |
|-------|--------|
| Nifty 50 | `^NSEI` |
| Sensex | `^BSESN` |
| Nifty Bank | `^NSEBANK` |
| Nifty IT | `^CNXIT` |
| Nifty Pharma | `^CNXPHARMA` |

Example:
```python
data_handler = YFinanceDataHandler(
    symbol="^NSEI",  # Nifty 50
    start_date="2020-01-01",
    end_date="2023-12-31"
)
```

## Example Use Cases

### 1. Test Strategy on Reliance

```python
from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover

data = YFinanceDataHandler("RELIANCE.NS", "2020-01-01", "2023-12-31")
strategy = MovingAverageCrossover(50, 200)
backtester = Backtester(data, strategy, 1000000, commission=0.0005)
results = backtester.run()
backtester.plot_results()
```

### 2. Compare Multiple NSE Stocks

```python
stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ITC"]

for stock in stocks:
    data = YFinanceDataHandler(f"{stock}.NS", "2020-01-01", "2023-12-31")
    backtester = Backtester(data, strategy, 1000000)
    results = backtester.run(verbose=False)
    print(f"{stock}: Return = {results['metrics']['Total Return (%)']:.2f}%")
```

### 3. Sector Analysis

```python
# IT Sector
it_stocks = ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"]

# Banking Sector
bank_stocks = ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS"]

# Auto Sector
auto_stocks = ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS"]
```

## Tips for NSE Trading

1. **Currency**: All values are in INR (Indian Rupees)
2. **Commission**: Use realistic commission rates (0.03% to 0.1%)
3. **Market Data**: Yahoo Finance provides NSE data with a slight delay
4. **Liquidity**: Focus on Nifty 50 stocks for better liquidity
5. **STT**: Consider Securities Transaction Tax (~0.025% on sell side)
6. **Holidays**: NSE has different holidays than US markets

## Finding NSE Stock Symbols

To find the correct symbol for an NSE stock:

1. Go to [Yahoo Finance](https://finance.yahoo.com/)
2. Search for the company name + "NSE"
3. The ticker will be shown as `SYMBOL.NS`

Or visit: https://www.nseindia.com/market-data/live-equity-market

## Advanced: Intraday Data

For intraday backtesting (if available):

```python
data_handler = YFinanceDataHandler(
    symbol="RELIANCE.NS",
    start_date="2023-11-01",
    end_date="2023-12-31",
    interval="5m"  # 5-minute candles
)
```

Available intervals:
- `1m`, `2m`, `5m`, `15m`, `30m`, `60m` (intraday)
- `1d` (daily - default)
- `1wk` (weekly)
- `1mo` (monthly)

**Note**: Intraday data has limited history (typically 7-60 days)

## Complete NSE Example

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover

# Backtest Reliance Industries
data = YFinanceDataHandler(
    symbol="RELIANCE.NS",
    start_date="2020-01-01",
    end_date="2023-12-31"
)

strategy = MovingAverageCrossover(short_window=50, long_window=200)

backtester = Backtester(
    data_handler=data,
    strategy=strategy,
    initial_capital=1000000,  # 10 Lakh INR
    commission=0.0005,  # 0.05%
    slippage=0.0005
)

results = backtester.run()

# Print results
print(f"\nInitial Capital: ₹{results['metrics']['Initial Value']:,.0f}")
print(f"Final Value: ₹{results['metrics']['Final Value']:,.0f}")
print(f"Total Return: {results['metrics']['Total Return (%)']:.2f}%")
print(f"Sharpe Ratio: {results['metrics']['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {results['metrics']['Max Drawdown (%)']:.2f}%")

backtester.plot_results()
```

## Troubleshooting

### Data Not Available
- Check if the ticker format is correct (include `.NS`)
- Verify the stock is listed on NSE
- Try a different date range

### No Trades Executed
- Reduce initial capital if stock price is high
- Check if strategy is generating signals
- Verify commission isn't eating all profits

### Performance Issues
- Use daily data instead of intraday for longer backtests
- Limit the date range
- Test on fewer stocks at once

## Further Resources

- NSE India: https://www.nseindia.com/
- Yahoo Finance: https://finance.yahoo.com/
- MoneyControl: https://www.moneycontrol.com/

---

Happy backtesting on NSE! 🇮🇳📈

