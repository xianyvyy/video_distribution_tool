"""
Security & compliance config: encryption, request interval, proxy pool.
All sensitive/rate-limit settings centralized here.
"""
import os
from typing import List

# AES-256 for account credentials
ENCRYPTION_KEY_ENV: str = os.getenv("ENCRYPTION_KEY_ENV", "VIDEO_TOOL_ENCRYPTION_KEY")
ENCRYPTION_ALGORITHM: str = "AES-256-GCM"

# Global request throttle (seconds between requests per platform when not in platform_config)
DEFAULT_REQUEST_INTERVAL_SEC: float = float(os.getenv("DEFAULT_REQUEST_INTERVAL_SEC", "1.0"))
MAX_CONCURRENT_REQUESTS_PER_PLATFORM: int = int(os.getenv("MAX_CONCURRENT_REQUESTS_PER_PLATFORM", "2"))

# Proxy pool (optional)
PROXY_POOL_ENABLED: bool = os.getenv("PROXY_POOL_ENABLED", "0").lower() in ("1", "true", "yes")
PROXY_LIST: List[str] = [
    s.strip() for s in os.getenv("PROXY_LIST", "").split(",") if s.strip()
]

# Vault (secrets management)
VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://localhost:8200")
VAULT_TOKEN: str = os.getenv("VAULT_TOKEN", "")
VAULT_SECRET_PATH: str = os.getenv("VAULT_SECRET_PATH", "secret/video_tool")
