"""API routes for Arcium bridge service"""

from fastapi import APIRouter, HTTPException
from ..bridge.arcium_client import ArciumBridgeClient
from ..bridge.models import (
    UserPreferences,
    UserHistory,
    CurveState,
    StrategyPlan,
    PortfolioContext,
    PerformanceHistory,
    MarketConditions,
    RiskAssessment,
    SizingPreferences,
    UserConstraints,
    CurveMetrics,
    ExecutionRecommendation,
)
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize bridge client
bridge_client = ArciumBridgeClient()


@router.post("/arcium/plan", response_model=StrategyPlan)
async def get_confidential_plan(
    user_preferences: UserPreferences,
    user_history: UserHistory,
    curve_state: CurveState,
):
    """
    Get confidential execution plan from Arcium MXE
    
    Computes optimal execution strategy based on encrypted user preferences,
    history, and public curve state.
    """
    try:
        plan = await bridge_client.get_confidential_plan(
            user_preferences=user_preferences,
            user_history=user_history,
            curve_state=curve_state,
        )
        return plan
    except Exception as e:
        logger.error(f"Error getting confidential plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/arcium/risk-score", response_model=RiskAssessment)
async def get_risk_score(
    portfolio_context: PortfolioContext,
    performance_history: PerformanceHistory,
    market_conditions: MarketConditions,
):
    """
    Get confidential risk assessment from Arcium MXE
    
    Evaluates trade risk using encrypted portfolio context, performance history,
    and public market conditions.
    """
    try:
        assessment = await bridge_client.get_risk_score(
            portfolio_context=portfolio_context,
            performance_history=performance_history,
            market_conditions=market_conditions,
        )
        return assessment
    except Exception as e:
        logger.error(f"Error getting risk score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/arcium/curve-eval", response_model=ExecutionRecommendation)
async def get_curve_evaluation(
    sizing_preferences: SizingPreferences,
    user_constraints: UserConstraints,
    curve_metrics: CurveMetrics,
):
    """
    Get confidential curve evaluation from Arcium MXE
    
    Analyzes bonding curve with encrypted user context to provide
    execution recommendations.
    """
    try:
        recommendation = await bridge_client.get_curve_evaluation(
            sizing_preferences=sizing_preferences,
            user_constraints=user_constraints,
            curve_metrics=curve_metrics,
        )
        return recommendation
    except Exception as e:
        logger.error(f"Error getting curve evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "evalys-arcium-bridge"}

