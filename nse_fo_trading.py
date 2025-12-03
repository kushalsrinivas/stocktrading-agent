"""
NSE F&O (Futures & Options) Stock Trading Framework

This script focuses specifically on F&O stocks with:
- All strategies from the sector framework
- F&O-specific filters and metrics
- Higher liquidity requirements
- Options-friendly volatility analysis

F&O stocks are ideal for:
- Leveraged trading
- Hedging strategies
- Higher liquidity
- Better price discovery
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the sector framework
from nse_sector_strategy import (
    NSE_NIFTY_50,
    NSE_NIFTY_NEXT_50,
    NSE_SECTORS,
    StockScreener,
    get_strategy_for_sector,
    run_sector_backtest,
    compare_sectors,
    screen_sector_stocks
)

from backtester import Backtester, YFinanceDataHandler


# ============================================================================
# NSE F&O STOCK UNIVERSE
# ============================================================================

# Most actively traded F&O stocks (as of 2024)
NSE_FO_STOCKS = {
    'HIGHLY_LIQUID_FO': [
        # Bank Nifty constituents (most liquid)
        'HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK', 'INDUSINDBK',
        
        # IT stocks with F&O
        'TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM', 'LTIM',
        
        # Auto stocks with F&O
        'TATAMOTORS', 'M&M', 'BAJAJ-AUTO', 'MARUTI', 'EICHERMOT', 'TVSMOTOR',
        
        # Heavy weights
        'RELIANCE', 'ITC', 'HINDUNILVR', 'LT', 'BHARTIARTL',
        
        # Metal & Energy
        'TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'ONGC', 'BPCL', 'NTPC',
        
        # Pharma with F&O
        'SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB',
        
        # Other liquid F&O
        'BAJFINANCE', 'TITAN', 'ASIANPAINT', 'ADANIPORTS', 'COALINDIA'
    ],
    
    'BANK_NIFTY_FO': [
        'HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK', 
        'INDUSINDBK', 'BANDHANBNK', 'FEDERALBNK', 'PNB', 'CANBK'
    ],
    
    'NIFTY_50_FO': [
        # All NIFTY 50 stocks have F&O
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR',
        'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK', 'LT', 'AXISBANK',
        'ASIANPAINT', 'MARUTI', 'HCLTECH', 'BAJFINANCE', 'TITAN',
        'SUNPHARMA', 'ULTRACEMCO', 'ONGC', 'TECHM', 'NESTLEIND',
        'TATAMOTORS', 'WIPRO', 'NTPC', 'POWERGRID', 'M&M', 'BAJAJFINSV',
        'TATASTEEL', 'JSWSTEEL', 'ADANIENT', 'INDUSINDBK', 'COALINDIA',
        'DRREDDY', 'HINDALCO', 'GRASIM', 'CIPLA', 'TATACONSUM',
        'BRITANNIA', 'DIVISLAB', 'EICHERMOT', 'HEROMOTOCO', 'SHRIRAMFIN',
        'ADANIPORTS', 'APOLLOHOSP', 'BAJAJ-AUTO', 'HDFCLIFE', 'SBILIFE',
        'BPCL', 'TRENT'
    ]
}


# ============================================================================
# F&O-SPECIFIC SCREENING
# ============================================================================

class FOStockScreener(StockScreener):
    """
    Enhanced screener for F&O stocks with stricter liquidity requirements
    """
    
    def __init__(self, start_date: str, end_date: str):
        super().__init__(start_date, end_date)
        self.fo_stocks_only = True
    
    def apply_fo_liquidity_filter(self, stocks: list, 
                                   min_volume: float = 1_000_000,  # 10 lakh shares (stricter)
                                   min_value: float = 100_00_00_000) -> list:  # ₹100 crore (stricter)
        """
        F&O-specific liquidity filter with higher thresholds
        F&O stocks need higher liquidity for options trading
        """
        print("\n🔍 Applying F&O Liquidity Filter (Stricter)...")
        print(f"   Min Volume: {min_volume:,.0f} shares/day (10 lakh+)")
        print(f"   Min Value Traded: ₹{min_value/1e7:.0f} crore/day (100 crore+)")
        
        return self.apply_liquidity_filter(stocks, min_volume, min_value)
    
    def calculate_iv_percentile(self, data: pd.DataFrame, period: int = 252) -> float:
        """
        Calculate Implied Volatility percentile (approximate using ATR)
        Useful for options traders
        """
        atr = self.calculate_atr(data)
        if len(atr) < period:
            period = len(atr)
        
        current_atr = atr.iloc[-1]
        historical_atrs = atr.tail(period)
        
        percentile = (historical_atrs < current_atr).sum() / len(historical_atrs) * 100
        return percentile
    
    def get_fo_metrics(self, stock: str) -> dict:
        """
        Get F&O-specific metrics for a stock
        """
        try:
            symbol = f"{stock}.NS"
            data = yf.download(symbol, start=self.start_date, end=self.end_date,
                             progress=False, show_errors=False)
            
            if data.empty or len(data) < 50:
                return None
            
            # Calculate metrics
            close = data['Close'].iloc[-1]
            atr = self.calculate_atr(data).iloc[-1]
            atr_pct = (atr / close) * 100
            
            # Volume metrics
            avg_volume = data['Volume'].mean()
            recent_volume = data['Volume'].tail(5).mean()
            volume_trend = (recent_volume / avg_volume - 1) * 100
            
            # Volatility percentile
            iv_percentile = self.calculate_iv_percentile(data)
            
            # Price momentum
            price_change_20d = ((close / data['Close'].iloc[-20] - 1) * 100 
                               if len(data) >= 20 else 0)
            
            return {
                'stock': stock,
                'close': close,
                'atr': atr,
                'atr_pct': atr_pct,
                'avg_volume': avg_volume,
                'volume_trend': volume_trend,
                'iv_percentile': iv_percentile,
                'price_change_20d': price_change_20d,
                'fo_suitable': atr_pct > 1.5  # Minimum volatility for F&O
            }
            
        except Exception:
            return None


# ============================================================================
# F&O-FOCUSED FUNCTIONS
# ============================================================================

def screen_fo_stocks(fo_category: str = 'HIGHLY_LIQUID_FO',
                     trading_type: str = 'swing',
                     start_date: str = None,
                     end_date: str = None):
    """
    Screen F&O stocks with enhanced filters
    
    Args:
        fo_category: 'HIGHLY_LIQUID_FO', 'BANK_NIFTY_FO', 'NIFTY_50_FO'
        trading_type: 'swing' or 'intraday'
        start_date: Start date for analysis
        end_date: End date for analysis
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"   F&O STOCK SCREENING")
    print(f"   Category: {fo_category}")
    print(f"   Trading Type: {trading_type.upper()}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"{'='*80}")
    
    # Get F&O stocks
    fo_stocks = NSE_FO_STOCKS.get(fo_category, [])
    if not fo_stocks:
        print(f"\n❌ Invalid F&O category: {fo_category}")
        print(f"Available: {', '.join(NSE_FO_STOCKS.keys())}")
        return None
    
    print(f"\n📝 Screening {len(fo_stocks)} F&O stocks...")
    
    # Initialize F&O screener
    screener = FOStockScreener(start_date, end_date)
    
    # Apply F&O liquidity filter (stricter)
    liquid_stocks = screener.apply_fo_liquidity_filter(fo_stocks)
    
    if not liquid_stocks:
        print("\n⚠️  No F&O stocks passed liquidity filter!")
        return None
    
    # Get F&O metrics for all candidates
    print(f"\n📊 Analyzing F&O metrics...")
    fo_candidates = []
    
    for stock in liquid_stocks:
        metrics = screener.get_fo_metrics(stock)
        if metrics and metrics['fo_suitable']:
            fo_candidates.append(metrics)
    
    if not fo_candidates:
        print("\n⚠️  No stocks suitable for F&O trading!")
        return None
    
    # Sort by liquidity and volatility
    df = pd.DataFrame(fo_candidates)
    df = df.sort_values(['avg_volume', 'atr_pct'], ascending=[False, False])
    
    # Display results
    print(f"\n{'='*80}")
    print(f"   F&O TRADING CANDIDATES ({len(fo_candidates)} stocks)")
    print(f"{'='*80}\n")
    
    display_df = df[['stock', 'close', 'atr_pct', 'volume_trend', 
                     'iv_percentile', 'price_change_20d']].head(20)
    
    display_df.columns = ['Stock', 'Close (₹)', 'ATR %', 'Vol Trend %', 
                          'IV %ile', '20d Change %']
    
    print(display_df.to_string(index=False, float_format='%.2f'))
    
    print(f"\n{'='*80}")
    print("\n💡 F&O Trading Insights:")
    print(f"   • High IV Percentile (>75) = Good for option selling")
    print(f"   • Low IV Percentile (<25) = Good for option buying")
    print(f"   • High ATR% (>3%) = Better option premiums")
    print(f"   • Volume Trend >0 = Increasing participation")
    print(f"\n{'='*80}")
    
    return fo_candidates


def get_fo_stock_details(stock: str):
    """
    Get detailed F&O information for a specific stock
    """
    print(f"\n{'='*80}")
    print(f"   F&O STOCK ANALYSIS: {stock}")
    print(f"{'='*80}")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    screener = FOStockScreener(start_date, end_date)
    metrics = screener.get_fo_metrics(stock)
    
    if not metrics:
        print(f"\n❌ Could not fetch data for {stock}")
        return None
    
    print(f"\n📊 CURRENT METRICS:")
    print(f"   Price:              ₹{metrics['close']:,.2f}")
    print(f"   ATR:                ₹{metrics['atr']:,.2f}")
    print(f"   ATR %:              {metrics['atr_pct']:.2f}%")
    print(f"   Avg Volume:         {metrics['avg_volume']:,.0f} shares")
    print(f"   Volume Trend:       {metrics['volume_trend']:+.1f}%")
    print(f"   IV Percentile:      {metrics['iv_percentile']:.1f}%")
    print(f"   20-day Change:      {metrics['price_change_20d']:+.2f}%")
    
    print(f"\n💡 F&O SUITABILITY:")
    if metrics['fo_suitable']:
        print(f"   ✅ Suitable for F&O trading")
    else:
        print(f"   ⚠️  Low volatility for F&O (ATR < 1.5%)")
    
    # Options strategy suggestions
    print(f"\n🎯 SUGGESTED OPTIONS STRATEGIES:")
    
    if metrics['iv_percentile'] > 75:
        print(f"   • High IV → Consider SELLING options")
        print(f"     - Short Straddle (if neutral)")
        print(f"     - Short Strangle (if range-bound)")
        print(f"     - Covered Call (if holding stock)")
    
    elif metrics['iv_percentile'] < 25:
        print(f"   • Low IV → Consider BUYING options")
        print(f"     - Long Straddle (expecting big move)")
        print(f"     - Long Call/Put (directional)")
        print(f"     - Bull/Bear Spread")
    
    else:
        print(f"   • Mid IV → Neutral strategies")
        print(f"     - Iron Condor")
        print(f"     - Butterfly")
        print(f"     - Calendar Spread")
    
    # Futures lot size approximation
    if metrics['close'] > 0:
        approx_lot_value = metrics['close'] * 500  # Typical lot size
        print(f"\n📦 LOT SIZE ESTIMATE:")
        print(f"   Approx lot value:   ₹{approx_lot_value:,.0f} (assuming 500 qty)")
        print(f"   Margin required:    ~₹{approx_lot_value * 0.15:,.0f} (15% approx)")
    
    print(f"\n{'='*80}")
    
    return metrics


def backtest_fo_stock_with_sector_strategy(stock: str, 
                                           sector: str = None,
                                           start_date: str = None,
                                           end_date: str = None):
    """
    Backtest F&O stock using appropriate sector strategy
    
    If sector not specified, auto-detects from NSE_SECTORS
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Auto-detect sector if not provided
    if not sector:
        for sector_name, sector_info in NSE_SECTORS.items():
            if stock in sector_info['stocks']:
                sector = sector_name
                break
        
        if not sector:
            print(f"⚠️  Could not auto-detect sector for {stock}")
            print(f"   Please specify sector manually")
            return None
    
    print(f"\n🎯 Backtesting F&O Stock with Sector Strategy")
    print(f"   Stock: {stock}")
    print(f"   Sector: {sector}")
    print(f"   Strategy: Optimized for {sector} characteristics\n")
    
    # Run backtest using sector framework
    results = run_sector_backtest(
        sector=sector,
        stock=stock,
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000  # ₹1 lakh
    )
    
    return results


def compare_fo_stocks_in_sector(sector: str, top_n: int = 5):
    """
    Compare top F&O stocks within a sector
    """
    print(f"\n{'='*80}")
    print(f"   COMPARING F&O STOCKS IN {sector}")
    print(f"{'='*80}")
    
    # Get sector stocks
    sector_info = NSE_SECTORS.get(sector)
    if not sector_info:
        print(f"\n❌ Invalid sector: {sector}")
        return None
    
    sector_stocks = sector_info['stocks']
    
    # Filter to only F&O stocks
    fo_stocks_all = set()
    for fo_list in NSE_FO_STOCKS.values():
        fo_stocks_all.update(fo_list)
    
    fo_stocks_in_sector = [s for s in sector_stocks if s in fo_stocks_all]
    
    if not fo_stocks_in_sector:
        print(f"\n⚠️  No F&O stocks found in {sector}")
        return None
    
    print(f"\n📊 Found {len(fo_stocks_in_sector)} F&O stocks in sector")
    print(f"   Comparing top {min(top_n, len(fo_stocks_in_sector))}...\n")
    
    # Backtest each stock
    results_list = []
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    for stock in fo_stocks_in_sector[:top_n]:
        try:
            print(f"Testing {stock}...")
            
            results = run_sector_backtest(
                sector=sector,
                stock=stock,
                start_date=start_date,
                end_date=end_date,
                initial_capital=100000
            )
            
            if results:
                metrics = results['metrics']
                results_list.append({
                    'Stock': stock,
                    'Return (%)': metrics['Total Return (%)'],
                    'Sharpe': metrics['Sharpe Ratio'],
                    'Max DD (%)': metrics['Max Drawdown (%)'],
                    'Win Rate (%)': metrics['Win Rate (%)'],
                    'Trades': metrics['Total Trades']
                })
                print(f"✅ {stock}: {metrics['Total Return (%)']:.2f}%\n")
            
        except Exception as e:
            print(f"❌ Error with {stock}: {e}\n")
    
    if not results_list:
        print("\n⚠️  No successful backtests")
        return None
    
    # Display comparison
    df = pd.DataFrame(results_list).sort_values('Return (%)', ascending=False)
    
    print(f"\n{'='*80}")
    print(f"   F&O STOCK COMPARISON - {sector}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"{'='*80}\n")
    
    print(df.to_string(index=False))
    print(f"\n{'='*80}")
    
    return results_list


def interactive_fo_menu():
    """
    Interactive menu for F&O stock trading
    """
    print("\n" + "="*80)
    print("   NSE F&O STOCK TRADING FRAMEWORK")
    print("="*80)
    print("\n🎯 Features:")
    print("   • Focus on high-liquidity F&O stocks")
    print("   • Sector-specific strategies applied")
    print("   • F&O-specific metrics (IV percentile, ATR)")
    print("   • Options strategy suggestions")
    print("="*80 + "\n")
    
    while True:
        print("\n📋 F&O TRADING MENU:")
        print("   1. Screen F&O stocks by category")
        print("   2. Get detailed F&O analysis for a stock")
        print("   3. Backtest F&O stock with sector strategy")
        print("   4. Compare F&O stocks within a sector")
        print("   5. Show F&O categories and stocks")
        print("   6. Run sector framework (all features)")
        print("   7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            # Screen F&O stocks
            print("\n📊 F&O Categories:")
            for i, category in enumerate(NSE_FO_STOCKS.keys(), 1):
                count = len(NSE_FO_STOCKS[category])
                print(f"   {i}. {category} ({count} stocks)")
            
            cat_choice = input("\nEnter category number: ").strip()
            try:
                cat_idx = int(cat_choice) - 1
                category = list(NSE_FO_STOCKS.keys())[cat_idx]
                
                trading_type = input("Trading type (swing/intraday) [default: swing]: ").strip().lower()
                if trading_type not in ['swing', 'intraday']:
                    trading_type = 'swing'
                
                screen_fo_stocks(category, trading_type)
                
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
        
        elif choice == '2':
            # Get stock details
            stock = input("\nEnter F&O stock symbol (e.g., RELIANCE, TCS): ").strip().upper()
            if stock:
                get_fo_stock_details(stock)
        
        elif choice == '3':
            # Backtest stock
            stock = input("\nEnter F&O stock symbol: ").strip().upper()
            
            print("\n📊 Available Sectors:")
            for i, sector in enumerate(NSE_SECTORS.keys(), 1):
                print(f"   {i}. {sector}")
            
            sector_choice = input("\nEnter sector number (or press Enter to auto-detect): ").strip()
            
            sector = None
            if sector_choice:
                try:
                    sector_idx = int(sector_choice) - 1
                    sector = list(NSE_SECTORS.keys())[sector_idx]
                except (ValueError, IndexError):
                    print("❌ Invalid sector, will auto-detect")
            
            if stock:
                backtest_fo_stock_with_sector_strategy(stock, sector)
        
        elif choice == '4':
            # Compare stocks in sector
            print("\n📊 Available Sectors:")
            for i, sector in enumerate(NSE_SECTORS.keys(), 1):
                print(f"   {i}. {sector}")
            
            sector_choice = input("\nEnter sector number: ").strip()
            try:
                sector_idx = int(sector_choice) - 1
                sector = list(NSE_SECTORS.keys())[sector_idx]
                
                top_n = input("Number of stocks to compare [default: 5]: ").strip()
                top_n = int(top_n) if top_n else 5
                
                compare_fo_stocks_in_sector(sector, top_n)
                
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
        
        elif choice == '5':
            # Show F&O stocks
            print("\n" + "="*80)
            print("   F&O STOCK CATEGORIES")
            print("="*80)
            
            for category, stocks in NSE_FO_STOCKS.items():
                print(f"\n{category} ({len(stocks)} stocks):")
                print(f"   {', '.join(stocks[:15])}")
                if len(stocks) > 15:
                    print(f"   ... and {len(stocks)-15} more")
            
            print("\n" + "="*80)
        
        elif choice == '6':
            # Run main sector framework
            print("\n🔄 Launching full sector framework...")
            from nse_sector_strategy import interactive_menu
            interactive_menu()
            break
        
        elif choice == '7':
            print("\n👋 Thank you for using F&O Trading Framework!")
            print("="*80 + "\n")
            break
        
        else:
            print("❌ Invalid choice!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        interactive_fo_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please try again or report this issue.\n")

