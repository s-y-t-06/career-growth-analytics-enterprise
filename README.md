# 职业成长分析与实验优化系统

本仓库是 Deepmanifold Take-home Challenge 的 Enterprise-level 版本，基于一个 AI 职业规划与岗位推荐产品，构建本地可运行的增长分析系统。系统包含 MVP 数据科学流程、流失预测模型、FastAPI 后端、SQLite 数据层和 React 前端，用于展示从数据生成到业务看板的完整闭环。

## 项目范围

- 模拟用户、事件、实验分组和干预记录。
- 校验数据质量并计算增长漏斗、cohort 留存和 A/B 实验指标。
- 构造无标签泄漏的流失预测特征。
- 训练并评估 Logistic Regression 与 HistGradientBoostingClassifier。
- 输出模型指标、分群风险和 Next Best Action 推荐。
- 提供 FastAPI API，供前端页面调用。
- 使用 SQLite 作为本地数据层，便于评审一键初始化。
- 使用 React + Vite + TypeScript + Recharts 构建可交互看板。

## 业务背景

模拟产品服务大学生和早期职业用户，帮助他们完成职业探索、简历上传、岗位推荐、成长任务和职业报告生成。系统目标是帮助增长团队理解用户生命周期表现，发现激活漏斗流失点，评估 onboarding 实验效果，识别高流失风险用户，并给出下一步干预建议。

核心路径：

```text
signup
-> onboarding_complete
-> profile_complete
-> resume_upload
-> job_recommendation_view
-> job_save
-> growth_task_complete
-> career_report_generate
-> retained / churned
```

## 目录结构

```text
career-growth-analytics/
|-- backend/                   # FastAPI 后端
|   |-- app/
|   |   |-- main.py            # API 入口
|   |   |-- routers/           # 路由层
|   |   |-- services/          # 业务服务层
|   |   |-- database.py        # SQLite 工具
|   |   `-- schemas.py         # Pydantic schema
|   |-- scripts/init_db.py     # 初始化本地数据库
|   `-- tests/                 # 后端测试
|-- data/
|   |-- sample/                # 样例 CSV 数据
|   |-- processed/             # 标签等派生结果
|   |-- app/                   # 本地 SQLite 数据库
|   `-- training/              # 本地训练数据，已 git ignore
|-- docs/                      # 架构、API、方法和模型说明
|-- frontend/                  # React 前端
|-- notebooks/                 # MVP 和建模 Notebook
|-- scripts/                   # 数据生成、分析和训练脚本
|-- src/career_growth/         # MVP 核心分析包
|-- tests/                     # MVP 测试
|-- pyproject.toml
|-- README.md
`-- LICENSE
```

## 技术栈

- Python 3.10+
- pandas、numpy、scikit-learn、scipy
- FastAPI、Pydantic、SQLite
- pytest、Jupyter
- React、Vite、TypeScript、Recharts

## 本地启动

安装 Python 依赖：

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

初始化后端数据库并启动 API：

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```

启动前端：

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics\frontend
npm install
npm run dev
```

访问地址：

- 前端页面：http://localhost:5173
- 后端文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 主要页面

- Overview：展示用户量、事件量、流失率、D7 留存和模型指标。
- Funnel：展示核心激活漏斗和每一步 drop-off。
- Retention：展示 cohort 留存矩阵。
- Experiment：展示 onboarding A/B 实验结果和 SRM 检查。
- Churn Risk：展示模型指标、风险分布和分群风险。
- User Detail：展示单用户画像、风险因素和 Next Best Action。

## 验证命令

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m pytest tests backend\tests -q
cd frontend
npm run build
```

## 模型结果

5,000 用户训练数据上的最终模型为 Logistic Regression：

| 指标 | Test Set |
| --- | ---: |
| PR-AUC | 0.5371 |
| ROC-AUC | 0.6942 |
| Brier Score | 0.2227 |
| F1 | 0.5884 |
| Threshold | 0.41 |

## 工程说明

本项目不使用云端部署。数据由本地脚本生成，SQLite 由初始化脚本构建，前后端均可在本地运行。Kafka、Redis、PostgreSQL、Flink 等组件没有被强行加入，因为当前业务展示不需要这些复杂依赖。
