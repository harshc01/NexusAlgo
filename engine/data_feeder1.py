#will use yfinance later
'''import yfinance as yf
from datetime import datetime, timedelta
import asyncio
from abc import ABC, abstractmethod
from core.models import MarketCandle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusEngine")

class BaseFeeder(ABC):
    """Abstract interface for all market data feeders."""
    @abstractmethod
    async def fetch_latest(self, symbol: str) -> MarketCandle | None:
        pass

class YFinanceFeeder(BaseFeeder):
    """Fallback feeder for historical backtesting."""
    
    async def fetch_latest(self, symbol: str, interval: str = '1m') -> MarketCandle | None:
        try:
            # wrap yfinance call in asyncio to prevent blocking the FastAPI event loop
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=lookback_minutes)
            
            stock = yf.Ticker(symbol)
            df = await asyncio.to_thread(
                stock.history, interval=interval, start=start_time, end=end_time
            )

            if df.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                return None

            latest = df.iloc[-1]
            return MarketCandle(
                symbol=symbol,
                timestamp=latest.name.to_pydatetime(),
                open_price=float(latest['Open']),
                high_price=float(latest['High']),
                low_price=float(latest['Low']),
                close_price=float(latest['Close']),
                volume=float(latest['Volume']),
                source="YFINANCE"
            ) 

        except Exception as e:
            logger.error(f"Feeder Error for {symbol}: {e}")
            return None '''