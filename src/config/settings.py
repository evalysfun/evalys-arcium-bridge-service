"""Application settings"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        # Fallback for older pydantic v2 versions
        from pydantic import BaseSettings
    except ImportError:
        # Fallback for pydantic v1
        from pydantic import BaseSettings

from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Arcium MXE Configuration
    # Note: Optional for demo mode (v0.1 uses simulated computation)
    arcium_mxe_program_id: Optional[str] = None
    arcium_cluster_offset: int = 1078779259
    arcium_rpc_url: str = "https://api.devnet.solana.com"
    
    # Solana Configuration
    solana_rpc_url: str = "https://api.devnet.solana.com"
    solana_keypair_path: Optional[str] = None
    
    # Service Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8010
    api_debug: bool = False
    
    # Arcium Client Configuration
    arcium_client_encryption_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

