from core.strategy import BaseStrategy
from core.models import MarketCandle
from engine.broker import SimulatedBroker

class EMACrossover(BaseStrategy):
    """EMA Crossover connected to the Virtual Broker."""
    def __init__(self, name: str, symbol: str, broker: SimulatedBroker, fast_period: int = 9, slow_period: int = 21):
        super().__init__(name, symbol)
        self.broker = broker
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.fast_ema = None
        self.slow_ema = None
        self.position = 0  

    def calculate_ema(self, current_price: float, previous_ema: float, period: int) -> float:
        multiplier = 2 / (period + 1)
        return (current_price - previous_ema) * multiplier + previous_ema

    async def on_candle(self, candle: MarketCandle):
        price = candle.close_price
        
        if self.fast_ema is None:
            self.fast_ema = price
            self.slow_ema = price
            self.log(f"Initialized EMAs at ${price:.2f}")
            return

        new_fast_ema = self.calculate_ema(price, self.fast_ema, self.fast_period)
        new_slow_ema = self.calculate_ema(price, self.slow_ema, self.slow_period)

        if self.fast_ema <= self.slow_ema and new_fast_ema > new_slow_ema:
            if self.position <= 0:
                self.log("Signal: GOLDEN CROSS")
                self.broker.process_signal(self.symbol, "BUY", price)
                self.position = 1
        
        elif self.fast_ema >= self.slow_ema and new_fast_ema < new_slow_ema:
            if self.position >= 0:
                self.log("Signal: DEATH CROSS")
                self.broker.process_signal(self.symbol, "SELL", price)
                self.position = -1

        self.fast_ema = new_fast_ema
        self.slow_ema = new_slow_ema
