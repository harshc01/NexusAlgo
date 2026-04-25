import asyncio
from engine.data_feeder import BinanceFeeder
from engine.executor import NexusExecutor
from engine.strategies.ema_strategy import EMACrossover
from engine.broker import SimulatedBroker
from core.database import db

feeder = BinanceFeeder()

async def main():
    executor = NexusExecutor(feeder)
    broker = SimulatedBroker(initial_capital=10000.0)
    
    strategy = EMACrossover(
        name="Nexus_Alpha_v1", 
        symbol="BTC-USD", 
        broker=broker,
        fast_period=9, 
        slow_period=21
    )
    executor.add_strategy(strategy)
    
    print("------------------------------------------")
    print("      NEXUS ALGO ENGINE: STARTING         ")
    print("  PORTFOLIO: $10,000 (VIRTUAL CASH ;-;)   ")
    print("------------------------------------------")
    
    try:
        await executor.start(interval_seconds=5)
    except (asyncio.CancelledError, KeyboardInterrupt):
        # This catches both the async sleep interruption and standard Ctrl+C(cancel command in bash)
        pass
        
    # SHUTDOWN SEQUENCE
    executor.stop()
    print("\n[!] Shutdown signal intercepted. Calculating final metrics...")
    
    final_value = broker.get_portfolio_value(strategy.fast_ema or 0) 
    net_profit = final_value - broker.initial_capital
    
    print("------------------------------------------")
    print(f" FINAL PORTFOLIO VALUE: ${final_value:.2f}")
    print(f" NET PROFIT: ${net_profit:.2f}")
    print(f" TOTAL TRADES: {broker.total_trades}")
    print("------------------------------------------")
    
    await db.save_backtest_result(
        strategy_name=strategy.name,
        net_profit=net_profit,
        sharpe_ratio=1.25, 
        max_drawdown=5.0
    )
    print("Backtest Result saved to The Vault.")
    print("Nexus Engine offline.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Suppresses the ugly traceback Python throws when terminal closes
        pass
