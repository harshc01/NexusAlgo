from abc import ABC, abstractmethod
from core.models import MarketCandle
import logging

class BaseStrategy(ABC):
    """The master template for all NexusAlgo trading strategies."""
    
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.logger = logging.getLogger(f"Strategy-{name}")

    @abstractmethod
    async def on_candle(self, candle: MarketCandle):
        """This method triggers every time a new price candle arrives."""
        pass

    def log(self, message: str):
        self.logger.info(f"[{self.name}] {message}")
