# Stock Backtesting API 📈

A FastAPI-based REST API for backtesting NSE stocks with 22+ trading strategies.

## Features

- 🚀 **22 Trading Strategies** including classic, advanced, and institutional-grade strategies
- 🔥 **Advanced S/R Strategies** with multiple confirmations (RSI, Volume, EMA, MACD)
- 📊 **Multiple Endpoints** for single/multi-ticker testing, strategy comparison, and optimization
- ⚡ **Fast & Async** powered by FastAPI and uvicorn
- 📖 **Interactive Docs** via Swagger UI at `/docs`
- 🔌 **Easy Integration** with any client (Python, JavaScript, curl, etc.)

## Quick Start

### 1. Start the API Server

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn

# Start server
python api_server.py
```

The server will start at `http://localhost:8000`

### 2. Access Interactive Documentation

Open your browser and visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test with Example Client

```bash
python api_client_example.py
```

## API Endpoints

### 1. **GET /** - Root

Get API information and available endpoints.

```bash
curl http://localhost:8000/
```

### 2. **GET /health** - Health Check

Check if the API is running.

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "timestamp": "2024-12-07T10:30:00"
}
```

### 3. **GET /strategies** - List All Strategies

Get information about all 22 available strategies.

```bash
curl http://localhost:8000/strategies
```

Response:

```json
{
  "total_strategies": 22,
  "strategies": {
    "sr_all_in_one": {
      "name": "S/R All-in-One COMBO",
      "type": "Institutional",
      "description": "⭐ 4 confirmations: S/R + RSI + EMA + Volume"
    },
    ...
  }
}
```

### 4. **POST /backtest** - Single Ticker Backtest

Run backtest for one ticker with one strategy.

```bash
curl -X POST http://localhost:8000/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "RELIANCE",
    "strategy": "sr_all_in_one",
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "initial_capital": 10000
  }'
```

Response:

```json
{
  "status": "success",
  "data": {
    "ticker": "RELIANCE",
    "strategy": "sr_all_in_one",
    "period": {
      "start_date": "2023-01-01",
      "end_date": "2024-12-31"
    },
    "metrics": {
      "initial_capital": 10000.0,
      "final_value": 12500.75,
      "total_return_pct": 25.01,
      "total_trades": 15,
      "win_rate_pct": 66.67,
      "profit_factor": 2.34,
      "sharpe_ratio": 1.85,
      "max_drawdown_pct": -8.5,
      "volatility_pct": 18.2
    },
    "historical_data": [
      {
        "date": "2023-01-01",
        "open": 2500.0,
        "high": 2550.0,
        "low": 2480.0,
        "close": 2530.0,
        "volume": 1500000
      },
      ...
    ],
    "equity_curve": [
      {
        "date": "2023-01-01",
        "value": 10000.0
      },
      {
        "date": "2023-01-02",
        "value": 10150.0
      },
      ...
    ],
    "trades": [...]
  }
}
```

### 5. **POST /compare** - Compare Strategies

Compare multiple strategies on a single ticker.

```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "TCS",
    "strategies": ["sr_all_in_one", "sr_rsi", "supertrend"],
    "start_date": "2023-01-01",
    "end_date": "2024-12-31"
  }'
```

Response:

```json
{
  "status": "success",
  "ticker": "TCS",
  "total_strategies_tested": 3,
  "best_strategy": {
    "name": "sr_all_in_one",
    "total_return_pct": 28.5,
    "sharpe_ratio": 2.1,
    "win_rate_pct": 70.0
  },
  "results": [...]
}
```

### 6. **POST /multi-ticker** - Test Multiple Tickers

Test multiple tickers with one strategy.

```bash
curl -X POST http://localhost:8000/multi-ticker \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["RELIANCE", "TCS", "INFY"],
    "strategy": "sr_all_in_one",
    "start_date": "2023-01-01",
    "end_date": "2024-12-31"
  }'
```

Response:

```json
{
  "status": "success",
  "strategy": "sr_all_in_one",
  "summary": {
    "total_tickers_tested": 3,
    "average_return_pct": 22.5,
    "median_return_pct": 21.0,
    "best_ticker": {
      "ticker": "TCS",
      "return_pct": 28.5
    }
  },
  "results": [...]
}
```

### 7. **POST /optimize** - Find Best Strategy

Find the best strategy for a ticker based on a metric.

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "INFY",
    "metric": "total_return",
    "start_date": "2023-01-01",
    "end_date": "2024-12-31"
  }'
```

Response:

```json
{
  "status": "success",
  "ticker": "INFY",
  "optimization_metric": "total_return",
  "best_strategy": {
    "name": "sr_all_in_one",
    "metrics": {...}
  },
  "top_5_strategies": [...]
}
```

## Available Strategies

### Classic Strategies

1. **rsi_bb** - RSI + Bollinger Bands (Mean Reversion)
2. **combined** - Combined Strategy (RSI + MACD + BB)
3. **ma_crossover** - Moving Average Crossover
4. **rsi_momentum** - RSI Momentum
5. **macd_momentum** - MACD Momentum

### Advanced Strategies

6. **stochastic_breakout** - Stochastic Breakout (Momentum)
7. **vwap_reversal** - VWAP Reversal (Mean Reversion)
8. **supertrend** - Supertrend Momentum (Trend Following)
9. **keltner_squeeze** - Keltner Squeeze (Breakout)
10. **williams_trend** - Williams Trend (Momentum)

### Donchian Strategies

11. **donchian_breakout** - Donchian Breakout (Classic)
12. **donchian_fast** - Donchian Fast (Aggressive)
13. **turtle_traders** - Turtle Traders (Original System)

### Trend Line & S/R Strategies

14. **trendline_bounce** - Trend Line Bounce
15. **trendline_breakout** - Trend Line Breakout
16. **sr_bounce** - Support/Resistance Bounce
17. **sr_breakout** - Support/Resistance Breakout

### Advanced S/R Strategies 🔥

18. **sr_rsi** - S/R + RSI (Momentum Confirmation) 🔥
19. **sr_volume** - S/R + Volume (Breakout Strength) 🔥
20. **sr_ema** - S/R + EMA (Trend Filter) 🔥
21. **sr_macd** - S/R + MACD (Trend Reversal) 🔥
22. **sr_all_in_one** - S/R All-in-One COMBO (Institutional) ⭐

## Python Client Usage

```python
import requests

# Single backtest
response = requests.post(
    "http://localhost:8000/backtest",
    json={
        "ticker": "RELIANCE",
        "strategy": "sr_all_in_one",
        "start_date": "2023-01-01",
        "end_date": "2024-12-31",
        "initial_capital": 10000
    }
)

result = response.json()
print(f"Total Return: {result['data']['metrics']['total_return_pct']:.2f}%")
```

### Using the Client Class

```python
from api_client_example import BacktestAPIClient

client = BacktestAPIClient()

# Single backtest
result = client.backtest_single(
    ticker="RELIANCE",
    strategy="sr_all_in_one",
    initial_capital=10000
)

# Compare strategies
comparison = client.compare_strategies(
    ticker="TCS",
    strategies=["sr_all_in_one", "sr_rsi", "supertrend"]
)

# Test multiple tickers
multi_result = client.test_multi_ticker(
    tickers=["RELIANCE", "TCS", "INFY"],
    strategy="sr_all_in_one"
)

# Find best strategy
best = client.optimize(
    ticker="INFY",
    metric="total_return"
)
```

## JavaScript/TypeScript Usage

### Basic Usage
```javascript
// Single backtest
const response = await fetch("http://localhost:8000/backtest", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    ticker: "RELIANCE",
    strategy: "sr_all_in_one",
    start_date: "2023-01-01",
    end_date: "2024-12-31",
    initial_capital: 10000,
  }),
});

const result = await response.json();
console.log(`Total Return: ${result.data.metrics.total_return_pct}%`);
```

### Charting Example (with Chart.js)
```javascript
// Run backtest
const response = await fetch("http://localhost:8000/backtest", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    ticker: "RELIANCE",
    strategy: "sr_all_in_one",
  }),
});

const result = await response.json();
const data = result.data;

// Create price chart
const priceChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: data.historical_data.map((d) => d.date),
    datasets: [
      {
        label: "Close Price",
        data: data.historical_data.map((d) => d.close),
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  },
});

// Create equity curve chart
const equityChart = new Chart(ctx2, {
  type: "line",
  data: {
    labels: data.equity_curve.map((d) => d.date),
    datasets: [
      {
        label: "Portfolio Value",
        data: data.equity_curve.map((d) => d.value),
        borderColor: "rgb(54, 162, 235)",
        fill: true,
      },
    ],
  },
});

// Create candlestick chart (with plotly.js)
const candlestick = {
  x: data.historical_data.map((d) => d.date),
  open: data.historical_data.map((d) => d.open),
  high: data.historical_data.map((d) => d.high),
  low: data.historical_data.map((d) => d.low),
  close: data.historical_data.map((d) => d.close),
  type: "candlestick",
};

Plotly.newPlot("chart", [candlestick]);
```

## Request Parameters

### Common Parameters

| Parameter         | Type   | Required | Default     | Description                            |
| ----------------- | ------ | -------- | ----------- | -------------------------------------- |
| `ticker`          | string | Yes      | -           | Stock symbol (e.g., "RELIANCE", "TCS") |
| `strategy`        | string | Yes      | -           | Strategy name (see list above)         |
| `start_date`      | string | No       | 2 years ago | Start date (YYYY-MM-DD)                |
| `end_date`        | string | No       | today       | End date (YYYY-MM-DD)                  |
| `initial_capital` | float  | No       | 10000       | Initial capital in INR                 |
| `commission`      | float  | No       | 0.0005      | Commission (0.0005 = 0.05%)            |

### Optimization Metrics

- `total_return` - Maximize total return percentage
- `sharpe_ratio` - Maximize risk-adjusted returns
- `win_rate` - Maximize win rate percentage

## Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    "ticker": "RELIANCE",
    "strategy": "sr_all_in_one",
    "period": {
      "start_date": "2023-01-01",
      "end_date": "2024-12-31"
    },
    "metrics": {
      "initial_capital": 10000.0,
      "final_value": 12500.75,
      "total_return_pct": 25.01,
      "total_trades": 15,
      "win_rate_pct": 66.67,
      "profit_factor": 2.34,
      "sharpe_ratio": 1.85,
      "max_drawdown_pct": -8.5,
      "volatility_pct": 18.2
    },
    "trades": [...]
  }
}
```

### Error Response

```json
{
  "detail": "Error message here"
}
```

## Response Data Fields

### Metrics
- **Total Return (%)**: Overall return on investment
- **Sharpe Ratio**: Risk-adjusted return (>1 is good, >2 is excellent)
- **Win Rate (%)**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss (>1 is profitable)
- **Max Drawdown (%)**: Largest peak-to-trough decline
- **Volatility (%)**: Standard deviation of returns
- **Total Trades**: Number of completed trades

### Historical Data (NEW! 📊)
Array of OHLCV data for the entire backtesting period:
- **date**: Trading date (YYYY-MM-DD)
- **open**: Opening price
- **high**: Highest price
- **low**: Lowest price
- **close**: Closing price
- **volume**: Trading volume

Perfect for creating candlestick charts, line charts, or any price visualization!

### Equity Curve (NEW! 📈)
Array showing portfolio value over time:
- **date**: Trading date (YYYY-MM-DD)
- **value**: Portfolio value at that date

Use this to visualize your strategy's performance over time!

### Trades
Array of executed trades with entry/exit details (limited to 50 most recent)

## Best Practices

### 1. Use Appropriate Date Ranges

- **Short-term (Swing)**: 3-6 months
- **Medium-term**: 1-2 years (default)
- **Long-term**: 3-5 years

### 2. Strategy Selection

- **Trending Markets**: Use trend-following strategies (Supertrend, Donchian, Turtle Traders)
- **Ranging Markets**: Use mean reversion strategies (RSI + BB, VWAP Reversal)
- **Unknown Conditions**: Use S/R All-in-One COMBO (works in all conditions)

### 3. Optimization

- Always test multiple strategies before choosing one
- Use the `/optimize` endpoint to find the best strategy
- Consider both return AND risk (Sharpe Ratio)

### 4. Commission & Slippage

- Default commission: 0.05% (typical discount broker)
- Adjust based on your broker's actual charges
- Higher commission = lower returns

## Performance Tips

### For Faster Results

- Test with shorter date ranges first
- Use specific strategy lists in `/compare` instead of testing all
- Cache results for frequently tested tickers

### For Better Accuracy

- Use at least 1 year of data
- Ensure sufficient trades (>20) for statistical significance
- Test in both bull and bear market periods

## Error Handling

Common errors and solutions:

### "No data available"

- Check if the ticker symbol is correct
- NSE stocks need `.NS` suffix (automatically added by API)
- Verify date range is valid

### "Strategy didn't generate signals"

- Try a longer date range
- Consider different stocks with more volatility
- Adjust strategy parameters

### Connection Refused

- Ensure API server is running: `python api_server.py`
- Check firewall settings
- Verify port 8000 is available

## Advanced Usage

### Custom Parameters

To use custom strategy parameters, you'll need to modify the `create_strategy()` function in `api_server.py`.

### Batch Processing

For processing many tickers, use the `/multi-ticker` endpoint or make parallel requests:

```python
import concurrent.futures

tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(client.backtest_single, ticker, "sr_all_in_one")
        for ticker in tickers
    ]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
```

## Deployment

### Production Deployment

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

To add new strategies:

1. Create strategy class in `strategies/` directory
2. Add to `create_strategy()` function in `api_server.py`
3. Add to `StrategyEnum` enum
4. Update strategy info in `/strategies` endpoint

## Support

For issues or questions:

- Check the interactive docs at `/docs`
- Review example code in `api_client_example.py`
- Ensure all dependencies are installed

## License

Same as the main project.

---

**Happy Backtesting! 📈🚀**
