"""
Platform-specific config: resolution, API base URL, request frequency.
Import per-platform configs for use in adapters.
"""
from .bilibili import BilibiliConfig
from .douyin import DouyinConfig
from .xiaohongshu import XiaohongshuConfig

__all__ = ["BilibiliConfig", "DouyinConfig", "XiaohongshuConfig"]
