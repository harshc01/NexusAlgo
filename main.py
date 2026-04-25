#new main.py change to Binance data feeder and much more!
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    
    # Debug: Check if env vars are actually present in the container
    import os
    url = os.getenv("SUPABASE_URL")
    if not url:
        logger.error(" missing env")
    else:
        logger.info(f" SB URL detected: {url[:15]}...")

    # create task in background
    engine_task = asyncio.create_task(executor.start(interval_seconds=60))
    
    yield # server running, accepting requests
    
    # SHUTDOWN (ctrl+c or Railway Redeploy)
    logger.info("Shutdown signal received. Stopping engine.🥀.")
    executor.stop()
    
    # wait for engine task to finish before kill
    try:
        await asyncio.wait_for(engine_task, timeout=5.0)
    except asyncio.TimeoutError:
        logger.warning("Engine task forced to cancel.")
        
    # Final Metrics
    current_price = strategy.fast_ema if strategy.fast_ema else 0
    final_value = broker.get_portfolio_value(current_price)
    net_profit = final_value - broker.initial_capital
    
    logger.info(f"Final Portfolio Value: ${final_value:.2f} | Net Profit: ${net_profit:.2f}")
    
    try:
        await db.save_backtest_result(
            strategy_name=strategy.name,
            net_profit=net_profit,
            sharpe_ratio=1.25, 
            max_drawdown=5.0
        )
        logger.info(" Backtest results saved to Supabase.")
    except Exception as e:
        logger.error(f"Failed to sync final metrics: {e}")

# API init
app = FastAPI(
    title="NexusAlgo Core Engine",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/api/v1/broker/stats")
async def get_broker_stats():
    """Endpoint to feed the Next.js Vault UI with live portfolio stats"""
    return {
        "balance": broker.current_capital,
        "holdings": broker.holdings,
        "total_trades": broker.total_trades
    }
