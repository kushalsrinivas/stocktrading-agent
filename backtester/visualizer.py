"""
Visualization utilities for backtesting results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 8)


class Visualizer:
    """Visualize backtesting results"""
    
    def __init__(self, results: Dict[str, Any]):
        """
        Initialize visualizer
        
        Args:
            results: Results dictionary from Backtester
        """
        self.results = results
        self.equity_curve = results['equity_curve']
        self.trade_history = results['trade_history']
        self.data = results['data']
        self.signals = results['signals']
    
    def plot_equity_curve(self):
        """Plot portfolio equity curve over time"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(
            self.equity_curve.index,
            self.equity_curve['value'],
            linewidth=2,
            label='Portfolio Value',
            color='#2E86AB'
        )
        
        # Add horizontal line for initial capital
        initial_value = self.equity_curve['value'].iloc[0]
        ax.axhline(
            y=initial_value,
            color='gray',
            linestyle='--',
            alpha=0.5,
            label=f'Initial Capital: ${initial_value:,.0f}'
        )
        
        ax.set_title('Portfolio Equity Curve', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        plt.show()
    
    def plot_drawdown(self):
        """Plot drawdown over time"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Calculate drawdown
        cumulative = self.equity_curve['value']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        
        ax.fill_between(
            drawdown.index,
            drawdown,
            0,
            alpha=0.3,
            color='red',
            label='Drawdown'
        )
        
        ax.plot(
            drawdown.index,
            drawdown,
            linewidth=1.5,
            color='darkred'
        )
        
        max_dd = drawdown.min()
        ax.set_title(f'Portfolio Drawdown (Max: {max_dd:.2f}%)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown (%)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_trades(self):
        """Plot price with buy/sell markers"""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot closing price
        ax.plot(
            self.data.index,
            self.data['Close'],
            linewidth=1.5,
            label='Close Price',
            color='black',
            alpha=0.7
        )
        
        if not self.trade_history.empty:
            # Plot buy signals
            buys = self.trade_history[self.trade_history['direction'] == 'buy']
            if not buys.empty:
                ax.scatter(
                    buys['timestamp'],
                    buys['price'],
                    marker='^',
                    color='green',
                    s=100,
                    label='Buy',
                    zorder=5,
                    alpha=0.8
                )
            
            # Plot sell signals
            sells = self.trade_history[self.trade_history['direction'] == 'sell']
            if not sells.empty:
                ax.scatter(
                    sells['timestamp'],
                    sells['price'],
                    marker='v',
                    color='red',
                    s=100,
                    label='Sell',
                    zorder=5,
                    alpha=0.8
                )
        
        ax.set_title('Trading Activity', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_returns_distribution(self):
        """Plot distribution of returns"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        returns = self.equity_curve['value'].pct_change().dropna() * 100
        
        ax.hist(returns, bins=50, alpha=0.7, color='#2E86AB', edgecolor='black')
        
        # Add vertical lines for mean and median
        ax.axvline(
            returns.mean(),
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Mean: {returns.mean():.3f}%'
        )
        ax.axvline(
            returns.median(),
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'Median: {returns.median():.3f}%'
        )
        
        ax.set_title('Returns Distribution', fontsize=16, fontweight='bold')
        ax.set_xlabel('Return (%)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_all(self):
        """Create comprehensive visualization with all plots"""
        fig = plt.figure(figsize=(16, 12))
        
        # Equity curve
        ax1 = plt.subplot(3, 2, (1, 2))
        ax1.plot(
            self.equity_curve.index,
            self.equity_curve['value'],
            linewidth=2,
            color='#2E86AB'
        )
        initial_value = self.equity_curve['value'].iloc[0]
        ax1.axhline(y=initial_value, color='gray', linestyle='--', alpha=0.5)
        ax1.set_title('Portfolio Equity Curve', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Portfolio Value ($)', fontsize=10)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax1.grid(True, alpha=0.3)
        
        # Drawdown
        ax2 = plt.subplot(3, 2, (3, 4))
        cumulative = self.equity_curve['value']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        ax2.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        ax2.plot(drawdown.index, drawdown, linewidth=1.5, color='darkred')
        ax2.set_title('Drawdown', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Drawdown (%)', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Returns distribution
        ax3 = plt.subplot(3, 2, 5)
        returns = self.equity_curve['value'].pct_change().dropna() * 100
        ax3.hist(returns, bins=30, alpha=0.7, color='#2E86AB', edgecolor='black')
        ax3.axvline(returns.mean(), color='red', linestyle='--', linewidth=2)
        ax3.set_title('Returns Distribution', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Return (%)', fontsize=10)
        ax3.set_ylabel('Frequency', fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        # Monthly returns heatmap (if enough data)
        ax4 = plt.subplot(3, 2, 6)
        returns_series = self.equity_curve['value'].pct_change()
        monthly_returns = returns_series.resample('M').apply(lambda x: (1 + x).prod() - 1) * 100
        
        if len(monthly_returns) > 12:
            # Create pivot table for heatmap
            monthly_returns_df = pd.DataFrame({
                'Year': monthly_returns.index.year,
                'Month': monthly_returns.index.month,
                'Return': monthly_returns.values
            })
            pivot = monthly_returns_df.pivot(index='Month', columns='Year', values='Return')
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax4, cbar_kws={'label': 'Return (%)'})
            ax4.set_title('Monthly Returns Heatmap', fontsize=14, fontweight='bold')
        else:
            ax4.bar(range(len(monthly_returns)), monthly_returns.values, color='#2E86AB')
            ax4.set_title('Monthly Returns', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Month', fontsize=10)
            ax4.set_ylabel('Return (%)', fontsize=10)
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

