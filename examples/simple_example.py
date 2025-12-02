"""
Simple example to get started quickly
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import backtester and strategies
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover


def main():
    """Simple backtest example"""
    
    # 1. Setup data handler
    data_handler = YFinanceDataHandler(
        symbol="AAPL",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # 2. Choose a strategy
    strategy = MovingAverageCrossover(short_window=50, long_window=200)
    
    # 3. Create backtester
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    # 4. Run backtest
    results = backtester.run()
    
    # 5. Visualize results
    backtester.plot_results()
    
    # 6. Access specific metrics
    metrics = backtester.get_metrics()
    print(f"\nTotal Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")


if __name__ == "__main__":
    main()

