"""
FastAPI app: mount v1 routes, CORS for frontend, health check.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from api.v1 import account, upload, dashboard
except ImportError:
    from video_distribution_tool.api.v1 import account, upload, dashboard

try:
    from config.base import CORS_ORIGINS, API_PREFIX
except ImportError:
    from video_distribution_tool.config.base import CORS_ORIGINS, API_PREFIX

app = FastAPI(
    title="Video Distribution Tool",
    version="1.0",
    description="多平台视频上传与数据追踪 API",
    docs_url="/docs",
    redoc_url="/redoc",
)
_origins = CORS_ORIGINS if CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=("*" not in _origins),
    allow_methods=["*"],
    allow_headers=["*"],
)
_prefix = API_PREFIX.rstrip("/") if API_PREFIX else ""
app.include_router(account.router, prefix=(_prefix + "/v1") if _prefix else "/v1")
app.include_router(upload.router, prefix=(_prefix + "/v1") if _prefix else "/v1")
app.include_router(dashboard.router, prefix=(_prefix + "/v1") if _prefix else "/v1")


@app.get("/health", tags=["health"])
def health():
    """就绪检查，用于负载均衡/容器探针。"""
    return {"status": "ok"}
