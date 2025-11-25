# Cryptographic Operations and Arcium API Usage

## Overview

This document specifies the cryptographic operations, key management, and Arcium API usage in the bridge service.

## Key Management

### Encryption Keys

**Arcium Client Encryption Key**

- **Location**: Environment variable `ARCIUM_CLIENT_ENCRYPTION_KEY`
- **Format**: Base64-encoded symmetric key
- **Usage**: Encrypts sensitive inputs before sending to Arcium MXE
- **Rotation**: Manual (update env var and restart service)

**Key Generation** (for development):
```python
import secrets
import base64

key = secrets.token_bytes(32)  # 256-bit key
encoded = base64.b64encode(key).decode('utf-8')
print(f"ARCIUM_CLIENT_ENCRYPTION_KEY={encoded}")
```

**Storage**: Never commit keys to repository. Use `.env` file (gitignored) or secret management service.

### Solana Keypair

**Location**: File path specified in `SOLANA_KEYPAIR_PATH` env var

**Usage**: 
- Sign transactions to submit to Arcium MXE
- Pay transaction fees

**Security**: 
- File permissions: 600 (read/write owner only)
- Never log private key
- Use separate keypair for each environment (devnet/mainnet)

## Confidential Compute Boundary

### What is Encrypted

**Sensitive Inputs** (encrypted before transmission):
- User preferences (desired_size, risk_appetite, slippage_tolerance)
- User history (recent_pnl, win_rate, avg_hold_time)
- Portfolio context (total_capital, current_exposure)
- Performance history (total_pnl, sharpe_ratio, max_drawdown)
- Sizing preferences (target_size, min_size, max_size)
- User constraints (max_slippage_bps, priority_level)

**Public Inputs** (not encrypted):
- Curve state (current_price, liquidity_depth, volatility)
- Market conditions (curve_volatility, liquidity_risk)
- Curve metrics (current_price, price_change_24h, buy_pressure)

### Encryption Process

1. **Input Validation**: Validate all inputs using Pydantic models
2. **Sensitive Field Extraction**: Separate sensitive vs public fields
3. **Encryption**: Encrypt sensitive fields using Arcium client SDK
4. **Payload Construction**: Combine encrypted + public fields
5. **Transmission**: Send to Arcium MXE via Solana transaction

### Decryption Process

1. **Receipt Verification**: Verify Arcium receipt signature
2. **Result Extraction**: Extract encrypted result from receipt
3. **Decryption**: Decrypt using Arcium client SDK
4. **Validation**: Validate decrypted result structure
5. **Return**: Return to Evalys component

## Arcium API Usage

### MXE Program Interaction

**Program ID**: `ARCIUM_MXE_PROGRAM_ID` (Solana program pubkey)

**Cluster**: Specified by `ARCIUM_CLUSTER_OFFSET` (default: 1078779259 for devnet)

**RPC Endpoint**: `ARCIUM_RPC_URL` (default: https://api.devnet.solana.com)

### Computation Types

**1. Confidential Strategy Plan**

- **MXE Function**: `confidential_strategy_plan()`
- **Inputs**: Encrypted user_preferences, user_history + public curve_state
- **Output**: StrategyPlan (recommended_mode, num_slices, timing_window, etc.)
- **Proof**: Arcium receipt with computation attestation

**2. Confidential Risk Score**

- **MXE Function**: `confidential_risk_score()`
- **Inputs**: Encrypted portfolio_context, performance_history + public market_conditions
- **Output**: RiskAssessment (overall_risk_score, recommendation, etc.)
- **Proof**: Arcium receipt with computation attestation

**3. Confidential Curve Evaluation**

- **MXE Function**: `confidential_curve_eval()`
- **Inputs**: Encrypted sizing_preferences, user_constraints + public curve_metrics
- **Output**: ExecutionRecommendation (recommended_size, execution_urgency, etc.)
- **Proof**: Arcium receipt with computation attestation

### Receipt/Proof Structure

**Arcium Receipt** (from MXE):
```python
{
    "receipt_id": "<arcium_receipt_id>",
    "computation_id": "<mxe_computation_id>",
    "result_hash": "<sha256_hash_of_result>",
    "signature": "<arcium_node_signature>",  # Ed25519 signature
    "timestamp": "<iso_timestamp>",
    "status": "completed",
    "encrypted_result": "<encrypted_blob>"
}
```

### Receipt Verification

**Verification Steps**:

1. **Signature Verification**:
   - Extract signature from receipt
   - Verify Ed25519 signature using Arcium node public key
   - Reject if signature invalid

2. **Result Hash Verification**:
   - Compute SHA256 hash of decrypted result
   - Compare with `result_hash` in receipt
   - Reject if hash mismatch

3. **Timestamp Validation**:
   - Check receipt timestamp is recent (within 5 minutes)
   - Reject if timestamp too old (prevent replay)

4. **Status Check**:
   - Verify status is "completed"
   - Reject if status is "failed" or other error state

**Implementation** (v0.1 - TODO):
```python
async def verify_receipt(receipt: ProofReceiptV1) -> bool:
    """
    Verify Arcium receipt signature and result hash.
    
    Returns True if receipt is valid, False otherwise.
    """
    # TODO: Implement signature verification using Arcium node public key
    # TODO: Implement result hash verification
    # TODO: Implement timestamp validation
    return True  # Placeholder
```

## Libraries and Dependencies

### Current Stack (v0.1)

- **Solana SDK**: `solana-py` for Solana RPC interaction
- **Encryption**: Placeholder (TODO: Arcium client SDK)
- **Signing**: `solders` for Ed25519 keypair operations
- **Validation**: `pydantic` for input/output validation

### Future Stack (v0.2+)

- **Arcium Client SDK**: Official Arcium client library
  - Encryption/decryption
  - MXE job submission
  - Receipt verification
- **Cryptography**: `cryptography` library for additional crypto primitives if needed

## Security Considerations

### Logging Policy

**NEVER Log**:
- Encryption keys
- Private keys
- Plaintext sensitive inputs
- Decrypted results (unless explicitly needed for debugging)

**Safe to Log**:
- Receipt IDs (public identifiers)
- Computation IDs
- Public inputs (curve state, market conditions)
- Error messages (sanitized, no sensitive data)
- Request/response metadata (timestamps, status codes)

**Logging Example**:
```python
# BAD - Never do this
logger.info(f"User preferences: {user_preferences}")  # Contains sensitive data

# GOOD - Safe logging
logger.info(f"Request received: intent_type={intent_type}, receipt_id={receipt_id}")
logger.debug(f"Encrypted payload size: {len(encrypted_payload)} bytes")
```

### Error Handling

**Error Messages**: Must not leak sensitive information

```python
# BAD - Leaks sensitive data
raise ValueError(f"Invalid user preferences: {user_preferences}")

# GOOD - Sanitized error
raise ValueError("Invalid user preferences: validation failed")
```

### Input Validation

**All inputs validated** using Pydantic models before:
- Encryption
- Transmission
- Logging (even if redacted)

**Validation Rules**:
- Type checking (int, str, etc.)
- Range validation (0-255 for risk scores, etc.)
- Required fields
- Format validation (timestamps, UUIDs, etc.)

## References

- [Arcium Developer Documentation](https://docs.arcium.com/developers) - Official Arcium docs
- [Arcium GitHub](https://github.com/orgs/arcium-hq/) - Source code and examples
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/) - Solana RPC reference
- [Ed25519 Signatures](https://ed25519.cr.yp.to/) - Signature scheme used by Arcium

