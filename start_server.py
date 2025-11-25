#!/usr/bin/env python3
"""
Quick start script for Arcium Bridge Service

This script starts the bridge service with minimal configuration for demo purposes.
For production, use proper .env configuration.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Set minimal environment variables for demo mode
os.environ.setdefault("API_HOST", "0.0.0.0")
os.environ.setdefault("API_PORT", "8010")
os.environ.setdefault("API_DEBUG", "true")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Arcium MXE program ID is optional for demo mode (v0.1 uses simulated computation)
# Uncomment and set if you have a real program ID:
# os.environ["ARCIUM_MXE_PROGRAM_ID"] = "your_program_id_here"

print("Starting Evalys Arcium Bridge Service in demo mode...")
print("Note: This uses simulated computation (v0.1)")
print("For production, configure .env file with real Arcium credentials")
print()

# Import and run server
if __name__ == "__main__":
    import uvicorn
    
    # Use import string for reload mode, direct import for non-reload
    api_debug = os.environ.get("API_DEBUG", "false").lower() == "true"
    
    if api_debug:
        # Reload mode requires import string
        uvicorn.run(
            "src.api.server:app",
            host=os.environ.get("API_HOST", "0.0.0.0"),
            port=int(os.environ.get("API_PORT", 8010)),
            reload=True,
        )
    else:
        # Non-reload mode can use direct import
        from src.api.server import app
        uvicorn.run(
            app,
            host=os.environ.get("API_HOST", "0.0.0.0"),
            port=int(os.environ.get("API_PORT", 8010)),
            reload=False,
        )

