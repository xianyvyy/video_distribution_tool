"""
Vault client for secrets. All platform credentials should be read via Vault;
business code must not store plaintext keys. Fallback: use env for dev.
"""
from typing import Any, Optional
import os

# Optional: hvac for HashiCorp Vault
try:
    import hvac
    _HAS_VAULT = True
except ImportError:
    _HAS_VAULT = False


def get_vault_client():
    if not _HAS_VAULT:
        return None
    try:
        from config.security import VAULT_ADDR, VAULT_TOKEN
    except ImportError:
        from video_distribution_tool.config.security import VAULT_ADDR, VAULT_TOKEN
    if not VAULT_ADDR or not VAULT_TOKEN:
        return None
    return hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)


def get_secret(path: str, key: Optional[str] = None) -> Any:
    """
    Read secret from Vault at path (e.g. secret/video_tool/bilibili).
    If key is given, return secret[key]; else return full secret dict.
    """
    client = get_vault_client()
    if not client or not client.is_authenticated():
        # Dev fallback: env
        env_key = path.replace("/", "_").upper() + ("_" + key if key else "")
        return os.environ.get(env_key)
    try:
        from config.security import VAULT_SECRET_PATH
    except ImportError:
        from video_distribution_tool.config.security import VAULT_SECRET_PATH
    full_path = f"{VAULT_SECRET_PATH}/{path}" if not path.startswith("secret/") else path
    try:
        resp = client.secrets.kv.v2.read_secret_version(mount_point="secret", path=full_path.replace("secret/", "", 1))
        data = resp.get("data", {}).get("data", {})
        return data.get(key) if key else data
    except Exception:
        return None


def set_secret(path: str, payload: dict) -> bool:
    """Write secret to Vault (admin only)."""
    client = get_vault_client()
    if not client or not client.is_authenticated():
        return False
    try:
        client.secrets.kv.v2.create_or_update_secret(mount_point="secret", path=path, secret=payload)
        return True
    except Exception:
        return False
