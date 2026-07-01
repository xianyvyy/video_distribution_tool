"""
Celery app: broker and result backend from config.
"""
from celery import Celery

try:
    from config.base import REDIS_CELERY_BROKER, CELERY_RESULT_BACKEND
except ImportError:
    from video_distribution_tool.config.base import REDIS_CELERY_BROKER, CELERY_RESULT_BACKEND

app = Celery(
    "video_distribution_tool",
    broker=REDIS_CELERY_BROKER,
    backend=CELERY_RESULT_BACKEND,
    include=["tasks.upload_task", "tasks.data_fetch_task", "tasks.alert_task"],
)
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
