# Getting Started Guide

Welcome to the Stock Trading Backtesting Framework! This guide will help you get up and running quickly.

## Installation

1. **Clone or navigate to the project directory:**
```bash
cd /Users/kushalsrinivas/apps/stocktrading
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Run Your First Backtest

The simplest way to get started is with the simple example:

```bash
python examples/simple_example.py
```

This will:
- Download AAPL stock data from 2022-2023
- Run a moving average crossover strategy
- Display performance metrics
- Show visualizations

### 2. Understanding the Code

Here's the basic structure of a backtest:

```python
from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover

# 1. Get your data
data_handler = YFinanceDataHandler(
    symbol="AAPL",
    start_date="2022-01-01",
    end_date="2023-12-31"
)

# 2. Choose a strategy
strategy = MovingAverageCrossover(short_window=50, long_window=200)

# 3. Create and run backtester
backtester = Backtester(
    data_handler=data_handler,
    strategy=strategy,
    initial_capital=100000
)

results = backtester.run()

# 4. Visualize
backtester.plot_results()
```

## Available Strategies

### 1. Moving Average Crossover
```python
from strategies import MovingAverageCrossover

strategy = MovingAverageCrossover(short_window=50, long_window=200)
```

### 2. RSI Momentum
```python
from strategies.momentum import RSIMomentumStrategy

strategy = RSIMomentumStrategy(period=14, oversold=30, overbought=70)
```

### 3. MACD Momentum
```python
from strategies.momentum import MACDMomentumStrategy

strategy = MACDMomentumStrategy(fast_period=12, slow_period=26, signal_period=9)
```

### 4. Bollinger Bands Mean Reversion
```python
from strategies import MeanReversionStrategy

strategy = MeanReversionStrategy(period=20, num_std=2.0)
```

### 5. Z-Score Mean Reversion
```python
from strategies.mean_reversion import ZScoreMeanReversion

strategy = ZScoreMeanReversion(period=20, buy_threshold=-2.0, sell_threshold=2.0)
```

## Creating Your Own Strategy

Create a new file in the `strategies/` folder:

```python
from backtester.strategy import Strategy
import pandas as pd

class MyCustomStrategy(Strategy):
    def __init__(self, my_parameter=10):
        super().__init__()
        self.my_parameter = my_parameter
        self.parameters = {'my_parameter': my_parameter}
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals
        
        Args:
            data: DataFrame with columns: Open, High, Low, Close, Volume
        
        Returns:
            DataFrame with 'signal' column:
                1 = Buy
                -1 = Sell
                0 = Hold
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Your logic here
        # Example: Buy when close > moving average
        ma = data['Close'].rolling(self.my_parameter).mean()
        signals.loc[data['Close'] > ma, 'signal'] = 1
        signals.loc[data['Close'] < ma, 'signal'] = -1
        
        return signals
```

Then use it:

```python
from strategies.my_strategy import MyCustomStrategy

strategy = MyCustomStrategy(my_parameter=20)
backtester = Backtester(data_handler, strategy, initial_capital=100000)
results = backtester.run()
```

## Advanced Features

### 1. Limit Orders

Add limit prices to your signals:

```python
def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    signals['limit_price'] = None
    
    # Buy at 5% below current price
    buy_condition = (some_condition)
    signals.loc[buy_condition, 'signal'] = 1
    signals.loc[buy_condition, 'limit_price'] = data['Close'] * 0.95
    
    return signals
```

### 2. Stop Loss Orders

Add stop prices to your signals:

```python
def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    signals['stop_price'] = None
    
    # Sell with stop loss at 10% below current price
    sell_condition = (some_condition)
    signals.loc[sell_condition, 'signal'] = -1
    signals.loc[sell_condition, 'stop_price'] = data['Close'] * 0.90
    
    return signals
```

### 3. Variable Position Sizing

Specify the number of shares:

```python
def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    signals['quantity'] = None
    
    # Buy specific quantity
    signals.loc[buy_condition, 'signal'] = 1
    signals.loc[buy_condition, 'quantity'] = 100  # Buy 100 shares
    
    return signals
```

### 4. Compare Multiple Strategies

```python
from examples.run_backtest import compare_strategies

comparison_df = compare_strategies()
```

## Understanding Results

### Performance Metrics

- **Total Return (%)**: Overall percentage gain/loss
- **Sharpe Ratio**: Risk-adjusted return (higher is better, >1 is good, >2 is very good)
- **Max Drawdown (%)**: Largest peak-to-trough decline (lower is better)
- **Volatility (%)**: Annualized standard deviation of returns
- **Win Rate (%)**: Percentage of profitable trades
- **Profit Factor**: Gross profit / Gross loss (>1 is profitable)

### Visualizations

The framework provides several visualizations:

1. **Equity Curve**: Portfolio value over time
2. **Drawdown Chart**: Drawdown percentage over time
3. **Trade Markers**: Buy/sell points on the price chart
4. **Returns Distribution**: Histogram of returns

```python
# Individual plots
backtester.plot_results()  # Shows equity curve, drawdown, and trades

# Or use visualizer directly for more control
from backtester.visualizer import Visualizer
viz = Visualizer(results)
viz.plot_equity_curve()
viz.plot_drawdown()
viz.plot_trades()
viz.plot_returns_distribution()
viz.plot_all()  # Comprehensive view
```

## Tips for Backtesting

1. **Avoid Overfitting**: Don't optimize parameters on the same data you're testing on
2. **Use Realistic Assumptions**: Include commission and slippage
3. **Out-of-Sample Testing**: Test on data the strategy hasn't "seen"
4. **Consider Transaction Costs**: Frequent trading can erode profits
5. **Mind the Lookback Period**: Ensure your indicators have enough data
6. **Check for Lookahead Bias**: Don't use future information in your signals

## Common Issues

### No Trading Activity

If you see no trades:
- Check if your strategy is generating signals (print `results['signals']`)
- Verify you have enough capital for at least one trade
- Make sure indicators have enough data (try increasing the date range)

### Poor Performance

- Try different parameter values
- Check if the strategy logic matches your intention
- Consider market conditions (trending vs. ranging markets)
- Review individual trades in the trade history

### Memory Issues

For large datasets:
- Reduce the date range
- Use fewer indicators
- Sample the data (e.g., weekly instead of daily)

## Next Steps

1. **Run the comparison example**: `python examples/run_backtest.py`
2. **Modify existing strategies** with different parameters
3. **Create your own strategy** based on your trading ideas
4. **Test on multiple stocks** to verify robustness
5. **Implement portfolio management** for multi-stock strategies

## Getting Help

- Check the `README.md` for architecture overview
- Look at example strategies in `strategies/` folder
- Review example scripts in `examples/` folder
- Read the docstrings in the code for detailed API documentation

Happy backtesting! 📈

