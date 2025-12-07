# Quick Start Guide 🚀

Get started with the Stock Backtesting API in 5 minutes!

## 1. Install Dependencies

```bash
# If using virtual environment (recommended)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## 2. Start the Server

### Option A: Using the startup script (easiest)
```bash
./start_api.sh
```

### Option B: Using Python directly
```bash
python api_server.py
```

The server will start at `http://localhost:8000`

## 3. Test the API

### Option A: Using the test script
```bash
python test_api.py
```

### Option B: Using your browser
Open: http://localhost:8000/docs

### Option C: Using curl
```bash
# Health check
curl http://localhost:8000/health

# List strategies
curl http://localhost:8000/strategies

# Run a backtest
curl -X POST http://localhost:8000/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "RELIANCE",
    "strategy": "sr_all_in_one",
    "initial_capital": 10000
  }'
```

## 4. Run Examples

```bash
python api_client_example.py
```

This will walk you through:
- Listing all strategies
- Running a single backtest
- Comparing strategies
- Testing multiple tickers
- Finding the best strategy

## 5. Common Use Cases

### Test a Single Stock
```python
import requests

response = requests.post(
    "http://localhost:8000/backtest",
    json={
        "ticker": "RELIANCE",
        "strategy": "sr_all_in_one",
        "initial_capital": 10000
    }
)

result = response.json()
data = result['data']

print(f"Return: {data['metrics']['total_return_pct']:.2f}%")

# NEW! Access historical price data for charting
print(f"Price data points: {len(data['historical_data'])}")
print(f"Equity curve points: {len(data['equity_curve'])}")
```

### Create Charts (NEW! 📊)
```python
# The response now includes historical_data and equity_curve
# Perfect for creating charts in your application!

import matplotlib.pyplot as plt

# Plot price chart
dates = [d['date'] for d in data['historical_data']]
prices = [d['close'] for d in data['historical_data']]
plt.plot(dates, prices)
plt.title(f"{data['ticker']} Price")
plt.show()

# Plot equity curve
dates = [d['date'] for d in data['equity_curve']]
values = [d['value'] for d in data['equity_curve']]
plt.plot(dates, values)
plt.title("Portfolio Value Over Time")
plt.show()
```

### Web Charting Example
Open `chart_example.html` in your browser for a beautiful interactive charting demo!

### Find Best Strategy for a Stock
```python
response = requests.post(
    "http://localhost:8000/optimize",
    json={
        "ticker": "TCS",
        "metric": "total_return"
    }
)

result = response.json()
print(f"Best: {result['best_strategy']['name']}")
```

### Test Multiple Stocks
```python
response = requests.post(
    "http://localhost:8000/multi-ticker",
    json={
        "tickers": ["RELIANCE", "TCS", "INFY"],
        "strategy": "sr_all_in_one"
    }
)

result = response.json()
print(f"Average Return: {result['summary']['average_return_pct']:.2f}%")
```

## Top 5 Recommended Strategies

1. **sr_all_in_one** ⭐ - Best overall (4 confirmations)
2. **sr_rsi** 🔥 - Great for beginners
3. **sr_ema** 🔥 - Best for trending markets
4. **supertrend** - Excellent trend follower
5. **turtle_traders** - Classic hedge fund strategy

## Quick Tips

- ✅ Use `sr_all_in_one` if unsure which strategy to pick
- ✅ Test with at least 1 year of data for reliable results
- ✅ Compare multiple strategies before committing
- ✅ Check both return AND Sharpe ratio
- ⚠️ Ensure at least 10-20 trades for statistical significance

## API Endpoints Cheat Sheet

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if API is running |
| `/strategies` | GET | List all 22 strategies |
| `/backtest` | POST | Test 1 ticker + 1 strategy |
| `/compare` | POST | Compare strategies on 1 ticker |
| `/multi-ticker` | POST | Test multiple tickers |
| `/optimize` | POST | Find best strategy |

## Need Help?

- **Interactive Docs**: http://localhost:8000/docs
- **Full Documentation**: See `API_README.md`
- **Example Code**: See `api_client_example.py`
- **Postman Collection**: Import `postman_collection.json`

## Troubleshooting

### "Connection refused"
→ Server not running. Run: `python api_server.py`

### "No data available"
→ Check ticker symbol (use NSE symbols like RELIANCE, TCS)

### "No signals generated"
→ Try longer date range or different stock

---

**That's it! You're ready to backtest. Happy trading! 📈**

