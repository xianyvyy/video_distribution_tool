"""
OAuth2.0 unified authorization flow.
Platform-specific OAuth steps can be delegated to adapters; this module provides common types and helpers.
"""
from .oauth_flow import get_authorization_url, exchange_code_for_tokens

__all__ = ["get_authorization_url", "exchange_code_for_tokens"]
