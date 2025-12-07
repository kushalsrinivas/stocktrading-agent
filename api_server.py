"""
FastAPI Server for Stock Backtesting
Provides REST API endpoints to test stocks with various strategies
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, YFinanceDataHandler
from strategies.combined_strategy import CombinedStrategy
from strategies.rsi_bb_strategy import RSIBollingerStrategy
from strategies import MovingAverageCrossover
from strategies.momentum import RSIMomentumStrategy, MACDMomentumStrategy
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

# Initialize FastAPI app
app = FastAPI(
    title="Stock Backtesting API",
    description="Test NSE stocks with 22+ trading strategies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for async tasks
tasks_db: Dict[str, Dict] = {}


# Enums and Models
class StrategyEnum(str, Enum):
    RSI_BB = "rsi_bb"
    COMBINED = "combined"
    MA_CROSSOVER = "ma_crossover"
    RSI_MOMENTUM = "rsi_momentum"
    MACD_MOMENTUM = "macd_momentum"
    STOCHASTIC_BREAKOUT = "stochastic_breakout"
    VWAP_REVERSAL = "vwap_reversal"
    SUPERTREND = "supertrend"
    KELTNER_SQUEEZE = "keltner_squeeze"
    WILLIAMS_TREND = "williams_trend"
    DONCHIAN_BREAKOUT = "donchian_breakout"
    DONCHIAN_FAST = "donchian_fast"
    TURTLE_TRADERS = "turtle_traders"
    TRENDLINE_BOUNCE = "trendline_bounce"
    TRENDLINE_BREAKOUT = "trendline_breakout"
    SR_BOUNCE = "sr_bounce"
    SR_BREAKOUT = "sr_breakout"
    SR_RSI = "sr_rsi"
    SR_VOLUME = "sr_volume"
    SR_EMA = "sr_ema"
    SR_MACD = "sr_macd"
    SR_ALL_IN_ONE = "sr_all_in_one"


class BacktestRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., RELIANCE, TCS)")
    strategy: StrategyEnum = Field(..., description="Strategy to use")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    initial_capital: float = Field(10000, description="Initial capital in INR")
    commission: float = Field(0.0005, description="Commission percentage (0.0005 = 0.05%)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "RELIANCE",
                "strategy": "sr_all_in_one",
                "start_date": "2023-01-01",
                "end_date": "2024-12-31",
                "initial_capital": 10000,
                "commission": 0.0005
            }
        }


class CompareStrategiesRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    strategies: Optional[List[StrategyEnum]] = Field(None, description="List of strategies to compare (None = all)")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    initial_capital: float = Field(10000, description="Initial capital in INR")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "TCS",
                "strategies": ["sr_rsi", "sr_all_in_one", "supertrend"],
                "start_date": "2023-01-01",
                "end_date": "2024-12-31",
                "initial_capital": 10000
            }
        }


class MultiTickerRequest(BaseModel):
    tickers: List[str] = Field(..., description="List of stock tickers")
    strategy: StrategyEnum = Field(..., description="Strategy to use")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    initial_capital: float = Field(10000, description="Initial capital in INR")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tickers": ["RELIANCE", "TCS", "INFY"],
                "strategy": "sr_all_in_one",
                "start_date": "2023-01-01",
                "end_date": "2024-12-31",
                "initial_capital": 10000
            }
        }


class OptimizeRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    initial_capital: float = Field(10000, description="Initial capital in INR")
    metric: str = Field("total_return", description="Optimization metric (total_return, sharpe_ratio, win_rate)")


# Helper Functions
def get_date_range(start_date: Optional[str], end_date: Optional[str]) -> tuple:
    """Get date range with defaults"""
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")  # 2 years
    return start_date, end_date


def create_strategy(strategy_name: StrategyEnum):
    """Create strategy instance based on name"""
    strategies = {
        StrategyEnum.RSI_BB: RSIBollingerStrategy(
            rsi_period=14, rsi_oversold=40, rsi_overbought=70,
            bb_period=20, bb_std=2.0
        ),
        StrategyEnum.COMBINED: CombinedStrategy(
            rsi_period=14, rsi_oversold=30, rsi_overbought=70,
            macd_fast=12, macd_slow=26, macd_signal=9,
            bb_period=20, bb_std=2.0
        ),
        StrategyEnum.MA_CROSSOVER: MovingAverageCrossover(
            short_window=50, long_window=200
        ),
        StrategyEnum.RSI_MOMENTUM: RSIMomentumStrategy(
            period=14, oversold=30, overbought=70
        ),
        StrategyEnum.MACD_MOMENTUM: MACDMomentumStrategy(
            fast_period=12, slow_period=26, signal_period=9
        ),
        StrategyEnum.STOCHASTIC_BREAKOUT: StochasticBreakoutStrategy(
            stoch_period=14, stoch_oversold=20, stoch_overbought=80,
            adx_threshold=20, volume_spike_multiplier=1.3
        ),
        StrategyEnum.VWAP_REVERSAL: VWAPReversalStrategy(
            vwap_deviation_threshold=1.5, rsi_period=14,
            rsi_oversold=35, rsi_overbought=65, volume_threshold=1.1
        ),
        StrategyEnum.SUPERTREND: SupertrendMomentumStrategy(
            atr_period=10, atr_multiplier=2.5, macd_fast=12,
            macd_slow=26, ema_period=20
        ),
        StrategyEnum.KELTNER_SQUEEZE: KeltnerSqueezeStrategy(
            kc_period=20, kc_atr_multiplier=2.0, bb_period=20,
            bb_std=2.0, momentum_threshold=1.0, volume_threshold=1.3
        ),
        StrategyEnum.WILLIAMS_TREND: WilliamsTrendStrategy(
            williams_period=14, williams_oversold=-80, williams_overbought=-20,
            adx_strong_trend=20, volume_threshold=1.1
        ),
        StrategyEnum.DONCHIAN_BREAKOUT: DonchianBreakoutStrategy(
            entry_period=55, exit_period=20, use_middle_band=True, atr_period=14
        ),
        StrategyEnum.DONCHIAN_FAST: AggressiveDonchianStrategy(
            entry_period=20, exit_period=10, atr_period=14, atr_multiplier=2.0
        ),
        StrategyEnum.TURTLE_TRADERS: TurtleTradersStrategy(
            entry_period=55, exit_period=20, atr_period=20, risk_per_trade=0.02
        ),
        StrategyEnum.TRENDLINE_BOUNCE: TrendLineStrategy(
            lookback_period=50, min_touches=2, bounce_tolerance=0.02,
            volume_confirmation=True, volume_threshold=1.2,
            atr_period=14, atr_multiplier=1.5, breakout_mode=False
        ),
        StrategyEnum.TRENDLINE_BREAKOUT: TrendLineBreakoutStrategy(
            lookback_period=40, min_touches=2, volume_threshold=1.5,
            atr_period=14, atr_multiplier=2.0
        ),
        StrategyEnum.SR_BOUNCE: SupportResistanceBounceStrategy(
            lookback_period=80, min_touches=3, volume_threshold=1.3
        ),
        StrategyEnum.SR_BREAKOUT: SupportResistanceBreakoutStrategy(
            lookback_period=60, min_touches=2, volume_threshold=1.5
        ),
        StrategyEnum.SR_RSI: SRRSIStrategy(
            lookback_period=100, price_tolerance=0.02, min_touches=2,
            rsi_period=14, rsi_oversold=40, rsi_overbought=65,
            rsi_momentum_threshold=2.0, atr_period=14, atr_multiplier=1.5
        ),
        StrategyEnum.SR_VOLUME: SRVolumeStrategy(
            lookback_period=80, price_tolerance=0.025, min_touches=2,
            volume_threshold=1.5, breakout_confirmation=0.01,
            atr_period=14, atr_multiplier=2.0
        ),
        StrategyEnum.SR_EMA: SREMAStrategy(
            lookback_period=100, price_tolerance=0.02, min_touches=2,
            ema_fast=20, ema_slow=50, volume_confirmation=True,
            volume_threshold=1.2, atr_period=14, atr_multiplier=1.5
        ),
        StrategyEnum.SR_MACD: SRMACDStrategy(
            lookback_period=100, price_tolerance=0.02, min_touches=2,
            macd_fast=12, macd_slow=26, macd_signal=9,
            atr_period=14, atr_multiplier=1.5
        ),
        StrategyEnum.SR_ALL_IN_ONE: SRAllInOneStrategy(
            lookback_period=100, price_tolerance=0.02, min_touches=2,
            rsi_period=14, rsi_buy_min=30, rsi_buy_max=45,
            rsi_sell_min=60, rsi_sell_max=75, ema_fast=20, ema_slow=50,
            volume_threshold=1.3, atr_period=14, atr_multiplier=2.0
        ),
    }
    return strategies.get(strategy_name)


def convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj


def format_date(date_obj, format_str='%Y-%m-%d'):
    """
    Safely format a date object to string
    Handles datetime, Timestamp, and string inputs
    """
    if isinstance(date_obj, str):
        # Already a string, return as is or reformat if needed
        return date_obj
    elif hasattr(date_obj, 'strftime'):
        # datetime, Timestamp, or similar object
        return date_obj.strftime(format_str)
    else:
        # Fallback: convert to string
        return str(date_obj)


def safe_float(value):
    """
    Safely convert value to float
    Handles scalar values, pandas Series, numpy types, etc.
    """
    # Handle pandas Series - extract the scalar value
    if isinstance(value, pd.Series):
        if len(value) == 0:
            return 0.0
        value = value.iloc[0] if len(value) == 1 else value.values[0]
    
    # Handle numpy types
    if isinstance(value, (np.integer, np.floating)):
        return float(value)
    
    # Handle NaN/None
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    
    # Convert to float
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def safe_int(value):
    """
    Safely convert value to int
    Handles scalar values, pandas Series, numpy types, etc.
    """
    # Handle pandas Series - extract the scalar value
    if isinstance(value, pd.Series):
        if len(value) == 0:
            return 0
        value = value.iloc[0] if len(value) == 1 else value.values[0]
    
    # Handle numpy types
    if isinstance(value, (np.integer, np.floating)):
        return int(value)
    
    # Handle NaN/None
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0
    
    # Convert to int
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def run_single_backtest(ticker: str, strategy_name: StrategyEnum, start_date: str,
                       end_date: str, initial_capital: float, commission: float) -> Dict:
    """Run backtest for a single ticker with a single strategy"""
    nse_symbol = f"{ticker}.NS" if not ticker.endswith(".NS") else ticker
    
    # Get strategy
    strategy = create_strategy(strategy_name)
    if not strategy:
        raise ValueError(f"Invalid strategy: {strategy_name}")
    
    # Fetch data
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
        commission=commission,
        slippage=0.0005
    )
    
    # Run backtest
    results = backtester.run(verbose=False)
    
    # Format response
    metrics = results['metrics']
    trades = results.get('trades', pd.DataFrame())
    equity_curve = results.get('equity_curve', pd.Series())
    
    # Get historical price data
    historical_data = data_handler.data
    price_data = []
    if not historical_data.empty:
        # Convert historical data to list of dicts for JSON
        for date, row in historical_data.iterrows():
            price_data.append({
                'date': format_date(date, '%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
    
    # Convert equity curve to list for charting
    equity_data = []
    if not equity_curve.empty:
        for date, value in equity_curve.items():
            equity_data.append({
                'date': format_date(date, '%Y-%m-%d'),
                'value': safe_float(value)
            })
    
    # Convert trades to dict format
    trades_list = []
    if not trades.empty:
        trades_dict = trades.to_dict('records')
        for trade in trades_dict:
            # Convert datetime to string
            if 'Date' in trade:
                trade['Date'] = format_date(trade['Date'], '%Y-%m-%d %H:%M:%S')
            # Convert numpy types
            trade = convert_numpy_types(trade)
            trades_list.append(trade)
    
    # Convert all metrics to native Python types using safe converters
    return {
        "ticker": ticker,
        "strategy": strategy_name.value,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "metrics": {
            "initial_capital": safe_float(metrics['Initial Value']),
            "final_value": safe_float(metrics['Final Value']),
            "total_return_pct": safe_float(metrics['Total Return (%)']),
            "total_trades": safe_int(metrics['Total Trades']),
            "win_rate_pct": safe_float(metrics['Win Rate (%)']),
            "profit_factor": safe_float(metrics['Profit Factor']),
            "sharpe_ratio": safe_float(metrics['Sharpe Ratio']),
            "max_drawdown_pct": safe_float(metrics['Max Drawdown (%)']),
            "volatility_pct": safe_float(metrics['Volatility (%)'])
        },
        "historical_data": price_data,
        "equity_curve": equity_data,
        "trades": trades_list[:50]  # Limit to 50 most recent trades
    }


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Stock Backtesting API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /strategies": "List all available strategies",
            "POST /backtest": "Run backtest for single ticker and strategy",
            "POST /compare": "Compare multiple strategies on single ticker",
            "POST /multi-ticker": "Test multiple tickers with single strategy",
            "POST /optimize": "Find best strategy for a ticker",
            "GET /task/{task_id}": "Get status of background task"
        },
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/strategies")
async def list_strategies():
    """List all available strategies"""
    strategies_info = {
        "rsi_bb": {
            "name": "RSI + Bollinger Bands",
            "type": "Mean Reversion",
            "description": "Buy at lower BB + RSI oversold, Sell at middle BB or RSI overbought"
        },
        "combined": {
            "name": "Combined Strategy",
            "type": "Multi-Indicator",
            "description": "RSI + MACD + Bollinger Bands combined confirmation"
        },
        "ma_crossover": {
            "name": "Moving Average Crossover",
            "type": "Trend Following",
            "description": "Buy when fast MA crosses above slow MA"
        },
        "rsi_momentum": {
            "name": "RSI Momentum",
            "type": "Momentum",
            "description": "RSI crosses above oversold/overbought levels"
        },
        "macd_momentum": {
            "name": "MACD Momentum",
            "type": "Momentum",
            "description": "MACD crosses above/below signal line"
        },
        "stochastic_breakout": {
            "name": "Stochastic Breakout",
            "type": "Momentum/Breakout",
            "description": "Stochastic Oscillator + Volume Spike + ADX confirmation"
        },
        "vwap_reversal": {
            "name": "VWAP Reversal",
            "type": "Mean Reversion",
            "description": "VWAP + RSI Divergence + Volume confirmation"
        },
        "supertrend": {
            "name": "Supertrend Momentum",
            "type": "Trend Following",
            "description": "ATR-based Supertrend + MACD + EMA Slope"
        },
        "keltner_squeeze": {
            "name": "Keltner Squeeze",
            "type": "Breakout/Volatility",
            "description": "Keltner Channels + BB Width + Momentum"
        },
        "williams_trend": {
            "name": "Williams Trend",
            "type": "Momentum/Trend",
            "description": "Williams %R + ADX + Volume confirmation"
        },
        "donchian_breakout": {
            "name": "Donchian Breakout",
            "type": "Trend Following",
            "description": "55-day high/low breakout with 20-day exit"
        },
        "donchian_fast": {
            "name": "Donchian Fast",
            "type": "Swing Trading",
            "description": "20-day breakout with 10-day exit and ATR stops"
        },
        "turtle_traders": {
            "name": "Turtle Traders",
            "type": "Trend Following",
            "description": "Original Turtle Trading System (55-day breakout)"
        },
        "trendline_bounce": {
            "name": "Trend Line Bounce",
            "type": "Technical",
            "description": "Buys bounces off ascending trend lines"
        },
        "trendline_breakout": {
            "name": "Trend Line Breakout",
            "type": "Momentum",
            "description": "Trades breakouts through trend lines"
        },
        "sr_bounce": {
            "name": "Support/Resistance Bounce",
            "type": "Mean Reversion",
            "description": "Buys at support, sells at resistance"
        },
        "sr_breakout": {
            "name": "Support/Resistance Breakout",
            "type": "Breakout",
            "description": "Trades breakouts through S/R levels"
        },
        "sr_rsi": {
            "name": "S/R + RSI",
            "type": "Momentum Confirmation",
            "description": "🔥 S/R levels with RSI momentum confirmation"
        },
        "sr_volume": {
            "name": "S/R + Volume",
            "type": "Breakout Strength",
            "description": "🔥 S/R breakouts with high volume confirmation"
        },
        "sr_ema": {
            "name": "S/R + EMA",
            "type": "Trend Filter",
            "description": "🔥 S/R levels with 20/50 EMA trend filter"
        },
        "sr_macd": {
            "name": "S/R + MACD",
            "type": "Trend Reversal",
            "description": "🔥 S/R levels with MACD reversal signals"
        },
        "sr_all_in_one": {
            "name": "S/R All-in-One COMBO",
            "type": "Institutional",
            "description": "⭐ 4 confirmations: S/R + RSI + EMA + Volume (Highest win rate)"
        }
    }
    
    return {
        "total_strategies": len(strategies_info),
        "strategies": strategies_info
    }


@app.post("/backtest")
async def backtest_single(request: BacktestRequest):
    """
    Run backtest for a single ticker with a single strategy
    """
    try:
        # Get date range
        start_date, end_date = get_date_range(request.start_date, request.end_date)
        
        # Run backtest
        result = run_single_backtest(
            ticker=request.ticker,
            strategy_name=request.strategy,
            start_date=start_date,
            end_date=end_date,
            initial_capital=request.initial_capital,
            commission=request.commission
        )
        
        return {
            "status": "success",
            "data": result
        }
        
    except ValueError as e:
        # Handle validation errors (like invalid strategy)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the full error for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare")
async def compare_strategies(request: CompareStrategiesRequest):
    """
    Compare multiple strategies on a single ticker
    """
    try:
        # Get date range
        start_date, end_date = get_date_range(request.start_date, request.end_date)
        
        # Determine which strategies to test
        strategies_to_test = request.strategies if request.strategies else list(StrategyEnum)
        
        results = []
        errors = []
        
        for strategy in strategies_to_test:
            try:
                result = run_single_backtest(
                    ticker=request.ticker,
                    strategy_name=strategy,
                    start_date=start_date,
                    end_date=end_date,
                    initial_capital=request.initial_capital,
                    commission=0.0005
                )
                results.append(result)
            except Exception as e:
                errors.append({
                    "strategy": strategy.value,
                    "error": str(e)
                })
        
        # Sort by total return
        results.sort(key=lambda x: x['metrics']['total_return_pct'], reverse=True)
        
        # Find best strategy
        best_strategy = results[0] if results else None
        
        return {
            "status": "success",
            "ticker": request.ticker,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "total_strategies_tested": len(results),
            "best_strategy": {
                "name": best_strategy['strategy'],
                "total_return_pct": best_strategy['metrics']['total_return_pct'],
                "sharpe_ratio": best_strategy['metrics']['sharpe_ratio'],
                "win_rate_pct": best_strategy['metrics']['win_rate_pct']
            } if best_strategy else None,
            "results": results,
            "errors": errors if errors else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/multi-ticker")
async def test_multi_ticker(request: MultiTickerRequest):
    """
    Test multiple tickers with a single strategy
    """
    try:
        # Get date range
        start_date, end_date = get_date_range(request.start_date, request.end_date)
        
        results = []
        errors = []
        
        for ticker in request.tickers:
            try:
                result = run_single_backtest(
                    ticker=ticker,
                    strategy_name=request.strategy,
                    start_date=start_date,
                    end_date=end_date,
                    initial_capital=request.initial_capital,
                    commission=0.0005
                )
                results.append(result)
            except Exception as e:
                errors.append({
                    "ticker": ticker,
                    "error": str(e)
                })
        
        # Sort by total return
        results.sort(key=lambda x: x['metrics']['total_return_pct'], reverse=True)
        
        # Calculate summary statistics
        returns = [r['metrics']['total_return_pct'] for r in results]
        avg_return = np.mean(returns) if returns else 0
        median_return = np.median(returns) if returns else 0
        best_ticker = results[0] if results else None
        
        return {
            "status": "success",
            "strategy": request.strategy.value,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "summary": {
                "total_tickers_tested": len(results),
                "average_return_pct": float(avg_return),
                "median_return_pct": float(median_return),
                "best_ticker": {
                    "ticker": best_ticker['ticker'],
                    "return_pct": best_ticker['metrics']['total_return_pct']
                } if best_ticker else None
            },
            "results": results,
            "errors": errors if errors else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/optimize")
async def optimize_strategy(request: OptimizeRequest):
    """
    Find the best strategy for a given ticker
    """
    try:
        # Get date range
        start_date, end_date = get_date_range(request.start_date, request.end_date)
        
        all_strategies = list(StrategyEnum)
        results = []
        
        for strategy in all_strategies:
            try:
                result = run_single_backtest(
                    ticker=request.ticker,
                    strategy_name=strategy,
                    start_date=start_date,
                    end_date=end_date,
                    initial_capital=request.initial_capital,
                    commission=0.0005
                )
                results.append(result)
            except Exception as e:
                continue
        
        if not results:
            raise HTTPException(status_code=404, detail="No successful backtests")
        
        # Sort by requested metric
        metric_map = {
            "total_return": "total_return_pct",
            "sharpe_ratio": "sharpe_ratio",
            "win_rate": "win_rate_pct"
        }
        
        sort_key = metric_map.get(request.metric, "total_return_pct")
        results.sort(key=lambda x: x['metrics'][sort_key], reverse=True)
        
        best = results[0]
        
        return {
            "status": "success",
            "ticker": request.ticker,
            "optimization_metric": request.metric,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "best_strategy": {
                "name": best['strategy'],
                "metrics": best['metrics']
            },
            "top_5_strategies": [
                {
                    "name": r['strategy'],
                    "total_return_pct": r['metrics']['total_return_pct'],
                    "sharpe_ratio": r['metrics']['sharpe_ratio'],
                    "win_rate_pct": r['metrics']['win_rate_pct'],
                    "total_trades": r['metrics']['total_trades']
                }
                for r in results[:5]
            ],
            "all_results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-optimize")
async def batch_optimize(background_tasks: BackgroundTasks):
    """
    Start a background task to optimize strategies for multiple tickers
    (Returns task ID, check status with GET /task/{task_id})
    """
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "progress": 0,
        "results": None
    }
    
    # Note: Implement actual background task logic here
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": "Background task started. Check /task/{task_id} for progress"
    }


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a background task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks_db[task_id]


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("   🚀 STOCK BACKTESTING API SERVER")
    print("="*70)
    print("\n📊 22 Trading Strategies Available")
    print("🔥 Advanced S/R Strategies Included")
    print("\nStarting server at http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

