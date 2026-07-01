"""
Account API v1: list/add accounts. Credentials never returned in list.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

try:
    from config.base import ALLOWED_PLATFORMS
except ImportError:
    from video_distribution_tool.config.base import ALLOWED_PLATFORMS
try:
    from api.v1.schemas import AccountAddBody
except ImportError:
    from video_distribution_tool.api.v1.schemas import AccountAddBody

router = APIRouter(prefix="/account", tags=["account"])


def get_account_service():
    try:
        from service.account_service import AccountService
    except ImportError:
        from video_distribution_tool.service.account_service import AccountService
    return AccountService()


def _check_platform(platform: str) -> None:
    if ALLOWED_PLATFORMS and platform not in ALLOWED_PLATFORMS:
        raise HTTPException(400, detail=f"Platform not allowed: {platform}. Allowed: {ALLOWED_PLATFORMS}")


@router.get("/list")
def list_accounts(
    platform: Optional[str] = None,
    active_only: bool = True,
    svc=Depends(get_account_service),
):
    if platform is not None:
        _check_platform(platform)
    return svc.list_accounts(platform=platform, active_only=active_only)


@router.post("/add")
def add_account(body: AccountAddBody, svc=Depends(get_account_service)):
    _check_platform(body.platform)
    try:
        return svc.add_account(
            platform=body.platform,
            name=body.name,
            operator=body.operator,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
