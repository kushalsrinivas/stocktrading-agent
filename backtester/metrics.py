"""
Performance Metrics Calculator
"""

import pandas as pd
import numpy as np
from typing import Dict


class PerformanceMetrics:
    """Calculate and store performance metrics for backtesting results"""
    
    @staticmethod
    def calculate_returns(equity_curve: pd.DataFrame) -> pd.Series:
        """
        Calculate returns from equity curve
        
        Args:
            equity_curve: DataFrame with 'value' column
            
        Returns:
            Series of returns
        """
        return equity_curve['value'].pct_change().fillna(0)
    
    @staticmethod
    def total_return(equity_curve: pd.DataFrame) -> float:
        """
        Calculate total return percentage
        
        Args:
            equity_curve: DataFrame with 'value' column
            
        Returns:
            Total return as percentage
        """
        initial_value = equity_curve['value'].iloc[0]
        final_value = equity_curve['value'].iloc[-1]
        return ((final_value - initial_value) / initial_value) * 100
    
    @staticmethod
    def sharpe_ratio(equity_curve: pd.DataFrame, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe ratio
        
        Args:
            equity_curve: DataFrame with 'value' column
            risk_free_rate: Annual risk-free rate (default 0.0)
            periods_per_year: Number of trading periods per year (252 for daily)
            
        Returns:
            Sharpe ratio
        """
        returns = PerformanceMetrics.calculate_returns(equity_curve)
        
        if returns.std() == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / periods_per_year)
        sharpe = np.sqrt(periods_per_year) * (excess_returns.mean() / returns.std())
        
        return sharpe
    
    @staticmethod
    def max_drawdown(equity_curve: pd.DataFrame) -> float:
        """
        Calculate maximum drawdown percentage
        
        Args:
            equity_curve: DataFrame with 'value' column
            
        Returns:
            Maximum drawdown as percentage (negative value)
        """
        cumulative = equity_curve['value']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        
        return drawdown.min()
    
    @staticmethod
    def volatility(equity_curve: pd.DataFrame, periods_per_year: int = 252) -> float:
        """
        Calculate annualized volatility
        
        Args:
            equity_curve: DataFrame with 'value' column
            periods_per_year: Number of trading periods per year
            
        Returns:
            Annualized volatility as percentage
        """
        returns = PerformanceMetrics.calculate_returns(equity_curve)
        return returns.std() * np.sqrt(periods_per_year) * 100
    
    @staticmethod
    def win_rate(trade_history: pd.DataFrame) -> float:
        """
        Calculate win rate from trade history
        
        Args:
            trade_history: DataFrame with trade information
            
        Returns:
            Win rate as percentage
        """
        if trade_history.empty or 'direction' not in trade_history.columns:
            return 0.0
        
        # Match buys with sells to calculate P&L per round trip
        buys = trade_history[trade_history['direction'] == 'buy'].copy()
        sells = trade_history[trade_history['direction'] == 'sell'].copy()
        
        if buys.empty or sells.empty:
            return 0.0
        
        wins = 0
        total_trades = 0
        
        for _, sell in sells.iterrows():
            # Find corresponding buy
            prior_buys = buys[buys['timestamp'] < sell['timestamp']]
            if not prior_buys.empty:
                buy = prior_buys.iloc[-1]
                pnl = (sell['price'] - buy['price']) * sell['quantity']
                if pnl > 0:
                    wins += 1
                total_trades += 1
        
        return (wins / total_trades * 100) if total_trades > 0 else 0.0
    
    @staticmethod
    def profit_factor(trade_history: pd.DataFrame) -> float:
        """
        Calculate profit factor (gross profit / gross loss)
        
        Args:
            trade_history: DataFrame with trade information
            
        Returns:
            Profit factor
        """
        if trade_history.empty or 'direction' not in trade_history.columns:
            return 0.0
        
        buys = trade_history[trade_history['direction'] == 'buy'].copy()
        sells = trade_history[trade_history['direction'] == 'sell'].copy()
        
        if buys.empty or sells.empty:
            return 0.0
        
        gross_profit = 0.0
        gross_loss = 0.0
        
        for _, sell in sells.iterrows():
            prior_buys = buys[buys['timestamp'] < sell['timestamp']]
            if not prior_buys.empty:
                buy = prior_buys.iloc[-1]
                pnl = (sell['price'] - buy['price']) * sell['quantity']
                if pnl > 0:
                    gross_profit += pnl
                else:
                    gross_loss += abs(pnl)
        
        return gross_profit / gross_loss if gross_loss > 0 else 0.0
    
    @staticmethod
    def calculate_all_metrics(
        equity_curve: pd.DataFrame,
        trade_history: pd.DataFrame,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252
    ) -> Dict[str, float]:
        """
        Calculate all performance metrics
        
        Args:
            equity_curve: DataFrame with 'value' column
            trade_history: DataFrame with trade information
            risk_free_rate: Annual risk-free rate
            periods_per_year: Number of trading periods per year
            
        Returns:
            Dictionary of all metrics
        """
        metrics = {
            'Total Return (%)': PerformanceMetrics.total_return(equity_curve),
            'Sharpe Ratio': PerformanceMetrics.sharpe_ratio(equity_curve, risk_free_rate, periods_per_year),
            'Max Drawdown (%)': PerformanceMetrics.max_drawdown(equity_curve),
            'Volatility (%)': PerformanceMetrics.volatility(equity_curve, periods_per_year),
            'Win Rate (%)': PerformanceMetrics.win_rate(trade_history),
            'Profit Factor': PerformanceMetrics.profit_factor(trade_history),
            'Total Trades': len(trade_history) // 2 if not trade_history.empty else 0,  # Round trips
            'Initial Value': equity_curve['value'].iloc[0] if not equity_curve.empty else 0,
            'Final Value': equity_curve['value'].iloc[-1] if not equity_curve.empty else 0,
        }
        
        return metrics
    
    @staticmethod
    def format_metrics(metrics: Dict[str, float]) -> str:
        """
        Format metrics for display
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            Formatted string
        """
        output = "\n" + "="*50 + "\n"
        output += "PERFORMANCE METRICS\n"
        output += "="*50 + "\n"
        
        for key, value in metrics.items():
            if isinstance(value, float):
                output += f"{key:.<30} {value:>15.2f}\n"
            else:
                output += f"{key:.<30} {value:>15}\n"
        
        output += "="*50 + "\n"
        
        return output

