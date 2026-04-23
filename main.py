from fastapi import FastAPI, HTTPException
from engine.data_feeder import YFinanceFeeder
from core.models import MarketCandle

app = FastAPI(
    title="NexusAlgo Core Engine",
    description="High-performance async trading backend.",
    version="1.0.0"
)

# to initialize active feeder
feeder = YFinanceFeeder()

@app.get("/")
async def engine_status():
    """Health check endpoint for the Next.js frontend."""
    return {
        "status": "online",
        "engine": "NexusAlgo v1.",
        "active_feeder": "YFinance"
    }

@app.get("/api/v1/market/quote/{symbol}", response_model=MarketCandle)
async def get_latest_quote(symbol: str):
    """ Fetch the latest OHLCV data for a specific symbol"""
    candle = await feeder.fetch_latest(symbol)
    
    if not candle:
        raise HTTPException(status_code=404, detail=f"Market data unavailable for {symbol}")
    
    return candle