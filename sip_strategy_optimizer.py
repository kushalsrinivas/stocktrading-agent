"""
SIP Strategy Optimizer

Analyzes all stocks from CSV, finds best strategy for each stock,
simulates SIP-style monthly investments, and visualizes results.

Usage:
    python sip_strategy_optimizer.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, YFinanceDataHandler
from strategies import (
    RSIBollingerStrategy,
    CombinedStrategy,
    MovingAverageCrossover,
    StochasticBreakoutStrategy,
    VWAPReversalStrategy,
    SupertrendMomentumStrategy,
    KeltnerSqueezeStrategy,
    WilliamsTrendStrategy,
    DonchianBreakoutStrategy,
    AggressiveDonchianStrategy,
    TurtleTradersStrategy
)
from strategies.momentum import RSIMomentumStrategy, MACDMomentumStrategy


class SIPStrategyOptimizer:
    """
    SIP Strategy Optimizer - Find best strategy for each stock and simulate SIP
    """
    
    def __init__(self, csv_file: str, monthly_investment: float = 10000):
        """
        Initialize optimizer
        
        Args:
            csv_file: Path to CSV file with stock data
            monthly_investment: Monthly SIP amount (default ₹10,000)
        """
        self.csv_file = csv_file
        self.monthly_investment = monthly_investment
        self.strategies = self._get_all_strategies()
        self.results = []
        
    def _get_all_strategies(self) -> Dict:
        """Get all available strategies"""
        return {
            'RSI + Bollinger': RSIBollingerStrategy(),
            'Combined': CombinedStrategy(),
            'MA Crossover': MovingAverageCrossover(short_window=20, long_window=50),
            'RSI Momentum': RSIMomentumStrategy(),
            'MACD Momentum': MACDMomentumStrategy(),
            'Stochastic Breakout': StochasticBreakoutStrategy(),
            'VWAP Reversal': VWAPReversalStrategy(),
            'Supertrend': SupertrendMomentumStrategy(),
            'Keltner Squeeze': KeltnerSqueezeStrategy(),
            'Williams Trend': WilliamsTrendStrategy(),
            'Donchian Breakout': DonchianBreakoutStrategy(entry_period=55, exit_period=20),
            'Donchian Fast': AggressiveDonchianStrategy(entry_period=20, exit_period=10),
            'Turtle Traders': TurtleTradersStrategy()
        }
    
    def load_stocks(self) -> pd.DataFrame:
        """Load stocks from CSV"""
        print(f"📂 Loading stocks from: {self.csv_file}")
        df = pd.read_csv(self.csv_file)
        print(f"✅ Loaded {len(df)} stocks")
        return df
    
    def find_best_strategy(self, symbol: str, start_date: str, end_date: str, 
                          verbose: bool = False) -> Tuple[str, Dict]:
        """
        Find best strategy for a single stock
        
        Returns:
            (best_strategy_name, results_dict)
        """
        nse_symbol = f"{symbol}.NS"
        best_strategy = None
        best_return = -np.inf
        best_results = None
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Testing: {symbol}")
            print(f"{'='*60}")
        
        for strategy_name, strategy in self.strategies.items():
            try:
                # Fetch data
                data_handler = YFinanceDataHandler(
                    symbol=nse_symbol,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Run backtest
                backtester = Backtester(
                    data_handler=data_handler,
                    strategy=strategy,
                    initial_capital=self.monthly_investment,
                    commission=0.0005,
                    slippage=0.0005
                )
                
                results = backtester.run(verbose=False)
                metrics = results['metrics']
                total_return = metrics['Total Return (%)']
                
                if verbose:
                    print(f"  {strategy_name:20s}: {total_return:>8.2f}%")
                
                # Track best strategy
                if total_return > best_return:
                    best_return = total_return
                    best_strategy = strategy_name
                    best_results = metrics
                    
            except Exception as e:
                if verbose:
                    print(f"  {strategy_name:20s}: Error - {str(e)[:30]}")
                continue
        
        if best_strategy:
            if verbose:
                print(f"\n  🏆 Best: {best_strategy} ({best_return:.2f}%)")
        
        return best_strategy, best_results
    
    def optimize_portfolio(self, stocks_df: pd.DataFrame, start_date: str, 
                          end_date: str, top_n: int = None, 
                          verbose: bool = True) -> pd.DataFrame:
        """
        Find best strategy for each stock
        
        Args:
            stocks_df: DataFrame with stock symbols
            start_date: Start date for backtesting
            end_date: End date for backtesting
            top_n: Number of top stocks to analyze (None = analyze ALL stocks)
            verbose: Print progress
            
        Returns:
            DataFrame with optimization results (filtered to stocks with trades > 0)
        """
        # Determine how many stocks to test
        total_stocks = len(stocks_df) if top_n is None else min(top_n, len(stocks_df))
        stocks_to_test = stocks_df.head(total_stocks) if top_n else stocks_df
        
        print(f"\n{'='*80}")
        print(f"🔍 OPTIMIZING PORTFOLIO: Testing {total_stocks} stocks")
        print(f"📅 Period: {start_date} to {end_date}")
        print(f"💰 Monthly SIP: ₹{self.monthly_investment:,.0f}")
        print(f"{'='*80}\n")
        
        results = []
        
        for idx, row in stocks_to_test.iterrows():
            symbol = row['Ticker']
            name = row['Name']
            
            print(f"[{idx+1}/{total_stocks}] Testing {symbol:12s} - {name[:40]:40s}", end=" ")
            
            try:
                best_strategy, metrics = self.find_best_strategy(
                    symbol, start_date, end_date, verbose=False
                )
                
                if best_strategy and metrics:
                    total_trades = metrics['Total Trades']
                    results.append({
                        'Symbol': symbol,
                        'Name': name,
                        'Sector': row.get('Sub-Sector', 'N/A'),
                        'Best Strategy': best_strategy,
                        'Total Return (%)': metrics['Total Return (%)'],
                        'Sharpe Ratio': metrics['Sharpe Ratio'],
                        'Max Drawdown (%)': metrics['Max Drawdown (%)'],
                        'Win Rate (%)': metrics['Win Rate (%)'],
                        'Total Trades': total_trades,
                        'Final Value': metrics['Final Value']
                    })
                    
                    if total_trades == 0:
                        print(f"⚠️  {best_strategy:20s} ({metrics['Total Return (%)']:>7.2f}%) - 0 trades (will be filtered)")
                    else:
                        print(f"✅ {best_strategy:20s} ({metrics['Total Return (%)']:>7.2f}%) - {total_trades} trades")
                else:
                    print(f"❌ No viable strategy found")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:40]}")
                continue
        
        results_df = pd.DataFrame(results)
        
        # Filter out stocks with 0 trades
        before_filter = len(results_df)
        results_df = results_df[results_df['Total Trades'] > 0]
        after_filter = len(results_df)
        
        print(f"\n{'='*80}")
        print(f"🎯 FILTERING RESULTS:")
        print(f"   Total stocks analyzed: {before_filter}")
        print(f"   Stocks with 0 trades (filtered out): {before_filter - after_filter}")
        print(f"   Stocks with active trades: {after_filter}")
        print(f"{'='*80}\n")
        
        return results_df
    
    def simulate_sip(self, optimized_df: pd.DataFrame, start_date: str, 
                    end_date: str, stocks_to_invest: int = 10) -> Dict:
        """
        Simulate SIP investment strategy
        
        Invests monthly SIP amount across top stocks with their best strategies
        
        Args:
            optimized_df: DataFrame with optimization results (already filtered for trades > 0)
            start_date: SIP start date
            end_date: SIP end date
            stocks_to_invest: Number of stocks in portfolio
            
        Returns:
            Dictionary with SIP simulation results
        """
        print(f"\n{'='*80}")
        print(f"💰 SIMULATING SIP INVESTMENT")
        print(f"{'='*80}\n")
        
        # Ensure we have enough stocks
        available_stocks = len(optimized_df)
        if available_stocks < stocks_to_invest:
            print(f"⚠️  Warning: Only {available_stocks} stocks available (requested {stocks_to_invest})")
            print(f"   Using all {available_stocks} stocks for portfolio\n")
            stocks_to_invest = available_stocks
        
        # Select top N stocks by return (already filtered for trades > 0)
        top_stocks = optimized_df.nlargest(stocks_to_invest, 'Total Return (%)')
        
        print(f"📊 Portfolio: Top {stocks_to_invest} stocks by return")
        print(f"💵 Monthly Investment: ₹{self.monthly_investment:,.0f}")
        print(f"📈 Per Stock: ₹{self.monthly_investment/stocks_to_invest:,.0f}\n")
        
        # Calculate monthly investment dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        months = []
        current = start
        while current <= end:
            months.append(current.strftime("%Y-%m-%d"))
            # Move to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        
        total_months = len(months)
        total_invested = self.monthly_investment * total_months
        
        print(f"📅 SIP Duration: {total_months} months")
        print(f"💰 Total Invested: ₹{total_invested:,.0f}\n")
        
        # Simulate investment
        portfolio_values = []
        monthly_details = []
        
        per_stock_investment = self.monthly_investment / stocks_to_invest
        
        for month_idx, month_date in enumerate(months):
            month_num = month_idx + 1
            month_invested = self.monthly_investment * month_num
            month_value = 0
            
            for _, stock in top_stocks.iterrows():
                # Simple simulation: apply return to invested amount
                # In reality, this would need actual price data at each SIP date
                stock_investment = per_stock_investment * month_num
                stock_return = stock['Total Return (%)'] / 100
                stock_value = stock_investment * (1 + stock_return)
                month_value += stock_value
            
            portfolio_values.append({
                'Month': month_num,
                'Date': month_date,
                'Invested': month_invested,
                'Value': month_value,
                'Gain/Loss': month_value - month_invested,
                'Return (%)': ((month_value - month_invested) / month_invested) * 100
            })
        
        portfolio_df = pd.DataFrame(portfolio_values)
        
        final_value = portfolio_df.iloc[-1]['Value']
        final_gain = final_value - total_invested
        final_return = (final_gain / total_invested) * 100
        
        # Calculate XIRR (approximation using average monthly return)
        avg_monthly_return = portfolio_df['Return (%)'].mean()
        annualized_return = ((1 + avg_monthly_return/100) ** 12 - 1) * 100
        
        results = {
            'portfolio': top_stocks,
            'monthly_values': portfolio_df,
            'total_invested': total_invested,
            'final_value': final_value,
            'total_gain': final_gain,
            'total_return_pct': final_return,
            'annualized_return': annualized_return,
            'months': total_months
        }
        
        return results
    
    def plot_results(self, sip_results: Dict, save_path: str = None):
        """
        Create visualization of SIP results
        
        Args:
            sip_results: Results from simulate_sip()
            save_path: Optional path to save plot
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        monthly_df = sip_results['monthly_values']
        portfolio = sip_results['portfolio']
        
        # 1. Portfolio Value Over Time
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(monthly_df['Month'], monthly_df['Invested'], 
                label='Total Invested', linewidth=2, linestyle='--', color='gray')
        ax1.plot(monthly_df['Month'], monthly_df['Value'], 
                label='Portfolio Value', linewidth=3, color='#2ecc71')
        ax1.fill_between(monthly_df['Month'], monthly_df['Invested'], 
                         monthly_df['Value'], alpha=0.3, color='#2ecc71')
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Amount (₹)', fontsize=12)
        ax1.set_title('SIP Portfolio Growth Over Time', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        # 2. Gain/Loss Over Time
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in monthly_df['Gain/Loss']]
        ax2.bar(monthly_df['Month'], monthly_df['Gain/Loss'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Gain/Loss (₹)', fontsize=12)
        ax2.set_title('Monthly Gain/Loss', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        # 3. Return % Over Time
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(monthly_df['Month'], monthly_df['Return (%)'], 
                linewidth=2, color='#3498db', marker='o', markersize=4)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax3.fill_between(monthly_df['Month'], 0, monthly_df['Return (%)'], 
                         alpha=0.3, color='#3498db')
        ax3.set_xlabel('Month', fontsize=12)
        ax3.set_ylabel('Return (%)', fontsize=12)
        ax3.set_title('Portfolio Return % Over Time', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Stock Performance
        ax4 = fig.add_subplot(gs[2, 0])
        stock_returns = portfolio.nlargest(10, 'Total Return (%)')[['Symbol', 'Total Return (%)']]
        colors_stocks = ['#2ecc71' if x > 0 else '#e74c3c' for x in stock_returns['Total Return (%)']]
        ax4.barh(stock_returns['Symbol'], stock_returns['Total Return (%)'], 
                color=colors_stocks, alpha=0.7)
        ax4.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax4.set_xlabel('Return (%)', fontsize=12)
        ax4.set_title('Top 10 Stocks by Return', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')
        
        # 5. Strategy Distribution
        ax5 = fig.add_subplot(gs[2, 1])
        strategy_counts = portfolio['Best Strategy'].value_counts()
        colors_pie = plt.cm.Set3(range(len(strategy_counts)))
        wedges, texts, autotexts = ax5.pie(strategy_counts.values, 
                                            labels=strategy_counts.index,
                                            autopct='%1.1f%%',
                                            colors=colors_pie,
                                            startangle=90)
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        ax5.set_title('Strategy Distribution in Portfolio', fontsize=14, fontweight='bold')
        
        # Add summary text
        summary_text = f"""
SIP SUMMARY
═══════════════════════════════════
Total Invested:    ₹{sip_results['total_invested']:>12,.0f}
Final Value:       ₹{sip_results['final_value']:>12,.0f}
Total Gain:        ₹{sip_results['total_gain']:>12,.0f}
Total Return:      {sip_results['total_return_pct']:>12.2f}%
Annualized Return: {sip_results['annualized_return']:>12.2f}%
Duration:          {sip_results['months']:>12} months
        """
        
        fig.text(0.02, 0.02, summary_text, fontsize=10, 
                family='monospace', verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.suptitle('📈 SIP Strategy Optimizer - Performance Dashboard', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n💾 Chart saved to: {save_path}")
        
        plt.show()
    
    def print_summary(self, optimized_df: pd.DataFrame, sip_results: Dict):
        """Print detailed summary of results"""
        print(f"\n{'='*80}")
        print(f"📊 OPTIMIZATION SUMMARY (Stocks with Active Trades Only)")
        print(f"{'='*80}\n")
        
        print(f"Total Stocks with Active Trades: {len(optimized_df)}")
        print(f"Profitable Strategies: {len(optimized_df[optimized_df['Total Return (%)'] > 0])}")
        print(f"Average Return: {optimized_df['Total Return (%)'].mean():.2f}%")
        print(f"Median Return: {optimized_df['Total Return (%)'].median():.2f}%")
        print(f"Best Return: {optimized_df['Total Return (%)'].max():.2f}%")
        print(f"Worst Return: {optimized_df['Total Return (%)'].min():.2f}%")
        print(f"Average Trades per Stock: {optimized_df['Total Trades'].mean():.1f}\n")
        
        # Strategy distribution
        print("Strategy Distribution:")
        strategy_dist = optimized_df['Best Strategy'].value_counts()
        for strategy, count in strategy_dist.items():
            pct = (count / len(optimized_df)) * 100
            print(f"  {strategy:25s}: {count:3d} stocks ({pct:5.1f}%)")
        
        print(f"\n{'='*80}")
        print(f"💰 SIP INVESTMENT RESULTS")
        print(f"{'='*80}\n")
        
        portfolio = sip_results['portfolio']
        
        print(f"Portfolio Composition ({len(portfolio)} stocks):\n")
        print(f"{'Symbol':12s} {'Name':30s} {'Strategy':20s} {'Return':>10s}")
        print(f"{'-'*80}")
        for _, stock in portfolio.iterrows():
            print(f"{stock['Symbol']:12s} {stock['Name'][:28]:30s} "
                  f"{stock['Best Strategy']:20s} {stock['Total Return (%)']:>9.2f}%")
        
        print(f"\n{'='*80}")
        print(f"💵 FINANCIAL SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Monthly SIP Amount:    ₹{self.monthly_investment:>12,.0f}")
        print(f"Investment Duration:   {sip_results['months']:>12} months")
        print(f"Total Amount Invested: ₹{sip_results['total_invested']:>12,.0f}")
        print(f"Final Portfolio Value: ₹{sip_results['final_value']:>12,.0f}")
        print(f"{'─'*80}")
        
        gain_loss_symbol = "📈" if sip_results['total_gain'] > 0 else "📉"
        print(f"Total Gain/Loss:       ₹{sip_results['total_gain']:>12,.0f} {gain_loss_symbol}")
        print(f"Total Return:          {sip_results['total_return_pct']:>12.2f}%")
        print(f"Annualized Return:     {sip_results['annualized_return']:>12.2f}%")
        
        print(f"\n{'='*80}\n")


def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("   📈 SIP STRATEGY OPTIMIZER 📈")
    print("="*80)
    print("\nThis tool will:")
    print("  1. Analyze all stocks in your CSV")
    print("  2. Find the best strategy for each stock")
    print("  3. Simulate a monthly SIP investment")
    print("  4. Show you detailed charts and results")
    print("\n" + "="*80 + "\n")
    
    # Get user inputs
    print("📋 Configuration:\n")
    
    csv_file = input("1. Enter CSV file path [default: data/Stock_Screener_03_12_2025.csv]: ").strip()
    if not csv_file:
        csv_file = "data/Stock_Screener_03_12_2025.csv"
    
    monthly_sip = input("2. Enter monthly SIP amount [default: ₹10,000]: ").strip()
    if not monthly_sip:
        monthly_sip = 10000
    else:
        monthly_sip = float(monthly_sip)
    
    # Date range
    print("\n📅 Date Range:")
    end_date = datetime.now().strftime("%Y-%m-%d")
    default_start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    date_choice = input(f"3. Use last 1 year? (Y/n) [default: {default_start} to {end_date}]: ").strip().lower()
    
    if date_choice == 'n':
        start_date = input("   Enter start date (YYYY-MM-DD): ").strip()
        end_date_input = input("   Enter end date (YYYY-MM-DD): ").strip()
        if end_date_input:
            end_date = end_date_input
    else:
        start_date = default_start
    
    # Number of stocks to analyze
    analyze_all = input("\n4. Analyze ALL stocks in CSV? (Y/n) [default: Yes]: ").strip().lower()
    if analyze_all == 'n':
        top_n = input("   How many top stocks to analyze? [default: 50]: ").strip()
        if not top_n:
            top_n = 50
        else:
            top_n = int(top_n)
    else:
        top_n = None  # None means analyze all stocks
    
    # Number of stocks in SIP portfolio
    portfolio_size = input("5. How many stocks in SIP portfolio? [default: 10]: ").strip()
    if not portfolio_size:
        portfolio_size = 10
    else:
        portfolio_size = int(portfolio_size)
    
    print("\n" + "="*80)
    print("✅ Configuration Complete!")
    print(f"   CSV File: {csv_file}")
    print(f"   Monthly SIP: ₹{monthly_sip:,.0f}")
    print(f"   Date Range: {start_date} to {end_date}")
    print(f"   Stocks to Analyze: {'ALL stocks in CSV' if top_n is None else top_n}")
    print(f"   Portfolio Size: {portfolio_size}")
    print("="*80 + "\n")
    
    proceed = input("Proceed with analysis? (Y/n): ").strip().lower()
    if proceed == 'n':
        print("\n❌ Analysis cancelled.")
        return
    
    # Initialize optimizer
    optimizer = SIPStrategyOptimizer(csv_file, monthly_sip)
    
    # Load stocks
    stocks_df = optimizer.load_stocks()
    
    # Optimize portfolio
    optimized_df = optimizer.optimize_portfolio(
        stocks_df, start_date, end_date, top_n=top_n, verbose=True
    )
    
    if len(optimized_df) == 0:
        print("\n❌ No stocks could be analyzed successfully. Exiting.")
        return
    
    # Simulate SIP
    sip_results = optimizer.simulate_sip(
        optimized_df, start_date, end_date, stocks_to_invest=portfolio_size
    )
    
    # Print summary
    optimizer.print_summary(optimized_df, sip_results)
    
    # Save results
    print("💾 Saving results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    optimized_df.to_csv(f"sip_optimization_results_{timestamp}.csv", index=False)
    print(f"✅ Results saved to: sip_optimization_results_{timestamp}.csv")
    
    # Plot results
    plot_choice = input("\n📊 Show charts? (Y/n): ").strip().lower()
    if plot_choice != 'n':
        chart_file = f"sip_portfolio_chart_{timestamp}.png"
        optimizer.plot_results(sip_results, save_path=chart_file)
    
    print("\n" + "="*80)
    print("✅ Analysis Complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

