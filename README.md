# 多平台视频分发与数据追踪工具

一套面向内容创作者的**一站式视频分发与数据追踪平台**，内置合规风控能力，支持 B 站、抖音、小红书等多平台统一上传和跨平台数据汇总。

## 架构设计

```
config → core → adapter → service → api → tasks
                    ↑                    ↑
               合规网关              异步队列
           (core/compliance)      (Celery + Redis)
```

**分层职责：**

| 层 | 目录 | 职责 |
|---|---|---|
| 配置层 | `config/` | 环境隔离、安全参数、平台差异化配置 |
| 核心层 | `core/` | 加解密、OAuth2.0、媒体转码、合规引擎 |
| 适配层 | `adapter/` | 平台统一接口，屏蔽各平台 API 差异 |
| 服务层 | `service/` | 账号管理、上传编排、数据追踪业务逻辑 |
| 接口层 | `api/` | FastAPI REST 路由（v1），Swagger 自动文档 |
| 任务层 | `tasks/` | Celery 异步上传、数据抓取、异常告警 |
| 存储层 | `storage/` | PostgreSQL（ORM）、Redis（缓存）、Vault（密钥） |

**关键设计决策：**
- 合规能力统一收口在 `core/compliance`，所有上传/数据操作强制经过审核与限频
- 适配器模式：新增平台只需增加一个 Adapter + 一份平台配置，无需改动服务和接口层
- 双通道架构：支持官方 API 与浏览器自动化（Mock）双路径，通过配置切换

## 支持的平台

| 平台 | 适配器 | 接入方式 | 限频间隔 |
|---|---|---|---|
| B 站 (Bilibili) | `BilibiliAdapter` | 开放 API | 1.0s |
| 抖音 (Douyin) | `DouyinAdapter` | 企业开放 API | 1.5s |
| 小红书 (Xiaohongshu) | `XiaohongshuAdapter` | 官方 API / Mock 双通道 | 2.0s |
| 通用 Mock | `MockAdapter` | 浏览器自动化（Puppeteer） | 可配置 |

## 核心功能

### 🔐 安全合规（P0 最高优先级）
- **敏感词过滤**：上传前对标题和描述进行正则匹配审查，命中则阻断并审计记录
- **操作审计**：所有账号操作、上传、数据拉取全程 JSON 结构化日志，面向 SIEM 集成
- **加密存储**：平台凭证经 AES-256-GCM 加密后入库，明文不落盘
- **请求限频**：按平台独立限流，线程安全，生产环境可切换 Redis 分布式限流
- **Vault 集成**：可选 HashiCorp Vault 作为企业级密钥管理后端

### 📤 视频上传
- 单平台 / 多平台一键分发
- FFmpeg 自动转码（H.264 + AAC），按平台规格缩放分辨率
- 断点续传支持（`resume_meta` 持久化上传状态）
- Celery 异步任务 + 自动重试（最多 3 次，间隔 60s）

### 📊 数据追踪
- 播放量、点赞、评论等指标跨平台汇总
- Redis 缓存（默认 1 小时 TTL），减少重复 API 调用
- 定时数据快照存入 PostgreSQL，支持历史趋势分析
- 异常指标告警（播放骤降、互动异常等）

### 🔑 账号管理
- 多平台账号统一管理，OAuth2.0 授权流程
- 凭证加密存储，列表接口不返回明文
- 活跃状态标记，支持批量查询

## 快速开始

### 环境要求

- Python 3.12+
- PostgreSQL（账号/任务/快照存储）
- Redis（Celery 消息队列 + 数据缓存）
- FFmpeg（视频转码，可选）

### 安装运行

```bash
# 1. 安装依赖
cd video_distribution_tool
pip install -r requirements.txt

# 2. 生成加密密钥（务必妥善保管）
export VIDEO_TOOL_ENCRYPTION_KEY=$(python -c "import os; print(os.urandom(32).hex())")

# 3. 配置数据库与 Redis（按需修改）
export DATABASE_URL=postgresql://user:pass@localhost:5432/video_tool
export REDIS_URL=redis://localhost:6379/0

# 4. 启动 Web 服务（默认 0.0.0.0:8000）
python run_server.py
# 或: uvicorn api.app:app --host 0.0.0.0 --port 8000

# 5. 启动 Celery Worker（另开终端）
celery -A tasks.celery_app worker --loglevel=info
```

### 前端对接

```bash
cd frontend
# 开发环境
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
npm install && npm run dev
# 生产部署时 VITE_API_BASE_URL 设为实际后端地址
```

### API 概览

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/health` | 健康检查 |
| `GET` | `/docs` | Swagger 交互文档 |
| `POST` | `/v1/account/add` | 添加平台账号 |
| `GET` | `/v1/account/list` | 账号列表（可选筛平台） |
| `POST` | `/v1/upload/to-platform` | 上传到单个平台 |
| `POST` | `/v1/upload/to-multiple` | 一键分发多平台 |
| `GET` | `/v1/dashboard/stats` | 跨平台数据看板（含缓存） |

### 运行测试

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

## 环境变量参考

| 变量 | 说明 | 默认值 |
|---|---|---|
| `HOST` | 监听地址 | `0.0.0.0` |
| `PORT` | Web 端口 | `8000` |
| `DATABASE_URL` | PostgreSQL 连接串 | — |
| `REDIS_URL` | Redis 连接串 | — |
| `VIDEO_TOOL_ENCRYPTION_KEY` | AES-256 密钥（64 位 hex） | — |
| `CORS_ORIGINS` | 允许的前端来源（逗号分隔） | `localhost:5173,…` |
| `ALLOWED_PLATFORMS` | 启用的平台（逗号分隔） | `bilibili,douyin,xiaohongshu` |
| `API_PREFIX` | 反向代理路径前缀 | 空 |
| `DEBUG` | 调试模式 | `false` |
| `VAULT_ADDR` | Vault 地址（可选） | — |

## 扩展新平台

```bash
# 1. 新增平台配置
touch config/platform_config/new_platform.py

# 2. 实现平台适配器
touch adapter/new_platform_adapter.py  # 继承 BasePlatformAdapter

# 3. 注册到工厂函数
# 编辑 service/account_service.py → get_adapter_for_platform()

# 无需修改 API、Service、Task 层代码
```

## 项目结构

```
video_distribution_tool/
├── config/                     # 配置层
│   ├── base.py                 # 全局配置（环境变量读取）
│   ├── security.py             # 加密/限频/Vault 配置
│   └── platform_config/        # 各平台参数
│       ├── bilibili.py
│       ├── douyin.py
│       └── xiaohongshu.py
├── core/                       # 核心能力（与业务解耦）
│   ├── auth/oauth_flow.py      # OAuth2.0 授权流程
│   ├── compliance/             # 合规引擎
│   │   ├── audit.py            # 审计日志
│   │   ├── rate_limit.py       # 请求限频
│   │   └── sensitive.py        # 敏感词过滤
│   ├── encryption/crypto.py    # AES-256-GCM 加解密
│   └── media_process/transcode.py  # FFmpeg 转码
├── adapter/                    # 平台适配层
│   ├── base_adapter.py         # 抽象基类 + 数据结构
│   ├── bilibili_adapter.py
│   ├── douyin_adapter.py
│   ├── xiaohongshu_adapter.py
│   └── mock_adapter.py         # 浏览器自动化适配器
├── service/                    # 业务服务层
│   ├── account_service.py      # 账号管理
│   ├── upload_service.py       # 上传编排
│   └── data_tracking.py        # 数据追踪
├── api/                        # 接口层
│   ├── app.py                  # FastAPI 应用入口
│   └── v1/
│       ├── account.py          # 账号接口
│       ├── upload.py           # 上传接口
│       ├── dashboard.py        # 数据看板接口
│       └── schemas.py          # Pydantic 请求/响应模型
├── tasks/                      # 异步任务层
│   ├── celery_app.py           # Celery 应用配置
│   ├── upload_task.py          # 上传任务（含重试）
│   ├── data_fetch_task.py      # 数据抓取任务
│   └── alert_task.py           # 异常告警任务
├── storage/                    # 存储层
│   ├── db/
│   │   ├── models.py           # SQLAlchemy ORM 模型
│   │   └── session.py          # 数据库连接管理
│   ├── cache/redis_client.py   # Redis 缓存工具
│   └── vault_client.py         # Vault 密钥管理
├── frontend/                   # 前端（Vite 骨架）
│   ├── src/api/index.js        # API 客户端
│   └── src/utils/format.js     # 格式化工具
├── tests/                      # 测试
│   ├── test_compliance.py      # 合规测试
│   ├── test_platform_adapter.py # 适配器测试
│   └── test_upload_service.py  # 上传服务测试
├── docs/                       # 文档
│   └── 优化目标与验收标准.md
├── requirements.txt
├── run_server.py
└── README.md
```
