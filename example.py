"""Example usage of Evalys Arcium Bridge Service"""

import asyncio
from src.bridge.arcium_client import ArciumBridgeClient
from src.bridge.models import (
    UserPreferences,
    UserHistory,
    CurveState,
    PortfolioContext,
    PerformanceHistory,
    MarketConditions,
    SizingPreferences,
    UserConstraints,
    CurveMetrics,
)


async def main():
    """Example usage"""
    client = ArciumBridgeClient()
    
    print("=== Example: Confidential Strategy Plan ===\n")
    
    # Example user preferences
    prefs = UserPreferences(
        desired_size=1_000_000_000,  # 1 SOL
        slippage_tolerance=100,  # 1%
        risk_appetite=150,  # Moderate
        preferred_hold_time=3600,  # 1 hour
    )
    
    # Example user history
    history = UserHistory(
        recent_pnl=5_000_000,  # 0.005 SOL profit
        win_rate=6500,  # 65%
        avg_hold_time=1800,  # 30 minutes
        total_trades=50,
    )
    
    # Example curve state
    curve = CurveState(
        current_price=1_000_000,  # 0.001 SOL per token
        liquidity_depth=5_000_000_000,  # 5 SOL
        volatility=300,  # Moderate volatility
        recent_volume=10_000_000_000,  # 10 SOL
    )
    
    # Get confidential plan
    plan = await client.get_confidential_plan(
        user_preferences=prefs,
        user_history=history,
        curve_state=curve,
    )
    
    print(f"Recommended Mode: {plan.recommended_mode}")
    print(f"Number of Slices: {plan.num_slices}")
    print(f"Slice Size Base: {plan.slice_size_base}")
    print(f"Timing Window: {plan.timing_window_sec}s")
    print(f"Risk Level: {plan.risk_level}")
    print(f"Max Notional: {plan.max_notional}")
    
    print("\n=== Example: Risk Score ===\n")
    
    # Example portfolio context
    portfolio = PortfolioContext(
        total_capital=10_000_000_000,  # 10 SOL
        current_exposure=3_000_000_000,  # 3 SOL
        diversification_score=180,  # Good diversification
        leverage_ratio=10_000,  # 1x leverage
    )
    
    # Example performance history
    perf = PerformanceHistory(
        total_pnl=2_000_000,  # 0.002 SOL profit
        sharpe_ratio=120,  # Good Sharpe ratio
        max_drawdown=2000,  # 20% max drawdown
        consistency_score=200,  # Good consistency
    )
    
    # Example market conditions
    market = MarketConditions(
        curve_volatility=400,  # Moderate volatility
        liquidity_risk=100,  # Low liquidity risk
        market_sentiment=50,  # Positive sentiment
    )
    
    # Get risk assessment
    risk = await client.get_risk_score(
        portfolio_context=portfolio,
        performance_history=perf,
        market_conditions=market,
    )
    
    print(f"Overall Risk Score: {risk.overall_risk_score}")
    print(f"Portfolio Risk: {risk.portfolio_risk}")
    print(f"Trade Risk: {risk.trade_risk}")
    print(f"Recommendation: {risk.recommendation}")
    
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

