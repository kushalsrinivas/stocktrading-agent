"""
Interactive NSE Stock Backtesting Script
Uses Combined Strategy (RSI + MACD + Bollinger Bands)

Run this script and enter any NSE stock ticker when prompted.
Initial capital is fixed at ₹10,000
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, YFinanceDataHandler
from strategies.combined_strategy import CombinedStrategy
from strategies.rsi_bb_strategy import RSIBollingerStrategy
from strategies import MovingAverageCrossover
from strategies.momentum import RSIMomentumStrategy, MACDMomentumStrategy


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("   NSE STOCK BACKTESTING - MULTIPLE STRATEGIES")
    print("="*70)
    print("\n💰 Initial Capital: ₹10,000")
    print("📈 Commission: 0.05% (typical discount broker)")
    print("="*70 + "\n")


def get_strategy_choice():
    """Let user choose a strategy"""
    print("\n📊 Available Strategies:\n")
    print("   1. RSI + Bollinger Bands (Mean Reversion)")
    print("      • Buy: Price at lower BB + RSI oversold")
    print("      • Sell: Price at middle BB or RSI overbought")
    print()
    print("   2. Combined (RSI + MACD + Bollinger Bands)")
    print("      • Buy: All indicators confirm oversold")
    print("      • Sell: Any indicator signals overbought")
    print()
    print("   3. Moving Average Crossover")
    print("      • Buy: Fast MA crosses above slow MA")
    print("      • Sell: Fast MA crosses below slow MA")
    print()
    print("   4. RSI Momentum")
    print("      • Buy: RSI crosses above oversold level")
    print("      • Sell: RSI crosses above overbought level")
    print()
    print("   5. MACD Momentum")
    print("      • Buy: MACD crosses above signal line")
    print("      • Sell: MACD crosses below signal line")
    
    while True:
        choice = input("\n   Choose strategy (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        print("   ❌ Invalid choice. Please enter 1, 2, 3, 4, or 5")


def create_strategy(choice):
    """Create strategy based on user choice"""
    strategies = {
        1: ("RSI + Bollinger Bands", RSIBollingerStrategy(
            rsi_period=14,
            rsi_oversold=40,
            rsi_overbought=70,
            bb_period=20,
            bb_std=2.0
        )),
        2: ("Combined Strategy", CombinedStrategy(
            rsi_period=14,
            rsi_oversold=30,
            rsi_overbought=70,
            macd_fast=12,
            macd_slow=26,
            macd_signal=9,
            bb_period=20,
            bb_std=2.0
        )),
        3: ("MA Crossover", MovingAverageCrossover(
            short_window=50,
            long_window=200
        )),
        4: ("RSI Momentum", RSIMomentumStrategy(
            period=14,
            oversold=30,
            overbought=70
        )),
        5: ("MACD Momentum", MACDMomentumStrategy(
            fast_period=12,
            slow_period=26,
            signal_period=9
        ))
    }
    
    return strategies[choice]


def get_stock_input():
    """Get stock ticker from user"""
    print("\n📝 Enter NSE Stock Details:\n")
    
    # Get stock symbol
    while True:
        symbol = input("Stock Symbol (e.g., RELIANCE, TCS, INFY): ").strip().upper()
        if symbol:
            break
        print("❌ Please enter a valid stock symbol!\n")
    
    # Get date range
    print("\n📅 Date Range:")
    print("   Press Enter for default (last 2 years)")
    
    start_date = input("   Start Date (YYYY-MM-DD) [default: 2 years ago]: ").strip()
    if not start_date:
        start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    
    end_date = input("   End Date (YYYY-MM-DD) [default: today]: ").strip()
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    return symbol, start_date, end_date


def run_backtest(symbol, start_date, end_date, strategy_choice):
    """
    Run backtest for given NSE stock
    
    Args:
        symbol: Stock symbol (without .NS)
        start_date: Start date for backtest
        end_date: End date for backtest
        strategy_choice: Strategy number (1-5)
    """
    # Add .NS suffix for NSE
    nse_symbol = f"{symbol}.NS"
    
    # Get strategy
    strategy_name, strategy = create_strategy(strategy_choice)
    
    print("\n" + "="*70)
    print(f"🔍 Fetching data for {symbol}...")
    print(f"📊 Strategy: {strategy_name}")
    print("="*70 + "\n")
    
    try:
        # Setup data handler
        data_handler = YFinanceDataHandler(
            symbol=nse_symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        # Create backtester with ₹10,000 initial capital
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=10000,  # ₹10,000
            commission=0.0005,  # 0.05%
            slippage=0.0005
        )
        
        # Run backtest
        print("⚙️  Running backtest...\n")
        results = backtester.run()
        
        # Print detailed summary
        print_summary(symbol, strategy_name, results)
        
        # Show visualizations
        print("\n📊 Generating visualizations...")
        backtester.plot_results()
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible reasons:")
        print("  • Stock symbol might be incorrect")
        print("  • No data available for the selected date range")
        print("  • Network connection issue")
        print(f"\n💡 Tip: Verify the symbol at https://www.nseindia.com/")
        return None


def print_summary(symbol, strategy_name, results):
    """Print detailed results summary"""
    metrics = results['metrics']
    
    print("\n" + "="*70)
    print(f"   BACKTEST RESULTS FOR {symbol}")
    print(f"   Strategy: {strategy_name}")
    print("="*70)
    
    # Capital summary
    print("\n💰 CAPITAL:")
    print(f"   Initial Capital:    ₹{metrics['Initial Value']:>10,.2f}")
    print(f"   Final Value:        ₹{metrics['Final Value']:>10,.2f}")
    profit_loss = metrics['Final Value'] - metrics['Initial Value']
    profit_emoji = "📈" if profit_loss > 0 else "📉"
    print(f"   Profit/Loss:        ₹{profit_loss:>10,.2f} {profit_emoji}")
    
    # Performance metrics
    print("\n📊 PERFORMANCE:")
    return_emoji = "✅" if metrics['Total Return (%)'] > 0 else "❌"
    print(f"   Total Return:       {metrics['Total Return (%)']:>10,.2f}% {return_emoji}")
    
    sharpe_emoji = "🌟" if metrics['Sharpe Ratio'] > 1 else "⭐" if metrics['Sharpe Ratio'] > 0 else "⚠️"
    print(f"   Sharpe Ratio:       {metrics['Sharpe Ratio']:>10,.2f} {sharpe_emoji}")
    
    print(f"   Max Drawdown:       {metrics['Max Drawdown (%)']:>10,.2f}%")
    print(f"   Volatility:         {metrics['Volatility (%)']:>10,.2f}%")
    
    # Trading activity
    print("\n📈 TRADING ACTIVITY:")
    print(f"   Total Trades:       {metrics['Total Trades']:>10}")
    
    if metrics['Total Trades'] > 0:
        win_emoji = "🎯" if metrics['Win Rate (%)'] > 50 else "⚠️"
        print(f"   Win Rate:           {metrics['Win Rate (%)']:>10,.2f}% {win_emoji}")
        
        pf_emoji = "💪" if metrics['Profit Factor'] > 1 else "⚠️"
        print(f"   Profit Factor:      {metrics['Profit Factor']:>10,.2f} {pf_emoji}")
    else:
        print(f"   Win Rate:                    N/A")
        print(f"   Profit Factor:               N/A")
    
    print("\n" + "="*70)
    
    # Interpretation
    print("\n💡 INTERPRETATION:")
    if metrics['Total Return (%)'] > 10:
        print("   ✅ Excellent returns!")
    elif metrics['Total Return (%)'] > 0:
        print("   ✅ Positive returns")
    else:
        print("   ❌ Strategy lost money on this stock")
    
    if metrics['Sharpe Ratio'] > 2:
        print("   ✅ Outstanding risk-adjusted returns")
    elif metrics['Sharpe Ratio'] > 1:
        print("   ✅ Good risk-adjusted returns")
    elif metrics['Sharpe Ratio'] > 0:
        print("   ⚠️  Moderate risk-adjusted returns")
    else:
        print("   ❌ Poor risk-adjusted returns")
    
    if metrics['Total Trades'] == 0:
        print("   ⚠️  No trades executed - strategy didn't generate signals")
        print("      Try a longer date range or different stock")
    elif metrics['Total Trades'] < 5:
        print("   ⚠️  Very few trades - results may not be statistically significant")
    
    print("\n" + "="*70)


def show_popular_stocks():
    """Show list of popular NSE stocks"""
    print("\n💡 Popular NSE Stocks:")
    print("\n   Large Cap:")
    print("   • RELIANCE   - Reliance Industries")
    print("   • TCS        - Tata Consultancy Services")
    print("   • INFY       - Infosys")
    print("   • HDFCBANK   - HDFC Bank")
    print("   • ICICIBANK  - ICICI Bank")
    print("   • SBIN       - State Bank of India")
    
    print("\n   Mid/Small Cap:")
    print("   • ITC        - ITC Limited")
    print("   • WIPRO      - Wipro")
    print("   • AXISBANK   - Axis Bank")
    print("   • BAJFINANCE - Bajaj Finance")
    print("   • TITAN      - Titan Company")
    
    print("\n   Indices:")
    print("   • NIFTY50    - Nifty 50 Index (use ^NSEI)")
    print("\n")


def compare_all_strategies(symbol):
    """
    Test all strategies on a single stock and compare results
    
    Args:
        symbol: Stock symbol (without .NS)
    """
    # Date range: 1 year from today
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    nse_symbol = f"{symbol}.NS"
    
    print("\n" + "="*70)
    print(f"🔄 COMPARING ALL STRATEGIES ON {symbol}")
    print(f"📅 Period: {start_date} to {end_date} (Last 1 Year)")
    print("="*70 + "\n")
    
    # Fetch data once
    try:
        data_handler = YFinanceDataHandler(
            symbol=nse_symbol,
            start_date=start_date,
            end_date=end_date
        )
        print(f"✅ Data fetched successfully\n")
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None
    
    # Test all strategies
    all_strategies = [
        (1, "RSI + Bollinger Bands"),
        (2, "Combined Strategy"),
        (3, "MA Crossover"),
        (4, "RSI Momentum"),
        (5, "MACD Momentum")
    ]
    
    results_list = []
    
    for strategy_num, strategy_name in all_strategies:
        print(f"Testing: {strategy_name}...")
        print("-" * 50)
        
        try:
            # Create strategy
            _, strategy = create_strategy(strategy_num)
            
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
                'Volatility (%)': metrics['Volatility (%)'],
                'Win Rate (%)': metrics['Win Rate (%)'],
                'Profit Factor': metrics['Profit Factor'],
                'Total Trades': metrics['Total Trades'],
                'Final Value (₹)': metrics['Final Value']
            })
            
            print(f"✅ Completed - Return: {metrics['Total Return (%)']:.2f}%\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
            results_list.append({
                'Strategy': strategy_name,
                'Total Return (%)': 0,
                'Sharpe Ratio': 0,
                'Max Drawdown (%)': 0,
                'Volatility (%)': 0,
                'Win Rate (%)': 0,
                'Profit Factor': 0,
                'Total Trades': 0,
                'Final Value (₹)': 10000
            })
    
    # Display comparison
    print_comparison_table(symbol, results_list, start_date, end_date)
    
    return results_list


def print_comparison_table(symbol, results_list, start_date, end_date):
    """Print formatted comparison table"""
    df = pd.DataFrame(results_list)
    
    print("\n" + "="*100)
    print(f"   STRATEGY COMPARISON FOR {symbol}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"   Initial Capital: ₹10,000")
    print("="*100)
    
    # Sort by Total Return
    df_sorted = df.sort_values('Total Return (%)', ascending=False)
    
    print("\n📊 PERFORMANCE SUMMARY:\n")
    print(df_sorted.to_string(index=False))
    print("\n" + "="*100)
    
    # Find best strategy
    best_return = df_sorted.iloc[0]
    best_sharpe = df.loc[df['Sharpe Ratio'].idxmax()]
    best_drawdown = df.loc[df['Max Drawdown (%)'].idxmax()]  # Least negative
    most_trades = df.loc[df['Total Trades'].idxmax()]
    
    print("\n🏆 HIGHLIGHTS:\n")
    print(f"   Best Return:        {best_return['Strategy']}")
    print(f"                       {best_return['Total Return (%)']:.2f}% return")
    print(f"                       Final Value: ₹{best_return['Final Value (₹)']:,.2f}")
    
    print(f"\n   Best Risk-Adjusted: {best_sharpe['Strategy']}")
    print(f"                       Sharpe Ratio: {best_sharpe['Sharpe Ratio']:.2f}")
    
    print(f"\n   Lowest Drawdown:    {best_drawdown['Strategy']}")
    print(f"                       Max Drawdown: {best_drawdown['Max Drawdown (%)']:.2f}%")
    
    print(f"\n   Most Active:        {most_trades['Strategy']}")
    print(f"                       {int(most_trades['Total Trades'])} trades")
    
    print("\n" + "="*100)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:\n")
    
    profitable = df[df['Total Return (%)'] > 0]
    if len(profitable) > 0:
        print(f"   ✅ {len(profitable)} out of 5 strategies were profitable")
        print(f"\n   Top 3 Strategies by Return:")
        for i, row in enumerate(df_sorted.head(3).itertuples(), 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            print(f"   {emoji} {row.Strategy}: {row._2:.2f}% (Sharpe: {row._3:.2f})")
    else:
        print(f"   ⚠️  No strategies were profitable in this period")
        print(f"   Consider:")
        print(f"   • Testing a different stock")
        print(f"   • Trying a different time period")
        print(f"   • Market conditions may not favor these strategies")
    
    # Trading frequency analysis
    avg_trades = df['Total Trades'].mean()
    print(f"\n   📈 Average Trading Frequency: {avg_trades:.1f} trades/year")
    
    if avg_trades < 5:
        print(f"   ⚠️  Low frequency - results may not be statistically significant")
    elif avg_trades > 30:
        print(f"   ⚠️  High frequency - watch out for commission costs")
    
    # Sharpe ratio analysis
    good_sharpe = df[df['Sharpe Ratio'] > 1]
    if len(good_sharpe) > 0:
        print(f"\n   ✅ {len(good_sharpe)} strategies have good risk-adjusted returns (Sharpe > 1)")
    
    print("\n" + "="*100)


def main():
    """Main execution function"""
    print_banner()
    
    while True:
        print("\nOptions:")
        print("  1. Backtest a stock (choose strategy)")
        print("  2. Compare all strategies on a stock (1 year)")
        print("  3. Show popular NSE stocks")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            strategy_choice = get_strategy_choice()
            symbol, start_date, end_date = get_stock_input()
            results = run_backtest(symbol, start_date, end_date, strategy_choice)
            
            if results:
                print("\n" + "="*70)
                print("✅ Backtest completed successfully!")
                print("="*70)
            
            # Ask if user wants to test another stock
            again = input("\n🔄 Test another? (y/n): ").strip().lower()
            if again != 'y':
                break
        
        elif choice == "2":
            print("\n📝 Enter Stock Symbol to Compare All Strategies:\n")
            symbol = input("Stock Symbol (e.g., RELIANCE, TCS, INFY): ").strip().upper()
            
            if symbol:
                results_list = compare_all_strategies(symbol)
                
                if results_list:
                    # Ask if user wants detailed view of best strategy
                    view_detail = input("\n📊 View detailed results for best strategy? (y/n): ").strip().lower()
                    if view_detail == 'y':
                        df = pd.DataFrame(results_list)
                        best_idx = df['Total Return (%)'].idxmax()
                        best_strategy_num = best_idx + 1
                        
                        print(f"\n🔍 Running detailed backtest for best strategy...")
                        
                        end_date = datetime.now().strftime("%Y-%m-%d")
                        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                        
                        results = run_backtest(symbol, start_date, end_date, best_strategy_num)
            
            again = input("\n🔄 Test another? (y/n): ").strip().lower()
            if again != 'y':
                break
                
        elif choice == "3":
            show_popular_stocks()
            
        elif choice == "4":
            print("\n👋 Thank you for using NSE Backtesting!")
            print("="*70 + "\n")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please try again or report this issue.\n")

