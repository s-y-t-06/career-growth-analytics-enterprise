# 项目交接说明

## 当前状态

项目已完成 MVP、Phase 2 建模和 Enterprise 本地全栈系统。当前仓库可以在本地运行数据生成、模型训练、FastAPI 后端和 React 前端。

## 已完成阶段

- Phase 1：数据生成、数据校验、漏斗分析、留存分析、实验分析和规则型 Next Best Action。
- Phase 2：流失标签、特征工程、模型训练、模型评估、可解释性和分群指标。
- Phase 3：FastAPI 后端、SQLite 本地数据库、React 前端、API 文档和架构文档。
- 前端展示优化：Overview、Funnel、Retention、Experiment、Churn Risk 和 User Detail 页面已完成评审友好化。

## 关键命令

```powershell
cd career-growth-analytics-enterprise
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

```powershell
cd career-growth-analytics-enterprise
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```

说明：启动后端前必须先运行 `backend.scripts.init_db` 初始化本地 SQLite 数据库。数据库位于 `data/app/career_growth.db`，仅保存在评审机器本地，不是云端部署。FastAPI 启动时也会检测数据库是否为空，若为空会自动 seed。

```powershell
cd career-growth-analytics-enterprise\frontend
npm install
npm run dev
npm run build
```

## 注意事项

- 不要删除 `data/sample/`、`data/processed/`、`artifacts/` 和 Notebook。
- 训练脚本默认写入 `data/training/`，不覆盖正式样例数据。
- Next Best Action 不能使用真实 label 作为在线推荐依据。
- 临时资源包括 `.pytest_cache`、`__pycache__`、`.ipynb_checkpoints` 和临时训练目录，任务完成后应清理。
