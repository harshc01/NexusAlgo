import requests
import asyncio
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from core.models import MarketCandle
import logging
import os
# from fyers_apiv3 import fyersModel  # TODO: enable when fyers_apiv3 is added to requirements.txt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusEngine")

class BaseFeeder(ABC):
    """Abstract interface for all market data feeders."""
    @abstractmethod
    async def fetch_latest(self, symbol: str) -> MarketCandle | None:
        pass

class BinanceFeeder(BaseFeeder):
    """High-speed crypto feeder. Active default for testing."""
    async def fetch_latest(self, symbol: str, interval: str = '1m') -> MarketCandle | None:
        binance_symbol = symbol.replace("-USD", "USDT").upper()
        url = f"https://api.binance.com/api/v3/klines?symbol={binance_symbol}&interval={interval}&limit=1"
        try:
            response = await asyncio.to_thread(requests.get, url)
            data = response.json()
            if not data or isinstance(data, dict): return None
            latest = data[0]
            return MarketCandle(
                symbol=symbol,
                timestamp=datetime.fromtimestamp(latest[0] / 1000.0),
                open_price=float(latest[1]),
                high_price=float(latest[2]),
                low_price=float(latest[3]),
                close_price=float(latest[4]),
                volume=float(latest[5]),
                source="BINANCE"
            )
        except Exception as e:
            logger.error(f"Binance Feeder Error: {e}")
            return None

# TODO: Uncomment FyersFeeder when fyers_apiv3 is added to requirements.txt
# class FyersFeeder(BaseFeeder):
#     """Official Fyers API adapter."""
#     def __init__(self):
#         client_id = os.getenv("FYERS_CLIENT_ID", "DUMMY_ID")
#         access_token = os.getenv("FYERS_ACCESS_TOKEN", "DUMMY_TOKEN")
#         self.fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")
#
#     async def fetch_latest(self, symbol: str, interval: str = '1') -> MarketCandle | None:
#         fyers_symbol = symbol if symbol.startswith("NSE:") else f"NSE:{symbol}-EQ"
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=2)
#
#         data = {
#             "symbol": fyers_symbol, "resolution": interval, "date_format": "0",
#             "range_from": int(start_date.timestamp()), "range_to": int(end_date.timestamp()), "cont_flag": "1"
#         }
#         try:
#             response = await asyncio.to_thread(self.fyers.history, data=data)
#             if response.get("s") != "ok" or not response.get("candles"): return None
#             latest = response["candles"][-1]
#             return MarketCandle(
#                 symbol=symbol, timestamp=datetime.fromtimestamp(latest[0]),
#                 open_price=float(latest[1]), high_price=float(latest[2]),
#                 low_price=float(latest[3]), close_price=float(latest[4]),
#                 volume=float(latest[5]), source="FYERS"
#             )
#         except Exception as e:
#             logger.error(f"Fyers Feeder Error: {e}")
#             return None