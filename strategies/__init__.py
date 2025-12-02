"""
Trading Strategies
"""

from .ma_crossover import MovingAverageCrossover
from .momentum import MomentumStrategy
from .mean_reversion import MeanReversionStrategy
from .combined_strategy import CombinedStrategy, AggressiveCombinedStrategy
from .rsi_bb_strategy import RSIBollingerStrategy, AggressiveRSIBBStrategy

__all__ = [
    'MovingAverageCrossover',
    'MomentumStrategy',
    'MeanReversionStrategy',
    'CombinedStrategy',
    'AggressiveCombinedStrategy',
    'RSIBollingerStrategy',
    'AggressiveRSIBBStrategy'
]

