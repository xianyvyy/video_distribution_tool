"""
Alert task: anomaly detection / threshold alert. Can be triggered by data_fetch or schedule.
"""
from typing import Any, Dict

from .celery_app import app

try:
    from core.compliance import audit_log
except ImportError:
    from video_distribution_tool.core.compliance import audit_log


@app.task
def check_anomaly_alert(platform: str, metrics: Dict[str, Any], thresholds: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Compare metrics to thresholds; log alert if exceeded. In production, send to notification channel.
    """
    thresholds = thresholds or {}
    alerts = []
    for key, limit in thresholds.items():
        val = metrics.get(key)
        if val is not None and float(val) >= limit:
            alerts.append({"metric": key, "value": val, "threshold": limit})
    if alerts:
        audit_log("alert.anomaly", "system", platform=platform, result="alert", details={"alerts": alerts})
    return {"platform": platform, "alerts": alerts}
