"""
Base configuration: database, Redis, Celery.
Environment-based (e.g. development, production).
"""
import os
from typing import Optional

# Database (PostgreSQL)
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/video_distribution",
)
DB_ECHO: bool = os.getenv("DB_ECHO", "0").lower() in ("1", "true", "yes")

# Redis
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_CELERY_BROKER: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)

# Celery
CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_TASK_SERIALIZER: str = "json"
CELERY_RESULT_SERIALIZER: str = "json"
CELERY_ACCEPT_CONTENT: list = ["json"]
CELERY_TIMEZONE: Optional[str] = os.getenv("TZ", "UTC")

# App / Web (backend deployment, frontend calls this)
HOST: str = os.getenv("HOST", "0.0.0.0")  # 0.0.0.0 for external access
_PORT_RAW: str = os.getenv("PORT", "8000")
PORT: int = max(1, min(65535, int(_PORT_RAW) if _PORT_RAW.isdigit() else 8000))
API_PREFIX: str = (os.getenv("API_PREFIX") or "").strip().rstrip("/")
# CORS: allow frontend origin (comma-separated). In DEBUG, "*" can be set for dev.
_CORS_RAW: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000")
CORS_ORIGINS: list = [s.strip() for s in _CORS_RAW.split(",") if s.strip()]

# Allowed platforms (API rejects others). Empty = allow all.
ALLOWED_PLATFORMS: list = [
    s.strip() for s in (os.getenv("ALLOWED_PLATFORMS") or "bilibili,douyin,xiaohongshu").split(",") if s.strip()
]

# App
DEBUG: bool = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")
ENV: str = os.getenv("ENV", "development")
