# Evalys Arcium Bridge Service

**FastAPI microservice that bridges Evalys components to [Arcium's encrypted supercomputer](https://arcium.com/).**

This service handles client encryption, submits confidential computation jobs to the unified Arcium gMPC MXE, and feeds results back into Evalys services.

**Built with Arcium**: This service integrates with [Arcium's decentralized private computation network](https://docs.arcium.com/developers) to enable confidential computation. Learn more:
- [Arcium Developer Documentation](https://docs.arcium.com/developers)
- [Arcium GitHub Organization](https://github.com/orgs/arcium-hq/)
- [Arcium Discord Community](https://discord.com/invite/arcium)

## Overview

The Arcium Bridge Service enables Evalys to:

- **Encrypt sensitive inputs** (user preferences, history, portfolio context) before sending to Arcium
- **Submit confidential computations** to the Evalys Confidential Intel MXE
- **Decrypt and process results** from Arcium MPC computations
- **Feed confidential intelligence** back to Evalys Privacy Engine, Curve Intelligence, and Execution Engine

## Architecture

```
Evalys Components → Bridge Service → Arcium MXE → MPC Cluster → Results → Bridge Service → Evalys Components
```

The bridge service:
1. Receives encrypted or plaintext inputs from Evalys components
2. Handles encryption using Arcium client SDK (if needed)
3. Submits computation requests to the MXE on Solana
4. Monitors computation completion
5. Decrypts results and returns structured data to Evalys

## API Endpoints

### `POST /arcium/plan`

Get confidential execution plan based on user preferences and history.

**Request:**
```json
{
  "user_preferences": {
    "desired_size": 1000000000,
    "slippage_tolerance": 100,
    "risk_appetite": 150,
    "preferred_hold_time": 3600
  },
  "user_history": {
    "recent_pnl": 5000000,
    "win_rate": 6500,
    "avg_hold_time": 1800,
    "total_trades": 50
  },
  "curve_state": {
    "current_price": 1000000,
    "liquidity_depth": 5000000000,
    "volatility": 300,
    "recent_volume": 10000000000
  }
}
```

**Response:**
```json
{
  "plan_id": "mxe-123...",
  "recommended_mode": "max_ghost",
  "num_slices": 8,
  "slice_size_base": 125000000,
  "timing_window_sec": 60,
  "risk_level": 180,
  "max_notional": 2000000000
}
```

### `POST /arcium/risk-score`

Get confidential risk assessment for a trade.

**Request:**
```json
{
  "portfolio_context": {
    "total_capital": 10000000000,
    "current_exposure": 3000000000,
    "diversification_score": 180,
    "leverage_ratio": 10000
  },
  "performance_history": {
    "total_pnl": 2000000,
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
```

**Response:**
```json
{
  "overall_risk_score": 120,
  "portfolio_risk": 110,
  "trade_risk": 130,
  "recommendation": "proceed"
}
```

### `POST /arcium/curve-eval`

Get confidential curve evaluation and execution recommendations.

**Request:**
```json
{
  "sizing_preferences": {
    "target_size": 500000000,
    "min_size": 100000000,
    "max_size": 1000000000,
    "capital_allocation_pct": 10
  },
  "user_constraints": {
    "max_slippage_bps": 200,
    "time_constraint_sec": 300,
    "priority_level": 150
  },
  "curve_metrics": {
    "current_price": 1000000,
    "price_change_24h": 500,
    "liquidity_depth": 2000000000,
    "buy_pressure": 150,
    "sell_pressure": 100
  }
}
```

**Response:**
```json
{
  "recommended_size": 500000000,
  "entry_price_target": 1010000,
  "execution_urgency": 150,
  "optimal_timing": 300,
  "confidence_score": 175
}
```

## Installation

```bash
# From evalys root directory (with shared venv activated)
cd evalys-arcium-bridge-service
pip install -r requirements.txt
pip install -e .
```

## Configuration

Create a `.env` file:

```env
# Arcium MXE Configuration
ARCIUM_MXE_PROGRAM_ID=your_mxe_program_id
ARCIUM_CLUSTER_OFFSET=1078779259
ARCIUM_RPC_URL=https://api.devnet.solana.com

# Solana Configuration
SOLANA_RPC_URL=https://api.devnet.solana.com
SOLANA_KEYPAIR_PATH=~/.config/solana/id.json

# Service Configuration
API_HOST=0.0.0.0
API_PORT=8010
API_DEBUG=false

# Arcium Client Configuration
ARCIUM_CLIENT_ENCRYPTION_KEY=your_encryption_key_here
```

## Running

```bash
# Activate shared venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\Activate.ps1  # Windows

# Set PYTHONPATH
export PYTHONPATH=.  # Linux/Mac
# or
$env:PYTHONPATH = "."  # Windows PowerShell

# Run the service
cd evalys-arcium-bridge-service
python -m src.api.server
```

## Integration with Evalys

### Privacy Engine Integration

The Privacy Engine can call the bridge service when `CONFIDENTIAL` mode is enabled:

```python
from evalys_arcium_bridge import ArciumBridgeClient

bridge = ArciumBridgeClient()
plan = await bridge.get_confidential_plan(
    user_preferences=prefs,
    user_history=history,
    curve_state=curve_state
)

# Use plan to configure privacy mode and execution parameters
```

### Curve Intelligence Integration

Curve Intelligence can optionally use confidential analytics:

```python
from evalys_arcium_bridge import ArciumBridgeClient

bridge = ArciumBridgeClient()
recommendation = await bridge.get_curve_evaluation(
    sizing_preferences=sizing,
    user_constraints=constraints,
    curve_metrics=metrics
)
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `solana` - Solana Python SDK
- `@arcium-hq/client` (via subprocess or HTTP) - Arcium client library
- `python-dotenv` - Environment variable management

## Security Considerations

- All sensitive data is encrypted before transmission
- Encryption keys are managed securely
- Results are decrypted only within the bridge service
- No sensitive data is logged or exposed

## License

See LICENSE file.

## Support

For questions or issues:
- Evalys: [GitHub Issues](https://github.com/evalysfun/evalys-arcium-bridge-service/issues)

## Arcium Resources

**Learn More About Arcium**:
- [Arcium Website](https://arcium.com/) - The encrypted supercomputer
- [Arcium Developer Documentation](https://docs.arcium.com/developers) - Complete developer guide
- [Arcium GitHub Organization](https://github.com/orgs/arcium-hq/) - Source code, examples, and tools
- [Arcium Discord](https://discord.com/invite/arcium) - Join the community

**Arcium enables**:
- Privacy-preserving applications on Solana
- Processing sensitive data while keeping it encrypted
- Familiar tooling (Arcis extends Anchor)
- Full composability within Solana ecosystem

This bridge service demonstrates how to integrate with Arcium's encrypted supercomputer. For more examples and tutorials, visit the [Arcium Developer Documentation](https://docs.arcium.com/developers).
- Arcium: [Discord](https://discord.gg/arcium)

