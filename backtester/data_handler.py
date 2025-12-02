"""
Data Handler for fetching and managing market data
"""

import yfinance as yf
import pandas as pd
from typing import Optional


class YFinanceDataHandler:
    """
    Handles data fetching from Yahoo Finance
    """
    
    def __init__(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = '1d'
    ):
        """
        Initialize data handler
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval ('1d', '1h', '1wk', etc.)
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical data from Yahoo Finance
        
        Returns:
            DataFrame with OHLCV data
        """
        print(f"Fetching data for {self.symbol} from {self.start_date} to {self.end_date}...")
        
        ticker = yf.Ticker(self.symbol)
        self.data = ticker.history(
            start=self.start_date,
            end=self.end_date,
            interval=self.interval
        )
        
        if self.data.empty:
            raise ValueError(f"No data returned for {self.symbol}")
        
        # Ensure we have the required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Missing required column: {col}")
        
        print(f"Fetched {len(self.data)} bars of data")
        return self.data
    
    def get_data(self) -> pd.DataFrame:
        """
        Get data (fetch if not already loaded)
        
        Returns:
            DataFrame with OHLCV data
        """
        if self.data is None:
            self.fetch_data()
        return self.data
    
    def get_latest_price(self) -> float:
        """Get the most recent closing price"""
        if self.data is None:
            self.fetch_data()
        return self.data['Close'].iloc[-1]
    
    def get_date_range(self) -> tuple:
        """Get the date range of loaded data"""
        if self.data is None:
            self.fetch_data()
        return (self.data.index[0], self.data.index[-1])
    
    def add_indicator(self, name: str, values: pd.Series):
        """
        Add a custom indicator to the data
        
        Args:
            name: Name of the indicator
            values: Series with indicator values (must match data index)
        """
        if self.data is None:
            self.fetch_data()
        self.data[name] = values
    
    def resample(self, new_interval: str) -> pd.DataFrame:
        """
        Resample data to a different interval
        
        Args:
            new_interval: New interval ('1h', '1d', '1wk', etc.)
            
        Returns:
            Resampled DataFrame
        """
        if self.data is None:
            self.fetch_data()
        
        resampled = self.data.resample(new_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })
        
        return resampled.dropna()
    
    def __repr__(self):
        return f"YFinanceDataHandler(symbol={self.symbol}, start={self.start_date}, end={self.end_date})"


class MultiSymbolDataHandler:
    """
    Handles data for multiple symbols
    """
    
    def __init__(
        self,
        symbols: list,
        start_date: str,
        end_date: str,
        interval: str = '1d'
    ):
        """
        Initialize multi-symbol data handler
        
        Args:
            symbols: List of stock ticker symbols
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval ('1d', '1h', '1wk', etc.)
        """
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = {}
    
    def fetch_data(self) -> dict:
        """
        Fetch data for all symbols
        
        Returns:
            Dictionary of {symbol: DataFrame}
        """
        print(f"Fetching data for {len(self.symbols)} symbols...")
        
        for symbol in self.symbols:
            handler = YFinanceDataHandler(
                symbol=symbol,
                start_date=self.start_date,
                end_date=self.end_date,
                interval=self.interval
            )
            try:
                self.data[symbol] = handler.fetch_data()
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
        
        return self.data
    
    def get_data(self, symbol: Optional[str] = None):
        """
        Get data for a specific symbol or all symbols
        
        Args:
            symbol: Optional symbol to get data for
            
        Returns:
            DataFrame or dict of DataFrames
        """
        if not self.data:
            self.fetch_data()
        
        if symbol:
            return self.data.get(symbol)
        return self.data

