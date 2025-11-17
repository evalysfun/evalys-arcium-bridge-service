"""Application settings"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings

from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Arcium MXE Configuration
    arcium_mxe_program_id: str
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

