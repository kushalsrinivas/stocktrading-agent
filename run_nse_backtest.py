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

# Import new advanced strategies
from strategies import (
    StochasticBreakoutStrategy,
    VWAPReversalStrategy,
    SupertrendMomentumStrategy,
    KeltnerSqueezeStrategy,
    WilliamsTrendStrategy,
    DonchianBreakoutStrategy,
    AggressiveDonchianStrategy,
    TurtleTradersStrategy,
    TrendLineStrategy,
    TrendLineBreakoutStrategy,
    SupportResistanceBounceStrategy,
    SupportResistanceBreakoutStrategy,
    SRRSIStrategy,
    SRVolumeStrategy,
    SREMAStrategy,
    SRMACDStrategy,
    SRAllInOneStrategy
)


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("   NSE STOCK BACKTESTING - 22 STRATEGIES AVAILABLE")
    print("="*70)
    print("\n💰 Initial Capital: ₹10,000")
    print("📈 Commission: 0.05% (typical discount broker)")
    print("🔥 New: Advanced S/R Strategies with Multiple Confirmations!")
    print("="*70 + "\n")


def get_strategy_choice():
    """Let user choose a strategy"""
    print("\n📊 Available Strategies:\n")
    print("   === CLASSIC STRATEGIES ===")
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
    print()
    print("   === ADVANCED STRATEGIES (NEW!) ===")
    print("   6. Stochastic Breakout (Momentum/Breakout)")
    print("      • Primary: Stochastic Oscillator")
    print("      • Confirmation: Volume Spike + ADX")
    print()
    print("   7. VWAP Reversal (Mean Reversion)")
    print("      • Primary: VWAP")
    print("      • Confirmation: RSI Divergence + Volume")
    print()
    print("   8. Supertrend Momentum (Trend Following)")
    print("      • Primary: Supertrend (ATR-based)")
    print("      • Confirmation: MACD + EMA Slope")
    print()
    print("   9. Keltner Squeeze (Breakout/Volatility)")
    print("      • Primary: Keltner Channels")
    print("      • Confirmation: BB Width + Momentum")
    print()
    print("   10. Williams Trend (Momentum/Trend)")
    print("       • Primary: Williams %R")
    print("       • Confirmation: ADX + Volume")
    print()
    print("   === DONCHIAN BREAKOUT STRATEGIES (NEW!) ===")
    print("   11. Donchian Breakout - Classic (Trend Following)")
    print("       • Entry: 55-day high/low breakout")
    print("       • Exit: 20-day channel")
    print("       • Pure trend-following system")
    print()
    print("   12. Donchian Fast - Aggressive (Swing Trading)")
    print("       • Entry: 20-day high/low breakout")
    print("       • Exit: 10-day channel + ATR stops")
    print("       • Higher frequency, tighter stops")
    print()
    print("   13. Turtle Traders - Original System")
    print("       • Entry: 55-day breakout")
    print("       • Exit: 20-day low")
    print("       • Famous hedge fund strategy")
    print()
    print("   === TREND LINE & S/R STRATEGIES (NEW!) ===")
    print("   14. Trend Line Bounce (Technical)")
    print("       • Identifies trend lines via swing points")
    print("       • Buys bounces off ascending trend lines")
    print("       • Volume + ATR confirmation")
    print()
    print("   15. Trend Line Breakout (Momentum)")
    print("       • Trades breakouts through trend lines")
    print("       • Strong volume confirmation required")
    print("       • ATR-based stop loss")
    print()
    print("   16. Support/Resistance Bounce (Mean Reversion)")
    print("       • Identifies horizontal S/R levels")
    print("       • Buys at support, sells at resistance")
    print("       • Price clustering + volume profile")
    print()
    print("   17. Support/Resistance Breakout (Breakout)")
    print("       • Trades breakouts through S/R levels")
    print("       • High volume breakouts only")
    print("       • Level becomes new support/resistance")
    print()
    print("   === ADVANCED S/R STRATEGIES (NEW! 🔥) ===")
    print("   18. S/R + RSI (Momentum Confirmation)")
    print("       🔥 Most reliable for beginners!")
    print("       • Buy support when RSI oversold & curling up")
    print("       • Sell resistance when RSI overbought")
    print()
    print("   19. S/R + Volume (Breakout Strength)")
    print("       🔥 Best for breakout traders!")
    print("       • Only trades high-volume breakouts (>150%)")
    print("       • Filters fake breakouts")
    print()
    print("   20. S/R + 20/50 EMA (Trend Filter)")
    print("       🔥 Best intraday + swing combo!")
    print("       • Only buys support in uptrend (price > EMA)")
    print("       • Avoids counter-trend trades")
    print()
    print("   21. S/R + MACD (Trend Reversal)")
    print("       🔥 Catches reversals early!")
    print("       • Buy support + MACD bullish cross")
    print("       • Sell resistance + MACD bearish cross")
    print()
    print("   22. S/R All-in-One COMBO (Most Profitable)")
    print("       ⭐ Institutional-style setup!")
    print("       • 4 confirmations: S/R + RSI + EMA + Volume")
    print("       • Highest win rate strategy")
    
    while True:
        choice = input("\n   Choose strategy (1-22): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']:
            return int(choice)
        print("   ❌ Invalid choice. Please enter 1-22")


def create_strategy(choice):
    """Create strategy based on user choice"""
    strategies = {
        # Classic strategies
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
        )),
        
        # Advanced strategies (NEW!)
        6: ("Stochastic Breakout", StochasticBreakoutStrategy(
            stoch_period=14,
            stoch_oversold=20,
            stoch_overbought=80,
            adx_threshold=20,
            volume_spike_multiplier=1.3
        )),
        7: ("VWAP Reversal", VWAPReversalStrategy(
            vwap_deviation_threshold=1.5,
            rsi_period=14,
            rsi_oversold=35,
            rsi_overbought=65,
            volume_threshold=1.1
        )),
        8: ("Supertrend Momentum", SupertrendMomentumStrategy(
            atr_period=10,
            atr_multiplier=2.5,
            macd_fast=12,
            macd_slow=26,
            ema_period=20
        )),
        9: ("Keltner Squeeze", KeltnerSqueezeStrategy(
            kc_period=20,
            kc_atr_multiplier=2.0,
            bb_period=20,
            bb_std=2.0,
            momentum_threshold=1.0,
            volume_threshold=1.3
        )),
        10: ("Williams Trend", WilliamsTrendStrategy(
            williams_period=14,
            williams_oversold=-80,
            williams_overbought=-20,
            adx_strong_trend=20,
            volume_threshold=1.1
        )),
        
        # Donchian Breakout strategies (NEW!)
        11: ("Donchian Breakout", DonchianBreakoutStrategy(
            entry_period=55,
            exit_period=20,
            use_middle_band=True,
            atr_period=14
        )),
        12: ("Donchian Fast", AggressiveDonchianStrategy(
            entry_period=20,
            exit_period=10,
            atr_period=14,
            atr_multiplier=2.0
        )),
        13: ("Turtle Traders", TurtleTradersStrategy(
            entry_period=55,
            exit_period=20,
            atr_period=20,
            risk_per_trade=0.02
        )),
        
        # Trend Line & S/R strategies (NEW!)
        14: ("Trend Line Bounce", TrendLineStrategy(
            lookback_period=50,
            min_touches=2,
            bounce_tolerance=0.02,
            volume_confirmation=True,
            volume_threshold=1.2,
            atr_period=14,
            atr_multiplier=1.5,
            breakout_mode=False
        )),
        15: ("Trend Line Breakout", TrendLineBreakoutStrategy(
            lookback_period=40,
            min_touches=2,
            volume_threshold=1.5,
            atr_period=14,
            atr_multiplier=2.0
        )),
        16: ("Support/Resistance Bounce", SupportResistanceBounceStrategy(
            lookback_period=80,
            min_touches=3,
            volume_threshold=1.3
        )),
        17: ("Support/Resistance Breakout", SupportResistanceBreakoutStrategy(
            lookback_period=60,
            min_touches=2,
            volume_threshold=1.5
        )),
        
        # Advanced S/R strategies (NEW!)
        18: ("S/R + RSI", SRRSIStrategy(
            lookback_period=100,
            price_tolerance=0.02,
            min_touches=2,
            rsi_period=14,
            rsi_oversold=40,
            rsi_overbought=65,
            rsi_momentum_threshold=2.0,
            atr_period=14,
            atr_multiplier=1.5
        )),
        19: ("S/R + Volume", SRVolumeStrategy(
            lookback_period=80,
            price_tolerance=0.025,
            min_touches=2,
            volume_threshold=1.5,
            breakout_confirmation=0.01,
            atr_period=14,
            atr_multiplier=2.0
        )),
        20: ("S/R + EMA", SREMAStrategy(
            lookback_period=100,
            price_tolerance=0.02,
            min_touches=2,
            ema_fast=20,
            ema_slow=50,
            volume_confirmation=True,
            volume_threshold=1.2,
            atr_period=14,
            atr_multiplier=1.5
        )),
        21: ("S/R + MACD", SRMACDStrategy(
            lookback_period=100,
            price_tolerance=0.02,
            min_touches=2,
            macd_fast=12,
            macd_slow=26,
            macd_signal=9,
            atr_period=14,
            atr_multiplier=1.5
        )),
        22: ("S/R All-in-One COMBO", SRAllInOneStrategy(
            lookback_period=100,
            price_tolerance=0.02,
            min_touches=2,
            rsi_period=14,
            rsi_buy_min=30,
            rsi_buy_max=45,
            rsi_sell_min=60,
            rsi_sell_max=75,
            ema_fast=20,
            ema_slow=50,
            volume_threshold=1.3,
            atr_period=14,
            atr_multiplier=2.0
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


def calculate_trade_levels(entry_price, direction, risk_reward_ratio=2.0, risk_pct=0.02):
    """
    Calculate stop loss and target prices based on entry price
    
    Args:
        entry_price: Entry price for the trade
        direction: 'buy' or 'sell'
        risk_reward_ratio: Reward to risk ratio (default 2:1)
        risk_pct: Risk percentage (default 2%)
    
    Returns:
        tuple: (stop_loss, target_price)
    """
    if direction == 'buy':
        stop_loss = entry_price * (1 - risk_pct)
        target_price = entry_price * (1 + (risk_pct * risk_reward_ratio))
    else:  # sell/short
        stop_loss = entry_price * (1 + risk_pct)
        target_price = entry_price * (1 - (risk_pct * risk_reward_ratio))
    
    return stop_loss, target_price


def print_trade_details(trades_df, max_trades=10):
    """
    Print detailed trade information with entry, target, and stop loss
    
    Args:
        trades_df: DataFrame with trade history
        max_trades: Maximum number of trades to display
    """
    if trades_df.empty:
        return
    
    print("\n" + "="*70)
    print("   📋 TRADE DETAILS (Entry, Target, Stop Loss)")
    print("="*70)
    
    # Group buy and sell trades into pairs
    trade_pairs = []
    current_buy = None
    
    for idx, trade in trades_df.iterrows():
        if trade['Type'] == 'BUY':
            current_buy = trade
        elif trade['Type'] == 'SELL' and current_buy is not None:
            # Calculate stop loss and target for the buy trade
            entry_price = current_buy['Price']
            exit_price = trade['Price']
            stop_loss, target_price = calculate_trade_levels(entry_price, 'buy')
            
            pnl = exit_price - entry_price
            pnl_pct = (pnl / entry_price) * 100
            
            trade_pairs.append({
                'Entry Date': current_buy['Date'],
                'Exit Date': trade['Date'],
                'Entry Price': entry_price,
                'Stop Loss': stop_loss,
                'Target': target_price,
                'Exit Price': exit_price,
                'P&L': pnl,
                'P&L %': pnl_pct,
                'Outcome': 'Target Hit' if exit_price >= target_price else 'Stop Hit' if exit_price <= stop_loss else 'Exit'
            })
            current_buy = None
    
    if not trade_pairs:
        print("\n   No completed trade pairs found.\n")
        return
    
    # Display trades
    print(f"\n   Showing {min(len(trade_pairs), max_trades)} most recent trades:\n")
    
    trades_to_show = trade_pairs[-max_trades:] if len(trade_pairs) > max_trades else trade_pairs
    
    for i, trade in enumerate(reversed(trades_to_show), 1):
        outcome_emoji = "🎯" if trade['Outcome'] == 'Target Hit' else "🛑" if trade['Outcome'] == 'Stop Hit' else "📤"
        pnl_emoji = "✅" if trade['P&L'] > 0 else "❌"
        
        print(f"   Trade #{len(trade_pairs) - i + 1}  {outcome_emoji}")
        print(f"   ─────────────────────────────────────────")
        print(f"   Entry:  {trade['Entry Date'].strftime('%Y-%m-%d')}  @  ₹{trade['Entry Price']:>8,.2f}")
        print(f"   Target:                    ₹{trade['Target']:>8,.2f}  (+{((trade['Target']/trade['Entry Price']-1)*100):.1f}%)")
        print(f"   Stop:                      ₹{trade['Stop Loss']:>8,.2f}  (-{((1-trade['Stop Loss']/trade['Entry Price'])*100):.1f}%)")
        print(f"   Exit:   {trade['Exit Date'].strftime('%Y-%m-%d')}  @  ₹{trade['Exit Price']:>8,.2f}  {pnl_emoji}")
        print(f"   P&L:                       ₹{trade['P&L']:>8,.2f}  ({trade['P&L %']:+.2f}%)")
        print()
    
    # Summary statistics
    total_trades = len(trade_pairs)
    target_hits = sum(1 for t in trade_pairs if t['Outcome'] == 'Target Hit')
    stop_hits = sum(1 for t in trade_pairs if t['Outcome'] == 'Stop Hit')
    other_exits = sum(1 for t in trade_pairs if t['Outcome'] == 'Exit')
    
    print("   " + "─" * 66)
    print(f"   Trade Outcomes:")
    print(f"   🎯 Target Hit: {target_hits} ({target_hits/total_trades*100:.1f}%)")
    print(f"   🛑 Stop Hit:   {stop_hits} ({stop_hits/total_trades*100:.1f}%)")
    print(f"   📤 Other Exit: {other_exits} ({other_exits/total_trades*100:.1f}%)")
    print("\n" + "="*70)


def print_summary(symbol, strategy_name, results):
    """Print detailed results summary with trade details"""
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
    
    # Trade details with stop loss and target
    if metrics['Total Trades'] > 0 and 'trades' in results:
        print_trade_details(results['trades'])
    
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
        # Classic strategies
        (1, "RSI + Bollinger Bands"),
        (2, "Combined Strategy"),
        (3, "MA Crossover"),
        (4, "RSI Momentum"),
        (5, "MACD Momentum"),
        # Advanced strategies
        (6, "Stochastic Breakout"),
        (7, "VWAP Reversal"),
        (8, "Supertrend Momentum"),
        (9, "Keltner Squeeze"),
        (10, "Williams Trend"),
        # Donchian Breakout strategies
        (11, "Donchian Breakout"),
        (12, "Donchian Fast"),
        (13, "Turtle Traders"),
        # Trend Line & S/R strategies
        (14, "Trend Line Bounce"),
        (15, "Trend Line Breakout"),
        (16, "Support/Resistance Bounce"),
        (17, "Support/Resistance Breakout"),
        # Advanced S/R strategies
        (18, "S/R + RSI"),
        (19, "S/R + Volume"),
        (20, "S/R + EMA"),
        (21, "S/R + MACD"),
        (22, "S/R All-in-One COMBO")
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
    
    print("\n" + "="*120)
    print(f"   STRATEGY COMPARISON FOR {symbol}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"   Initial Capital: ₹10,000")
    print("="*120)
    
    # Sort by Total Return
    df_sorted = df.sort_values('Total Return (%)', ascending=False)
    
    print("\n📊 PERFORMANCE SUMMARY:\n")
    print(df_sorted.to_string(index=False))
    print("\n" + "="*120)
    
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
    
    print("\n" + "="*120)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:\n")
    
    profitable = df[df['Total Return (%)'] > 0]
    total_strategies = len(df)
    if len(profitable) > 0:
        print(f"   ✅ {len(profitable)} out of {total_strategies} strategies were profitable")
        print(f"\n   Top 5 Strategies by Return:")
        for i, row in enumerate(df_sorted.head(5).itertuples(), 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
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

