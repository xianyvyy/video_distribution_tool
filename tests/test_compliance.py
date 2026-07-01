"""
Compliance tests: sensitive-word check, rate limit, audit log.
"""
import logging
import pytest

# Ensure package path
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_check_sensitive_text_pass():
    from core.compliance.sensitive import check_sensitive_text
    passed, matched = check_sensitive_text("normal title")
    assert passed is True
    assert matched is None


def test_check_sensitive_text_block():
    from core.compliance.sensitive import check_sensitive_text, set_sensitive_patterns
    set_sensitive_patterns([r"badword", "blockme"])
    passed, matched = check_sensitive_text("hello blockme world")
    assert passed is False
    assert matched is not None
    set_sensitive_patterns([])  # reset


def test_audit_log(caplog):
    from core.compliance.audit import audit_log
    logging.getLogger("compliance.audit").setLevel(logging.INFO)
    with caplog.at_level(logging.INFO, logger="compliance.audit"):
        audit_log("test.action", "operator1", platform="bilibili", result="success")
    assert "AUDIT" in caplog.text and "test.action" in caplog.text


def test_rate_limit_acquire():
    from core.compliance.rate_limit import rate_limit_acquire, _LAST_REQUEST
    platform = "test_platform_rate_limit"
    _LAST_REQUEST.pop(platform, None)
    rate_limit_acquire(platform, 0.01)  # 10ms
    rate_limit_acquire(platform, 0.01)
    assert platform in _LAST_REQUEST
