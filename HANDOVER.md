# 交接报告：Career Growth Analytics Phase 1 整改

> 本报告用于会话重启后下一任 AI 快速接手。请优先阅读本文件，再阅读 `PHASE1_REMEDIATION_REPORT.md`。
> 新增永久协作约束：每次新会话必须独立阅读 HANDOVER.md、任务书/验收要求、最近阶段报告、README.md、git status 和最近 5 条 commit；工作结束前必须更新 HANDOVER.md 并写入 `docs/worklogs/`。

## 1. 项目基本信息

- **MVP 仓库**：`C:\Users\Administrator\Desktop\career-growth-analytics`
- **项目名**：Career Growth Analytics
- **业务场景**：AI Career Platform 用户生命周期增长与实验优化系统
- **当前阶段**：Phase 2 流失预测与模型评估已完成
- **严格约束**：**不得开始 API、数据库、前端开发或 Enterprise 系统**，必须等 Codex 审批
- **合规要求**：不得使用任何 lychas 相关代码、数据或命名

## 2. 当前 git 状态

`	ext
b32666a feat: Phase 2 churn prediction with LR baseline and HistGradientBoosting
`

工作目录干净，无未提交修改。

## 3. 已完成的整改内容（Phase 1 Remediation）

整改报告已写入 `PHASE1_REMEDIATION_REPORT.md`，核心结果如下：

| 整改项 | 状态 | 关键文件 |
|---|---|---|
| 移除 `uuid.uuid4()`，全量确定性 ID | 完成 | `src/career_growth/data_generation/events.py`, `interventions.py` |
| Reproducibility 测试增强 | 完成 | `tests/test_data_generation.py` |
| Cohort retention 时区与一致性修复 | 完成 | `src/career_growth/analytics/retention.py`, `tests/test_analytics.py` |
| SRM 改用 `chisquare(observed, f_exp=expected)` | 完成 | `src/career_growth/analytics/experiments.py`, `tests/test_analytics.py` |
| 干预逻辑基于 churn label | 完成 | `src/career_growth/data_generation/interventions.py`, `generator.py` |
| Onboarding treatment 机制重构与校准 | 完成 | `src/career_growth/data_generation/events.py`, `config.py` |
| 仓库清理与 sample 数据缩小 | 完成 | `data/sample/*` 现为 1,000 用户，`.gitignore` 已完善 |
| 文档规范（README、pyproject、methodology） | 完成 | `README.md`, `pyproject.toml`, `docs/methodology.md` |
| Notebook 可执行 | 完成 | `notebooks/lifecycle_analysis.ipynb` |
| 验收报告 | 完成 | `PHASE1_REMEDIATION_REPORT.md` |
| 本地 .venv 环境可用，命令可复验 | 完成 | `.venv/`（已加入 `.gitignore`），`README.md` 已更新 |
| 源码/脚本/测试注释恢复专业英文 | 完成 | 全部 24 个 Python 文件；非 ASCII 扫描结果为 0 |

### 当前关键校准参数

在 `src/career_growth/config.py` 中：

```python
ONBOARDING_VARIANTS = [
    {"variant_id": "control",    "allocation": 0.40, "effect": 0.0},
    {"variant_id": "personalized", "allocation": 0.30, "effect": 0.30},
    {"variant_id": "simplified",  "allocation": 0.30, "effect": 0.15},
]
```

在 `src/career_growth/data_generation/events.py` 中：

- `direct_effect` 仅作用于 `onboarding_start` 和 `onboarding_complete`
- `profile_complete` 的 `onboarding_complete` state bonus 为 `0.25`
- 第一周每日活跃概率：`0.01 + 0.50 * engagement_score + 0.05 * onboarding_complete`
- 后期每日活跃概率：`0.001 + 0.08 * engagement_score + 0.015 * num_core_actions`

### 当前 Python 环境

- 真实基础解释器：`C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe`（通过 `uv` 安装的 CPython 3.11.15）
- 项目虚拟环境解释器：`.venv\Scripts\python.exe`
- 解释器版本：Python 3.11.15
- 依赖安装方式：`.venv\Scripts\python.exe -m pip install -e ".[dev]"`
- 注意：Windows Store 的 `python.exe` 路径（`C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\...`）是 0 字节重定向器，无法在新终端直接按绝对路径调用；因此必须使用真实 CPython 创建 `.venv`。

### 当前测试状态

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m pytest tests -q
```

结果（Phase 1 + Phase 2 共 47 项）：

`	ext
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\Administrator\Desktop\career-growth-analytics
configfile: pyproject.toml
testpaths: tests
collected 47 items

tests\test_analytics.py .........
tests\test_data_generation.py ........
tests\test_decisions.py ..
tests\test_features.py ...
tests\test_model_features.py ........
tests\test_modeling.py ...............
tests\test_nba_integration.py ....
tests\test_validation.py ....

============================= 47 passed =============================
`

### 当前数据状态

- 仓库提交的 sample 数据为 **1,000 用户**，位于 `data/sample/` 和 `data/processed/`
- 完整 **5,000 用户** 数据需本地重新生成：
  ```powershell
  $env:PYTHONPATH = "src"
  .venv\Scripts\python.exe scripts/generate_data.py --count 5000 --seed 42
  ```

### 最新全量 5,000 用户指标（供参考）

- Users: 5,000 / Events: 88,975 / Churn rate: 34.94%
- D1 / D7 / D14 retention: 63.16% / 46.58% / 8.52%
- SRM p-value: 0.6677
- Onboarding: personalized +30.0% (p=4.44e-10)，simplified +12.9% (p=0.006)
- Profile: personalized +25.5% (p=4.73e-08)，simplified +9.4% (p=0.041)
- D7 retention: personalized +6.8% (p=0.079)，simplified +9.8% (p=0.010)
- Interventions: win-back 413 条，全部发给 churned 用户

## 4. Codex 原始约束（必须继续遵守）

以下内容来自 Codex 对 Phase 1 整改的要求，下一任 AI 必须继续遵守：

### 4.1 范围约束

- **当前仍处于 Phase 1 整改阶段，暂时不要开发 Phase 2。**
- 不得开始模型训练、API、数据库或前端开发。
- 整改完成后停止，等待 Codex 复验。

### 4.2 修复确定性

1. 清除数据生成流程中的 `uuid.uuid4()`。
2. `session_id`、`job_id`、`message_id` 等必须由 seed、user_id、时间或业务序号确定性生成。
3. 扩充 reproducibility 测试：相同 seed 两次生成的全部 CSV 内容应完全一致；应比较文件哈希或完整 DataFrame。

### 4.3 修复留存分析

1. 检查 `compute_cohort_retention` 中 `event_date` 和 `signup_date` 的时区。
2. 保证两者使用一致的日期类型。
3. 增加测试证明 cohort retention 不是全 0。
4. 检查 cohort 汇总结果与整体 D1、D7、D14 留存是否具有合理一致性。
5. 支持或清楚展示按 experiment variant 分组的留存结果。

### 4.4 修复实验统计

1. SRM 使用 `scipy.stats.chisquare(observed, f_exp=expected)` 或统计意义等价的一元卡方拟合优度检验。
2. 不要使用 `chi2_contingency([observed, expected])`。
3. 增加与 scipy 标准结果直接对比的单元测试。
4. 检查实验报告中 SRM p-value 是否随修复更新。

### 4.5 修复干预数据逻辑

1. `win-back` 不能仅使用 `last_action <= label_end` 判断流失。
2. 流失定义应与标签一致：注册后第 8 至 21 天没有 `user_action` 才算 churn。
3. 不得向 retained 用户错误发送 win-back。
4. 增加 retained/churned 用户干预目标测试。
5. 干预记录也必须可复现。

### 4.6 提高实验数据真实性

1. onboarding 实验不应以相同 effect 直接提高全部下游事件概率。
2. treatment 应主要直接影响 `onboarding_complete` 或早期引导行为。
3. profile、resume、job save、career report 和 retention 的提升应主要通过用户状态和漏斗传导产生。
4. 重新校准效果，使实验结果具有统计显著性但不过度夸张。
5. 在文档中说明这是 synthetic causal mechanism，不是现实业务结论。

### 4.7 数据和仓库清理

1. 测试统一使用 `pytest tmp_path`，不在项目根目录遗留 `data_test_*`。
2. 删除现有 `data_test_a`、`data_test_b`、`data_test_dup`、`data_test_orphan`、`data_test_shared`、`data_test_source` 等临时目录。
3. GitHub sample data 建议缩小到约 500 至 1000 用户。
4. 完整 5000 用户数据继续由生成脚本本地生成。
5. 清理 pytest cache 和不应提交的生成产物，并完善 `.gitignore`。

### 4.8 文档规范

1. 删除或替换虚构的 `github.com/deepmanifold/...` 仓库地址。
2. `pyproject.toml` 不要以 Deepmanifold Candidate 冒充项目作者或公司官方项目。
3. 作者可使用 Su Yutong，或暂时不填写。
4. 将 README 中装饰性 Unicode 箭头、长破折号等替换为正式 ASCII 表达。
5. README 必须准确说明安装、数据生成、测试和 Notebook 运行方式。

### 4.9 运行环境与验收

1. 提供实际运行测试时的 Python executable 路径。
2. 确保新环境可根据 README 从零安装并运行。
3. 执行完整测试。
4. 重新运行数据生成、验证、分析和 Notebook。
5. 不要只汇报“测试通过”，需要提供命令和关键输出。
6. 整改完成后提交 `PHASE1_REMEDIATION_REPORT.md`。

### 4.10 临时资源清理约束

每次任务完成、测试结束或阶段交付前，必须：

1. 停止本任务启动的后台进程、开发服务器和容器。
2. 删除临时测试目录、渲染文件、缓存及中间产物。
3. 清理 pytest、Python、Notebook 和构建缓存。
4. 不得删除源码、正式文档、必要样例数据、验收报告及用户原有文件。
5. 清理前确认目标路径属于项目目录或明确的临时目录。
6. 在阶段报告中列出已释放的临时资源。
7. 若某项资源必须保留，说明用途、路径和保留原因。

完成资源清理后才能声明任务完成。

## 5. 关键命令速查

```powershell
# 进入项目目录
cd C:\Users\Administrator\Desktop\career-growth-analytics

# 创建并激活本地虚拟环境（首次；需预先安装 CPython 3.11）
py -3.11 -m venv .venv
.venv\Scripts\activate

# 安装依赖（每次 pyproject.toml 变更后）
.venv\Scripts\python.exe -m pip install -e ".[dev]"

# 设置 PYTHONPATH（Windows PowerShell）
$env:PYTHONPATH = "src"

# 生成 sample 数据（1000 用户）
.venv\Scripts\python.exe scripts/generate_data.py --count 1000 --seed 42

# 生成完整数据（5000 用户）
.venv\Scripts\python.exe scripts/generate_data.py --count 5000 --seed 42

# 运行完整分析
.venv\Scripts\python.exe scripts/run_analysis.py

# 打印摘要
.venv\Scripts\python.exe scripts/compute_summary.py

# 运行测试
.venv\Scripts\python.exe -m pytest tests -q

# 重建并执行 Notebook
.venv\Scripts\python.exe scripts/build_notebook.py
.venv\Scripts\python.exe -m nbconvert --execute --to notebook --inplace notebooks/lifecycle_analysis.ipynb
```

## 6. 关键文件清单

| 类别 | 文件 |
|---|---|
| 数据生成 | `src/career_growth/data_generation/events.py`, `generator.py`, `interventions.py`, `users.py`, `experiments.py` |
| 配置 | `src/career_growth/config.py` |
| Schema | `src/career_growth/schemas.py` |
| 标签 | `src/career_growth/features/labels.py` |
| 特征工程 | `src/career_growth/features/model_features.py` |
| 校验 | `src/career_growth/validation/validator.py` |
| 分析 | `src/career_growth/analytics/funnel.py`, `retention.py`, `experiments.py` |
| 建模 | `src/career_growth/modeling/split.py`, `pipeline.py`, `evaluate.py`, `explain.py`, `train.py` |
| 决策 | `src/career_growth/decisions/next_best_action.py` |
| 测试 | `tests/test_data_generation.py`, `test_validation.py`, `test_analytics.py`, `test_features.py`, `test_decisions.py`, `test_model_features.py`, `test_modeling.py`, `test_nba_integration.py`, `tests/conftest.py` |
| 脚本 | `scripts/generate_data.py`, `run_analysis.py`, `compute_summary.py`, `build_notebook.py`, `train_churn_model.py` |
| 文档 | `README.md`, `docs/data_schema.md`, `docs/methodology.md`, `docs/model_card.md`, `pyproject.toml`, `.gitignore` |
| 产物 | `artifacts/churn_model.joblib`, `model_metadata.json`, `metrics.json`, `feature_schema.json`, `explainability.json`, `user_explanations.json`, `subgroup_metrics.*`, `nba_examples.*`, `plots/*.png` |
| 验收 | `PHASE1_REMEDIATION_REPORT.md`, `PHASE2_MODELING_REPORT.md`, `HANDOVER.md`（本文件） |

## 7. 尚未解决的风险

- D7 retention 的 personalized 变体在 5,000 用户下 p=0.079，未达传统 0.05 显著性；这是合成数据的特性，不影响整改通过，但后续若需更显著结果可进一步校准。
- 1,000 用户的 sample 数据由于样本量小，部分指标 p 值不显著；完整 5,000 用户分析更稳定。
- 尚未开始 Phase 2；后续进入 Phase 2 前必须获得 Codex 明确批准。
- 依赖安装过程中网络较慢，若在新环境安装失败可多试几次或使用 `uv pip install`。

## 8. 下一步建议

1. 等待 Codex 对 Phase 2 进行最终验收。
2. 若 Codex 批准，则开始 Phase 3：Enterprise API 设计与实现、数据库存储、前端展示或生产部署准备。
3. 若 Codex 提出新整改要求，继续按上述约束执行。

---

## 附录：本次会话工作记录摘要

- **会话时间**：2026-06-15
- **本次任务**：修复 `.venv` 指向 Windows Store alias 的问题；安装真实 CPython 3.11.15 并重新创建 `.venv`；将源码/脚本/测试注释恢复为专业英文；执行非 ASCII 扫描；用 `.venv` 重新运行 29 项测试、1,000 用户数据生成、`run_analysis.py`、`compute_summary.py`；更新 README/HANDOVER/整改报告；清理临时资源；提交修改。
- **详细工作日志**：见 `docs/worklogs/2026-06-15_phase1_final-remediation.md`
