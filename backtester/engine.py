"""
Core Backtesting Engine
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from .portfolio import Portfolio, Order, OrderType
from .strategy import Strategy
from .data_handler import YFinanceDataHandler
from .metrics import PerformanceMetrics
from .visualizer import Visualizer


class Backtester:
    """
    Main backtesting engine that orchestrates strategy execution
    """
    
    def __init__(
        self,
        data_handler: YFinanceDataHandler,
        strategy: Strategy,
        initial_capital: float = 100000,
        commission: float = 0.001,  # 0.1% commission per trade
        slippage: float = 0.0005,  # 0.05% slippage
    ):
        """
        Initialize backtester
        
        Args:
            data_handler: Data handler for market data
            strategy: Trading strategy to backtest
            initial_capital: Starting capital
            commission: Commission rate as decimal (e.g., 0.001 = 0.1%)
            slippage: Slippage rate as decimal
        """
        self.data_handler = data_handler
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        
        self.portfolio = Portfolio(initial_capital)
        self.data = None
        self.signals = None
        self.results = None
        
    def run(self, verbose: bool = True) -> Dict[str, Any]:
        """
        Run the backtest
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            Dictionary containing results and metrics
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Running backtest: {self.strategy.name}")
            print(f"Symbol: {self.data_handler.symbol}")
            print(f"Initial Capital: ${self.initial_capital:,.2f}")
            print(f"{'='*60}\n")
        
        # Fetch data
        self.data = self.data_handler.get_data()
        
        if self.data.empty:
            raise ValueError("No data available for backtesting")
        
        # Generate signals
        if verbose:
            print("Generating signals...")
        self.signals = self.strategy.generate_signals(self.data)
        
        # Validate signals
        if 'signal' not in self.signals.columns:
            raise ValueError("Strategy must return a DataFrame with 'signal' column")
        
        # Reset portfolio
        self.portfolio.reset()
        
        # Run through each bar
        if verbose:
            print("Executing trades...\n")
        
        for timestamp, bar in self.data.iterrows():
            # Get signal for this bar
            if timestamp not in self.signals.index:
                continue
                
            signal_row = self.signals.loc[timestamp]
            signal = signal_row['signal']
            
            # Process any pending orders first
            self.portfolio.process_orders(
                current_price=bar['Close'],
                timestamp=timestamp,
                symbol=self.data_handler.symbol
            )
            
            # Generate new orders based on signals
            if signal == 1:  # Buy signal
                self._execute_buy_signal(timestamp, bar, signal_row)
            elif signal == -1:  # Sell signal
                self._execute_sell_signal(timestamp, bar, signal_row)
            
            # Update equity curve
            portfolio_value = self.portfolio.get_portfolio_value(
                {self.data_handler.symbol: bar['Close']}
            )
            self.portfolio.update_equity_curve(timestamp, portfolio_value)
        
        # Calculate final metrics
        equity_curve = self.portfolio.get_equity_curve_df()
        trade_history = self.portfolio.get_trade_history_df()
        
        metrics = PerformanceMetrics.calculate_all_metrics(
            equity_curve=equity_curve,
            trade_history=trade_history
        )
        
        # Format trades for display
        trades_formatted = self._format_trades_for_display(trade_history)
        
        self.results = {
            'metrics': metrics,
            'equity_curve': equity_curve,
            'trade_history': trade_history,
            'trades': trades_formatted,
            'portfolio': self.portfolio,
            'data': self.data,
            'signals': self.signals
        }
        
        # Print results
        if verbose:
            print(PerformanceMetrics.format_metrics(metrics))
        
        return self.results
    
    def _execute_buy_signal(
        self,
        timestamp: pd.Timestamp,
        bar: pd.Series,
        signal_row: pd.Series
    ):
        """Execute a buy signal"""
        # Determine order type and parameters
        order_type = OrderType.MARKET
        limit_price = None
        stop_price = None
        
        if 'limit_price' in signal_row and pd.notna(signal_row['limit_price']):
            order_type = OrderType.LIMIT
            limit_price = signal_row['limit_price']
        elif 'stop_price' in signal_row and pd.notna(signal_row['stop_price']):
            order_type = OrderType.STOP_LOSS
            stop_price = signal_row['stop_price']
        
        # Determine quantity
        if 'quantity' in signal_row and pd.notna(signal_row['quantity']):
            quantity = int(signal_row['quantity'])
        else:
            # Default: use all available cash
            available_cash = self.portfolio.cash * 0.95  # Keep 5% buffer
            estimated_price = limit_price if limit_price else bar['Close']
            quantity = int(available_cash / (estimated_price * (1 + self.commission + self.slippage)))
        
        if quantity > 0:
            order = Order(
                symbol=self.data_handler.symbol,
                quantity=quantity,
                order_type=order_type,
                direction='buy',
                limit_price=limit_price,
                stop_price=stop_price
            )
            self.portfolio.add_order(order)
    
    def _execute_sell_signal(
        self,
        timestamp: pd.Timestamp,
        bar: pd.Series,
        signal_row: pd.Series
    ):
        """Execute a sell signal"""
        # Check if we have a position to sell
        current_position = self.portfolio.get_position(self.data_handler.symbol)
        
        if current_position <= 0:
            return
        
        # Determine order type and parameters
        order_type = OrderType.MARKET
        limit_price = None
        stop_price = None
        
        if 'limit_price' in signal_row and pd.notna(signal_row['limit_price']):
            order_type = OrderType.LIMIT
            limit_price = signal_row['limit_price']
        elif 'stop_price' in signal_row and pd.notna(signal_row['stop_price']):
            order_type = OrderType.STOP_LOSS
            stop_price = signal_row['stop_price']
        
        # Determine quantity
        if 'quantity' in signal_row and pd.notna(signal_row['quantity']):
            quantity = min(int(signal_row['quantity']), current_position)
        else:
            # Default: sell entire position
            quantity = current_position
        
        if quantity > 0:
            order = Order(
                symbol=self.data_handler.symbol,
                quantity=quantity,
                order_type=order_type,
                direction='sell',
                limit_price=limit_price,
                stop_price=stop_price
            )
            self.portfolio.add_order(order)
    
    def _format_trades_for_display(self, trade_history: pd.DataFrame) -> pd.DataFrame:
        """
        Format trade history for display with Date, Type, Price columns
        
        Args:
            trade_history: Raw trade history DataFrame
            
        Returns:
            Formatted DataFrame with Date, Type, Price columns
        """
        if trade_history.empty:
            return pd.DataFrame(columns=['Date', 'Type', 'Price', 'Quantity', 'Value'])
        
        formatted = trade_history.copy()
        formatted['Date'] = formatted['timestamp']
        formatted['Type'] = formatted['direction'].str.upper()
        formatted['Price'] = formatted['price']
        formatted['Quantity'] = formatted['quantity']
        formatted['Value'] = formatted['value']
        
        return formatted[['Date', 'Type', 'Price', 'Quantity', 'Value']]
    
    def plot_results(self):
        """Plot backtest results"""
        if self.results is None:
            raise ValueError("Must run backtest before plotting results")
        
        visualizer = Visualizer(self.results)
        visualizer.plot_equity_curve()
        visualizer.plot_drawdown()
        visualizer.plot_trades()
    
    def get_results(self) -> Optional[Dict[str, Any]]:
        """Get backtest results"""
        return self.results
    
    def get_metrics(self) -> Optional[Dict[str, float]]:
        """Get performance metrics"""
        if self.results:
            return self.results['metrics']
        return None
    
    def reset(self):
        """Reset backtester state"""
        self.portfolio.reset()
        self.results = None

