"""
Redis operations: cache, session, task state.
Dashboard stats TTL configurable per platform.
"""
from .redis_client import get_redis, cache_get, cache_set, cache_delete

__all__ = ["get_redis", "cache_get", "cache_set", "cache_delete"]
