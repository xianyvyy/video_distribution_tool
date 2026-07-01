"""
Douyin platform config: enterprise API, resolution, rate limit.
"""
from dataclasses import dataclass
from typing import List

DOUYIN_OPEN_API_BASE: str = "https://open.douyin.com"
DOUYIN_SUPPORTED_RESOLUTIONS: List[tuple] = [(1920, 1080), (1280, 720), (720, 1280)]
DOUYIN_MAX_TITLE_LEN: int = 55
DOUYIN_MAX_VIDEO_SIZE_MB: int = 4000
DOUYIN_MAX_VIDEO_DURATION_SEC: int = 600  # 10 min typical
DOUYIN_REQUEST_INTERVAL_SEC: float = 1.5  # stricter for enterprise API


@dataclass
class DouyinConfig:
    api_base: str = DOUYIN_OPEN_API_BASE
    request_interval_sec: float = DOUYIN_REQUEST_INTERVAL_SEC
    supported_resolutions: List[tuple] = None
    max_title_len: int = DOUYIN_MAX_TITLE_LEN
    max_video_size_mb: int = DOUYIN_MAX_VIDEO_SIZE_MB
    max_video_duration_sec: int = DOUYIN_MAX_VIDEO_DURATION_SEC

    def __post_init__(self) -> None:
        if self.supported_resolutions is None:
            self.supported_resolutions = list(DOUYIN_SUPPORTED_RESOLUTIONS)
