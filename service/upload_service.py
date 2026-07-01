"""
Upload service: video distribution, resumable upload, retry. Uses adapter + core/compliance + media.
"""
from typing import Any, Dict, List, Optional

try:
    from core.compliance import audit_log, check_sensitive_text, rate_limit_acquire
except ImportError:
    from video_distribution_tool.core.compliance import audit_log, check_sensitive_text, rate_limit_acquire

try:
    from adapter.base_adapter import BasePlatformAdapter, UploadResult
    from service.account_service import get_adapter_for_platform, AccountService
except ImportError:
    from video_distribution_tool.adapter.base_adapter import BasePlatformAdapter, UploadResult
    from video_distribution_tool.service.account_service import get_adapter_for_platform, AccountService


class UploadService:
    """One-shot or multi-platform upload with compliance and retry."""

    def __init__(self, account_service: Optional[AccountService] = None) -> None:
        self._account_service = account_service or AccountService()

    def upload_to_platform(
        self,
        platform: str,
        video_path: str,
        title: str,
        description: Optional[str] = None,
        credential: Optional[Dict[str, Any]] = None,
        resume_meta: Optional[Dict[str, Any]] = None,
        operator: str = "system",
    ) -> UploadResult:
        """Single platform upload: sensitive check -> audit -> adapter.upload_video."""
        passed, matched = check_sensitive_text(title)
        if not passed:
            audit_log("upload.video", operator, platform=platform, result="blocked", details={"reason": "sensitive", "matched": matched})
            return UploadResult(success=False, error=f"Sensitive content in title: {matched}")
        if description:
            passed, matched = check_sensitive_text(description)
            if not passed:
                audit_log("upload.video", operator, platform=platform, result="blocked", details={"reason": "sensitive", "matched": matched})
                return UploadResult(success=False, error=f"Sensitive content in description: {matched}")
        cred = credential or self._account_service.get_credential_for_account(platform)
        adapter = get_adapter_for_platform(platform)
        result = adapter.upload_video(video_path, title, description, cred, resume_meta)
        audit_log(
            "upload.video",
            operator,
            platform=platform,
            result="success" if result.success else "failure",
            details={"url": result.url, "error": result.error},
        )
        return result

    def upload_to_multiple_platforms(
        self,
        platforms: List[str],
        video_path: str,
        title: str,
        description: Optional[str] = None,
        operator: str = "system",
    ) -> Dict[str, UploadResult]:
        """Dispatch to each platform; returns dict platform -> UploadResult."""
        results = {}
        for platform in platforms:
            results[platform] = self.upload_to_platform(
                platform, video_path, title, description, None, None, operator
            )
        return results
