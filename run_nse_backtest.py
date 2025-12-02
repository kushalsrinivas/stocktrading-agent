"""
Interactive NSE Stock Backtesting Script
Uses Combined Strategy (RSI + MACD + Bollinger Bands)

Run this script and enter any NSE stock ticker when prompted.
Initial capital is fixed at ₹10,000
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

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


def main():
    """Main execution function"""
    print_banner()
    
    while True:
        print("\nOptions:")
        print("  1. Backtest a stock")
        print("  2. Show popular NSE stocks")
        print("  3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            strategy_choice = get_strategy_choice()
            symbol, start_date, end_date = get_stock_input()
            results = run_backtest(symbol, start_date, end_date, strategy_choice)
            
            if results:
                print("\n" + "="*70)
                print("✅ Backtest completed successfully!")
                print("="*70)
            
            # Ask if user wants to test another stock
            again = input("\n🔄 Test another stock? (y/n): ").strip().lower()
            if again != 'y':
                break
                
        elif choice == "2":
            show_popular_stocks()
            
        elif choice == "3":
            print("\n👋 Thank you for using NSE Backtesting!")
            print("="*70 + "\n")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please try again or report this issue.\n")

