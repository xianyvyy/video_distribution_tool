"""
AES-256-GCM encryption for account credentials.
Key must come from env or Vault; never hardcode.
"""
import base64
import os
from typing import Optional

# Prefer cryptography if available
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.backends import default_backend
    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def _get_key_bytes() -> bytes:
    key_hex = os.environ.get("VIDEO_TOOL_ENCRYPTION_KEY")
    if not key_hex or len(key_hex) < 32:
        raise ValueError(
            "VIDEO_TOOL_ENCRYPTION_KEY must be set and at least 32 hex chars (16 bytes) for AES-128, "
            "64 hex chars (32 bytes) for AES-256"
        )
    return bytes.fromhex(key_hex[:64] if len(key_hex) >= 64 else key_hex.ljust(64, "0")[:64])


def encrypt_credential(plaintext: str) -> str:
    """Encrypt a credential string; returns base64(nonce + ciphertext + tag)."""
    if not _HAS_CRYPTO:
        raise RuntimeError("Install cryptography: pip install cryptography")
    key = _get_key_bytes()
    if len(key) != 32:
        key = (key + b"\x00" * 32)[:32]
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ct).decode("ascii")


def decrypt_credential(ciphertext_b64: str) -> str:
    """Decrypt a credential string from base64(nonce + ciphertext + tag)."""
    if not _HAS_CRYPTO:
        raise RuntimeError("Install cryptography: pip install cryptography")
    key = _get_key_bytes()
    if len(key) != 32:
        key = (key + b"\x00" * 32)[:32]
    aesgcm = AESGCM(key)
    raw = base64.b64decode(ciphertext_b64)
    nonce, ct = raw[:12], raw[12:]
    return aesgcm.decrypt(nonce, ct, None).decode("utf-8")
