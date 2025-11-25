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
- **Submit confidential computations** to the unified Arcium gMPC MXE
- **Decrypt and process results** from Arcium MPC computations
- **Feed confidential intelligence** back to Evalys Privacy Engine, Curve Intelligence, and Execution Engine

## Status: v0.1 (Alpha)

### What's Live Now (v0.1)

✅ **API Endpoints**: FastAPI REST API with 3 endpoints:
- `POST /arcium/plan` - Confidential strategy planning
- `POST /arcium/risk-score` - Confidential risk assessment
- `POST /arcium/curve-eval` - Confidential curve evaluation

✅ **Message Schemas**: Pydantic models for all request/response types

✅ **Simulated Computation**: Placeholder logic that simulates Arcium computation (for development/testing)

✅ **Basic Error Handling**: HTTP error responses and logging

✅ **Documentation**: Bridge spec, crypto docs, and API documentation

### What's Next

🔜 **v0.2**: Real Arcium SDK Integration
- Actual Arcium client SDK integration
- Real encryption/decryption using Arcium keys
- Solana transaction submission to MXE

🔜 **v0.3**: Receipt Verification
- Proof/receipt signature verification
- Result hash validation
- Timestamp validation (replay prevention)

🔜 **v0.4**: Multi-Relay Routing
- Support for multiple Arcium relay nodes
- Automatic failover
- Load balancing

🔜 **v0.5**: Threshold Signing
- Distributed key management
- Sharded signing support

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

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

See `.env.example` for all required configuration options.

**Required Configuration**:
- `ARCIUM_MXE_PROGRAM_ID`: Solana program ID for the unified Arcium gMPC MXE
- `SOLANA_RPC_URL`: Solana RPC endpoint
- `ARCIUM_CLIENT_ENCRYPTION_KEY`: 256-bit encryption key (base64 encoded)

**Optional Configuration**:
- `API_HOST`, `API_PORT`: Server binding (default: 0.0.0.0:8010)
- `LOG_LEVEL`: Logging level (default: INFO)

## Running

### Quick Start (Demo Mode)

The easiest way to start the service for demo/testing:

```bash
# Quick start script (no configuration needed)
python start_server.py
```

This starts the service on `http://localhost:8010` with simulated computation (v0.1).

### Standard Start

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

### Using Uvicorn

```bash
uvicorn src.api.server:app --host 0.0.0.0 --port 8010 --reload
```

**Note**: For demo mode (v0.1), no `.env` file is required. The service uses simulated computation. For production (v0.2+), configure `.env` with real Arcium credentials.

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

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

## Project Structure

```
evalys-arcium-bridge-service/
├── src/
│   ├── api/              # FastAPI routes and server
│   │   ├── routes.py     # API endpoints
│   │   └── server.py     # FastAPI app
│   ├── bridge/           # Bridge logic
│   │   ├── arcium_client.py  # Arcium client (simulated in v0.1)
│   │   └── models.py     # Pydantic models
│   ├── config/          # Configuration
│   │   └── settings.py  # Settings from env vars
│   └── utils/           # Utilities
│       └── logger.py    # Logging setup
├── tests/               # Test suite
│   ├── test_intent_validation.py
│   ├── test_receipt_verification.py
│   └── test_confidential_boundary.py
├── docs/                # Documentation
│   ├── bridge-spec.md   # Protocol specification
│   └── crypto.md        # Cryptographic operations
├── examples/            # Example scripts
│   └── demo.py          # API demo script
├── .env.example         # Configuration template
└── README.md
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `solana-py` - Solana Python SDK
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variable management

**Future Dependencies** (v0.2+):
- Arcium client SDK (when available)
- Additional crypto libraries for receipt verification

## Documentation

- **[Bridge Specification](docs/bridge-spec.md)**: Protocol specification with actors, message types, flows, and failure modes
- **[Cryptographic Operations](docs/crypto.md)**: Key management, encryption/decryption, and Arcium API usage
- **[Arcium Integration Guide](../ARCIUM_INTEGRATION_GUIDE.md)**: Complete integration guide for Evalys + Arcium

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_intent_validation.py
pytest tests/test_receipt_verification.py
pytest tests/test_confidential_boundary.py
```

**Test Coverage**:
- ✅ Intent schema validation (malformed inputs rejected)
- ✅ Receipt verification (placeholder - to be implemented in v0.3)
- ✅ Confidential boundary enforcement (placeholder - to be implemented in v0.2)

## Demo

Run the interactive demo script:

```bash
# Start the bridge service first
python -m src.api.server

# In another terminal, run the demo
python examples/demo.py
```

The demo shows:
- Confidential strategy plan request/response
- Risk score assessment
- Curve evaluation
- Health check

**Expected Output**: See `examples/demo.py` for example requests and expected responses.

## Security Considerations

**v0.1 (Current)**:
- Input validation using Pydantic models
- Basic error handling (no sensitive data in errors)
- Structured logging (no sensitive data in logs)

**v0.2+ (Planned)**:
- All sensitive data encrypted before transmission
- Encryption keys managed securely (env vars or secret management)
- Results decrypted only within bridge service
- Receipt/proof verification before trusting results
- No sensitive data logged or exposed

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

