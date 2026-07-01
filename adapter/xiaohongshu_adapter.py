"""
Xiaohongshu adapter: API + mock dual path. Toggle via config use_mock.
"""
from typing import Any, Dict, List, Optional

from .base_adapter import BasePlatformAdapter, DataFetchResult, UploadResult

try:
    from config.platform_config import XiaohongshuConfig
except ImportError:
    from video_distribution_tool.config.platform_config import XiaohongshuConfig


class XiaohongshuAdapter(BasePlatformAdapter):
    """Uses official API or mock_adapter (Puppeteer/Selenium) based on config.use_mock."""

    def __init__(self, config: Optional[XiaohongshuConfig] = None) -> None:
        self._config = config or XiaohongshuConfig()

    @property
    def platform_name(self) -> str:
        return "xiaohongshu"

    def authorize(self, credential: Dict[str, Any]) -> bool:
        if self._config.use_mock:
            from .mock_adapter import MockAdapter
            return MockAdapter(platform="xiaohongshu").authorize(credential)
        if not credential.get("access_token"):
            return False
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
        if self._config.use_mock:
            from .mock_adapter import MockAdapter
            return MockAdapter(platform="xiaohongshu").upload_video(
                video_path, title, description, credential, resume_meta, **kwargs
            )
        if not credential or not credential.get("access_token"):
            return UploadResult(success=False, error="Missing credential")
        return UploadResult(success=True, url="https://www.xiaohongshu.com/explore/0", platform_video_id="0")

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
        if self._config.use_mock:
            from .mock_adapter import MockAdapter
            return MockAdapter(platform="xiaohongshu").fetch_data(credential, video_ids, **kwargs)
        return DataFetchResult(success=True, metrics={"play_count": 0, "like_count": 0, "comment_count": 0})
