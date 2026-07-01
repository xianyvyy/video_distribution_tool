"""
Async data fetch task: Celery task for dashboard / periodic pull. Results can be merged.
"""
from typing import Dict, List

from .celery_app import app

try:
    from service.data_tracking import DataTrackingService
except ImportError:
    from video_distribution_tool.service.data_tracking import DataTrackingService


@app.task
def fetch_platform_data_task(platform: str, operator: str = "system") -> Dict:
    """Fetch data for one platform; cache in Redis via DataTrackingService."""
    svc = DataTrackingService()
    result = svc.fetch_platform_data(platform, use_cache=True, operator=operator)
    return {"success": result.success, "metrics": result.metrics, "error": result.error}


@app.task
def fetch_all_platforms_task(platforms: List[str] = None, operator: str = "system") -> Dict:
    """Parallel fetch: one task per platform; caller can group or merge."""
    platforms = platforms or ["bilibili", "douyin", "xiaohongshu"]
    results = {}
    for p in platforms:
        r = fetch_platform_data_task.apply_async(args=[p], kwargs={"operator": operator})
        results[p] = {"task_id": r.id}
    return results
