# Phase 3 Enterprise 系统报告

## 目标

Phase 3 将 MVP 数据科学项目扩展为本地可运行的企业级系统，使评审可以通过 API 和前端页面理解业务指标、模型结果和推荐逻辑。

## 后端

- 使用 FastAPI 构建 API 服务。
- 使用 SQLite 作为本地数据层。
- 路由覆盖 health、overview、funnel、retention、experiment、model、users 和 nba。
- service 层复用 MVP 分析包和模型 artifacts。
- 后端测试覆盖核心 API。

## 前端

- 使用 React + Vite + TypeScript。
- 页面覆盖 Overview、Funnel、Retention、Experiment、Churn Risk 和 User Detail。
- 图表使用 Recharts。
- 所有展示数据来自 FastAPI，不使用硬编码假结果。

## 本地运行

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

## 设计取舍

项目没有强行加入 Kafka、Redis、PostgreSQL 或 Flink。当前场景重点是本地复现和评审展示，SQLite 已足够支撑样例数据查询和前端看板。
