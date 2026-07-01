"""
Xiaohongshu platform config: API + mock dual-path, resolution, rate limit.
"""
from dataclasses import dataclass
from typing import List

XHS_API_BASE: str = "https://edith.xiaohongshu.com"
XHS_USE_MOCK: bool = False  # Toggle: True = mock (Puppeteer/Selenium), False = official API
XHS_SUPPORTED_RESOLUTIONS: List[tuple] = [(1920, 1080), (1080, 1920), (720, 1280)]
XHS_MAX_TITLE_LEN: int = 20
XHS_MAX_VIDEO_SIZE_MB: int = 1000
XHS_MAX_VIDEO_DURATION_SEC: int = 600
XHS_REQUEST_INTERVAL_SEC: float = 2.0  # conservative for XHS


@dataclass
class XiaohongshuConfig:
    api_base: str = XHS_API_BASE
    use_mock: bool = XHS_USE_MOCK
    request_interval_sec: float = XHS_REQUEST_INTERVAL_SEC
    supported_resolutions: List[tuple] = None
    max_title_len: int = XHS_MAX_TITLE_LEN
    max_video_size_mb: int = XHS_MAX_VIDEO_SIZE_MB
    max_video_duration_sec: int = XHS_MAX_VIDEO_DURATION_SEC

    def __post_init__(self) -> None:
        if self.supported_resolutions is None:
            self.supported_resolutions = list(XHS_SUPPORTED_RESOLUTIONS)
