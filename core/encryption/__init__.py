"""
AES-256 encryption/decryption for account credentials only.
Business code must not store plaintext credentials; use this layer.
"""
from .crypto import encrypt_credential, decrypt_credential

__all__ = ["encrypt_credential", "decrypt_credential"]
