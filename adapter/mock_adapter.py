"""
Mock adapter: Puppeteer/Selenium encapsulation for platforms without official API.
Isolated from API adapters; used when platform_config use_mock=True (e.g. xiaohongshu).
"""
from typing import Any, Dict, List, Optional

from .base_adapter import BasePlatformAdapter, DataFetchResult, UploadResult


class MockAdapter(BasePlatformAdapter):
    """Simulates browser automation. Real impl would use Puppeteer/Selenium."""

    def __init__(self, platform: str = "unknown") -> None:
        self._platform = platform

    @property
    def platform_name(self) -> str:
        return self._platform

    def authorize(self, credential: Dict[str, Any]) -> bool:
        # Mock: cookie or login flow
        return bool(credential.get("cookie") or credential.get("access_token"))

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: Optional[str] = None,
        credential: Optional[Dict[str, Any]] = None,
        resume_meta: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> UploadResult:
        if not credential:
            return UploadResult(success=False, error="Missing credential for mock upload")
        # Placeholder: would drive browser to upload page, fill form, submit
        return UploadResult(success=True, url=f"https://mock/{self._platform}/0", platform_video_id="mock_0")

    def fetch_data(
        self,
        credential: Optional[Dict[str, Any]] = None,
        video_ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> DataFetchResult:
        return DataFetchResult(success=True, metrics={"play_count": 0, "like_count": 0, "comment_count": 0})
