import asyncio
from typing import List
from core.strategy import BaseStrategy
from engine.data_feeder import BaseFeeder
from core.database import db

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
        print(f"Nexus Engine: Starting execution for {len(self.strategies)} strategies.")
        
        while self.is_running:
            for strategy in self.strategies:
                #Fetch latest data
                candle = await self.feeder.fetch_latest(strategy.symbol)
                
                if candle:
                    #Feed data to the strategy
                    await strategy.on_candle(candle)
                    
                    #Storage in Supabase for the 'Dashboard' UI simultaneously. 
                    await db.save_candle(candle)
            
            await asyncio.sleep(interval_seconds)

    def stop(self):
        self.is_running = False
