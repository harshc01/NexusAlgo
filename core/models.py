from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal

class MarketCandle(BaseModel):
    """Standardized OHLCV data model for all feed sources."""
    model_config = ConfigDict(populate_by_name=True)

    symbol: str = Field(..., description="The ticker symbol (e.g., BTCUSD, INFY, NVDA)")
    timestamp: datetime
    open_price: float = Field(..., gt=0)
    high_price: float = Field(..., gt=0)
    low_price: float = Field(..., gt=0)
    close_price: float = Field(..., gt=0)
    volume: float = Field(default=0.0, ge=0)
    source: Literal["YFINANCE", "ALPACA", "FYERS"] = "YFINANCE"

class BacktestResult(BaseModel):
    """Model for sending backtest metrics to the Next.js Vault UI."""
    strategy_name: str
    run_date: datetime = Field(default_factory=datetime.utcnow)
    net_profit: float
    sharpe_ratio: float
    max_drawdown: float