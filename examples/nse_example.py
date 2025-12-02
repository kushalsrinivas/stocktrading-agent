"""
Example for backtesting NSE (National Stock Exchange) stocks
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import backtester and strategies
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import MovingAverageCrossover
from strategies.momentum import RSIMomentumStrategy
from strategies import MeanReversionStrategy


def backtest_nse_stock(symbol, strategy, start_date="2020-01-01", end_date="2023-12-31"):
    """
    Backtest a strategy on an NSE stock
    
    Args:
        symbol: NSE stock symbol (without .NS suffix)
        strategy: Trading strategy instance
        start_date: Start date for backtest
        end_date: End date for backtest
    """
    # Add .NS suffix for NSE stocks
    nse_symbol = f"{symbol}.NS"
    
    print(f"\n{'='*70}")
    print(f"Backtesting {symbol} on NSE")
    print(f"{'='*70}\n")
    
    # Setup data handler
    data_handler = YFinanceDataHandler(
        symbol=nse_symbol,
        start_date=start_date,
        end_date=end_date
    )
    
    # Create backtester
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=1000000,  # 10 Lakh INR
        commission=0.0005,  # 0.05% (typical Indian brokerage)
        slippage=0.0005
    )
    
    # Run backtest
    results = backtester.run()
    
    # Visualize results
    backtester.plot_results()
    
    return results


def compare_nse_stocks():
    """Compare multiple NSE stocks with the same strategy"""
    print("\n" + "="*70)
    print("COMPARING MULTIPLE NSE STOCKS")
    print("="*70)
    
    # Popular NSE stocks
    nse_stocks = [
        "RELIANCE",   # Reliance Industries
        "TCS",        # Tata Consultancy Services
        "INFY",       # Infosys
        "HDFCBANK",   # HDFC Bank
        "ITC",        # ITC Limited
    ]
    
    # Use MA Crossover strategy for comparison
    strategy = MovingAverageCrossover(short_window=50, long_window=200)
    
    results_comparison = []
    
    for stock in nse_stocks:
        print(f"\nTesting: {stock}")
        print("-" * 50)
        
        nse_symbol = f"{stock}.NS"
        data_handler = YFinanceDataHandler(
            symbol=nse_symbol,
            start_date="2020-01-01",
            end_date="2023-12-31"
        )
        
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=1000000,  # 10 Lakh INR
            commission=0.0005
        )
        
        try:
            results = backtester.run(verbose=False)
            
            results_comparison.append({
                'Stock': stock,
                'Total Return (%)': results['metrics']['Total Return (%)'],
                'Sharpe Ratio': results['metrics']['Sharpe Ratio'],
                'Max Drawdown (%)': results['metrics']['Max Drawdown (%)'],
                'Win Rate (%)': results['metrics']['Win Rate (%)'],
                'Total Trades': results['metrics']['Total Trades'],
                'Final Value (₹)': results['metrics']['Final Value']
            })
        except Exception as e:
            print(f"Error with {stock}: {e}")
    
    # Print comparison table
    import pandas as pd
    comparison_df = pd.DataFrame(results_comparison)
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    print(comparison_df.to_string(index=False))
    print("="*70)
    
    return comparison_df


def test_multiple_strategies_on_nse():
    """Test different strategies on a single NSE stock"""
    print("\n" + "="*70)
    print("TESTING MULTIPLE STRATEGIES ON RELIANCE")
    print("="*70)
    
    stock = "RELIANCE"
    nse_symbol = f"{stock}.NS"
    
    strategies = [
        ("MA Crossover (50/200)", MovingAverageCrossover(50, 200)),
        ("RSI Momentum", RSIMomentumStrategy(14, 30, 70)),
        ("Bollinger Bands", MeanReversionStrategy(20, 2.0)),
    ]
    
    results_comparison = []
    
    for name, strategy in strategies:
        print(f"\nTesting: {name}")
        print("-" * 50)
        
        data_handler = YFinanceDataHandler(
            symbol=nse_symbol,
            start_date="2020-01-01",
            end_date="2023-12-31"
        )
        
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=1000000,
            commission=0.0005
        )
        
        results = backtester.run(verbose=False)
        
        results_comparison.append({
            'Strategy': name,
            'Total Return (%)': results['metrics']['Total Return (%)'],
            'Sharpe Ratio': results['metrics']['Sharpe Ratio'],
            'Max Drawdown (%)': results['metrics']['Max Drawdown (%)'],
            'Win Rate (%)': results['metrics']['Win Rate (%)'],
            'Final Value (₹)': results['metrics']['Final Value']
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
    
    # Example 1: Backtest a single NSE stock
    print("\n" + "="*70)
    print("NSE STOCK BACKTESTING EXAMPLES")
    print("="*70)
    
    # Uncomment the example you want to run:
    
    # Example 1: Single stock backtest
    # strategy = MovingAverageCrossover(short_window=50, long_window=200)
    # backtest_nse_stock("RELIANCE", strategy, "2020-01-01", "2023-12-31")
    
    # Example 2: Compare multiple NSE stocks
    # compare_nse_stocks()
    
    # Example 3: Compare strategies on one stock
    test_multiple_strategies_on_nse()
    
    print("\n" + "="*70)
    print("NSE backtesting completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

