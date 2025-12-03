"""
Advanced Strategies Example

This example demonstrates how to use the new advanced trading strategies
with primary and confirmation indicators.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import strategies
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import the new strategies
from strategies import (
    StochasticBreakoutStrategy,
    AggressiveStochasticStrategy,
    VWAPReversalStrategy,
    AggressiveVWAPStrategy,
    SupertrendMomentumStrategy,
    AggressiveSupertrendStrategy,
    KeltnerSqueezeStrategy,
    AggressiveSqueezeStrategy,
    WilliamsTrendStrategy,
    AggressiveWilliamsStrategy
)

from backtester.engine import BacktestEngine
from backtester.visualizer import plot_results, plot_equity_curve


def generate_sample_data(days=252):
    """Generate sample OHLCV data for testing"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate random walk price data
    np.random.seed(42)
    returns = np.random.randn(days) * 0.02
    price = 100 * np.exp(np.cumsum(returns))
    
    # Generate OHLC from close prices
    data = pd.DataFrame({
        'Open': price * (1 + np.random.randn(days) * 0.01),
        'High': price * (1 + np.abs(np.random.randn(days) * 0.02)),
        'Low': price * (1 - np.abs(np.random.randn(days) * 0.02)),
        'Close': price,
        'Volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
    # Ensure High is highest and Low is lowest
    data['High'] = data[['Open', 'High', 'Close']].max(axis=1)
    data['Low'] = data[['Open', 'Low', 'Close']].min(axis=1)
    
    return data


def test_single_strategy(data, strategy, strategy_name):
    """Test a single strategy and print results"""
    print(f"\n{'='*60}")
    print(f"Testing: {strategy_name}")
    print(f"{'='*60}")
    
    # Initialize backtest engine
    engine = BacktestEngine(
        data=data,
        strategy=strategy,
        initial_capital=100000,
        commission=0.001  # 0.1% commission
    )
    
    # Run backtest
    results = engine.run()
    
    # Print results
    print(f"\nStrategy Parameters: {strategy.parameters}")
    print(f"\nPerformance Metrics:")
    print(f"  Total Return: {results['total_return']:.2f}%")
    print(f"  Annual Return: {results['annual_return']:.2f}%")
    print(f"  Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"  Max Drawdown: {results['max_drawdown']:.2f}%")
    print(f"  Win Rate: {results['win_rate']:.2f}%")
    print(f"  Total Trades: {results['total_trades']}")
    print(f"  Avg Trade Return: {results['avg_trade_return']:.2f}%")
    
    return results


def compare_all_strategies(data):
    """Compare all strategies side by side"""
    print("\n" + "="*80)
    print("COMPARING ALL ADVANCED STRATEGIES")
    print("="*80)
    
    strategies = [
        ("Stochastic Breakout", StochasticBreakoutStrategy()),
        ("Aggressive Stochastic", AggressiveStochasticStrategy()),
        ("VWAP Reversal", VWAPReversalStrategy()),
        ("Aggressive VWAP", AggressiveVWAPStrategy()),
        ("Supertrend Momentum", SupertrendMomentumStrategy()),
        ("Aggressive Supertrend", AggressiveSupertrendStrategy()),
        ("Keltner Squeeze", KeltnerSqueezeStrategy()),
        ("Aggressive Squeeze", AggressiveSqueezeStrategy()),
        ("Williams Trend", WilliamsTrendStrategy()),
        ("Aggressive Williams", AggressiveWilliamsStrategy())
    ]
    
    results_summary = []
    
    for name, strategy in strategies:
        try:
            engine = BacktestEngine(
                data=data,
                strategy=strategy,
                initial_capital=100000,
                commission=0.001
            )
            results = engine.run()
            
            results_summary.append({
                'Strategy': name,
                'Total Return (%)': f"{results['total_return']:.2f}",
                'Sharpe Ratio': f"{results['sharpe_ratio']:.2f}",
                'Max Drawdown (%)': f"{results['max_drawdown']:.2f}",
                'Win Rate (%)': f"{results['win_rate']:.2f}",
                'Total Trades': results['total_trades']
            })
        except Exception as e:
            print(f"Error testing {name}: {str(e)}")
            results_summary.append({
                'Strategy': name,
                'Total Return (%)': 'ERROR',
                'Sharpe Ratio': 'ERROR',
                'Max Drawdown (%)': 'ERROR',
                'Win Rate (%)': 'ERROR',
                'Total Trades': 'ERROR'
            })
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame(results_summary)
    print("\n" + comparison_df.to_string(index=False))
    
    return comparison_df


def main():
    """Main execution function"""
    
    # Generate sample data
    print("Generating sample data...")
    data = generate_sample_data(days=252)  # 1 year of data
    
    print(f"\nData shape: {data.shape}")
    print(f"Date range: {data.index[0]} to {data.index[-1]}")
    print(f"\nFirst few rows:")
    print(data.head())
    
    # Example 1: Test Stochastic Breakout Strategy
    print("\n" + "="*80)
    print("EXAMPLE 1: Stochastic Breakout Strategy")
    print("="*80)
    strategy1 = StochasticBreakoutStrategy(
        stoch_period=14,
        stoch_oversold=20,
        stoch_overbought=80,
        adx_threshold=20,
        volume_spike_multiplier=1.3
    )
    test_single_strategy(data, strategy1, "Stochastic Breakout (Standard)")
    
    # Example 2: Test VWAP Reversal Strategy
    print("\n" + "="*80)
    print("EXAMPLE 2: VWAP Reversal Strategy")
    print("="*80)
    strategy2 = VWAPReversalStrategy(
        vwap_deviation_threshold=1.5,
        rsi_period=14,
        divergence_lookback=10
    )
    test_single_strategy(data, strategy2, "VWAP Reversal (Standard)")
    
    # Example 3: Test Supertrend Momentum Strategy
    print("\n" + "="*80)
    print("EXAMPLE 3: Supertrend Momentum Strategy")
    print("="*80)
    strategy3 = SupertrendMomentumStrategy(
        atr_period=10,
        atr_multiplier=2.5,
        ema_period=20
    )
    test_single_strategy(data, strategy3, "Supertrend Momentum (Standard)")
    
    # Example 4: Compare all strategies
    print("\n" + "="*80)
    print("EXAMPLE 4: Compare All Strategies")
    print("="*80)
    comparison = compare_all_strategies(data)
    
    # Save comparison to CSV
    comparison.to_csv('strategy_comparison.csv', index=False)
    print("\n✓ Comparison saved to 'strategy_comparison.csv'")
    
    print("\n" + "="*80)
    print("EXAMPLES COMPLETED!")
    print("="*80)
    print("\nNext steps:")
    print("1. Try with your own market data")
    print("2. Optimize parameters for specific assets")
    print("3. Combine multiple strategies for portfolio approach")
    print("4. Use the aggressive variants for higher frequency trading")
    print("\nSee ADVANCED_STRATEGIES_GUIDE.md for detailed documentation")


if __name__ == "__main__":
    main()

