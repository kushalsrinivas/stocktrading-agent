"""
Harmonic Pattern Recognition Strategy Example

This example demonstrates how to use harmonic pattern detection strategies.

Harmonic patterns are geometric price formations based on Fibonacci ratios.
They help identify potential reversal zones (PRZ) where price may reverse.

Pattern Types Supported:
1. Gartley - Classic harmonic pattern
2. Bat - Deep 88.6% retracement
3. Butterfly - D extends beyond X
4. Crab - Most precise, 161.8% extension
5. Cypher - Modified Fibonacci ratios

How It Works:
- Identifies 5 swing points: X → A → B → C → D
- Checks if Fibonacci ratios match known patterns
- Trades at D point (Potential Reversal Zone)
- Uses stop loss beyond D and Fibonacci-based profit targets
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Backtester, YFinanceDataHandler
from strategies.harmonic_patterns import HarmonicPatternStrategy, SimpleHarmonicStrategy


def example_1_simple_harmonic():
    """
    Example 1: Simple Harmonic Strategy (Beginner-Friendly)
    
    Uses only Gartley and Bat patterns with relaxed parameters.
    Good for learning harmonic trading concepts.
    """
    print("=" * 80)
    print("EXAMPLE 1: Simple Harmonic Strategy (Gartley & Bat Only)")
    print("=" * 80)
    print()
    
    # Setup data
    data_handler = YFinanceDataHandler(
        symbol="YATRA.NS",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # Create simple harmonic strategy
    strategy = SimpleHarmonicStrategy(
        lookback_period=80,           # Look back 80 bars for patterns
        zigzag_threshold=0.04,        # 4% minimum swing
        min_confidence=60.0,          # 60% minimum confidence
    )
    
    print(f"Strategy: {strategy}")
    print(f"Parameters: {strategy.parameters}")
    print()
    
    # Run backtest
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    print("Running backtest...")
    results = backtester.run()
    
    # Display results
    metrics = backtester.get_metrics()
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    
    # Visualize
    backtester.plot_results()
    
    return backtester


def example_2_all_patterns():
    """
    Example 2: Full Harmonic Strategy (All Patterns)
    
    Uses all 5 harmonic patterns: Gartley, Bat, Butterfly, Crab, Cypher.
    More pattern detection but requires stricter Fibonacci matching.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Full Harmonic Strategy (All 5 Patterns)")
    print("=" * 80)
    print()
    
    data_handler = YFinanceDataHandler(
        symbol="MSFT",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # Create full harmonic strategy
    strategy = HarmonicPatternStrategy(
        lookback_period=100,          # Look back 100 bars
        min_pattern_bars=20,          # Minimum 20 bars per pattern
        max_pattern_bars=80,          # Maximum 80 bars per pattern
        zigzag_threshold=0.03,        # 3% minimum swing
        ratio_tolerance=0.05,         # 5% Fibonacci ratio tolerance
        min_confidence=70.0,          # 70% minimum confidence
        use_gartley=True,
        use_bat=True,
        use_butterfly=True,
        use_crab=True,
        use_cypher=True,
        stop_loss_pct=0.02,           # 2% stop loss
        take_profit_1_pct=0.382,      # First target: 38.2% retracement
        take_profit_2_pct=0.618,      # Second target: 61.8% retracement
    )
    
    print(f"Strategy: {strategy}")
    print(f"Enabled Patterns: {strategy.parameters['patterns_enabled']}")
    print()
    
    # Run backtest
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    print("Running backtest...")
    results = backtester.run()
    
    # Display results
    metrics = backtester.get_metrics()
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    
    backtester.plot_results()
    
    return backtester


def example_3_aggressive_harmonic():
    """
    Example 3: Aggressive Harmonic Strategy
    
    Uses relaxed parameters to catch more patterns.
    Higher trade frequency but lower confidence requirements.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Aggressive Harmonic Strategy")
    print("=" * 80)
    print()
    
    data_handler = YFinanceDataHandler(
        symbol="GOOGL",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # Aggressive settings
    strategy = HarmonicPatternStrategy(
        lookback_period=80,
        min_pattern_bars=15,
        max_pattern_bars=60,
        zigzag_threshold=0.025,       # Lower threshold = more swings
        ratio_tolerance=0.08,         # More lenient ratio matching
        min_confidence=55.0,          # Lower confidence = more trades
        use_gartley=True,
        use_bat=True,
        use_butterfly=True,
        use_crab=False,               # Crab is rare
        use_cypher=False,             # Cypher is rare
        stop_loss_pct=0.025,
        take_profit_1_pct=0.382,
        take_profit_2_pct=0.618,
    )
    
    print(f"Strategy: {strategy}")
    print("Settings: Aggressive (Lower confidence, more patterns)")
    print()
    
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    print("Running backtest...")
    results = backtester.run()
    
    metrics = backtester.get_metrics()
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    
    backtester.plot_results()
    
    return backtester


def example_4_conservative_harmonic():
    """
    Example 4: Conservative Harmonic Strategy
    
    Strict Fibonacci matching, only trades highest confidence patterns.
    Lower trade frequency but higher quality setups.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Conservative Harmonic Strategy")
    print("=" * 80)
    print()
    
    data_handler = YFinanceDataHandler(
        symbol="TSLA",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # Conservative settings
    strategy = HarmonicPatternStrategy(
        lookback_period=120,          # Longer lookback
        min_pattern_bars=25,          # Longer minimum duration
        max_pattern_bars=100,
        zigzag_threshold=0.04,        # Higher threshold = fewer swings
        ratio_tolerance=0.03,         # Strict ratio matching
        min_confidence=80.0,          # High confidence only
        use_gartley=True,
        use_bat=True,
        use_butterfly=True,
        use_crab=True,
        use_cypher=True,
        stop_loss_pct=0.015,          # Tighter stop
        take_profit_1_pct=0.382,
        take_profit_2_pct=0.618,
    )
    
    print(f"Strategy: {strategy}")
    print("Settings: Conservative (High confidence, strict ratios)")
    print()
    
    backtester = Backtester(
        data_handler=data_handler,
        strategy=strategy,
        initial_capital=100000
    )
    
    print("Running backtest...")
    results = backtester.run()
    
    metrics = backtester.get_metrics()
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    
    backtester.plot_results()
    
    return backtester


def example_5_compare_patterns():
    """
    Example 5: Compare Different Pattern Types
    
    Runs separate backtests for each pattern type to see which performs best.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Compare Individual Pattern Performance")
    print("=" * 80)
    print()
    
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    patterns_to_test = {
        'Gartley Only': {'use_gartley': True, 'use_bat': False, 'use_butterfly': False, 
                        'use_crab': False, 'use_cypher': False},
        'Bat Only': {'use_gartley': False, 'use_bat': True, 'use_butterfly': False, 
                    'use_crab': False, 'use_cypher': False},
        'Butterfly Only': {'use_gartley': False, 'use_bat': False, 'use_butterfly': True, 
                          'use_crab': False, 'use_cypher': False},
        'Crab Only': {'use_gartley': False, 'use_bat': False, 'use_butterfly': False, 
                     'use_crab': True, 'use_cypher': False},
        'Cypher Only': {'use_gartley': False, 'use_bat': False, 'use_butterfly': False, 
                       'use_crab': False, 'use_cypher': True},
    }
    
    results_comparison = {}
    
    for pattern_name, pattern_flags in patterns_to_test.items():
        print(f"\nTesting {pattern_name}...")
        
        data_handler = YFinanceDataHandler(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        strategy = HarmonicPatternStrategy(
            lookback_period=100,
            min_pattern_bars=20,
            max_pattern_bars=80,
            zigzag_threshold=0.03,
            ratio_tolerance=0.05,
            min_confidence=70.0,
            **pattern_flags
        )
        
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=100000
        )
        
        results = backtester.run()
        metrics = backtester.get_metrics()
        
        results_comparison[pattern_name] = {
            'Return': metrics['Total Return (%)'],
            'Sharpe': metrics['Sharpe Ratio'],
            'Max DD': metrics['Max Drawdown (%)'],
            'Win Rate': metrics['Win Rate (%)'],
            'Trades': metrics['Total Trades']
        }
    
    # Display comparison
    print("\n" + "=" * 80)
    print("PATTERN PERFORMANCE COMPARISON")
    print("=" * 80)
    print(f"{'Pattern':<20} {'Return %':<12} {'Sharpe':<10} {'Max DD %':<12} {'Win Rate %':<12} {'Trades':<10}")
    print("-" * 80)
    
    for pattern_name, metrics in results_comparison.items():
        print(f"{pattern_name:<20} {metrics['Return']:>10.2f}  {metrics['Sharpe']:>8.2f}  "
              f"{metrics['Max DD']:>10.2f}  {metrics['Win Rate']:>10.2f}  {metrics['Trades']:>8.0f}")
    
    print("=" * 80)


def main():
    """Run harmonic pattern examples"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "HARMONIC PATTERN RECOGNITION EXAMPLES" + " " * 21 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    print("This script demonstrates different ways to use harmonic pattern detection.")
    print()
    print("Choose an example to run:")
    print("  1. Simple Harmonic (Gartley & Bat only) - Beginner friendly")
    print("  2. All Patterns (Complete harmonic suite) - Advanced")
    print("  3. Aggressive (More trades, lower confidence) - Active trading")
    print("  4. Conservative (Fewer trades, high confidence) - Quality over quantity")
    print("  5. Compare Patterns (See which pattern performs best)")
    print("  6. Run all examples")
    print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == '1':
        example_1_simple_harmonic()
    elif choice == '2':
        example_2_all_patterns()
    elif choice == '3':
        example_3_aggressive_harmonic()
    elif choice == '4':
        example_4_conservative_harmonic()
    elif choice == '5':
        example_5_compare_patterns()
    elif choice == '6':
        print("\nRunning all examples...\n")
        example_1_simple_harmonic()
        example_2_all_patterns()
        example_3_aggressive_harmonic()
        example_4_conservative_harmonic()
        example_5_compare_patterns()
    else:
        print("Invalid choice. Running Example 1 (Simple Harmonic)...")
        example_1_simple_harmonic()
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

