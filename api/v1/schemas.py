"""
Pydantic schemas for API v1 request/response.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class AccountAddBody(BaseModel):
    platform: str = Field(..., description="平台标识")
    name: Optional[str] = None
    operator: str = "system"


class UploadToPlatformBody(BaseModel):
    platform: str = Field(..., description="平台标识")
    video_path: str = Field(..., description="视频文件路径")
    title: str = Field(..., description="标题")
    description: Optional[str] = None
    operator: str = "system"


class UploadToMultipleBody(BaseModel):
    platforms: List[str] = Field(..., description="平台列表")
    video_path: str
    title: str
    description: Optional[str] = None
    operator: str = "system"
