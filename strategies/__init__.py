"""
Trading Strategies
"""

from .ma_crossover import MovingAverageCrossover
from .momentum import MomentumStrategy
from .mean_reversion import MeanReversionStrategy
from .combined_strategy import CombinedStrategy, AggressiveCombinedStrategy
from .rsi_bb_strategy import RSIBollingerStrategy, AggressiveRSIBBStrategy
from .stochastic_breakout import StochasticBreakoutStrategy, AggressiveStochasticStrategy
from .vwap_reversal import VWAPReversalStrategy, AggressiveVWAPStrategy
from .supertrend_momentum import SupertrendMomentumStrategy, AggressiveSupertrendStrategy
from .keltner_squeeze import KeltnerSqueezeStrategy, AggressiveSqueezeStrategy
from .williams_trend import WilliamsTrendStrategy, AggressiveWilliamsStrategy
from .donchian_breakout import (
    DonchianBreakoutStrategy,
    AggressiveDonchianStrategy,
    TurtleTradersStrategy
)

__all__ = [
    'MovingAverageCrossover',
    'MomentumStrategy',
    'MeanReversionStrategy',
    'CombinedStrategy',
    'AggressiveCombinedStrategy',
    'RSIBollingerStrategy',
    'AggressiveRSIBBStrategy',
    'StochasticBreakoutStrategy',
    'AggressiveStochasticStrategy',
    'VWAPReversalStrategy',
    'AggressiveVWAPStrategy',
    'SupertrendMomentumStrategy',
    'AggressiveSupertrendStrategy',
    'KeltnerSqueezeStrategy',
    'AggressiveSqueezeStrategy',
    'WilliamsTrendStrategy',
    'AggressiveWilliamsStrategy',
    'DonchianBreakoutStrategy',
    'AggressiveDonchianStrategy',
    'TurtleTradersStrategy'
]

