# Quick Reference Guide

## Project Structure

```
stocktrading/
├── backtester/          # Core backtesting engine
│   ├── engine.py        # Main backtesting orchestrator
│   ├── strategy.py      # Base strategy class
│   ├── data_handler.py  # Data fetching (yfinance)
│   ├── portfolio.py     # Portfolio & order management
│   ├── metrics.py       # Performance calculations
│   └── visualizer.py    # Plotting utilities
├── strategies/          # Trading strategies
│   ├── ma_crossover.py  # Moving average strategies
│   ├── momentum.py      # Momentum strategies (RSI, MACD, ROC)
│   └── mean_reversion.py # Mean reversion strategies
├── examples/            # Example scripts
│   ├── simple_example.py    # Quickstart
│   └── run_backtest.py      # Full examples & comparison
└── requirements.txt     # Python dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## Minimal Example

```python
from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover

data_handler = YFinanceDataHandler("AAPL", "2022-01-01", "2023-12-31")
strategy = MovingAverageCrossover(short_window=50, long_window=200)
backtester = Backtester(data_handler, strategy, initial_capital=100000)
results = backtester.run()
backtester.plot_results()
```

## Available Strategies

| Strategy | Import | Key Parameters |
|----------|--------|----------------|
| MA Crossover | `from strategies import MovingAverageCrossover` | `short_window=50, long_window=200` |
| EMA Crossover | `from strategies.ma_crossover import ExponentialMovingAverageCrossover` | `short_window=12, long_window=26` |
| RSI | `from strategies.momentum import RSIMomentumStrategy` | `period=14, oversold=30, overbought=70` |
| MACD | `from strategies.momentum import MACDMomentumStrategy` | `fast=12, slow=26, signal=9` |
| ROC | `from strategies.momentum import MomentumStrategy` | `period=20, buy_threshold=5, sell_threshold=-5` |
| Bollinger | `from strategies import MeanReversionStrategy` | `period=20, num_std=2.0` |
| Z-Score | `from strategies.mean_reversion import ZScoreMeanReversion` | `period=20, buy_threshold=-2, sell_threshold=2` |
| Percentile | `from strategies.mean_reversion import PercentileReversion` | `period=20, buy_percentile=20, sell_percentile=80` |

## Key Classes & Methods

### Backtester
```python
backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=100000,
    commission=0.001,      # 0.1% per trade
    slippage=0.0005        # 0.05% slippage
)

results = backtester.run(verbose=True)
backtester.plot_results()
metrics = backtester.get_metrics()
```

### YFinanceDataHandler
```python
data_handler = YFinanceDataHandler(
    symbol="AAPL",
    start_date="2020-01-01",
    end_date="2023-12-31",
    interval="1d"  # '1d', '1h', '1wk', etc.
)

data = data_handler.get_data()
price = data_handler.get_latest_price()
```

### Strategy Base Class
```python
class MyStrategy(Strategy):
    def __init__(self, param1):
        super().__init__()
        self.param1 = param1
        self.parameters = {'param1': param1}
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0  # 1=buy, -1=sell, 0=hold
        
        # Optional columns:
        # signals['limit_price'] = ...
        # signals['stop_price'] = ...
        # signals['quantity'] = ...
        
        return signals
```

## Performance Metrics

| Metric | Description | Good Value |
|--------|-------------|------------|
| Total Return (%) | Overall gain/loss | Positive |
| Sharpe Ratio | Risk-adjusted return | > 1 (good), > 2 (excellent) |
| Max Drawdown (%) | Largest decline | Smaller is better |
| Volatility (%) | Return variability | Depends on risk tolerance |
| Win Rate (%) | Profitable trades % | > 50% |
| Profit Factor | Gross profit / loss | > 1 |

## Data Format

Input data (from `data_handler.get_data()`):
```
DatetimeIndex | Open | High | Low | Close | Volume
```

Output signals (from `strategy.generate_signals()`):
```
DatetimeIndex | signal | [limit_price] | [stop_price] | [quantity]
```

## Order Types

### Market Order (Default)
```python
signals['signal'] = 1  # Executed at current market price
```

### Limit Order
```python
signals['signal'] = 1
signals['limit_price'] = current_price * 0.95  # Buy at 5% discount
```

### Stop Loss
```python
signals['signal'] = -1
signals['stop_price'] = current_price * 0.90  # Sell if drops 10%
```

## Common Patterns

### Test Multiple Symbols
```python
symbols = ["AAPL", "MSFT", "GOOGL"]
for symbol in symbols:
    data_handler = YFinanceDataHandler(symbol, start_date, end_date)
    backtester = Backtester(data_handler, strategy, 100000)
    results = backtester.run()
```

### Parameter Optimization
```python
best_sharpe = -999
best_params = None

for short in range(10, 51, 10):
    for long in range(100, 201, 20):
        strategy = MovingAverageCrossover(short, long)
        backtester = Backtester(data_handler, strategy, 100000)
        results = backtester.run(verbose=False)
        
        if results['metrics']['Sharpe Ratio'] > best_sharpe:
            best_sharpe = results['metrics']['Sharpe Ratio']
            best_params = (short, long)

print(f"Best: short={best_params[0]}, long={best_params[1]}, Sharpe={best_sharpe:.2f}")
```

### Access Trade History
```python
results = backtester.run()
trades = results['trade_history']
print(trades)  # DataFrame with timestamp, direction, quantity, price, value
```

### Access Equity Curve
```python
equity = results['equity_curve']
print(equity)  # DataFrame with timestamp and portfolio value
```

## Visualization Options

```python
# All plots at once
backtester.plot_results()

# Individual plots
from backtester.visualizer import Visualizer
viz = Visualizer(results)
viz.plot_equity_curve()
viz.plot_drawdown()
viz.plot_trades()
viz.plot_returns_distribution()
viz.plot_all()  # Comprehensive dashboard
```

## Tips

1. **Start Simple**: Use `examples/simple_example.py` first
2. **Check Signals**: Print `results['signals']` to debug
3. **Realistic Parameters**: Include commission and slippage
4. **Enough Data**: Ensure date range covers indicator periods
5. **Compare Strategies**: Use `compare_strategies()` function

## Run Examples

```bash
# Simple quickstart
python examples/simple_example.py

# Full examples with strategy comparison
python examples/run_backtest.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No trades executed | Check if signals are generated, verify sufficient capital |
| Import errors | Ensure virtual env is activated and packages installed |
| Indicator errors | Increase date range to provide enough lookback data |
| Poor performance | Try different parameters, check market conditions |

## Further Reading

- `README.md` - Project overview and architecture
- `GETTING_STARTED.md` - Detailed tutorial
- Code docstrings - API documentation
- `examples/` - Working code examples

