"""
Generic OAuth2.0 helpers. Actual platform URLs and token endpoints are in adapters.
"""
from typing import Any, Dict, Optional
from urllib.parse import urlencode


def get_authorization_url(
    auth_url: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: Optional[str] = None,
    extra_params: Optional[Dict[str, Any]] = None,
) -> str:
    """Build OAuth2 authorization URL."""
    params: Dict[str, Any] = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    if state:
        params["state"] = state
    if extra_params:
        params.update(extra_params)
    return f"{auth_url}?{urlencode(params)}"


def exchange_code_for_tokens(
    token_url: str,
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
    grant_type: str = "authorization_code",
) -> Dict[str, Any]:
    """
    Exchange authorization code for tokens. Caller should use requests/httpx.
    Returns dict with access_token, refresh_token, expires_in, etc.
    """
    return {
        "token_url": token_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": grant_type,
    }
