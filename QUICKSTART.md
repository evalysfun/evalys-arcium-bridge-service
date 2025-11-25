# Quick Start Guide

## Running the Bridge Service for Demo

### Option 1: Quick Start Script (Easiest)

```bash
# Make sure you're in the evalys-arcium-bridge-service directory
cd evalys-arcium-bridge-service

# Activate virtual environment (if using one)
# source venv/bin/activate  # Linux/Mac
# venv\Scripts\Activate.ps1  # Windows

# Run the quick start script
python start_server.py
```

This will start the service on `http://localhost:8010` with minimal configuration (demo mode).

### Option 2: Using Python Module

```bash
# Set PYTHONPATH
export PYTHONPATH=.  # Linux/Mac
# or
$env:PYTHONPATH = "."  # Windows PowerShell

# Run the server
python -m src.api.server
```

### Option 3: Using Uvicorn Directly

```bash
# Set PYTHONPATH
export PYTHONPATH=.  # Linux/Mac
# or
$env:PYTHONPATH = "."  # Windows PowerShell

# Run with uvicorn
uvicorn src.api.server:app --host 0.0.0.0 --port 8010 --reload
```

## Running the Demo Script

Once the server is running, open a **new terminal** and run:

```bash
cd evalys-arcium-bridge-service
python examples/demo.py
```

## Verification

Check if the service is running:

```bash
# Health check
curl http://localhost:8010/health

# Or in browser
# http://localhost:8010/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "evalys-arcium-bridge"
}
```

## Troubleshooting

### Port Already in Use

If port 8010 is already in use:

```bash
# Change the port in start_server.py or use environment variable:
export API_PORT=8011
python start_server.py
```

### Module Not Found Errors

Make sure PYTHONPATH is set:

```bash
# Linux/Mac
export PYTHONPATH=.

# Windows PowerShell
$env:PYTHONPATH = "."

# Windows CMD
set PYTHONPATH=.
```

### Missing Dependencies

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

## Production Setup

For production, create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Then run the service normally - it will load configuration from `.env`.

