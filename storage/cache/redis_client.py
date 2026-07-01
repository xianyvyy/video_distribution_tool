"""
Redis client and cache helpers. Uses config.base.REDIS_URL.
"""
import json
from typing import Any, Optional

_redis = None


def get_redis():
    global _redis
    if _redis is None:
        try:
            import redis
            try:
                from config.base import REDIS_URL
            except ImportError:
                from video_distribution_tool.config.base import REDIS_URL
            _redis = redis.from_url(REDIS_URL, decode_responses=True)
        except ImportError:
            _redis = None  # optional: run without Redis
    return _redis


def cache_get(key: str) -> Optional[Any]:
    """Get JSON value from cache."""
    r = get_redis()
    if not r:
        return None
    raw = r.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def cache_set(key: str, value: Any, ttl_sec: int = 3600) -> bool:
    """Set JSON value with TTL (default 1h for dashboard stats)."""
    r = get_redis()
    if not r:
        return False
    if not isinstance(value, (str, bytes)):
        value = json.dumps(value)
    r.setex(key, ttl_sec, value)
    return True


def cache_delete(key: str) -> bool:
    r = get_redis()
    if not r:
        return False
    r.delete(key)
    return True
