"""
Data tracking: multi-platform data fetch, cache, anomaly alert. Uses adapter + storage/cache.
"""
from typing import Any, Dict, List, Optional

try:
    from core.compliance import audit_log
except ImportError:
    from video_distribution_tool.core.compliance import audit_log

try:
    from storage.cache import cache_get, cache_set
except ImportError:
    from video_distribution_tool.storage.cache import cache_get, cache_set

from adapter.base_adapter import DataFetchResult
from service.account_service import get_adapter_for_platform

# Dashboard cache TTL (e.g. 1 hour per platform update frequency)
DASHBOARD_CACHE_TTL = 3600


class DataTrackingService:
    """Fetch and optionally cache stats; audit all fetches."""

    def fetch_platform_data(
        self,
        platform: str,
        credential: Optional[Dict[str, Any]] = None,
        video_ids: Optional[List[str]] = None,
        use_cache: bool = True,
        operator: str = "system",
    ) -> DataFetchResult:
        """Fetch data for one platform; optionally use Redis cache for dashboard."""
        cache_key = f"dashboard:{platform}:{','.join(sorted(video_ids or []))}"
        if use_cache:
            cached = cache_get(cache_key)
            if cached is not None:
                audit_log("data.fetch", operator, platform=platform, result="cache_hit")
                return DataFetchResult(success=True, metrics=cached)
        adapter = get_adapter_for_platform(platform)
        result = adapter.fetch_data(credential, video_ids)
        if result.success and result.metrics and use_cache:
            cache_set(cache_key, result.metrics, ttl_sec=DASHBOARD_CACHE_TTL)
        audit_log(
            "data.fetch",
            operator,
            platform=platform,
            result="success" if result.success else "failure",
            details={"error": result.error},
        )
        return result

    def fetch_all_platforms(
        self,
        platforms: List[str],
        credentials: Optional[Dict[str, Dict[str, Any]]] = None,
        operator: str = "system",
    ) -> Dict[str, DataFetchResult]:
        """Parallel-friendly: fetch each platform; merge for dashboard."""
        credentials = credentials or {}
        return {
            p: self.fetch_platform_data(p, credentials.get(p), use_cache=True, operator=operator)
            for p in platforms
        }
