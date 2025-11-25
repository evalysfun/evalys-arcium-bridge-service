# Bridge Specification v0.1

## Overview

This document specifies the Evalys-Arcium Bridge Service protocol, including actors, message types, flows, and failure modes.

## Actors

### 1. Client (Evalys Components)

**Role**: Initiates confidential computation requests

**Components**:
- Privacy Gradient Engine
- Curve Intelligence Layer
- Execution Engine

**Responsibilities**:
- Encrypt sensitive inputs (or provide plaintext for bridge to encrypt)
- Submit requests to bridge service
- Handle responses and integrate results

**Trust Model**: Trusts bridge service to handle encryption and Arcium communication

### 2. Bridge Service (This Repo)

**Role**: Mediates between Evalys and Arcium

**Responsibilities**:
- Receive encrypted or plaintext inputs from Evalys components
- Encrypt sensitive data using Arcium client SDK
- Submit computation jobs to Arcium MXE
- Monitor job completion
- Verify receipts/proofs from Arcium
- Decrypt and return results to Evalys components

**Trust Model**: 
- Trusts Arcium MXE for confidential computation
- Trusts Solana RPC for transaction submission
- Does NOT trust clients (validates all inputs)

### 3. Arcium Confidential Compute Runtime

**Role**: Executes confidential computations in MPC

**Components**:
- Unified MXE: `evalys-arcium-gmpc-mxe` (Solana program)
- Arcium MPC Cluster: Network of compute nodes

**Responsibilities**:
- Receive encrypted computation requests
- Execute MPC computation without revealing inputs
- Return encrypted results with proof/receipt
- Attest to computation integrity

**Trust Model**: Trusted for confidential computation (MPC guarantees)

### 4. Solana RPC / Launchpad Adapter

**Role**: Blockchain interaction layer

**Components**:
- Solana RPC nodes
- Launchpad adapters (Pump.fun, Bonk.fun)

**Responsibilities**:
- Submit transactions to Solana
- Query on-chain state
- Interact with launchpad programs

**Trust Model**: Trusts Solana network consensus

## Message Types

### IntentEnvelopeV1

**Purpose**: Encapsulates user intent for confidential computation

**Structure**:
```python
{
    "version": "v1",
    "intent_type": "strategy_plan" | "risk_score" | "curve_eval",
    "encrypted_payload": "<base64_encrypted_data>",
    "public_context": {
        "curve_state": {...},  # Public on-chain data
        "market_conditions": {...}
    },
    "nonce": "<random_nonce>",
    "timestamp": "<iso_timestamp>"
}
```

**Encryption**: Sensitive fields encrypted using Arcium client SDK before transmission

### ConfidentialPayload

**Purpose**: Encrypted data sent to Arcium MXE

**Structure**:
```python
{
    "encrypted_inputs": "<encrypted_blob>",
    "computation_type": "confidential_strategy" | "confidential_risk" | "confidential_curve",
    "public_inputs": {...},  # Unencrypted context
    "metadata": {
        "request_id": "<uuid>",
        "client_id": "<evalys_component_id>"
    }
}
```

**Encryption**: Uses Arcium's encryption scheme (details in `docs/crypto.md`)

### ProofReceiptV1

**Purpose**: Attestation of confidential computation completion

**Structure**:
```python
{
    "version": "v1",
    "receipt_id": "<arcium_receipt_id>",
    "computation_id": "<mxe_computation_id>",
    "result_hash": "<sha256_hash_of_result>",
    "signature": "<arcium_node_signature>",
    "timestamp": "<iso_timestamp>",
    "status": "completed" | "failed",
    "result": {
        "encrypted_output": "<encrypted_result_blob>",
        "public_output": {...}  # Non-sensitive results
    }
}
```

**Verification**: Bridge verifies signature and result hash before returning to client

## Flow Diagrams

### Flow 1: Confidential Strategy Plan

```
1. Privacy Engine → Bridge Service
   POST /arcium/plan
   {
     user_preferences: {...},
     user_history: {...},
     curve_state: {...}
   }

2. Bridge Service
   - Encrypts user_preferences and user_history
   - Constructs ConfidentialPayload
   - Submits to Arcium MXE via Solana transaction

3. Arcium MXE
   - Receives encrypted payload
   - Executes confidential_strategy_plan() in MPC
   - Returns encrypted result + proof

4. Bridge Service
   - Verifies proof/receipt signature
   - Decrypts result
   - Validates result structure

5. Bridge Service → Privacy Engine
   Returns StrategyPlan {
     plan_id: "mxe-123...",
     recommended_mode: "max_ghost",
     num_slices: 8,
     ...
   }
```

### Flow 2: Confidential Risk Score

```
1. Curve Intelligence → Bridge Service
   POST /arcium/risk-score
   {
     portfolio_context: {...},
     performance_history: {...},
     market_conditions: {...}
   }

2. Bridge Service
   - Encrypts portfolio_context and performance_history
   - Submits to Arcium MXE

3. Arcium MXE
   - Executes confidential_risk_score() in MPC
   - Returns RiskAssessment + proof

4. Bridge Service
   - Verifies proof
   - Decrypts result

5. Bridge Service → Curve Intelligence
   Returns RiskAssessment {
     overall_risk_score: 120,
     recommendation: "proceed",
     ...
   }
```

### Flow 3: Confidential Curve Evaluation

```
1. Execution Engine → Bridge Service
   POST /arcium/curve-eval
   {
     sizing_preferences: {...},
     user_constraints: {...},
     curve_metrics: {...}
   }

2. Bridge Service
   - Encrypts sizing_preferences and user_constraints
   - Submits to Arcium MXE

3. Arcium MXE
   - Executes confidential_curve_eval() in MPC
   - Returns ExecutionRecommendation + proof

4. Bridge Service
   - Verifies proof
   - Decrypts result

5. Bridge Service → Execution Engine
   Returns ExecutionRecommendation {
     recommended_size: 500000000,
     execution_urgency: 150,
     ...
   }
```

## Failure Modes

### 1. Arcium Job Timeout

**Scenario**: MXE computation exceeds timeout threshold

**Detection**: No receipt received within timeout window (default: 60s)

**Handling**:
- Retry with exponential backoff (max 3 retries)
- If all retries fail, return error to client
- Log timeout for monitoring

**Response to Client**:
```json
{
  "error": "computation_timeout",
  "message": "Arcium computation exceeded timeout",
  "retry_after": 5
}
```

### 2. Invalid Proof/Receipt

**Scenario**: Receipt signature verification fails

**Detection**: Signature verification returns invalid

**Handling**:
- Reject receipt immediately
- Log security event
- Do NOT retry (security risk)
- Return error to client

**Response to Client**:
```json
{
  "error": "invalid_receipt",
  "message": "Receipt verification failed"
}
```

### 3. Transaction Simulation Failure

**Scenario**: Solana transaction simulation fails before submission

**Detection**: `simulateTransaction` returns error

**Handling**:
- Validate inputs before retry
- Return error to client (don't submit invalid tx)
- Log simulation failure

**Response to Client**:
```json
{
  "error": "simulation_failed",
  "message": "Transaction simulation failed: <reason>"
}
```

### 4. Network/Connection Errors

**Scenario**: Cannot reach Arcium MXE or Solana RPC

**Detection**: Connection timeout or network error

**Handling**:
- Retry with exponential backoff
- Circuit breaker pattern (stop retrying after N failures)
- Return error after max retries

**Response to Client**:
```json
{
  "error": "network_error",
  "message": "Failed to connect to Arcium service",
  "retry_after": 10
}
```

### 5. Decryption Failure

**Scenario**: Cannot decrypt Arcium result

**Detection**: Decryption returns error or invalid data

**Handling**:
- Log security event
- Do NOT retry (indicates key mismatch or corruption)
- Return error to client

**Response to Client**:
```json
{
  "error": "decryption_failed",
  "message": "Failed to decrypt Arcium result"
}
```

## Retry/Backoff Rules

### Retry Policy

- **Max Retries**: 3 attempts
- **Initial Backoff**: 1 second
- **Backoff Multiplier**: 2x (exponential)
- **Max Backoff**: 10 seconds

### Retryable Errors

- Network timeouts
- Arcium job timeouts
- Transient Solana RPC errors

### Non-Retryable Errors

- Invalid proof/receipt
- Decryption failures
- Invalid input validation errors
- Authentication failures

## Security Boundaries

### Confidential Boundary

**Rule**: Plaintext sensitive data must NEVER be:
- Logged (use structured logging with redaction)
- Serialized to disk
- Exposed in error messages
- Transmitted unencrypted

**Enforcement**:
- All sensitive fields encrypted before logging
- Error messages sanitized (no sensitive data)
- Input validation before encryption

### Verification Boundary

**Rule**: All receipts/proofs from Arcium MUST be verified before:
- Decrypting results
- Returning to client
- Trusting computation integrity

**Enforcement**:
- Signature verification required
- Result hash validation required
- Receipt timestamp validation (prevent replay)

## Versioning

### Current Version: v0.1

**Status**: Alpha - Simulated computation (TODOs in code)

**Implemented**:
- Message schemas (Pydantic models)
- API endpoints (FastAPI routes)
- Simulated computation logic
- Basic error handling

**Not Yet Implemented**:
- Actual Arcium client SDK integration
- Receipt/proof verification
- Real encryption/decryption
- Solana transaction submission

### Future Versions

- **v0.2**: Real Arcium SDK integration
- **v0.3**: Receipt verification and proof validation
- **v0.4**: Multi-relay routing
- **v0.5**: Threshold signing support

## References

- [Arcium Developer Documentation](https://docs.arcium.com/developers)
- [Arcium GitHub Organization](https://github.com/orgs/arcium-hq/)
- [Arcium Discord](https://discord.com/invite/arcium)

