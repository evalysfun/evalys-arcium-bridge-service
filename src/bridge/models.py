"""Data models for Arcium bridge"""

from pydantic import BaseModel
from typing import Optional


# Strategy Plan Models
class UserPreferences(BaseModel):
    """User preferences for strategy planning"""
    desired_size: int  # Desired trade size in lamports
    slippage_tolerance: int  # Slippage tolerance in basis points
    risk_appetite: int  # Risk appetite: 0-255
    preferred_hold_time: int  # Preferred hold time in seconds


class UserHistory(BaseModel):
    """User trading history"""
    recent_pnl: int  # Recent PnL (can be negative)
    win_rate: int  # Win rate in basis points (0-10000)
    avg_hold_time: int  # Average hold time in seconds
    total_trades: int  # Total number of trades


class CurveState(BaseModel):
    """Public curve state"""
    current_price: int  # Current token price
    liquidity_depth: int  # Available liquidity
    volatility: int  # Volatility metric
    recent_volume: int  # Recent trading volume


class StrategyPlan(BaseModel):
    """Confidential strategy plan result"""
    plan_id: Optional[str] = None
    recommended_mode: str  # "normal", "stealth", "max_ghost"
    num_slices: int  # Recommended number of order slices
    slice_size_base: int  # Base slice size
    timing_window_sec: int  # Recommended timing window
    risk_level: int  # Computed risk level: 0-255
    max_notional: int  # Maximum notional to commit


# Risk Score Models
class PortfolioContext(BaseModel):
    """User portfolio context"""
    total_capital: int  # Total portfolio value
    current_exposure: int  # Current exposure in trades
    diversification_score: int  # How diversified (0-255)
    leverage_ratio: int  # Leverage ratio in basis points


class PerformanceHistory(BaseModel):
    """User performance history"""
    total_pnl: int  # Total PnL (can be negative)
    sharpe_ratio: int  # Sharpe ratio (scaled by 100)
    max_drawdown: int  # Max drawdown in basis points
    consistency_score: int  # Consistency: 0-255


class MarketConditions(BaseModel):
    """Market conditions"""
    curve_volatility: int  # Curve volatility
    liquidity_risk: int  # Liquidity risk: 0-255
    market_sentiment: int  # Market sentiment: -128 to 127


class RiskAssessment(BaseModel):
    """Risk assessment result"""
    overall_risk_score: int  # Overall risk: 0-255
    portfolio_risk: int  # Portfolio-specific risk
    trade_risk: int  # Trade-specific risk
    recommendation: str  # "proceed", "caution", "avoid"


# Curve Evaluation Models
class SizingPreferences(BaseModel):
    """User sizing preferences"""
    target_size: int  # Target position size
    min_size: int  # Minimum acceptable size
    max_size: int  # Maximum acceptable size
    capital_allocation_pct: int  # Capital allocation percentage (0-100)


class UserConstraints(BaseModel):
    """User execution constraints"""
    max_slippage_bps: int  # Max slippage in basis points
    time_constraint_sec: int  # Time constraint for execution
    priority_level: int  # Priority: 0-255


class CurveMetrics(BaseModel):
    """Curve metrics"""
    current_price: int  # Current price
    price_change_24h: int  # 24h price change (can be negative)
    liquidity_depth: int  # Available liquidity
    buy_pressure: int  # Buy pressure indicator
    sell_pressure: int  # Sell pressure indicator


class ExecutionRecommendation(BaseModel):
    """Execution recommendation result"""
    recommended_size: int  # Recommended execution size
    entry_price_target: int  # Target entry price
    execution_urgency: int  # Urgency: 0-255
    optimal_timing: int  # Optimal timing window in seconds
    confidence_score: int  # Confidence: 0-255

