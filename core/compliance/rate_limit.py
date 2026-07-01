"""
Request rate limiting per platform. Uses config/platform_config and config/security.
In-memory implementation here; production should use Redis for distributed limit.
"""
import time
import threading
from typing import Optional

# In-memory: platform -> last request time (for single process). Use Redis in production.
_LAST_REQUEST: dict = {}
_LOCK = threading.Lock()


def rate_limit_acquire(platform: str, interval_sec: float) -> None:
    """
    Block until at least interval_sec has passed since last request for this platform.
    Call before issuing platform API request.
    """
    with _LOCK:
        last = _LAST_REQUEST.get(platform, 0)
        now = time.monotonic()
        wait = last + interval_sec - now
        if wait > 0:
            time.sleep(wait)
        _LAST_REQUEST[platform] = time.monotonic()


def rate_limit_release(platform: str) -> None:
    """Optional: mark request done (for future token-bucket impl). Currently no-op."""
    pass
