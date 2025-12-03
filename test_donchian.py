"""
Quick test script for Donchian Breakout strategies

This script tests all three Donchian variants on a sample stock
to verify the implementation works correctly.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import (
    DonchianBreakoutStrategy,
    AggressiveDonchianStrategy,
    TurtleTradersStrategy
)


def test_donchian_strategies(symbol="RELIANCE", days_back=365):
    """
    Test all Donchian strategies on a stock
    
    Args:
        symbol: Stock symbol (without .NS)
        days_back: Number of days to backtest
    """
    print("\n" + "="*80)
    print("🐢 DONCHIAN BREAKOUT STRATEGY TEST")
    print("="*80)
    
    # Date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    nse_symbol = f"{symbol}.NS"
    
    print(f"\n📊 Testing Stock: {symbol}")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"💰 Initial Capital: ₹10,000")
    print("\n" + "="*80 + "\n")
    
    # Define strategies
    strategies = [
        ("Donchian Breakout (55/20)", DonchianBreakoutStrategy(
            entry_period=55,
            exit_period=20,
            use_middle_band=True,
            atr_period=14
        )),
        ("Donchian Fast (20/10)", AggressiveDonchianStrategy(
            entry_period=20,
            exit_period=10,
            atr_period=14,
            atr_multiplier=2.0
        )),
        ("Turtle Traders (55/20)", TurtleTradersStrategy(
            entry_period=55,
            exit_period=20,
            atr_period=20,
            risk_per_trade=0.02
        ))
    ]
    
    results_list = []
    
    for strategy_name, strategy in strategies:
        print(f"Testing: {strategy_name}")
        print("-" * 80)
        
        try:
            # Fetch data
            data_handler = YFinanceDataHandler(
                symbol=nse_symbol,
                start_date=start_date,
                end_date=end_date
            )
            
            # Create backtester
            backtester = Backtester(
                data_handler=data_handler,
                strategy=strategy,
                initial_capital=10000,
                commission=0.0005,
                slippage=0.0005
            )
            
            # Run backtest
            results = backtester.run(verbose=False)
            metrics = results['metrics']
            
            # Store results
            results_list.append({
                'Strategy': strategy_name,
                'Total Return (%)': metrics['Total Return (%)'],
                'Sharpe Ratio': metrics['Sharpe Ratio'],
                'Max Drawdown (%)': metrics['Max Drawdown (%)'],
                'Win Rate (%)': metrics['Win Rate (%)'],
                'Total Trades': metrics['Total Trades'],
                'Final Value (₹)': metrics['Final Value']
            })
            
            # Print summary
            print(f"✅ Total Return: {metrics['Total Return (%)']:>8.2f}%")
            print(f"   Sharpe Ratio: {metrics['Sharpe Ratio']:>8.2f}")
            print(f"   Max Drawdown: {metrics['Max Drawdown (%)']:>8.2f}%")
            print(f"   Total Trades: {metrics['Total Trades']:>8}")
            print(f"   Win Rate:     {metrics['Win Rate (%)']:>8.2f}%")
            print(f"   Final Value:  ₹{metrics['Final Value']:>8,.2f}")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
            continue
    
    # Print comparison
    print("="*80)
    print("📊 COMPARISON SUMMARY")
    print("="*80 + "\n")
    
    if results_list:
        # Sort by return
        results_list.sort(key=lambda x: x['Total Return (%)'], reverse=True)
        
        print(f"{'Strategy':<30} {'Return':>10} {'Sharpe':>10} {'Trades':>10} {'Win Rate':>10}")
        print("-" * 80)
        
        for result in results_list:
            print(f"{result['Strategy']:<30} "
                  f"{result['Total Return (%)']:>9.2f}% "
                  f"{result['Sharpe Ratio']:>9.2f} "
                  f"{result['Total Trades']:>9} "
                  f"{result['Win Rate (%)']:>9.2f}%")
        
        print("\n" + "="*80)
        
        # Best strategy
        best = results_list[0]
        print(f"\n🏆 Best Strategy: {best['Strategy']}")
        print(f"   Return: {best['Total Return (%)']:.2f}%")
        print(f"   Final Value: ₹{best['Final Value (₹)']:,.2f}")
        print(f"   Sharpe Ratio: {best['Sharpe Ratio']:.2f}")
        
        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80 + "\n")
        
        return results_list
    else:
        print("\n❌ No results to display")
        return None


def main():
    """Main execution"""
    print("\n🐢 Donchian Breakout Strategy Test")
    print("This will test all three Donchian variants on RELIANCE stock\n")
    
    # Option to test different stock
    custom = input("Test on RELIANCE for 1 year? (Y/n): ").strip().lower()
    
    if custom == 'n':
        symbol = input("Enter stock symbol (e.g., TCS, INFY): ").strip().upper()
        days = input("Enter days to backtest [default: 365]: ").strip()
        days = int(days) if days else 365
        test_donchian_strategies(symbol, days)
    else:
        test_donchian_strategies("RELIANCE", 365)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

