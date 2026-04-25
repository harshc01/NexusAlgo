#new main.py change to Binance data feeder and much more!
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import logging
from engine.data_feeder import BinanceFeeder
from engine.executor import NexusExecutor
from engine.strategies.ema_strategy import EMACrossover
from engine.broker import SimulatedBroker
from core.models import MarketCandle
from core.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusAPI")

# initialize engine components
feeder = BinanceFeeder()
executor = NexusExecutor(feeder)
broker = SimulatedBroker(initial_capital=10000.0) #i've run this for more than elon's net worth and it feels amazing paper trading xD

# EMAC Strategy config
strategy = EMACrossover(
    name="Nexus_Alpha_v1", 
    symbol="BTC-USD", 
    broker=broker,
    fast_period=9, 
    slow_period=21
)
executor.add_strategy(strategy)

@asynccontextmanager
async def lifespan(app: FastAPI): #to run indefinitely
    """This function runs when the server starts and stops"""
    # STARTUP
    logger.info("Starting NexusAlgo Engine.🚀.")
    # create task in background
    engine_task = asyncio.create_task(executor.start(interval_seconds=60))
    
    yield # server running, accepting requests
    
    # SHUTDOWN (ctrl+c)
    logger.info("Shutdown signal received. Stopping engine.🥀.")
    executor.stop()
    
    # wait for engine task to finish before kill
    try:
        await asyncio.wait_for(engine_task, timeout=5.0)
    except asyncio.TimeoutError:
        logger.warning("Engine task forced to cancel.")
        
    # Final Metrics
    final_value = broker.get_portfolio_value(strategy.fast_ema or 0)
    net_profit = final_value - broker.initial_capital
    
    logger.info(f"Final Portfolio Value: ${final_value:.2f} | Net Profit: ${net_profit:.2f}")
    
    await db.save_backtest_result(
        strategy_name=strategy.name,
        net_profit=net_profit,
        sharpe_ratio=1.25, 
        max_drawdown=5.0
    )
    logger.info("Backtest results saved to Supabase.")
#
app = FastAPI(
    title="NexusAlgo Core Engine",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"status": "online", "engine": "NexusAlgo v1", "active_feeder": "Binance"}

@app.get("/api/v1/market/quote/{symbol}", response_model=MarketCandle)
async def get_latest_quote(symbol: str):
    candle = await feeder.fetch_latest(symbol)
    if not candle:
        raise HTTPException(status_code=404, detail="Data unavailable")
    return candle