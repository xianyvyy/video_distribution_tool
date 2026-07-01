"""
Operation audit log: account ops, video upload, data fetch.
Records operator, time, platform, result. Must not be skipped for sensitive actions.
"""
import logging
from datetime import datetime, timezone
from typing import Any, Optional

# Use structured logging; in production can ship to SIEM/audit store
_AUDIT = logging.getLogger("compliance.audit")


def audit_log(
    action: str,
    operator: str,
    platform: Optional[str] = None,
    result: str = "success",
    details: Optional[dict] = None,
) -> None:
    """
    Log an auditable event. action e.g. 'account.bind', 'upload.video', 'data.fetch'.
    """
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "operator": operator,
        "platform": platform,
        "result": result,
        "details": details or {},
    }
    _AUDIT.info("AUDIT %s", payload)
