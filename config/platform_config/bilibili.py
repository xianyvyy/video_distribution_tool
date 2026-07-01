"""
Bilibili platform config: API base URL, resolution, rate limit.
"""
from dataclasses import dataclass
from typing import List

# API
BILIBILI_API_BASE: str = "https://api.bilibili.com"
BILIBILI_PASSPORT_BASE: str = "https://passport.bilibili.com"

# Video constraints
BILIBILI_SUPPORTED_RESOLUTIONS: List[tuple] = [(1920, 1080), (1280, 720)]
BILIBILI_MAX_TITLE_LEN: int = 80
BILIBILI_MAX_DESC_LEN: int = 250
BILIBILI_MAX_VIDEO_SIZE_MB: int = 4000
BILIBILI_MAX_VIDEO_DURATION_SEC: int = 3600 * 2  # 2 hours

# Rate limit (seconds between API calls)
BILIBILI_REQUEST_INTERVAL_SEC: float = 1.0


@dataclass
class BilibiliConfig:
    api_base: str = BILIBILI_API_BASE
    passport_base: str = BILIBILI_PASSPORT_BASE
    request_interval_sec: float = BILIBILI_REQUEST_INTERVAL_SEC
    supported_resolutions: List[tuple] = None
    max_title_len: int = BILIBILI_MAX_TITLE_LEN
    max_desc_len: int = BILIBILI_MAX_DESC_LEN
    max_video_size_mb: int = BILIBILI_MAX_VIDEO_SIZE_MB
    max_video_duration_sec: int = BILIBILI_MAX_VIDEO_DURATION_SEC

    def __post_init__(self) -> None:
        if self.supported_resolutions is None:
            self.supported_resolutions = list(BILIBILI_SUPPORTED_RESOLUTIONS)
