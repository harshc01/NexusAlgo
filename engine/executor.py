import asyncio
import logging
from typing import List
from core.strategy import BaseStrategy
from engine.data_feeder import BaseFeeder
from core.database import db

logger = logging.getLogger("NexusExecutor")

class NexusExecutor:
    """The engine that pumps data into your strategies and saves the heartbeat."""
    
    def __init__(self, feeder: BaseFeeder):
        self.feeder = feeder
        self.strategies: List[BaseStrategy] = []
        self.is_running = False

    def add_strategy(self, strategy: BaseStrategy):
        self.strategies.append(strategy)

    async def start(self, interval_seconds: int = 60):
        """Main loop that drives the entire NexusAlgo ecosystem."""
        self.is_running = True
        logger.info(f"Nexus Engine: Starting execution for {len(self.strategies)} strategies.")
        
        while self.is_running:
            logger.info("Nexus Engine: Running iteration for all strategies.")
            try:
                for strategy in self.strategies:
                    #Fetch latest data
                    candle = await self.feeder.fetch_latest(strategy.symbol)
                    
                    if candle:
                        #Feed data to the strategy
                        await strategy.on_candle(candle)
                        
                        #Storage in Supabase for the 'Dashboard' UI simultaneously. 
                        await db.save_candle(candle)
                    else:
                        logger.warning(f"Nexus Engine: No candle data returned for symbol '{strategy.symbol}'.")
            except Exception as e:
                logger.error(f"Nexus Engine: Unhandled exception in main loop: {e}", exc_info=True)
            
            await asyncio.sleep(interval_seconds)

    def stop(self):
        self.is_running = False
