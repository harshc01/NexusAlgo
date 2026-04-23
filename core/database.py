from supabase import create_client, Client
from core.config import settings
from core.models import MarketCandle
import logging

logger = logging.getLogger("NexusDB")

class NexusDB:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    async def save_candle(self, candle: MarketCandle):
        """Saves a single market candle to the 'market_data' table in Supabase."""
        try:
            data = candle.model_dump()
            # Convert datetime to string for JSON compatibility
            data['timestamp'] = data['timestamp'].isoformat()
            
            response = self.client.table("market_data").upsert(data).execute()
            return response
        except Exception as e:
            logger.error(f"Database Error: {e}")
            return None

db = NexusDB()
