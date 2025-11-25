#!/usr/bin/env python3
"""
Evalys Arcium Bridge Service - Demo Script

Demonstrates the bridge service API endpoints with example requests.
Shows expected output for each endpoint.

Usage:
    # Start the bridge service first:
    python -m src.api.server
    
    # Then run this demo:
    python examples/demo.py
"""

import sys
import requests
import json
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

API_BASE = "http://localhost:8010/api/v1"


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}\n")


def print_request(endpoint, payload):
    """Print formatted request"""
    print(f"POST {endpoint}")
    print(f"Request Body:")
    print(json.dumps(payload, indent=2))
    print()


def print_response(response):
    """Print formatted response"""
    print("Response:")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")
    print()


def demo_confidential_plan():
    """Demo: Confidential Strategy Plan"""
    print_section("Demo 1: Confidential Strategy Plan")
    
    payload = {
        "user_preferences": {
            "desired_size": 1_000_000_000,  # 1 SOL in lamports
            "slippage_tolerance": 100,
            "risk_appetite": 150,
            "preferred_hold_time": 3600
        },
        "user_history": {
            "recent_pnl": 5_000_000,
            "win_rate": 6500,
            "avg_hold_time": 1800,
            "total_trades": 50
        },
        "curve_state": {
            "current_price": 1_000_000,
            "liquidity_depth": 5_000_000_000,
            "volatility": 300,
            "recent_volume": 10_000_000_000
        }
    }
    
    print_request("/arcium/plan", payload)
    
    response = requests.post(f"{API_BASE}/arcium/plan", json=payload)
    print_response(response)
    
    time.sleep(1)


def demo_risk_score():
    """Demo: Confidential Risk Score"""
    print_section("Demo 2: Confidential Risk Score")
    
    payload = {
        "portfolio_context": {
            "total_capital": 10_000_000_000,
            "current_exposure": 3_000_000_000,
            "diversification_score": 180,
            "leverage_ratio": 10000
        },
        "performance_history": {
            "total_pnl": 2_000_000,
            "sharpe_ratio": 120,
            "max_drawdown": 2000,
            "consistency_score": 200
        },
        "market_conditions": {
            "curve_volatility": 400,
            "liquidity_risk": 100,
            "market_sentiment": 50
        }
    }
    
    print_request("/arcium/risk-score", payload)
    
    response = requests.post(f"{API_BASE}/arcium/risk-score", json=payload)
    print_response(response)
    
    time.sleep(1)


def demo_curve_eval():
    """Demo: Confidential Curve Evaluation"""
    print_section("Demo 3: Confidential Curve Evaluation")
    
    payload = {
        "sizing_preferences": {
            "target_size": 500_000_000,
            "min_size": 100_000_000,
            "max_size": 1_000_000_000,
            "capital_allocation_pct": 10
        },
        "user_constraints": {
            "max_slippage_bps": 200,
            "time_constraint_sec": 300,
            "priority_level": 150
        },
        "curve_metrics": {
            "current_price": 1_000_000,
            "price_change_24h": 500,
            "liquidity_depth": 2_000_000_000,
            "buy_pressure": 150,
            "sell_pressure": 100
        }
    }
    
    print_request("/arcium/curve-eval", payload)
    
    response = requests.post(f"{API_BASE}/arcium/curve-eval", json=payload)
    print_response(response)
    
    time.sleep(1)


def demo_health_check():
    """Demo: Health Check"""
    print_section("Demo 4: Health Check")
    
    print("GET /health\n")
    
    response = requests.get("http://localhost:8010/health")
    print_response(response)


def main():
    """Run all demos"""
    print_section("Evalys Arcium Bridge Service - API Demo")
    print("Make sure the bridge service is running:")
    print("  python -m src.api.server")
    print("\nOr:")
    print("  uvicorn src.api.server:app --host 0.0.0.0 --port 8010")
    
    try:
        # Check if server is running (use root health endpoint)
        response = requests.get("http://localhost:8010/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ Server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print(f"\n❌ Cannot connect to bridge service at {API_BASE}")
        print("   Please start the server first!")
        return
    
    print("\n✅ Server is running!")
    time.sleep(1)
    
    # Run demos
    demo_health_check()
    demo_confidential_plan()
    demo_risk_score()
    demo_curve_eval()
    
    print_section("Demo Complete")
    print("✅ All endpoints demonstrated")
    print("\nNote: This demo uses simulated computation (v0.1).")
    print("In v0.2+, these will use actual Arcium MXE computation.")


if __name__ == "__main__":
    main()

