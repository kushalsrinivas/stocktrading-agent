"""
Example script demonstrating how to use the backtesting framework
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import backtester and strategies
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover, MomentumStrategy, MeanReversionStrategy
from strategies.momentum import RSIMomentumStrategy, MACDMomentumStrategy
from strategies.mean_reversion import ZScoreMeanReversion


def run_ma_crossover_example():
    """Example: Moving Average Crossover Strategy"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Moving Average Crossover Strategy")
    print("="*70)
    
    # Setup
    data_handler = YFinanceDataHandler(
        symbol="AAPL",
        start_date="2020-01-01",
        end_date="2023-12-31"
    )
    
    strategy = MovingAverageCrossover(short_window=50, long_window=200)
    
    # Run backtest
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    results = backtester.run()
    
    # Visualize
    backtester.plot_results()
    
    return results


def run_momentum_example():
    """Example: RSI Momentum Strategy"""
    print("\n" + "="*70)
    print("EXAMPLE 2: RSI Momentum Strategy")
    print("="*70)
    
    # Setup
    data_handler = YFinanceDataHandler(
        symbol="TSLA",
        start_date="2020-01-01",
        end_date="2023-12-31"
    )
    
    strategy = RSIMomentumStrategy(period=14, oversold=30, overbought=70)
    
    # Run backtest
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    results = backtester.run()
    
    # Visualize
    backtester.plot_results()
    
    return results


def run_mean_reversion_example():
    """Example: Mean Reversion with Bollinger Bands"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Mean Reversion Strategy (Bollinger Bands)")
    print("="*70)
    
    # Setup
    data_handler = YFinanceDataHandler(
        symbol="MSFT",
        start_date="2020-01-01",
        end_date="2023-12-31"
    )
    
    strategy = MeanReversionStrategy(period=20, num_std=2.0)
    
    # Run backtest
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    results = backtester.run()
    
    # Visualize
    backtester.plot_results()
    
    return results


def compare_strategies():
    """Compare multiple strategies on the same stock"""
    print("\n" + "="*70)
    print("STRATEGY COMPARISON")
    print("="*70)
    
    symbol = "SPY"
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    initial_capital = 100000
    
    strategies = [
        ("MA Crossover (50/200)", MovingAverageCrossover(50, 200)),
        ("RSI Momentum", RSIMomentumStrategy(14, 30, 70)),
        ("MACD Momentum", MACDMomentumStrategy(12, 26, 9)),
        ("Bollinger Bands", MeanReversionStrategy(20, 2.0)),
        ("Z-Score Reversion", ZScoreMeanReversion(20, -2.0, 2.0))
    ]
    
    results_comparison = []
    
    for name, strategy in strategies:
        print(f"\nTesting: {name}")
        print("-" * 50)
        
        data_handler = YFinanceDataHandler(symbol, start_date, end_date)
        
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=initial_capital
        )
        
        results = backtester.run(verbose=False)
        
        results_comparison.append({
            'Strategy': name,
            'Total Return (%)': results['metrics']['Total Return (%)'],
            'Sharpe Ratio': results['metrics']['Sharpe Ratio'],
            'Max Drawdown (%)': results['metrics']['Max Drawdown (%)'],
            'Win Rate (%)': results['metrics']['Win Rate (%)'],
            'Total Trades': results['metrics']['Total Trades']
        })
    
    # Print comparison table
    import pandas as pd
    comparison_df = pd.DataFrame(results_comparison)
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    print(comparison_df.to_string(index=False))
    print("="*70)
    
    return comparison_df


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("STOCK TRADING BACKTESTING FRAMEWORK - EXAMPLES")
    print("="*70)
    
    # Uncomment the examples you want to run
    
    # Example 1: Moving Average Crossover
    # run_ma_crossover_example()
    
    # Example 2: Momentum Strategy
    # run_momentum_example()
    
    # Example 3: Mean Reversion Strategy
    # run_mean_reversion_example()
    
    # Example 4: Compare Multiple Strategies
    compare_strategies()
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

