# Operations Runbook

## Deployment

### Prerequisites

- Python 3.11+
- Solana CLI tools (for keypair management)
- Access to Arcium MXE program ID
- Arcium encryption key

### Environment Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/evalysfun/evalys-arcium-bridge-service
   cd evalys-arcium-bridge-service
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Required Configuration

**Arcium MXE Configuration**:
- `ARCIUM_MXE_PROGRAM_ID`: Solana program ID for unified Arcium gMPC MXE
- `ARCIUM_RPC_URL`: Arcium RPC endpoint
- `ARCIUM_CLIENT_ENCRYPTION_KEY`: 256-bit encryption key (base64)

**Solana Configuration**:
- `SOLANA_RPC_URL`: Solana RPC endpoint
- `SOLANA_KEYPAIR_PATH`: Path to Solana keypair file

**Service Configuration**:
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8010)
- `LOG_LEVEL`: Logging level (default: INFO)

### Running Locally

```bash
# Activate venv
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=.

# Run service
python -m src.api.server
```

### Running with Docker

```bash
# Build image
docker build -t evalys-arcium-bridge .

# Run container
docker run -d \
  --name evalys-arcium-bridge \
  -p 8010:8010 \
  --env-file .env \
  evalys-arcium-bridge
```

### Running with Docker Compose

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

## Monitoring

### Health Check

The service exposes a health check endpoint:

```bash
curl http://localhost:8010/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "evalys-arcium-bridge"
}
```

### Logging

**Log Levels**:
- `DEBUG`: Detailed debugging information
- `INFO`: General operational messages
- `WARNING`: Warning messages (non-critical issues)
- `ERROR`: Error messages (operation failures)
- `CRITICAL`: Critical errors (service may be down)

**Log Location**: Console (stdout/stderr)

**Log Format**: Structured JSON (recommended for production)

**Safe Logging Rules**:
- ✅ Log: Request IDs, receipt IDs, computation IDs, timestamps
- ✅ Log: Public inputs (curve state, market conditions)
- ❌ Never log: Encryption keys, private keys, plaintext sensitive data

### Metrics (Future)

Planned metrics for v0.2+:
- Request count by endpoint
- Average response time
- Error rate
- Arcium computation success rate
- Receipt verification failures

## Troubleshooting

### Service Won't Start

**Check**:
1. Port 8010 is not already in use
2. `.env` file exists and is properly configured
3. All required environment variables are set
4. Python dependencies are installed

**Solution**:
```bash
# Check port
lsof -i :8010  # Linux/Mac
netstat -ano | findstr :8010  # Windows

# Check environment
python -c "from src.config.settings import Settings; s = Settings(); print(s.dict())"
```

### Cannot Connect to Arcium MXE

**Check**:
1. `ARCIUM_MXE_PROGRAM_ID` is correct
2. `ARCIUM_RPC_URL` is accessible
3. Network connectivity to Solana RPC

**Solution**:
```bash
# Test Solana RPC
curl -X POST $SOLANA_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}'
```

### Receipt Verification Failures

**Check**:
1. Arcium encryption key is correct
2. Receipt signature is valid
3. Result hash matches decrypted result

**Solution**:
- Check logs for specific verification error
- Verify encryption key matches Arcium configuration
- Ensure receipt is from valid Arcium node

### High Error Rate

**Check**:
1. Arcium MXE is operational
2. Solana RPC is responsive
3. Network connectivity

**Solution**:
- Check Arcium service status
- Verify Solana RPC health
- Review error logs for patterns

## Security

### Key Management

**Encryption Keys**:
- Store in `.env` file (gitignored)
- Use secret management service in production (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate keys periodically
- Never commit keys to repository

**Solana Keypair**:
- File permissions: 600 (read/write owner only)
- Use separate keypairs for devnet/mainnet
- Never log private key

### Access Control

**API Access**:
- Use reverse proxy (nginx, Traefik) for authentication
- Implement rate limiting
- Use HTTPS in production

**Network Security**:
- Firewall rules: Only expose port 8010 to trusted networks
- Use VPN for internal service communication
- Monitor for unauthorized access

### Incident Response

**If Encryption Key Compromised**:
1. Immediately rotate encryption key
2. Update `.env` file
3. Restart service
4. Review logs for unauthorized access
5. Notify affected users

**If Private Key Compromised**:
1. Generate new Solana keypair
2. Update `SOLANA_KEYPAIR_PATH`
3. Restart service
4. Review transaction history
5. Consider moving funds if needed

## Maintenance

### Updates

**Updating Service**:
```bash
# Pull latest code
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
# (method depends on deployment)
```

**Updating Configuration**:
1. Update `.env` file
2. Restart service
3. Verify health check passes

### Backup

**What to Backup**:
- `.env` file (encrypted, secure location)
- Solana keypair (encrypted, secure location)
- Logs (if persisted)

**Backup Frequency**: Daily for production

### Scaling

**Horizontal Scaling**:
- Run multiple instances behind load balancer
- Use shared state (Redis) for session management if needed
- Ensure idempotency of operations

**Vertical Scaling**:
- Increase CPU/memory for high computation load
- Monitor resource usage

## Support

**Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-arcium-bridge-service/issues)

**Documentation**:
- [Bridge Specification](bridge-spec.md)
- [Cryptographic Operations](crypto.md)
- [Arcium Integration Guide](../ARCIUM_INTEGRATION_GUIDE.md)

**Arcium Resources**:
- [Arcium Developer Documentation](https://docs.arcium.com/developers)
- [Arcium GitHub](https://github.com/orgs/arcium-hq/)
- [Arcium Discord](https://discord.com/invite/arcium)

