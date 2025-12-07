# Charting Guide 📊

The API now returns historical price data and equity curve data, making it easy to create beautiful charts in your application!

## What's New

The `/backtest` endpoint now returns two additional fields:

### 1. `historical_data` - OHLCV Price Data
Complete historical price data for the backtesting period:

```json
{
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
  ]
}
```

Perfect for:
- 📈 Line charts (close prices)
- 🕯️ Candlestick charts
- 📊 OHLC bar charts
- 📉 Volume charts

### 2. `equity_curve` - Portfolio Performance
Portfolio value at each date during the backtest:

```json
{
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
  ]
}
```

Perfect for:
- 💰 Portfolio value charts
- 📈 Performance comparison
- 📊 Drawdown visualization

## Quick Example

### Python with Matplotlib

```python
import requests
import matplotlib.pyplot as plt

# Run backtest
response = requests.post("http://localhost:8000/backtest", json={
    "ticker": "RELIANCE",
    "strategy": "sr_all_in_one"
})

data = response.json()['data']

# Plot price chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Price chart
dates = [d['date'] for d in data['historical_data']]
closes = [d['close'] for d in data['historical_data']]
ax1.plot(dates, closes, label='Close Price', linewidth=2)
ax1.set_title(f"{data['ticker']} Price Chart")
ax1.set_ylabel('Price (₹)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Equity curve
eq_dates = [d['date'] for d in data['equity_curve']]
eq_values = [d['value'] for d in data['equity_curve']]
ax2.plot(eq_dates, eq_values, label='Portfolio Value', linewidth=2, color='green')
ax2.axhline(y=data['metrics']['initial_capital'], color='red', linestyle='--', label='Initial Capital')
ax2.set_title('Portfolio Performance')
ax2.set_ylabel('Value (₹)')
ax2.set_xlabel('Date')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### JavaScript with Chart.js

```javascript
// Run backtest
const response = await fetch('http://localhost:8000/backtest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ticker: 'RELIANCE',
    strategy: 'sr_all_in_one'
  })
});

const result = await response.json();
const data = result.data;

// Create price chart
const priceChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: data.historical_data.map(d => d.date),
    datasets: [{
      label: 'Close Price',
      data: data.historical_data.map(d => d.close),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        ticks: {
          callback: value => '₹' + value.toLocaleString()
        }
      }
    }
  }
});

// Create equity curve chart
const equityChart = new Chart(ctx2, {
  type: 'line',
  data: {
    labels: data.equity_curve.map(d => d.date),
    datasets: [{
      label: 'Portfolio Value',
      data: data.equity_curve.map(d => d.value),
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      fill: true
    }]
  }
});
```

### React Example

```jsx
import { Line } from 'react-chartjs-2';
import { useState, useEffect } from 'react';

function BacktestChart({ ticker, strategy }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/backtest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, strategy })
    })
      .then(res => res.json())
      .then(result => {
        const data = result.data;
        
        setChartData({
          labels: data.historical_data.map(d => d.date),
          datasets: [{
            label: 'Price',
            data: data.historical_data.map(d => d.close),
            borderColor: 'rgb(75, 192, 192)'
          }, {
            label: 'Portfolio',
            data: data.equity_curve.map(d => d.value),
            borderColor: 'rgb(54, 162, 235)',
            yAxisID: 'y1'
          }]
        });
      });
  }, [ticker, strategy]);

  if (!chartData) return <div>Loading...</div>;

  return <Line data={chartData} />;
}
```

## Interactive Demo

Open `chart_example.html` in your browser to see a fully functional charting demo with:

- ✅ Real-time backtesting
- ✅ Price chart
- ✅ Equity curve chart
- ✅ Combined comparison chart
- ✅ Performance metrics display
- ✅ Interactive controls

```bash
# Open in browser
open chart_example.html
# or
python -m http.server 8080
# then visit http://localhost:8080/chart_example.html
```

## Advanced Charting

### Candlestick Chart (Plotly.js)

```javascript
const candlestick = {
  x: data.historical_data.map(d => d.date),
  open: data.historical_data.map(d => d.open),
  high: data.historical_data.map(d => d.high),
  low: data.historical_data.map(d => d.low),
  close: data.historical_data.map(d => d.close),
  type: 'candlestick',
  name: 'Price'
};

Plotly.newPlot('chart', [candlestick]);
```

### Volume Chart

```javascript
const volumeChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: data.historical_data.map(d => d.date),
    datasets: [{
      label: 'Volume',
      data: data.historical_data.map(d => d.volume),
      backgroundColor: 'rgba(54, 162, 235, 0.5)'
    }]
  }
});
```

### Drawdown Chart

```python
import numpy as np

# Calculate drawdown
equity = [d['value'] for d in data['equity_curve']]
running_max = np.maximum.accumulate(equity)
drawdown = [(e - m) / m * 100 for e, m in zip(equity, running_max)]

plt.plot(eq_dates, drawdown, color='red')
plt.fill_between(eq_dates, 0, drawdown, alpha=0.3, color='red')
plt.title('Drawdown Chart')
plt.ylabel('Drawdown (%)')
plt.grid(True)
```

### Comparison Chart (Strategy vs Buy & Hold)

```python
# Calculate buy & hold performance
initial_price = data['historical_data'][0]['close']
buy_hold = [(d['close'] / initial_price) * data['metrics']['initial_capital'] 
            for d in data['historical_data']]

# Plot comparison
plt.plot(dates, buy_hold, label='Buy & Hold', linestyle='--')
plt.plot(eq_dates, eq_values, label=f"Strategy ({data['strategy']})")
plt.title('Strategy vs Buy & Hold')
plt.legend()
plt.grid(True)
```

## Chart Libraries

### Recommended Libraries

**Python:**
- 📊 **Matplotlib** - Standard plotting library
- 📈 **Plotly** - Interactive charts
- 🎨 **Seaborn** - Statistical visualizations
- 💹 **mplfinance** - Financial charts

**JavaScript:**
- 📊 **Chart.js** - Simple and flexible
- 📈 **Plotly.js** - Interactive and feature-rich
- 📉 **Highcharts** - Professional charts
- 💹 **TradingView** - Advanced financial charts
- 🎨 **D3.js** - Custom visualizations

**React:**
- react-chartjs-2
- recharts
- victory
- nivo

## Data Format Reference

### Historical Data Fields
| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Trading date (YYYY-MM-DD) |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | int | Trading volume |

### Equity Curve Fields
| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date (YYYY-MM-DD) |
| `value` | float | Portfolio value (₹) |

## Best Practices

### 1. Data Sampling for Large Datasets
```python
# If you have too many data points, sample them
if len(data['historical_data']) > 500:
    # Sample every nth point
    n = len(data['historical_data']) // 500
    sampled_data = data['historical_data'][::n]
```

### 2. Date Formatting
```javascript
// Format dates for better display
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-IN', { 
    month: 'short', 
    day: 'numeric' 
  });
};
```

### 3. Responsive Charts
```javascript
// Make charts responsive
const options = {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 2
};
```

### 4. Performance Optimization
```javascript
// Limit data points for better performance
const maxPoints = 1000;
if (data.historical_data.length > maxPoints) {
  const step = Math.ceil(data.historical_data.length / maxPoints);
  data.historical_data = data.historical_data.filter((_, i) => i % step === 0);
}
```

## Troubleshooting

### Issue: Charts not rendering
**Solution:** Ensure Chart.js or your charting library is loaded:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### Issue: Dates not displaying correctly
**Solution:** Format dates properly:
```javascript
labels: data.historical_data.map(d => new Date(d.date))
```

### Issue: Too many data points
**Solution:** Sample or aggregate the data:
```python
# Weekly aggregation
df = pd.DataFrame(data['historical_data'])
df['date'] = pd.to_datetime(df['date'])
weekly = df.set_index('date').resample('W').last()
```

## Next Steps

1. ✅ Try the `chart_example.html` demo
2. ✅ Integrate charting into your application
3. ✅ Customize chart styles to match your brand
4. ✅ Add interactivity (tooltips, zoom, pan)
5. ✅ Export charts as images for reports

## Resources

- **Chart.js Docs**: https://www.chartjs.org/docs/
- **Plotly Python**: https://plotly.com/python/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
- **TradingView**: https://www.tradingview.com/lightweight-charts/

---

**Happy Charting! 📊🎨**

