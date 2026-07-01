"""
Bilibili adapter: official API. Uses platform_config and compliance rate limit.
"""
from typing import Any, Dict, List, Optional

from .base_adapter import BasePlatformAdapter, DataFetchResult, UploadResult

try:
    from config.platform_config import BilibiliConfig
except ImportError:
    from video_distribution_tool.config.platform_config import BilibiliConfig


class BilibiliAdapter(BasePlatformAdapter):
    def __init__(self, config: Optional[BilibiliConfig] = None) -> None:
        self._config = config or BilibiliConfig()

    @property
    def platform_name(self) -> str:
        return "bilibili"

    def authorize(self, credential: Dict[str, Any]) -> bool:
        # Validate access_token or refresh; call B站 API if needed
        if not credential.get("access_token"):
            return False
        # TODO: optional token validation request
        return True

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: Optional[str] = None,
        credential: Optional[Dict[str, Any]] = None,
        resume_meta: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> UploadResult:
        try:
            from core.compliance import rate_limit_acquire
        except ImportError:
            from video_distribution_tool.core.compliance import rate_limit_acquire
        rate_limit_acquire(self.platform_name, self._config.request_interval_sec)
        # Placeholder: real impl would call B站 upload API (preupload -> multipart)
        if not credential or not credential.get("access_token"):
            return UploadResult(success=False, error="Missing credential")
        # Simulate success for structure
        return UploadResult(success=True, url="https://www.bilibili.com/video/av0", platform_video_id="0")

    def fetch_data(
        self,
        credential: Optional[Dict[str, Any]] = None,
        video_ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> DataFetchResult:
        try:
            from core.compliance import rate_limit_acquire
        except ImportError:
            from video_distribution_tool.core.compliance import rate_limit_acquire
        rate_limit_acquire(self.platform_name, self._config.request_interval_sec)
        # Placeholder: call B站 stats API
        return DataFetchResult(success=True, metrics={"play_count": 0, "like_count": 0, "comment_count": 0})
