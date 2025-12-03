"""
NSE Sector-Based Stock Selection and Trading Framework

This script implements a comprehensive framework for NSE stock trading:
1. Stock Selection Framework (Liquidity, Trend, Volatility Filters)
2. Sector-Wise Strategy Mapping
3. Complete Trading Strategy with Entry/Exit Rules

Author: Stock Trading Framework
Date: December 2024
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, YFinanceDataHandler
from backtester.strategy import Strategy


# ============================================================================
# NSE STOCK UNIVERSE DEFINITIONS
# ============================================================================

NSE_NIFTY_50 = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'ITC',
    'SBIN', 'BHARTIARTL', 'KOTAKBANK', 'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI',
    'HCLTECH', 'BAJFINANCE', 'TITAN', 'SUNPHARMA', 'ULTRACEMCO', 'ONGC',
    'TECHM', 'NESTLEIND', 'TATAMOTORS', 'WIPRO', 'NTPC', 'POWERGRID', 'M&M',
    'BAJAJFINSV', 'TATASTEEL', 'JSWSTEEL', 'ADANIENT', 'INDUSINDBK', 'COALINDIA',
    'DRREDDY', 'HINDALCO', 'GRASIM', 'CIPLA', 'TATACONSUM', 'BRITANNIA',
    'DIVISLAB', 'EICHERMOT', 'HEROMOTOCO', 'SHRIRAMFIN', 'ADANIPORTS', 'APOLLOHOSP',
    'BAJAJ-AUTO', 'HDFCLIFE', 'SBILIFE', 'BPCL', 'TRENT'
]

NSE_NIFTY_NEXT_50 = [
    'ADANIGREEN', 'ADANIPOWER', 'ATGL', 'BANDHANBNK', 'BEL', 'BOSCHLTD',
    'CANBK', 'CHOLAFIN', 'COLPAL', 'DABUR', 'DLF', 'GAIL', 'GODREJCP',
    'HAVELLS', 'HINDPETRO', 'ICICIPRULI', 'INDIGO', 'IOC', 'JIOFIN',
    'LTIM', 'MARICO', 'MOTHERSON', 'NYKAA', 'PAGEIND', 'PETRONET',
    'PGHH', 'PIDILITIND', 'PNB', 'RECLTD', 'SBICARD', 'SHREECEM',
    'SIEMENS', 'SRF', 'TATACOMM', 'TATAPOWER', 'TORNTPHARM', 'TVSMOTOR',
    'UBL', 'UNIONBANK', 'VBL', 'VEDL', 'VOLTAS', 'ZOMATO', 'ZYDUSLIFE',
    'ALKEM', 'AMBUJACEM', 'ABB', 'ACC', 'BAJAJHLDNG', 'BERGEPAINT'
]

# NSE Sector Indices and their constituent stocks
NSE_SECTORS = {
    'NIFTY_BANK': {
        'index': '^NSEBANK',
        'stocks': ['HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK', 
                   'INDUSINDBK', 'BANDHANBNK', 'FEDERALBNK', 'AUBANK', 'IDFCFIRSTB',
                   'PNB', 'CANBK', 'UNIONBANK', 'BANKBARODA']
    },
    'NIFTY_IT': {
        'index': '^CNXIT',
        'stocks': ['TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM', 'LTIM',
                   'COFORGE', 'PERSISTENT', 'MPHASIS', 'LTTS']
    },
    'NIFTY_AUTO': {
        'index': '^CNXAUTO',
        'stocks': ['MARUTI', 'TATAMOTORS', 'M&M', 'BAJAJ-AUTO', 'EICHERMOT',
                   'HEROMOTOCO', 'TVSMOTOR', 'ASHOKLEY', 'MOTHERSON', 'BALKRISIND',
                   'MRF', 'APOLLOTYRE', 'ESCORTS', 'BOSCHLTD']
    },
    'NIFTY_PHARMA': {
        'index': '^CNXPHARMA',
        'stocks': ['SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB', 'TORNTPHARM',
                   'APOLLOHOSP', 'LAURUSLABS', 'ALKEM', 'BIOCON', 'ZYDUSLIFE',
                   'AUROPHARMA', 'LUPIN', 'IPCALAB', 'GRANULES']
    },
    'NIFTY_FMCG': {
        'index': '^CNXFMCG',
        'stocks': ['HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'TATACONSUM',
                   'DABUR', 'MARICO', 'GODREJCP', 'COLPAL', 'UBL', 'PGHH',
                   'VBL', 'MCDOWELL-N', 'EMAMILTD']
    },
    'NIFTY_METAL': {
        'index': '^CNXMETAL',
        'stocks': ['TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'VEDL', 'COALINDIA',
                   'SAIL', 'JINDALSTEL', 'NMDC', 'NATIONALUM', 'HINDZINC',
                   'RATNAMANI', 'WELCORP', 'APLAPOLLO']
    },
    'NIFTY_ENERGY': {
        'index': '^CNXENERGY',
        'stocks': ['RELIANCE', 'ONGC', 'NTPC', 'POWERGRID', 'BPCL', 'IOC',
                   'GAIL', 'HINDPETRO', 'TATAPOWER', 'ADANIGREEN', 'ADANIPOWER',
                   'ATGL', 'PETRONET']
    },
    'NIFTY_PSU_BANK': {
        'index': '^CNXPSUBANK',
        'stocks': ['SBIN', 'PNB', 'CANBK', 'UNIONBANK', 'BANKBARODA', 'INDIANB',
                   'CANBK', 'MAHABANK', 'CENTRALBK', 'IOBB', 'UCO']
    }
}


# ============================================================================
# STOCK SCREENING AND FILTERING
# ============================================================================

class StockScreener:
    """Implements the 3-filter stock selection framework"""
    
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.screened_stocks = {}
    
    def apply_liquidity_filter(self, stocks: List[str], 
                               min_volume: float = 500000,  # 5 lakh shares
                               min_value: float = 50_00_00_000) -> List[str]:  # ₹50 crore
        """
        Filter A: Liquidity Filter
        Keep only stocks with sufficient volume and value traded
        """
        print("\n🔍 Applying Liquidity Filter...")
        print(f"   Min Volume: {min_volume:,.0f} shares/day")
        print(f"   Min Value Traded: ₹{min_value/1e7:.0f} crore/day")
        
        liquid_stocks = []
        
        for stock in stocks:
            try:
                symbol = f"{stock}.NS"
                data = yf.download(symbol, start=self.start_date, end=self.end_date, 
                                 progress=False, show_errors=False)
                
                if data.empty:
                    continue
                
                avg_volume = data['Volume'].mean()
                avg_close = data['Close'].mean()
                avg_value_traded = avg_volume * avg_close
                
                if avg_volume >= min_volume and avg_value_traded >= min_value:
                    liquid_stocks.append(stock)
                    
            except Exception:
                continue
        
        print(f"   ✅ {len(liquid_stocks)}/{len(stocks)} stocks passed liquidity filter")
        return liquid_stocks
    
    def calculate_ema(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def apply_trend_filter(self, stocks: List[str], sector: str) -> List[str]:
        """
        Filter B: Trend Filter (Sector + Stock Alignment)
        Step 1: Check if sector is strong
        Step 2: Pick strongest stocks within strong sector
        """
        print(f"\n🔍 Applying Trend Filter for {sector}...")
        
        # Step 1: Check sector strength
        sector_info = NSE_SECTORS.get(sector)
        if not sector_info:
            print(f"   ⚠️  Sector {sector} not found")
            return []
        
        sector_index = sector_info['index']
        
        try:
            sector_data = yf.download(sector_index, start=self.start_date, 
                                     end=self.end_date, progress=False, show_errors=False)
            
            if sector_data.empty:
                print(f"   ⚠️  No data for sector index {sector_index}")
                return []
            
            # Check sector conditions
            sector_50ema = self.calculate_ema(sector_data, 50).iloc[-1]
            sector_close = sector_data['Close'].iloc[-1]
            sector_rsi = self.calculate_rsi(sector_data).iloc[-1]
            
            # Higher highs/higher lows check (simple version)
            recent_highs = sector_data['High'].tail(20)
            is_making_higher_highs = recent_highs.iloc[-1] > recent_highs.iloc[-10]
            
            sector_strong = (sector_close > sector_50ema and 
                           sector_rsi > 50 and 
                           is_making_higher_highs)
            
            print(f"   Sector Index: {sector_index}")
            print(f"   - Close: {sector_close:.2f}, 50-EMA: {sector_50ema:.2f}")
            print(f"   - RSI: {sector_rsi:.2f}")
            print(f"   - Higher Highs: {is_making_higher_highs}")
            print(f"   - Sector Strong: {'✅' if sector_strong else '❌'}")
            
            if not sector_strong:
                print(f"   ⚠️  Sector not strong enough - skipping stock selection")
                return []
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing sector: {e}")
            return []
        
        # Step 2: Pick strongest stocks in strong sector
        strong_stocks = []
        
        print(f"\n   Analyzing {len(stocks)} stocks in sector...")
        for stock in stocks:
            try:
                symbol = f"{stock}.NS"
                data = yf.download(symbol, start=self.start_date, end=self.end_date,
                                 progress=False, show_errors=False)
                
                if len(data) < 200:  # Need enough data for 200 EMA
                    continue
                
                # Calculate indicators
                close = data['Close'].iloc[-1]
                ema_20 = self.calculate_ema(data, 20).iloc[-1]
                ema_50 = self.calculate_ema(data, 50).iloc[-1]
                ema_200 = self.calculate_ema(data, 200).iloc[-1]
                rsi = self.calculate_rsi(data).iloc[-1]
                
                # Check conditions
                above_emas = close > ema_20 and close > ema_50 and close > ema_200
                rsi_range = 55 <= rsi <= 65
                
                if above_emas and rsi_range:
                    strong_stocks.append({
                        'stock': stock,
                        'close': close,
                        'rsi': rsi,
                        'ema_20': ema_20,
                        'ema_50': ema_50,
                        'ema_200': ema_200
                    })
                    
            except Exception:
                continue
        
        print(f"   ✅ {len(strong_stocks)} stocks passed trend filter")
        return [s['stock'] for s in strong_stocks]
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(period).mean()
        
        return atr
    
    def apply_volatility_filter(self, stocks: List[str], 
                                trading_type: str = 'swing') -> Dict[str, List[str]]:
        """
        Filter C: Volatility Filter
        ATR/Price < 3% → Low volatility → Good for swing
        ATR/Price > 3% → High volatility → Good for intraday
        """
        print(f"\n🔍 Applying Volatility Filter (for {trading_type} trading)...")
        
        categorized_stocks = {
            'swing': [],  # Low volatility
            'intraday': []  # High volatility
        }
        
        for stock in stocks:
            try:
                symbol = f"{stock}.NS"
                data = yf.download(symbol, start=self.start_date, end=self.end_date,
                                 progress=False, show_errors=False)
                
                if len(data) < 14:
                    continue
                
                atr = self.calculate_atr(data).iloc[-1]
                close = data['Close'].iloc[-1]
                atr_pct = (atr / close) * 100
                
                if atr_pct < 3.0:
                    categorized_stocks['swing'].append({
                        'stock': stock,
                        'atr_pct': atr_pct,
                        'volatility': 'Low'
                    })
                else:
                    categorized_stocks['intraday'].append({
                        'stock': stock,
                        'atr_pct': atr_pct,
                        'volatility': 'High'
                    })
                    
            except Exception:
                continue
        
        print(f"   ✅ Swing Trading Candidates: {len(categorized_stocks['swing'])}")
        print(f"   ✅ Intraday Trading Candidates: {len(categorized_stocks['intraday'])}")
        
        return categorized_stocks


# ============================================================================
# SECTOR-SPECIFIC STRATEGIES
# ============================================================================

class SectorTrendBreakoutStrategy(Strategy):
    """
    Complete Trading Strategy: Sector Trend + Stock Strength + Volume Breakout
    
    This implements the complete rule-based system described in the framework.
    """
    
    def __init__(self, 
                 sector: str = 'NIFTY_AUTO',
                 rr_ratio: float = 2.0,  # Risk:Reward ratio
                 atr_multiplier: float = 1.5):
        super().__init__()
        self.sector = sector
        self.rr_ratio = rr_ratio
        self.atr_multiplier = atr_multiplier
        self.parameters = {
            'sector': sector,
            'rr_ratio': rr_ratio,
            'atr_multiplier': atr_multiplier
        }
    
    def calculate_ema(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate EMA"""
        return prices.ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate ATR"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(period).mean()
        
        return atr
    
    def find_swing_high(self, data: pd.DataFrame, lookback: int = 20) -> pd.Series:
        """Find swing highs (local maxima)"""
        swing_highs = data['High'].rolling(window=lookback, center=True).max()
        return swing_highs
    
    def find_swing_low(self, data: pd.DataFrame, lookback: int = 20) -> pd.Series:
        """Find swing lows (local minima)"""
        swing_lows = data['Low'].rolling(window=lookback, center=True).min()
        return swing_lows
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the complete framework
        
        Entry Rules (ALL must align):
        1. Price breaks last swing high
        2. Breakout candle volume ≥ 1.5× average volume
        3. RSI remains above 55
        
        Exit Rules (ANY triggers exit):
        1. RSI falls below 50
        2. Price closes below 20 EMA
        3. Volume spike + inverted candle
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Calculate all indicators
        signals['ema_20'] = self.calculate_ema(data['Close'], 20)
        signals['ema_50'] = self.calculate_ema(data['Close'], 50)
        signals['ema_200'] = self.calculate_ema(data['Close'], 200)
        signals['rsi'] = self.calculate_rsi(data['Close'])
        signals['atr'] = self.calculate_atr(data)
        
        # Calculate volume metrics
        signals['avg_volume'] = data['Volume'].rolling(window=20).mean()
        signals['volume_ratio'] = data['Volume'] / signals['avg_volume']
        
        # Find swing points
        signals['swing_high'] = self.find_swing_high(data, lookback=20)
        signals['swing_low'] = self.find_swing_low(data, lookback=20)
        
        # Track position state
        in_position = False
        entry_price = 0
        stop_loss = 0
        
        for i in range(200, len(data)):  # Start after 200 bars for indicators
            
            if not in_position:
                # Entry conditions
                price = data['Close'].iloc[i]
                prev_swing_high = signals['swing_high'].iloc[i-1]
                
                # Check all entry conditions
                breakout = price > prev_swing_high
                volume_surge = signals['volume_ratio'].iloc[i] >= 1.5
                rsi_strong = signals['rsi'].iloc[i] > 55
                above_emas = (price > signals['ema_20'].iloc[i] and 
                            price > signals['ema_50'].iloc[i] and
                            price > signals['ema_200'].iloc[i])
                
                if breakout and volume_surge and rsi_strong and above_emas:
                    signals.iloc[i, signals.columns.get_loc('signal')] = 1
                    in_position = True
                    entry_price = price
                    
                    # Set stop loss (previous swing low or ATR-based)
                    prev_swing_low = signals['swing_low'].iloc[i-1]
                    atr_stop = price - (self.atr_multiplier * signals['atr'].iloc[i])
                    stop_loss = max(prev_swing_low, atr_stop)
            
            else:
                # Exit conditions
                price = data['Close'].iloc[i]
                rsi = signals['rsi'].iloc[i]
                ema_20 = signals['ema_20'].iloc[i]
                
                # Exit condition 1: RSI falls below 50
                rsi_exit = rsi < 50
                
                # Exit condition 2: Price closes below 20 EMA
                ema_exit = price < ema_20
                
                # Exit condition 3: Volume spike with bearish candle
                volume_spike = signals['volume_ratio'].iloc[i] > 2.0
                bearish_candle = data['Close'].iloc[i] < data['Open'].iloc[i]
                reversal_exit = volume_spike and bearish_candle
                
                # Exit condition 4: Stop loss hit
                stop_loss_hit = price <= stop_loss
                
                if rsi_exit or ema_exit or reversal_exit or stop_loss_hit:
                    signals.iloc[i, signals.columns.get_loc('signal')] = -1
                    in_position = False
                    entry_price = 0
                    stop_loss = 0
                else:
                    # Trail stop loss with 20 EMA for position trades
                    stop_loss = max(stop_loss, ema_20)
        
        return signals[['signal']]


# ============================================================================
# SECTOR-SPECIFIC STRATEGY FACTORY
# ============================================================================

def get_strategy_for_sector(sector: str) -> Strategy:
    """
    Returns the appropriate strategy for each NSE sector based on characteristics
    """
    
    if sector in ['NIFTY_BANK', 'NIFTY_PSU_BANK']:
        # Intraday Breakout Strategy for high volatility banking sector
        return IntradayBreakoutStrategy(sector=sector)
    
    elif sector == 'NIFTY_IT':
        # Swing Trading Strategy for smooth trending IT sector
        return SwingTrendStrategy(sector=sector)
    
    elif sector == 'NIFTY_AUTO':
        # Breakout + Trend Following for Auto sector
        return SectorTrendBreakoutStrategy(sector=sector)
    
    elif sector == 'NIFTY_FMCG':
        # Mean Reversion for slow-moving FMCG
        return MeanReversionStrategy(sector=sector)
    
    elif sector in ['NIFTY_METAL', 'NIFTY_ENERGY']:
        # Cycle-based swing trading for commodities
        return CycleBasedStrategy(sector=sector)
    
    elif sector == 'NIFTY_PHARMA':
        # Range Breakout for Pharma
        return RangeBreakoutStrategy(sector=sector)
    
    else:
        # Default: Universal sector trend breakout strategy
        return SectorTrendBreakoutStrategy(sector=sector)


class IntradayBreakoutStrategy(Strategy):
    """Intraday Breakout Strategy for Banking/Financial Stocks"""
    
    def __init__(self, sector: str = 'NIFTY_BANK'):
        super().__init__()
        self.sector = sector
        self.parameters = {'sector': sector}
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        VWAP + 5/20 EMA crossover + Volume spikes
        Buy when price crosses day high with volume
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Calculate VWAP
        signals['vwap'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
        
        # EMAs
        signals['ema_5'] = data['Close'].ewm(span=5, adjust=False).mean()
        signals['ema_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        
        # Volume
        signals['avg_volume'] = data['Volume'].rolling(20).mean()
        signals['volume_ratio'] = data['Volume'] / signals['avg_volume']
        
        # Entry: Price > VWAP, 5 EMA > 20 EMA, Volume > 1.5x
        buy_condition = ((data['Close'] > signals['vwap']) & 
                        (signals['ema_5'] > signals['ema_20']) &
                        (signals['volume_ratio'] > 1.5))
        
        signals.loc[buy_condition, 'signal'] = 1
        
        # Exit: Price < VWAP or 5 EMA < 20 EMA
        sell_condition = ((data['Close'] < signals['vwap']) | 
                         (signals['ema_5'] < signals['ema_20']))
        
        signals.loc[sell_condition, 'signal'] = -1
        
        return signals[['signal']]


class SwingTrendStrategy(Strategy):
    """Swing Trading Strategy for IT Sector"""
    
    def __init__(self, sector: str = 'NIFTY_IT'):
        super().__init__()
        self.sector = sector
        self.parameters = {'sector': sector}
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        20-EMA trendline + RSI 50 bounce
        Buy on pullback to 20 EMA, Exit when RSI > 70
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        signals['ema_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        signals['rsi'] = self.calculate_rsi(data['Close'])
        
        # Entry: Price bounces off 20 EMA, RSI > 50
        price_near_ema = np.abs(data['Close'] - signals['ema_20']) / signals['ema_20'] < 0.02
        buy_condition = (price_near_ema & 
                        (signals['rsi'] > 50) &
                        (data['Close'] > signals['ema_20']))
        
        signals.loc[buy_condition, 'signal'] = 1
        
        # Exit: RSI > 70 (overbought)
        sell_condition = signals['rsi'] > 70
        signals.loc[sell_condition, 'signal'] = -1
        
        return signals[['signal']]


class MeanReversionStrategy(Strategy):
    """Mean Reversion Strategy for FMCG Sector"""
    
    def __init__(self, sector: str = 'NIFTY_FMCG'):
        super().__init__()
        self.sector = sector
        self.parameters = {'sector': sector, 'bb_period': 20, 'bb_std': 2.0}
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Bollinger Band pullbacks + RSI oversold
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Bollinger Bands
        signals['sma'] = data['Close'].rolling(20).mean()
        signals['std'] = data['Close'].rolling(20).std()
        signals['bb_upper'] = signals['sma'] + (2 * signals['std'])
        signals['bb_lower'] = signals['sma'] - (2 * signals['std'])
        
        signals['rsi'] = self.calculate_rsi(data['Close'])
        
        # Entry: Price at lower BB, RSI oversold (35-40)
        buy_condition = ((data['Close'] <= signals['bb_lower']) & 
                        (signals['rsi'] >= 35) & 
                        (signals['rsi'] <= 40))
        
        signals.loc[buy_condition, 'signal'] = 1
        
        # Exit: Price at middle BB or RSI > 60
        sell_condition = ((data['Close'] >= signals['sma']) | (signals['rsi'] > 60))
        signals.loc[sell_condition, 'signal'] = -1
        
        return signals[['signal']]


class CycleBasedStrategy(Strategy):
    """Cycle-Based Strategy for Metal/Energy Sectors"""
    
    def __init__(self, sector: str = 'NIFTY_METAL'):
        super().__init__()
        self.sector = sector
        self.parameters = {'sector': sector}
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        MACD for cycle trends + Supertrend for entries/exits
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # MACD
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        signals['macd'] = exp1 - exp2
        signals['signal_line'] = signals['macd'].ewm(span=9, adjust=False).mean()
        
        # Entry: MACD crosses above signal line
        macd_cross_up = ((signals['macd'] > signals['signal_line']) & 
                        (signals['macd'].shift(1) <= signals['signal_line'].shift(1)))
        
        signals.loc[macd_cross_up, 'signal'] = 1
        
        # Exit: MACD crosses below signal line
        macd_cross_down = ((signals['macd'] < signals['signal_line']) & 
                          (signals['macd'].shift(1) >= signals['signal_line'].shift(1)))
        
        signals.loc[macd_cross_down, 'signal'] = -1
        
        return signals[['signal']]


class RangeBreakoutStrategy(Strategy):
    """Range Breakout Strategy for Pharma Sector"""
    
    def __init__(self, sector: str = 'NIFTY_PHARMA'):
        super().__init__()
        self.sector = sector
        self.parameters = {'sector': sector}
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        RSI divergence + Daily consolidation breakout + Volume surge
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        signals['rsi'] = self.calculate_rsi(data['Close'])
        
        # Identify consolidation ranges (low volatility periods)
        signals['range'] = data['High'].rolling(20).max() - data['Low'].rolling(20).min()
        signals['avg_range'] = signals['range'].rolling(50).mean()
        signals['consolidating'] = signals['range'] < (0.5 * signals['avg_range'])
        
        # Volume
        signals['avg_volume'] = data['Volume'].rolling(20).mean()
        signals['volume_surge'] = data['Volume'] > (1.5 * signals['avg_volume'])
        
        # Breakout from consolidation with volume
        price_breakout_up = data['Close'] > data['High'].rolling(20).max().shift(1)
        buy_condition = (price_breakout_up & 
                        signals['consolidating'].shift(1) & 
                        signals['volume_surge'])
        
        signals.loc[buy_condition, 'signal'] = 1
        
        # Exit: RSI > 70 or price falls back into range
        range_high = data['High'].rolling(20).max()
        sell_condition = ((signals['rsi'] > 70) | 
                         (data['Close'] < range_high.shift(1)))
        
        signals.loc[sell_condition, 'signal'] = -1
        
        return signals[['signal']]


# ============================================================================
# MAIN EXECUTION FUNCTIONS
# ============================================================================

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print("   NSE SECTOR-BASED STOCK SELECTION & TRADING FRAMEWORK")
    print("="*80)
    print("\n📊 3-Filter Stock Selection:")
    print("   1. Liquidity Filter (Volume + Value Traded)")
    print("   2. Trend Filter (Sector + Stock Alignment)")
    print("   3. Volatility Filter (Swing vs Intraday)")
    print("\n🎯 Sector-Specific Strategies:")
    print("   • Banking: Intraday Breakout (VWAP + Volume)")
    print("   • IT: Swing Trend (20-EMA + RSI Bounce)")
    print("   • Auto: Breakout + Trend Following")
    print("   • FMCG: Mean Reversion (Bollinger + RSI)")
    print("   • Metal/Energy: Cycle-Based (MACD)")
    print("   • Pharma: Range Breakout (RSI Divergence)")
    print("\n" + "="*80 + "\n")


def screen_sector_stocks(sector: str, trading_type: str = 'swing',
                        start_date: str = None, end_date: str = None):
    """
    Run complete stock screening for a sector
    
    Args:
        sector: NSE sector name (e.g., 'NIFTY_AUTO')
        trading_type: 'swing' or 'intraday'
        start_date: Start date for analysis
        end_date: End date for analysis
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"   SCREENING STOCKS FOR {sector}")
    print(f"   Trading Type: {trading_type.upper()}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"{'='*80}")
    
    # Get sector stocks
    sector_info = NSE_SECTORS.get(sector)
    if not sector_info:
        print(f"\n❌ Sector {sector} not found!")
        print(f"Available sectors: {', '.join(NSE_SECTORS.keys())}")
        return None
    
    sector_stocks = sector_info['stocks']
    print(f"\n📝 Analyzing {len(sector_stocks)} stocks in {sector}...")
    
    # Initialize screener
    screener = StockScreener(start_date, end_date)
    
    # Apply filters
    liquid_stocks = screener.apply_liquidity_filter(sector_stocks)
    
    if not liquid_stocks:
        print("\n⚠️  No stocks passed liquidity filter!")
        return None
    
    trending_stocks = screener.apply_trend_filter(liquid_stocks, sector)
    
    if not trending_stocks:
        print("\n⚠️  No stocks passed trend filter!")
        return None
    
    categorized = screener.apply_volatility_filter(trending_stocks, trading_type)
    
    # Get final candidates
    final_candidates = categorized[trading_type]
    
    if not final_candidates:
        print(f"\n⚠️  No stocks suitable for {trading_type} trading!")
        return None
    
    # Display results
    print(f"\n{'='*80}")
    print(f"   FINAL CANDIDATES FOR {trading_type.upper()} TRADING")
    print(f"{'='*80}\n")
    
    df = pd.DataFrame(final_candidates)
    print(df.to_string(index=False))
    print(f"\n{'='*80}")
    
    return final_candidates


def run_sector_backtest(sector: str, stock: str, 
                       start_date: str = None, end_date: str = None,
                       initial_capital: float = 100000):
    """
    Run backtest using sector-specific strategy
    
    Args:
        sector: NSE sector name
        stock: Stock symbol (without .NS)
        start_date: Start date
        end_date: End date
        initial_capital: Starting capital in INR
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"   BACKTESTING {stock} ({sector})")
    print(f"   Period: {start_date} to {end_date}")
    print(f"   Initial Capital: ₹{initial_capital:,.0f}")
    print(f"{'='*80}\n")
    
    try:
        # Get sector-specific strategy
        strategy = get_strategy_for_sector(sector)
        print(f"📊 Strategy: {strategy.__class__.__name__}")
        print(f"   Optimized for {sector} characteristics\n")
        
        # Setup data handler
        nse_symbol = f"{stock}.NS"
        data_handler = YFinanceDataHandler(
            symbol=nse_symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        # Create backtester
        backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            initial_capital=initial_capital,
            commission=0.0005,  # 0.05%
            slippage=0.0005
        )
        
        # Run backtest
        print("⚙️  Running backtest...\n")
        results = backtester.run()
        
        # Print results
        print_backtest_results(stock, sector, results)
        
        # Visualize
        print("\n📊 Generating visualizations...")
        backtester.plot_results()
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def print_backtest_results(stock: str, sector: str, results: dict):
    """Print formatted backtest results"""
    metrics = results['metrics']
    
    print(f"\n{'='*80}")
    print(f"   BACKTEST RESULTS: {stock} ({sector})")
    print(f"{'='*80}")
    
    # Performance
    print("\n💰 PERFORMANCE:")
    print(f"   Initial Capital:    ₹{metrics['Initial Value']:>12,.2f}")
    print(f"   Final Value:        ₹{metrics['Final Value']:>12,.2f}")
    profit = metrics['Final Value'] - metrics['Initial Value']
    emoji = "📈" if profit > 0 else "📉"
    print(f"   Profit/Loss:        ₹{profit:>12,.2f} {emoji}")
    print(f"   Total Return:       {metrics['Total Return (%)']:>12,.2f}%")
    
    # Risk metrics
    print("\n📊 RISK METRICS:")
    print(f"   Sharpe Ratio:       {metrics['Sharpe Ratio']:>12,.2f}")
    print(f"   Max Drawdown:       {metrics['Max Drawdown (%)']:>12,.2f}%")
    print(f"   Volatility:         {metrics['Volatility (%)']:>12,.2f}%")
    
    # Trading activity
    print("\n📈 TRADING ACTIVITY:")
    print(f"   Total Trades:       {metrics['Total Trades']:>12}")
    if metrics['Total Trades'] > 0:
        print(f"   Win Rate:           {metrics['Win Rate (%)']:>12,.2f}%")
        print(f"   Profit Factor:      {metrics['Profit Factor']:>12,.2f}")
    
    print(f"\n{'='*80}")


def compare_sectors(stock: str, start_date: str = None, end_date: str = None):
    """
    Compare performance across different sector strategies for a single stock
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"   COMPARING SECTOR STRATEGIES ON {stock}")
    print(f"   Period: {start_date} to {end_date}")
    print(f"{'='*80}\n")
    
    results_list = []
    
    for sector in NSE_SECTORS.keys():
        try:
            print(f"Testing {sector} strategy...")
            
            strategy = get_strategy_for_sector(sector)
            nse_symbol = f"{stock}.NS"
            
            data_handler = YFinanceDataHandler(
                symbol=nse_symbol,
                start_date=start_date,
                end_date=end_date
            )
            
            backtester = Backtester(
                data_handler=data_handler,
                strategy=strategy,
                initial_capital=100000,
                commission=0.0005,
                slippage=0.0005
            )
            
            results = backtester.run(verbose=False)
            metrics = results['metrics']
            
            results_list.append({
                'Sector Strategy': sector,
                'Return (%)': metrics['Total Return (%)'],
                'Sharpe': metrics['Sharpe Ratio'],
                'Max DD (%)': metrics['Max Drawdown (%)'],
                'Win Rate (%)': metrics['Win Rate (%)'],
                'Trades': metrics['Total Trades']
            })
            
            print(f"✅ {sector}: {metrics['Total Return (%)']:.2f}%\n")
            
        except Exception as e:
            print(f"❌ Error with {sector}: {e}\n")
    
    # Display comparison
    if results_list:
        df = pd.DataFrame(results_list).sort_values('Return (%)', ascending=False)
        print(f"\n{'='*80}")
        print(f"   STRATEGY COMPARISON RESULTS")
        print(f"{'='*80}\n")
        print(df.to_string(index=False))
        print(f"\n{'='*80}")
    
    return results_list


def interactive_menu():
    """Interactive menu for the framework"""
    print_banner()
    
    while True:
        print("\n📋 MENU:")
        print("   1. Screen stocks in a sector (3-filter framework)")
        print("   2. Backtest a stock with sector-specific strategy")
        print("   3. Compare all sector strategies on a stock")
        print("   4. Show NSE sectors and stocks")
        print("   5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            # Screen stocks
            print("\n📊 Available Sectors:")
            for i, sector in enumerate(NSE_SECTORS.keys(), 1):
                print(f"   {i}. {sector}")
            
            sector_choice = input("\nEnter sector number: ").strip()
            try:
                sector_idx = int(sector_choice) - 1
                sector = list(NSE_SECTORS.keys())[sector_idx]
                
                trading_type = input("Trading type (swing/intraday) [default: swing]: ").strip().lower()
                if trading_type not in ['swing', 'intraday']:
                    trading_type = 'swing'
                
                screen_sector_stocks(sector, trading_type)
                
            except (ValueError, IndexError):
                print("❌ Invalid sector selection!")
        
        elif choice == '2':
            # Backtest stock
            print("\n📊 Available Sectors:")
            for i, sector in enumerate(NSE_SECTORS.keys(), 1):
                print(f"   {i}. {sector}")
            
            sector_choice = input("\nEnter sector number: ").strip()
            stock = input("Enter stock symbol (e.g., RELIANCE, TCS): ").strip().upper()
            
            try:
                sector_idx = int(sector_choice) - 1
                sector = list(NSE_SECTORS.keys())[sector_idx]
                
                run_sector_backtest(sector, stock)
                
            except (ValueError, IndexError):
                print("❌ Invalid sector selection!")
        
        elif choice == '3':
            # Compare strategies
            stock = input("\nEnter stock symbol (e.g., RELIANCE, TCS): ").strip().upper()
            compare_sectors(stock)
        
        elif choice == '4':
            # Show sectors
            print("\n📊 NSE SECTORS AND STOCKS:")
            print("="*80)
            for sector, info in NSE_SECTORS.items():
                print(f"\n{sector}:")
                print(f"   Index: {info['index']}")
                print(f"   Stocks ({len(info['stocks'])}): {', '.join(info['stocks'][:10])}...")
            print("\n" + "="*80)
        
        elif choice == '5':
            print("\n👋 Thank you for using NSE Sector Framework!")
            print("="*80 + "\n")
            break
        
        else:
            print("❌ Invalid choice!")


def example_usage():
    """Example: Screen and backtest NIFTY AUTO sector"""
    print_banner()
    
    print("\n🎯 EXAMPLE: Analyzing NIFTY AUTO Sector\n")
    print("="*80)
    
    # Step 1: Screen stocks
    print("\nSTEP 1: Screening stocks in NIFTY AUTO...")
    candidates = screen_sector_stocks('NIFTY_AUTO', trading_type='swing')
    
    if candidates and len(candidates) > 0:
        # Step 2: Backtest top candidate
        print("\nSTEP 2: Backtesting top candidate...")
        top_stock = candidates[0]['stock']
        
        results = run_sector_backtest(
            sector='NIFTY_AUTO',
            stock=top_stock,
            initial_capital=100000
        )
        
        if results:
            print("\n✅ Example completed successfully!")
    else:
        print("\n⚠️  No candidates found. Try a different sector or time period.")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        # Run interactive menu
        interactive_menu()
        
        # Or run example
        # example_usage()
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please try again or report this issue.\n")

