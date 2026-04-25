import logging

logger = logging.getLogger("NexusBroker")

class SimulatedBroker:
    """A virtual broker to simulate trades, track capital, and calculate PnL."""
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.holdings = 0.0
        self.total_trades = 0

    def process_signal(self, symbol: str, action: str, price: float):
        if action == "BUY" and self.current_capital > 0:
            self.holdings = self.current_capital / price
            self.current_capital = 0.0
            self.total_trades += 1
            logger.info(f"🟢➕️ BROKER: Bought {self.holdings:.4f} {symbol} @ ${price:.2f}")

        elif action == "SELL" and self.holdings > 0:
            self.current_capital = self.holdings * price
            self.holdings = 0.0
            self.total_trades += 1
            pnl = self.current_capital - self.initial_capital
            logger.info(f"🔴➖️ BROKER: Sold {symbol} @ ${price:.2f} | Balance: ${self.current_capital:.2f} | PnL: ${pnl:.2f}")

    def get_portfolio_value(self, current_price: float) -> float:
        """Calculates total net worth (Cash + Active Asset Value)."""
        return self.current_capital + (self.holdings * current_price)
