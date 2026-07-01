"""
Dashboard API v1: aggregated stats from multiple platforms (cached).
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException

try:
    from config.base import ALLOWED_PLATFORMS
except ImportError:
    from video_distribution_tool.config.base import ALLOWED_PLATFORMS

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_tracking_service():
    try:
        from service.data_tracking import DataTrackingService
    except ImportError:
        from video_distribution_tool.service.data_tracking import DataTrackingService
    return DataTrackingService()


@router.get("/stats")
def get_stats(
    platforms: Optional[List[str]] = Query(None, description="平台列表，不传则默认全部"),
    operator: str = "system",
    svc=Depends(get_tracking_service),
):
    if platforms is None or len(platforms) == 0:
        platforms = ALLOWED_PLATFORMS if ALLOWED_PLATFORMS else ["bilibili", "douyin", "xiaohongshu"]
    for p in platforms:
        if ALLOWED_PLATFORMS and p not in ALLOWED_PLATFORMS:
            raise HTTPException(400, detail=f"Platform not allowed: {p}")
    try:
        results = svc.fetch_all_platforms(platforms, operator=operator)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    return {
        p: {"success": r.success, "metrics": r.metrics, "error": r.error}
        for p, r in results.items()
    }
