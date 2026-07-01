"""
Compliance core: sensitive-word check, operation audit log, rate limiting.
All sensitive operations must go through this layer.
"""
from .audit import audit_log
from .rate_limit import rate_limit_acquire, rate_limit_release
from .sensitive import check_sensitive_text

__all__ = [
    "audit_log",
    "rate_limit_acquire",
    "rate_limit_release",
    "check_sensitive_text",
]
