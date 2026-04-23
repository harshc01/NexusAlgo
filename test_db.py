import asyncio
from core.database import db
from core.models import MarketCandle
from datetime import datetime

async def test():
    test_candle = MarketCandle(
        symbol="TEST",
        timestamp=datetime.now(),
        open_price=100.0,
        high_price=110.0,
        low_price=90.0,
        close_price=105.0,
        volume=1000.0,
        source="YFINANCE"
    )
    print("Sending test candle to Supabase...")
    res = await db.save_candle(test_candle)
    print("Response:", res)

if __name__ == "__main__":
    asyncio.run(test())
