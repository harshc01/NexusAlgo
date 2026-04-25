from supabase import create_client, Client
from core.config import settings
from core.models import MarketCandle
import logging

logger = logging.getLogger("NexusDB")

class NexusDB:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    async def save_candle(self, candle: MarketCandle):
        """Saves a single market candle to the 'market_data' table."""
        try:
            data = candle.model_dump()
            # convert datetime to string for JSON compatbility
            data['timestamp'] = data['timestamp'].isoformat()
            
            response = self.client.table("market_data").upsert(data).execute()
            return response
        except Exception as e:
            logger.error(f"Database Error: {e}")
            return None

    async def save_backtest_result(self, strategy_name: str, net_profit: float, sharpe_ratio: float, max_drawdown: float):
        """Saves the final run metrics to The Vault."""
        try:
            data = {
                "strategy_name": strategy_name,
                "net_profit": net_profit,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown
            }
            response = self.client.table("backtest_results").insert(data).execute()
            logger.info("saved backtest results to The Vault.")
            return response
        except Exception as e:
            logger.error(f"Failed to save backtest: {e}")
            return None
            
db = NexusDB()
