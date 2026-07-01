"""
Sensitive word check for title/description. Fail = block upload and record.
"""
import re
from typing import List, Optional, Tuple

# Default block list (load from config or DB in production)
_DEFAULT_BLOCK_PATTERNS: List[str] = []


def set_sensitive_patterns(patterns: List[str]) -> None:
    """Set regex or literal block patterns."""
    global _DEFAULT_BLOCK_PATTERNS
    _DEFAULT_BLOCK_PATTERNS = list(patterns)


def check_sensitive_text(text: str, extra_patterns: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Check text for sensitive content. Returns (passed, matched_pattern).
    If passed is False, matched_pattern indicates what matched (for logging).
    """
    if not text:
        return True, None
    patterns = list(_DEFAULT_BLOCK_PATTERNS) + (extra_patterns or [])
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE):
                return False, p
        except re.error:
            if p in text:
                return False, p
    return True, None
