"""
Upload API v1: single or multi-platform upload. Compliance runs in service layer.
"""
from fastapi import APIRouter, Depends, HTTPException

try:
    from config.base import ALLOWED_PLATFORMS
except ImportError:
    from video_distribution_tool.config.base import ALLOWED_PLATFORMS
try:
    from api.v1.schemas import UploadToPlatformBody, UploadToMultipleBody
except ImportError:
    from video_distribution_tool.api.v1.schemas import UploadToPlatformBody, UploadToMultipleBody

router = APIRouter(prefix="/upload", tags=["upload"])


def get_upload_service():
    try:
        from service.upload_service import UploadService
        from service.account_service import AccountService
    except ImportError:
        from video_distribution_tool.service.upload_service import UploadService
        from video_distribution_tool.service.account_service import AccountService
    return UploadService(account_service=AccountService())


def _check_platform(platform: str) -> None:
    if ALLOWED_PLATFORMS and platform not in ALLOWED_PLATFORMS:
        raise HTTPException(400, detail=f"Platform not allowed: {platform}. Allowed: {ALLOWED_PLATFORMS}")


@router.post("/to-platform")
def upload_to_platform(body: UploadToPlatformBody, svc=Depends(get_upload_service)):
    _check_platform(body.platform)
    try:
        result = svc.upload_to_platform(
            body.platform,
            body.video_path,
            body.title,
            body.description,
            operator=body.operator,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    return {"success": result.success, "url": result.url, "error": result.error}


@router.post("/to-multiple")
def upload_to_multiple(body: UploadToMultipleBody, svc=Depends(get_upload_service)):
    for p in body.platforms:
        _check_platform(p)
    try:
        results = svc.upload_to_multiple_platforms(
            body.platforms,
            body.video_path,
            body.title,
            body.description,
            operator=body.operator,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    return {p: {"success": r.success, "url": r.url, "error": r.error} for p, r in results.items()}
