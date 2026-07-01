"""
Async upload task: Celery task with resumable state in Redis. Retry on failure.
"""
from typing import Any, Dict, List, Optional

from .celery_app import app

try:
    from service.upload_service import UploadService
    from service.account_service import AccountService
except ImportError:
    from video_distribution_tool.service.upload_service import UploadService
    from video_distribution_tool.service.account_service import AccountService


@app.task(bind=True, max_retries=3)
def upload_video_task(
    self,
    platform: str,
    video_path: str,
    title: str,
    description: Optional[str] = None,
    resume_meta: Optional[Dict[str, Any]] = None,
    operator: str = "system",
) -> Dict[str, Any]:
    """Run upload in worker; update resume_meta in Redis for resumable upload."""
    try:
        svc = UploadService(account_service=AccountService())
        result = svc.upload_to_platform(
            platform, video_path, title, description, resume_meta=resume_meta, operator=operator
        )
        return {"success": result.success, "url": result.url, "error": result.error, "platform_video_id": result.platform_video_id}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task
def upload_to_multiple_platforms_task(
    platforms: List[str],
    video_path: str,
    title: str,
    description: Optional[str] = None,
    operator: str = "system",
) -> Dict[str, Dict[str, Any]]:
    """Dispatch upload to each platform as sub-tasks or sequential."""
    results = {}
    for p in platforms:
        r = upload_video_task.apply_async(args=[p, video_path, title], kwargs={"description": description, "operator": operator})
        results[p] = {"task_id": r.id, "status": "pending"}
    return results
