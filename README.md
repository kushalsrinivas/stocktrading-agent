# Stock Trading Backtesting Framework

A simple and modular Python framework for backtesting trading strategies on stock data.

## Features

- 📊 Free historical data via yfinance
- 🇮🇳 **NSE Stock Support** - Backtest Indian stocks (see `NSE_GUIDE.md`)
- 🇺🇸 US Stock Support - Works with any Yahoo Finance ticker
- 🎯 Support for multiple order types (market, limit, stop loss)
- 📈 Built-in performance metrics (total return, Sharpe ratio, max drawdown, etc.)
- 🔧 Modular strategy interface - easily create and test your own strategies
- 📉 Visualization of equity curves and performance
- 💡 Example strategies included (MA crossover, momentum, mean reversion)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from backtester.engine import Backtester
from backtester.data_handler import YFinanceDataHandler
from strategies.ma_crossover import MovingAverageCrossover

# Load data (works with US stocks and NSE stocks)
data_handler = YFinanceDataHandler("AAPL", "2020-01-01", "2023-12-31")
# For NSE: YFinanceDataHandler("RELIANCE.NS", "2020-01-01", "2023-12-31")

# Create strategy
strategy = MovingAverageCrossover(short_window=50, long_window=200)

# Run backtest
backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=100000
)

results = backtester.run()
print(results)

# Visualize
backtester.plot_results()
```

## Project Structure

```
stocktrading/
├── backtester/
│   ├── engine.py           # Core backtesting engine
│   ├── strategy.py         # Base strategy class
│   ├── data_handler.py     # Data fetching and management
│   ├── portfolio.py        # Portfolio and order management
│   ├── metrics.py          # Performance metrics
│   └── visualizer.py       # Plotting utilities
├── strategies/
│   ├── ma_crossover.py     # Moving average crossover
│   ├── momentum.py         # Momentum strategy
│   └── mean_reversion.py   # Mean reversion strategy
├── examples/
│   ├── simple_example.py   # Quick start
│   ├── run_backtest.py     # Full examples
│   └── nse_example.py      # NSE stock examples
├── requirements.txt
├── README.md
├── GETTING_STARTED.md      # Detailed tutorial
├── QUICK_REFERENCE.md      # Cheat sheet
└── NSE_GUIDE.md           # Guide for Indian NSE stocks
```

## Creating Your Own Strategy

```python
from backtester.strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, param1, param2):
        super().__init__()
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data):
        # Your logic here
        # Return signals dataframe with 'signal' column
        # 1 = buy, -1 = sell, 0 = hold
        pass
```

## License

MIT

# stocktrading-agent
