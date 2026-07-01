"""
Base platform adapter: unified interface for authorize, upload_video, fetch_data.
All platform-specific logic lives in concrete adapters; service layer uses only this interface.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UploadResult:
    success: bool
    url: Optional[str] = None
    platform_video_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DataFetchResult:
    success: bool
    metrics: Optional[Dict[str, Any]] = None  # play_count, like_count, comment_count, etc.
    error: Optional[str] = None


class BasePlatformAdapter(ABC):
    """Base class for all platform adapters. Implements unified API + optional mock path."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """e.g. bilibili, douyin, xiaohongshu."""
        pass

    @abstractmethod
    def authorize(self, credential: Dict[str, Any]) -> bool:
        """
        Validate/refresh token with given credential. Return True if authorized.
        credential may contain access_token, refresh_token, etc. (from Vault/encrypted store).
        """
        pass

    @abstractmethod
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: Optional[str] = None,
        credential: Optional[Dict[str, Any]] = None,
        resume_meta: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> UploadResult:
        """
        Upload video to platform. resume_meta for resumable upload (chunk/offset).
        """
        pass

    @abstractmethod
    def fetch_data(
        self,
        credential: Optional[Dict[str, Any]] = None,
        video_ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> DataFetchResult:
        """Fetch stats (play, like, comment, etc.) for account or given videos."""
        pass
