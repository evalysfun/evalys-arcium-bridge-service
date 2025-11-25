"""
Tests for intent schema validation

Tests that malformed or invalid intents are rejected before processing.
"""

import pytest
from pydantic import ValidationError
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


def test_user_preferences_validation():
    """Test that UserPreferences validates correctly"""
    # Valid preferences
    prefs = UserPreferences(
        desired_size=1_000_000_000,
        slippage_tolerance=100,
        risk_appetite=150,
        preferred_hold_time=3600
    )
    assert prefs.desired_size == 1_000_000_000
    
    # Invalid: negative size
    with pytest.raises(ValidationError):
        UserPreferences(
            desired_size=-1000,
            slippage_tolerance=100,
            risk_appetite=150,
            preferred_hold_time=3600
        )
    
    # Invalid: risk_appetite out of range (should be 0-255)
    with pytest.raises(ValidationError):
        UserPreferences(
            desired_size=1_000_000_000,
            slippage_tolerance=100,
            risk_appetite=300,  # Out of range
            preferred_hold_time=3600
        )


def test_user_history_validation():
    """Test that UserHistory validates correctly"""
    # Valid history
    history = UserHistory(
        recent_pnl=-5000000,  # Can be negative
        win_rate=6500,
        avg_hold_time=1800,
        total_trades=50
    )
    assert history.recent_pnl == -5000000
    
    # Invalid: win_rate out of range (should be 0-10000)
    with pytest.raises(ValidationError):
        UserHistory(
            recent_pnl=5000000,
            win_rate=15000,  # Out of range
            avg_hold_time=1800,
            total_trades=50
        )


def test_curve_state_validation():
    """Test that CurveState validates correctly"""
    # Valid curve state
    curve = CurveState(
        current_price=1000000,
        liquidity_depth=5000000000,
        volatility=300,
        recent_volume=10000000000
    )
    assert curve.current_price == 1000000
    
    # Invalid: negative price
    with pytest.raises(ValidationError):
        CurveState(
            current_price=-1000,
            liquidity_depth=5000000000,
            volatility=300,
            recent_volume=10000000000
        )


def test_portfolio_context_validation():
    """Test that PortfolioContext validates correctly"""
    # Valid context
    context = PortfolioContext(
        total_capital=10_000_000_000,
        current_exposure=3_000_000_000,
        diversification_score=180,
        leverage_ratio=10000
    )
    assert context.total_capital == 10_000_000_000
    
    # Invalid: exposure exceeds capital
    # (This is a business logic check, not validation - but good to test)
    context = PortfolioContext(
        total_capital=1_000_000_000,
        current_exposure=2_000_000_000,  # Exceeds capital (but validation passes)
        diversification_score=180,
        leverage_ratio=10000
    )
    # Note: Pydantic validation doesn't check business logic
    # This would be checked in the risk assessment logic


def test_missing_required_fields():
    """Test that missing required fields are rejected"""
    # Missing desired_size
    with pytest.raises(ValidationError):
        UserPreferences(
            slippage_tolerance=100,
            risk_appetite=150,
            preferred_hold_time=3600
            # Missing desired_size
        )


def test_type_validation():
    """Test that wrong types are rejected"""
    # String instead of int
    with pytest.raises(ValidationError):
        UserPreferences(
            desired_size="not_a_number",  # Should be int
            slippage_tolerance=100,
            risk_appetite=150,
            preferred_hold_time=3600
        )

