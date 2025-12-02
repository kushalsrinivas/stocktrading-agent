"""
Portfolio and Order Management
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
import pandas as pd


class OrderType(Enum):
    """Types of orders supported"""
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"


class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"


@dataclass
class Order:
    """Represents a trading order"""
    symbol: str
    quantity: int
    order_type: OrderType
    direction: str  # 'buy' or 'sell'
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    fill_price: Optional[float] = None
    timestamp: Optional[pd.Timestamp] = None
    
    def __post_init__(self):
        """Validate order parameters"""
        if self.order_type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError("Limit orders must have a limit_price")
        if self.order_type == OrderType.STOP_LOSS and self.stop_price is None:
            raise ValueError("Stop loss orders must have a stop_price")
        if self.direction not in ['buy', 'sell']:
            raise ValueError("Direction must be 'buy' or 'sell'")


class Portfolio:
    """Manages portfolio state, positions, and orders"""
    
    def __init__(self, initial_capital: float):
        """
        Initialize portfolio
        
        Args:
            initial_capital: Starting cash balance
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}  # {symbol: quantity}
        self.orders = []  # List of all orders
        self.pending_orders = []  # Orders waiting to be filled
        self.trade_history = []  # History of filled orders
        self.equity_curve = []  # Track portfolio value over time
        
    def get_position(self, symbol: str) -> int:
        """Get current position for a symbol"""
        return self.positions.get(symbol, 0)
    
    def add_order(self, order: Order):
        """Add an order to the portfolio"""
        self.orders.append(order)
        if order.status == OrderStatus.PENDING:
            self.pending_orders.append(order)
    
    def process_orders(self, current_price: float, timestamp: pd.Timestamp, symbol: str):
        """
        Process pending orders based on current market price
        
        Args:
            current_price: Current market price
            timestamp: Current timestamp
            symbol: Stock symbol
        """
        filled_orders = []
        
        for order in self.pending_orders:
            if order.symbol != symbol:
                continue
                
            should_fill = False
            fill_price = None
            
            # Check if order should be filled based on type
            if order.order_type == OrderType.MARKET:
                should_fill = True
                fill_price = current_price
                
            elif order.order_type == OrderType.LIMIT:
                if order.direction == 'buy' and current_price <= order.limit_price:
                    should_fill = True
                    fill_price = order.limit_price
                elif order.direction == 'sell' and current_price >= order.limit_price:
                    should_fill = True
                    fill_price = order.limit_price
                    
            elif order.order_type == OrderType.STOP_LOSS:
                if order.direction == 'sell' and current_price <= order.stop_price:
                    should_fill = True
                    fill_price = current_price
                elif order.direction == 'buy' and current_price >= order.stop_price:
                    should_fill = True
                    fill_price = current_price
            
            # Execute order if conditions met
            if should_fill:
                if self._execute_order(order, fill_price, timestamp):
                    filled_orders.append(order)
        
        # Remove filled orders from pending
        for order in filled_orders:
            self.pending_orders.remove(order)
    
    def _execute_order(self, order: Order, fill_price: float, timestamp: pd.Timestamp) -> bool:
        """
        Execute an order
        
        Returns:
            bool: True if order was successfully executed
        """
        total_cost = fill_price * order.quantity
        
        if order.direction == 'buy':
            # Check if we have enough cash
            if total_cost > self.cash:
                return False
            
            self.cash -= total_cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.quantity
            
        elif order.direction == 'sell':
            # Check if we have enough shares
            current_position = self.positions.get(order.symbol, 0)
            if order.quantity > current_position:
                return False
            
            self.cash += total_cost
            self.positions[order.symbol] -= order.quantity
            
            # Remove position if fully sold
            if self.positions[order.symbol] == 0:
                del self.positions[order.symbol]
        
        # Update order status
        order.status = OrderStatus.FILLED
        order.fill_price = fill_price
        order.timestamp = timestamp
        
        # Add to trade history
        self.trade_history.append({
            'timestamp': timestamp,
            'symbol': order.symbol,
            'direction': order.direction,
            'quantity': order.quantity,
            'price': fill_price,
            'value': total_cost
        })
        
        return True
    
    def get_portfolio_value(self, current_prices: dict) -> float:
        """
        Calculate current portfolio value
        
        Args:
            current_prices: Dictionary of {symbol: price}
            
        Returns:
            Total portfolio value (cash + positions)
        """
        positions_value = sum(
            qty * current_prices.get(symbol, 0)
            for symbol, qty in self.positions.items()
        )
        return self.cash + positions_value
    
    def update_equity_curve(self, timestamp: pd.Timestamp, value: float):
        """Record portfolio value at a point in time"""
        self.equity_curve.append({
            'timestamp': timestamp,
            'value': value
        })
    
    def get_equity_curve_df(self) -> pd.DataFrame:
        """Get equity curve as DataFrame"""
        return pd.DataFrame(self.equity_curve).set_index('timestamp')
    
    def get_trade_history_df(self) -> pd.DataFrame:
        """Get trade history as DataFrame"""
        if not self.trade_history:
            return pd.DataFrame()
        return pd.DataFrame(self.trade_history)
    
    def reset(self):
        """Reset portfolio to initial state"""
        self.cash = self.initial_capital
        self.positions = {}
        self.orders = []
        self.pending_orders = []
        self.trade_history = []
        self.equity_curve = []

