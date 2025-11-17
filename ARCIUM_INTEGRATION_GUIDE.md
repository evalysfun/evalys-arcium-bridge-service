# Evalys + Arcium Integration Guide

**Complete guide to integrating Arcium's encrypted supercomputer with Evalys.**

## Overview

Evalys now integrates with Arcium to provide **confidential computation** for strategy planning, risk assessment, and curve analytics. This enables privacy-preserving intelligence without exposing sensitive user data (wallet graphs, PnL history, alpha signals).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Evalys Components                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Privacy    │  │    Curve     │  │  Execution   │     │
│  │   Engine     │  │ Intelligence │  │   Engine     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            Arcium Bridge Service (Port 8010)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Encrypts sensitive inputs                          │  │
│  │  • Submits computations to MXE                       │  │
│  │  • Monitors computation completion                    │  │
│  │  • Decrypts and returns results                       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         Evalys Confidential Intel MXE (Solana)             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • confidential_strategy_plan()                      │  │
│  │  • confidential_risk_score()                         │  │
│  │  • confidential_curve_eval()                         │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Arcium MPC Cluster (Off-Chain)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Executes encrypted computations                  │  │
│  │  • Returns encrypted results                        │  │
│  │  • Never exposes raw data                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. evalys-confidential-intel-mxe

**Rust/Arcis MXE program** deployed on Solana that defines encrypted computation functions.

**Location**: `evalys-confidential-intel-mxe/`

**Key Files**:
- `encrypted-ixs/confidential_strategy.rs` - Strategy planning computation
- `encrypted-ixs/confidential_risk.rs` - Risk scoring computation
- `encrypted-ixs/confidential_curve.rs` - Curve evaluation computation
- `programs/evalys-confidential-intel/` - Solana program that invokes encrypted instructions

**Deployment**:
```bash
cd evalys-confidential-intel-mxe
arcium deploy \
  --cluster-offset 1078779259 \
  --keypair-path ~/.config/solana/id.json \
  --rpc-url https://devnet.helius-rpc.com/?api-key=<your-key>
```

### 2. evalys-arcium-bridge-service

**Python FastAPI service** that bridges Evalys to Arcium.

**Location**: `evalys-arcium-bridge-service/`

**API Endpoints**:
- `POST /api/v1/arcium/plan` - Get confidential execution plan
- `POST /api/v1/arcium/risk-score` - Get confidential risk assessment
- `POST /api/v1/arcium/curve-eval` - Get confidential curve evaluation
- `GET /api/v1/health` - Health check

**Running**:
```bash
cd evalys-arcium-bridge-service
python -m src.api.server
```

### 3. Updated Components

#### evalys-privacy-engine

**New Features**:
- `PrivacyMode.CONFIDENTIAL` - Arcium-powered confidential mode
- `PrivacyLevel.use_arcium` - Flag indicating Arcium usage
- `PrivacyLevel.arcium_plan_id` - Plan ID from Arcium MXE
- `PrivacyGradientEngine.select_mode()` with `enable_arcium` parameter

**Usage**:
```python
from src.pge.orchestrator import PrivacyGradientEngine

pge = PrivacyGradientEngine()
privacy_config = pge.select_mode(
    user_preference="confidential",
    enable_arcium=True,
    arcium_inputs={
        "user_preferences": {...},
        "user_history": {...},
        "curve_state": {...},
    }
)
```

#### evalys-curve-intelligence

**New Features**:
- `use_confidential_intel` parameter in `CurveIntelligenceLayer`
- `get_confidential_curve_evaluation()` method for Arcium-powered analytics

**Usage**:
```python
from src.curve_intelligence.intelligence_layer import CurveIntelligenceLayer

curve_intel = CurveIntelligenceLayer(use_confidential_intel=True)
recommendation = await curve_intel.get_confidential_curve_evaluation(
    token_mint=token_mint,
    sizing_preferences={...},
    user_constraints={...},
)
```

## Integration Flows

### Flow A: Confidential Entry with Arcium Shield

1. **User enables Arcium Shield** in UI
2. **Privacy Engine** collects sensitive inputs (preferences, history)
3. **Bridge Service** encrypts inputs and submits to MXE
4. **Arcium MXE** computes strategy plan confidentially
5. **Privacy Engine** receives plan and configures execution
6. **Execution Engine** executes using confidential plan parameters

### Flow B: Confidential Multi-User Analytics

1. **Multiple users** opt in to Arcium-powered intel
2. **Evalys** ships encrypted per-user stats to shared MXE
3. **Arcium MPC** computes aggregated insights without exposing individual data
4. **Curve Intelligence** consumes aggregated metrics
5. **All users** benefit from "big brain intel" without privacy loss

## Configuration

### Bridge Service Configuration

Create `.env` in `evalys-arcium-bridge-service/`:

```env
ARCIUM_MXE_PROGRAM_ID=your_mxe_program_id_here
ARCIUM_CLUSTER_OFFSET=1078779259
ARCIUM_RPC_URL=https://api.devnet.solana.com
SOLANA_RPC_URL=https://api.devnet.solana.com
API_PORT=8010
```

### Privacy Engine Configuration

The Privacy Engine automatically detects Arcium bridge service availability. No additional configuration needed if bridge service is running.

## Example Usage

See `integration-examples/arcium_confidential_example.py` for a complete example.

## Security Model

- **Input Encryption**: All sensitive inputs encrypted using x25519 + Rescue cipher
- **MPC Execution**: Computations run in Arcium's MPC network (Cerberus protocol)
- **Output Encryption**: Results encrypted and only decryptable by requesting client
- **No Data Exposure**: Raw sensitive data never leaves encrypted form

## Positioning

**One-liner for docs**:

> Evalys now plugs into Arcium's encrypted supercomputer – your trading intent, risk profile, and strategy are computed confidentially via MPC, while Evalys executes the resulting plan using burner swarms, MEV-safe routing, and launchpad adapters on Solana.

## Next Steps

1. Deploy `evalys-confidential-intel-mxe` to Solana devnet
2. Start `evalys-arcium-bridge-service` on port 8010
3. Enable Arcium Shield in Privacy Engine
4. Test with integration examples
5. Deploy to production

## Support

- Evalys: [GitHub Issues](https://github.com/evalysfun)
- Arcium: [Discord](https://discord.gg/arcium)

