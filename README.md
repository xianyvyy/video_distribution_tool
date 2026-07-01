# 多平台视频上传与数据追踪工具

分层架构：config → core → adapter → service → api → tasks，合规能力收口在 core/compliance。

## 结构概览

- **config/** 配置与各平台参数
- **core/** 加密、授权、媒体处理、合规（审计/敏感词/限频）
- **adapter/** 平台适配层（B站、抖音、小红书、Mock）
- **service/** 账号、上传、数据追踪
- **api/** FastAPI v1 路由
- **tasks/** Celery 异步任务
- **storage/** DB、Redis、Vault
- **frontend/** 前端骨架（Vite）
- **tests/** 合规、适配器、上传服务测试

## 运行（后端 Web 端口，供前端调用）

后端默认监听 **8000** 端口，可通过环境变量修改：

```bash
cd video_distribution_tool
pip install -r requirements.txt
export VIDEO_TOOL_ENCRYPTION_KEY=$(python -c "import os; print(os.urandom(32).hex())")

# 默认: HOST=0.0.0.0 PORT=8000（前端可调用 http://<服务器>:8000/v1/...）
python run_server.py
# 或指定端口: PORT=9000 python run_server.py
# 或: uvicorn api.app:app --host 0.0.0.0 --port 8000
```

| 环境变量 | 说明 | 默认 |
|----------|------|------|
| `HOST` | 监听地址（0.0.0.0 允许外网访问） | 0.0.0.0 |
| `PORT` | Web 端口 | 8000 |
| `CORS_ORIGINS` | 允许的前端来源（逗号分隔） | localhost:5173, localhost:3000 等 |
| `API_PREFIX` | 反向代理时的 API 前缀（如 /api） | 空 |
| `ALLOWED_PLATFORMS` | 允许的平台列表（逗号分隔，空则全开） | bilibili,douyin,xiaohongshu |

前端对接：开发时在 `frontend/.env` 中设置 `VITE_API_BASE_URL=http://localhost:8000`，生产部署时设为实际后端地址（如 `https://api.example.com`）。

**健康检查**：`GET /health` 返回 `{"status":"ok"}`，可用于负载均衡或容器探针。**API 文档**：`/docs`（Swagger）、`/redoc`。

## 测试

```bash
cd video_distribution_tool
pytest tests/ -v
```

## 合规与扩展

- 密钥经 Vault 或加密存储，业务不落盘明文。
- 新增平台：在 `adapter/` 增加新适配器并实现 `BasePlatformAdapter`，在 `config/platform_config/` 增加配置即可。
