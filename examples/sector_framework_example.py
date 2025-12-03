"""
Example Usage of NSE Sector-Based Stock Selection Framework

This script demonstrates how to use the framework with practical examples.
Run this to see the framework in action.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nse_sector_strategy import (
    screen_sector_stocks,
    run_sector_backtest,
    compare_sectors,
    NSE_SECTORS
)


def example_1_screen_auto_sector():
    """
    Example 1: Screen stocks in NIFTY AUTO sector
    
    This will apply all 3 filters:
    1. Liquidity filter
    2. Trend filter (sector + stock alignment)
    3. Volatility filter (for swing trading)
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Screening NIFTY AUTO Sector for Swing Trading")
    print("="*80)
    
    # Define time period (last 6 months)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    # Screen stocks
    candidates = screen_sector_stocks(
        sector='NIFTY_AUTO',
        trading_type='swing',  # or 'intraday'
        start_date=start_date,
        end_date=end_date
    )
    
    if candidates:
        print("\n✅ Screening completed!")
        print(f"   Found {len(candidates)} candidates for swing trading")
        print("\n💡 Next Step: Pick top candidate and backtest it (see Example 2)")
    else:
        print("\n⚠️  No candidates found in current market conditions")
        print("   Try a different sector or time period")
    
    return candidates


def example_2_backtest_stock():
    """
    Example 2: Backtest a specific stock with sector-appropriate strategy
    
    This will:
    1. Use NIFTY AUTO strategy (Breakout + Trend Following)
    2. Run backtest on historical data
    3. Show performance metrics
    4. Generate visualizations
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Backtesting TATA MOTORS with NIFTY AUTO Strategy")
    print("="*80)
    
    # Define time period (last 2 years for robust backtest)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    
    # Run backtest
    results = run_sector_backtest(
        sector='NIFTY_AUTO',
        stock='TATAMOTORS',
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000  # ₹1 lakh
    )
    
    if results:
        metrics = results['metrics']
        print("\n✅ Backtest completed!")
        print(f"\n📊 Quick Summary:")
        print(f"   Return: {metrics['Total Return (%)']:.2f}%")
        print(f"   Sharpe: {metrics['Sharpe Ratio']:.2f}")
        print(f"   Trades: {metrics['Total Trades']}")
        
        if metrics['Total Return (%)'] > 15:
            print("\n🎯 This strategy performed well!")
        elif metrics['Total Return (%)'] > 0:
            print("\n✅ Strategy was profitable but modest returns")
        else:
            print("\n⚠️  Strategy didn't work well for this stock/period")
    
    return results


def example_3_compare_strategies():
    """
    Example 3: Compare all sector strategies on a single stock
    
    This will test the same stock with strategies from all sectors:
    - Banking strategy (Intraday Breakout)
    - IT strategy (Swing Trend)
    - Auto strategy (Breakout + Trend)
    - FMCG strategy (Mean Reversion)
    - Metal strategy (Cycle-Based)
    - Pharma strategy (Range Breakout)
    
    Helps find which strategy works best for that particular stock.
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Comparing All Sector Strategies on RELIANCE")
    print("="*80)
    
    # Define time period (last 1 year)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Compare strategies
    results_list = compare_sectors(
        stock='RELIANCE',
        start_date=start_date,
        end_date=end_date
    )
    
    if results_list:
        print("\n✅ Comparison completed!")
        print("\n💡 Key Insights:")
        print("   • Each strategy has different characteristics")
        print("   • Best strategy varies by stock and market conditions")
        print("   • Consider top 2-3 strategies for diversification")
    
    return results_list


def example_4_it_sector_swing():
    """
    Example 4: IT Sector - Perfect for Swing Trading
    
    IT sector characteristics:
    - Smooth trends
    - Fewer whipsaws
    - Good for pullback entries
    
    Strategy: 20-EMA bounce + RSI confirmation
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: IT Sector Swing Trading (TCS)")
    print("="*80)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    
    results = run_sector_backtest(
        sector='NIFTY_IT',
        stock='TCS',
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    return results


def example_5_banking_intraday():
    """
    Example 5: Banking Sector - High Volatility Intraday
    
    Banking sector characteristics:
    - High volatility
    - News-driven
    - Fast moves
    
    Strategy: VWAP + Volume breakouts
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Banking Sector Intraday Strategy (HDFCBANK)")
    print("="*80)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    results = run_sector_backtest(
        sector='NIFTY_BANK',
        stock='HDFCBANK',
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    return results


def example_6_fmcg_mean_reversion():
    """
    Example 6: FMCG Sector - Mean Reversion
    
    FMCG characteristics:
    - Low volatility
    - Stable trends
    - Good for mean reversion
    
    Strategy: Bollinger Band pullbacks
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: FMCG Mean Reversion (HINDUNILVR)")
    print("="*80)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    
    results = run_sector_backtest(
        sector='NIFTY_FMCG',
        stock='HINDUNILVR',
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    return results


def show_all_examples():
    """Run all examples in sequence"""
    print("\n" + "="*80)
    print("   NSE SECTOR FRAMEWORK - ALL EXAMPLES")
    print("="*80)
    
    examples = [
        ("Screen Auto Sector", example_1_screen_auto_sector),
        ("Backtest Tata Motors", example_2_backtest_stock),
        ("Compare Strategies on Reliance", example_3_compare_strategies),
        ("IT Sector Swing (TCS)", example_4_it_sector_swing),
        ("Banking Intraday (HDFC)", example_5_banking_intraday),
        ("FMCG Mean Reversion (HUL)", example_6_fmcg_mean_reversion),
    ]
    
    print("\n📋 Available Examples:\n")
    for i, (name, _) in enumerate(examples, 1):
        print(f"   {i}. {name}")
    print(f"   {len(examples)+1}. Run all examples")
    print(f"   0. Exit")
    
    choice = input(f"\nSelect example (0-{len(examples)+1}): ").strip()
    
    try:
        choice_num = int(choice)
        
        if choice_num == 0:
            print("\n👋 Goodbye!")
            return
        
        elif choice_num == len(examples) + 1:
            # Run all examples
            for name, func in examples:
                print(f"\n{'='*80}")
                print(f"Running: {name}")
                print(f"{'='*80}")
                
                try:
                    func()
                    print(f"\n✅ {name} completed")
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
                
                input("\nPress Enter to continue to next example...")
        
        elif 1 <= choice_num <= len(examples):
            # Run specific example
            name, func = examples[choice_num - 1]
            print(f"\n{'='*80}")
            print(f"Running: {name}")
            print(f"{'='*80}")
            
            try:
                func()
                print(f"\n✅ {name} completed successfully!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        else:
            print("❌ Invalid choice!")
    
    except ValueError:
        print("❌ Please enter a valid number!")


def quick_tutorial():
    """Quick tutorial for new users"""
    print("\n" + "="*80)
    print("   QUICK TUTORIAL: NSE Sector Framework")
    print("="*80)
    
    print("\n📚 How This Framework Works:\n")
    
    print("Step 1: STOCK SELECTION (3 Filters)")
    print("-" * 40)
    print("   A. Liquidity Filter")
    print("      → Ensures stock has enough volume for easy entry/exit")
    print("      → Min: 5 lakh shares/day, ₹50 crore value traded")
    
    print("\n   B. Trend Filter")
    print("      → Checks if sector is strong (above 50 EMA, RSI > 50)")
    print("      → Then picks strongest stocks in that sector")
    print("      → Stock must be above 20/50/200 EMAs, RSI 55-65")
    
    print("\n   C. Volatility Filter")
    print("      → Low volatility (ATR < 3%) → Swing trading")
    print("      → High volatility (ATR > 3%) → Intraday trading")
    
    print("\n\nStep 2: SECTOR-SPECIFIC STRATEGY")
    print("-" * 40)
    print("   Each sector behaves differently:")
    print("   • Banking → Fast, volatile → Intraday breakouts")
    print("   • IT → Smooth trends → Swing trading")
    print("   • Auto → Long trends → Breakout + trend following")
    print("   • FMCG → Stable → Mean reversion")
    print("   • Metal/Energy → Cyclical → MACD-based")
    print("   • Pharma → Ranging → Breakout from consolidation")
    
    print("\n\nStep 3: ENTRY & EXIT RULES")
    print("-" * 40)
    print("   Entry (ALL must be true):")
    print("   ✅ Price breaks swing high")
    print("   ✅ Volume surge (1.5x average)")
    print("   ✅ RSI > 55")
    print("   ✅ Above key EMAs")
    
    print("\n   Exit (ANY triggers exit):")
    print("   ❌ RSI < 50")
    print("   ❌ Price < 20 EMA")
    print("   ❌ Volume spike + bearish candle")
    print("   ❌ Stop loss hit")
    
    print("\n\nStep 4: BACKTEST & VERIFY")
    print("-" * 40)
    print("   • Test strategy on historical data")
    print("   • Check metrics: Return, Sharpe, Drawdown")
    print("   • Verify win rate > 50% and profit factor > 1")
    print("   • Paper trade before using real money")
    
    print("\n" + "="*80)
    print("\n💡 Ready to try? Run the examples above!")
    print("   Recommended order: Example 1 → Example 2 → Example 3")
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n🎯 NSE SECTOR FRAMEWORK - EXAMPLES\n")
    
    while True:
        print("\n📋 Main Menu:")
        print("   1. Show Quick Tutorial")
        print("   2. Browse & Run Examples")
        print("   3. Show Available Sectors")
        print("   0. Exit")
        
        choice = input("\nSelect option (0-3): ").strip()
        
        if choice == '1':
            quick_tutorial()
            input("\nPress Enter to return to menu...")
        
        elif choice == '2':
            show_all_examples()
            break  # Exit after running examples
        
        elif choice == '3':
            print("\n" + "="*80)
            print("   NSE SECTORS IN FRAMEWORK")
            print("="*80)
            
            for i, (sector, info) in enumerate(NSE_SECTORS.items(), 1):
                print(f"\n{i}. {sector}")
                print(f"   Index: {info['index']}")
                print(f"   Stocks: {len(info['stocks'])} constituents")
                print(f"   Examples: {', '.join(info['stocks'][:5])}...")
            
            print("\n" + "="*80)
            input("\nPress Enter to return to menu...")
        
        elif choice == '0':
            print("\n👋 Thank you for exploring the NSE Sector Framework!")
            print("   Happy Trading! 📈")
            print("="*80 + "\n")
            break
        
        else:
            print("❌ Invalid choice!")

