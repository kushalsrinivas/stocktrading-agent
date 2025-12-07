"""
Example API Client for Stock Backtesting API
Demonstrates how to use the API endpoints
"""

import requests
import json
from typing import Dict, List
import time

# API Base URL
BASE_URL = "http://localhost:8000"


class BacktestAPIClient:
    """Client wrapper for Backtest API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def health_check(self) -> Dict:
        """Check if API is healthy"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def list_strategies(self) -> Dict:
        """Get list of all available strategies"""
        response = requests.get(f"{self.base_url}/strategies")
        return response.json()
    
    def backtest_single(self, ticker: str, strategy: str, 
                       start_date: str = None, end_date: str = None,
                       initial_capital: float = 10000) -> Dict:
        """
        Run backtest for single ticker with single strategy
        
        Args:
            ticker: Stock symbol (e.g., 'RELIANCE', 'TCS')
            strategy: Strategy name (e.g., 'sr_all_in_one', 'supertrend')
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            initial_capital: Starting capital in INR
            
        Returns:
            Backtest results dict
        """
        payload = {
            "ticker": ticker,
            "strategy": strategy,
            "initial_capital": initial_capital
        }
        
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        
        response = requests.post(f"{self.base_url}/backtest", json=payload)
        return response.json()
    
    def compare_strategies(self, ticker: str, strategies: List[str] = None,
                          start_date: str = None, end_date: str = None,
                          initial_capital: float = 10000) -> Dict:
        """
        Compare multiple strategies on a single ticker
        
        Args:
            ticker: Stock symbol
            strategies: List of strategy names (None = test all)
            start_date: Start date (optional)
            end_date: End date (optional)
            initial_capital: Starting capital
            
        Returns:
            Comparison results dict
        """
        payload = {
            "ticker": ticker,
            "initial_capital": initial_capital
        }
        
        if strategies:
            payload["strategies"] = strategies
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        
        response = requests.post(f"{self.base_url}/compare", json=payload)
        return response.json()
    
    def test_multi_ticker(self, tickers: List[str], strategy: str,
                         start_date: str = None, end_date: str = None,
                         initial_capital: float = 10000) -> Dict:
        """
        Test multiple tickers with single strategy
        
        Args:
            tickers: List of stock symbols
            strategy: Strategy name
            start_date: Start date (optional)
            end_date: End date (optional)
            initial_capital: Starting capital
            
        Returns:
            Results for all tickers
        """
        payload = {
            "tickers": tickers,
            "strategy": strategy,
            "initial_capital": initial_capital
        }
        
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        
        response = requests.post(f"{self.base_url}/multi-ticker", json=payload)
        return response.json()
    
    def optimize(self, ticker: str, metric: str = "total_return",
                start_date: str = None, end_date: str = None,
                initial_capital: float = 10000) -> Dict:
        """
        Find best strategy for a ticker
        
        Args:
            ticker: Stock symbol
            metric: Optimization metric ('total_return', 'sharpe_ratio', 'win_rate')
            start_date: Start date (optional)
            end_date: End date (optional)
            initial_capital: Starting capital
            
        Returns:
            Best strategy and all results
        """
        payload = {
            "ticker": ticker,
            "metric": metric,
            "initial_capital": initial_capital
        }
        
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        
        response = requests.post(f"{self.base_url}/optimize", json=payload)
        return response.json()


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*70)
    print(f"   {title}")
    print("="*70 + "\n")


def example_1_single_backtest():
    """Example: Run single backtest"""
    print_section("EXAMPLE 1: Single Backtest")
    
    client = BacktestAPIClient()
    
    result = client.backtest_single(
        ticker="RELIANCE",
        strategy="sr_all_in_one",
        start_date="2023-01-01",
        end_date="2024-12-31",
        initial_capital=10000
    )
    
    if result['status'] == 'success':
        data = result['data']
        metrics = data['metrics']
        
        print(f"Ticker: {data['ticker']}")
        print(f"Strategy: {data['strategy']}")
        print(f"Period: {data['period']['start_date']} to {data['period']['end_date']}")
        print(f"\nResults:")
        print(f"  Initial Capital: ₹{metrics['initial_capital']:,.2f}")
        print(f"  Final Value:     ₹{metrics['final_value']:,.2f}")
        print(f"  Total Return:    {metrics['total_return_pct']:.2f}%")
        print(f"  Total Trades:    {metrics['total_trades']}")
        print(f"  Win Rate:        {metrics['win_rate_pct']:.2f}%")
        print(f"  Sharpe Ratio:    {metrics['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown:    {metrics['max_drawdown_pct']:.2f}%")
        
        # Show data availability for charting
        if 'historical_data' in data and data['historical_data']:
            print(f"\n📊 Chart Data Available:")
            print(f"  Historical Price Data: {len(data['historical_data'])} data points")
            print(f"  First Date: {data['historical_data'][0]['date']}")
            print(f"  Last Date:  {data['historical_data'][-1]['date']}")
            print(f"  Price Range: ₹{min(d['low'] for d in data['historical_data']):.2f} - ₹{max(d['high'] for d in data['historical_data']):.2f}")
        
        if 'equity_curve' in data and data['equity_curve']:
            print(f"  Equity Curve Data: {len(data['equity_curve'])} data points")
    else:
        print(f"Error: {result}")


def example_2_compare_strategies():
    """Example: Compare multiple strategies"""
    print_section("EXAMPLE 2: Compare Strategies")
    
    client = BacktestAPIClient()
    
    # Compare top 5 strategies
    strategies = ["sr_all_in_one", "sr_rsi", "sr_ema", "supertrend", "turtle_traders"]
    
    print(f"Comparing {len(strategies)} strategies on TCS...\n")
    
    result = client.compare_strategies(
        ticker="TCS",
        strategies=strategies,
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    if result['status'] == 'success':
        print(f"Best Strategy: {result['best_strategy']['name']}")
        print(f"  Total Return: {result['best_strategy']['total_return_pct']:.2f}%")
        print(f"  Sharpe Ratio: {result['best_strategy']['sharpe_ratio']:.2f}")
        print(f"  Win Rate:     {result['best_strategy']['win_rate_pct']:.2f}%")
        
        print(f"\nAll Results:")
        print(f"{'Strategy':<25} {'Return %':>10} {'Sharpe':>8} {'Win Rate %':>12} {'Trades':>8}")
        print("-" * 70)
        
        for r in result['results']:
            print(f"{r['strategy']:<25} "
                  f"{r['metrics']['total_return_pct']:>10.2f} "
                  f"{r['metrics']['sharpe_ratio']:>8.2f} "
                  f"{r['metrics']['win_rate_pct']:>12.2f} "
                  f"{r['metrics']['total_trades']:>8}")


def example_3_multi_ticker():
    """Example: Test multiple tickers"""
    print_section("EXAMPLE 3: Multiple Tickers")
    
    client = BacktestAPIClient()
    
    tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
    
    print(f"Testing {len(tickers)} tickers with S/R All-in-One strategy...\n")
    
    result = client.test_multi_ticker(
        tickers=tickers,
        strategy="sr_all_in_one",
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    if result['status'] == 'success':
        summary = result['summary']
        print(f"Summary:")
        print(f"  Total Tickers Tested: {summary['total_tickers_tested']}")
        print(f"  Average Return:       {summary['average_return_pct']:.2f}%")
        print(f"  Median Return:        {summary['median_return_pct']:.2f}%")
        print(f"  Best Ticker:          {summary['best_ticker']['ticker']} ({summary['best_ticker']['return_pct']:.2f}%)")
        
        print(f"\nDetailed Results:")
        print(f"{'Ticker':<12} {'Return %':>10} {'Sharpe':>8} {'Win Rate %':>12} {'Trades':>8}")
        print("-" * 60)
        
        for r in result['results']:
            print(f"{r['ticker']:<12} "
                  f"{r['metrics']['total_return_pct']:>10.2f} "
                  f"{r['metrics']['sharpe_ratio']:>8.2f} "
                  f"{r['metrics']['win_rate_pct']:>12.2f} "
                  f"{r['metrics']['total_trades']:>8}")


def example_4_optimize():
    """Example: Find best strategy for a ticker"""
    print_section("EXAMPLE 4: Optimize Strategy")
    
    client = BacktestAPIClient()
    
    print("Finding best strategy for INFY (this may take a minute)...\n")
    
    result = client.optimize(
        ticker="INFY",
        metric="total_return",
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    if result['status'] == 'success':
        best = result['best_strategy']
        
        print(f"Best Strategy: {best['name']}")
        print(f"\nMetrics:")
        print(f"  Total Return:  {best['metrics']['total_return_pct']:.2f}%")
        print(f"  Sharpe Ratio:  {best['metrics']['sharpe_ratio']:.2f}")
        print(f"  Win Rate:      {best['metrics']['win_rate_pct']:.2f}%")
        print(f"  Total Trades:  {best['metrics']['total_trades']}")
        print(f"  Max Drawdown:  {best['metrics']['max_drawdown_pct']:.2f}%")
        
        print(f"\nTop 5 Strategies:")
        print(f"{'Strategy':<25} {'Return %':>10} {'Sharpe':>8} {'Win Rate %':>12}")
        print("-" * 60)
        
        for s in result['top_5_strategies']:
            print(f"{s['name']:<25} "
                  f"{s['total_return_pct']:>10.2f} "
                  f"{s['sharpe_ratio']:>8.2f} "
                  f"{s['win_rate_pct']:>12.2f}")


def example_5_list_strategies():
    """Example: List all strategies"""
    print_section("EXAMPLE 5: List All Strategies")
    
    client = BacktestAPIClient()
    
    result = client.list_strategies()
    
    print(f"Total Strategies Available: {result['total_strategies']}\n")
    
    # Group by type
    by_type = {}
    for key, info in result['strategies'].items():
        strategy_type = info['type']
        if strategy_type not in by_type:
            by_type[strategy_type] = []
        by_type[strategy_type].append((key, info))
    
    for strategy_type, strategies in by_type.items():
        print(f"\n{strategy_type}:")
        print("-" * 60)
        for key, info in strategies:
            print(f"  • {info['name']} ({key})")
            print(f"    {info['description']}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("   📈 STOCK BACKTESTING API - CLIENT EXAMPLES")
    print("="*70)
    
    # Check if API is running
    try:
        client = BacktestAPIClient()
        health = client.health_check()
        print(f"\n✅ API is healthy (Status: {health['status']})")
    except Exception as e:
        print(f"\n❌ Error: Cannot connect to API at {BASE_URL}")
        print(f"   Make sure the API server is running: python api_server.py")
        return
    
    # Run examples
    try:
        example_5_list_strategies()
        
        print("\n\nPress Enter to continue to Example 1 (or Ctrl+C to exit)...")
        input()
        example_1_single_backtest()
        
        print("\n\nPress Enter to continue to Example 2 (or Ctrl+C to exit)...")
        input()
        example_2_compare_strategies()
        
        print("\n\nPress Enter to continue to Example 3 (or Ctrl+C to exit)...")
        input()
        example_3_multi_ticker()
        
        print("\n\nPress Enter to continue to Example 4 (or Ctrl+C to exit)...")
        input()
        example_4_optimize()
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    
    print("\n" + "="*70)
    print("✅ Examples Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

