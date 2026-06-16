# Phase 2 收尾：训练数据目录隔离

## 会话信息

- **日期**：2026-06-16
- **项目阶段**：Phase 2 流失预测建模
- **任务类型**：阻塞问题修复（不进入 Phase 3）
- **执行环境**：Windows PowerShell
- **真实基础 Python**：`C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe`
- **项目虚拟环境**：`C:\Users\Administrator\Desktop\career-growth-analytics\.venv\Scripts\python.exe`
- **提交 hash**：`bf08265 fix: isolate 5,000-user training data from committed sample data`

## 问题描述

Codex Phase 2 核心验收已 56/56 tests passed、5,000 用户训练成功、Notebook 执行成功、ASCII scan clean、artifacts 存在。

唯一阻塞问题：运行

```powershell
.venv\Scripts\python.exe scripts\train_churn_model.py --count 5000 --seed 42
```

默认会把生成的 5,000 用户数据写入 `data/sample/` 和 `data/processed/labels.csv`，覆盖仓库正式提交的 1,000 用户 sample 数据。

## 整改内容

1. **修改 `scripts/train_churn_model.py`**
   - `--data-dir` 默认值从 `"data"` 改为 `"data/training"`。
   - 更新 help 文本，说明默认训练目录不会覆盖正式 sample 数据。
   - `parse_args()` 增加可选 `argv` 参数，便于单元测试注入空参数列表。

2. **修改 `src/career_growth/features/model_features.py`**
   - `save_model_features` 默认输出路径从 `data/processed/model_features.csv` 改为 `data/training/processed/model_features.csv`，与训练脚本默认目录一致。

3. **更新 `.gitignore`**
   - 新增 `data/training/` 忽略规则，并补充说明。

4. **移除污染文件**
   - 删除已提交的 `data/processed/model_features.csv`（该文件实际为 5,000 用户训练输出，不属于 1,000 用户 sample 数据）。
   - 今后训练生成的 `model_features.csv` 统一写入 `data/training/processed/model_features.csv`。

5. **新增测试 `tests/test_train_script.py`**
   - `test_default_data_dir_is_training`：验证训练脚本默认数据目录为 `data/training`。
   - `test_training_script_respects_data_dir_and_does_not_touch_sample`：以子进程运行训练脚本（200 用户），验证生成数据只写入配置的 `data-dir`，且 `data/sample/users.csv` 与 `data/processed/labels.csv` 内容保持不变。

6. **更新文档**
   - `README.md`：训练命令说明中明确训练数据写入 `data/training/`，`model_features.csv` 路径更新为 `data/training/processed/model_features.csv`。
   - `PHASE2_MODELING_REPORT.md`：第 7 节 Artifacts 说明更新。
   - `HANDOVER.md`：数据状态与关键文件清单更新。

## 复验命令与结果

### Full tests

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m pytest tests -q
```

结果：

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\Administrator\Desktop\career-growth-analytics
configfile: pyproject.toml
plugins: anyio-4.13.0, cov-7.1.0
collected 58 items

tests\test_analytics.py ...........
tests\test_data_generation.py .........
tests\test_decisions.py ..
tests\test_features.py ...
tests\test_model_features.py ........
tests\test_modeling.py ...............
tests\test_nba_integration.py ....
tests\test_train_script.py ..
tests\test_validation.py ....

======================= 58 passed in 351.85s (0:05:51) ========================
```

### 5,000 用户训练

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts\train_churn_model.py --count 5000 --seed 42
```

结果：

```text
Generating 5000 users with seed 42
Building pre-cutoff features and attaching labels...
Model matrix shape: (5000, 40)
Churn rate: 34.94%
Train/Val/Test sizes: 3000 / 1000 / 1000
Selected model: logistic_regression
Validation metrics: {'pr_auc': 0.5514720158953248, ...}
Test metrics: {'pr_auc': 0.5370783543026523, ...}
Saved model to artifacts\churn_model.joblib
Saved plots to artifacts\plots
Training complete.
```

训练指标与整改前完全一致：

| Metric | Value |
|---|---|
| PR-AUC | 0.5371 |
| ROC-AUC | 0.6942 |
| Brier score | 0.2227 |
| F1 score | 0.5884 |
| Threshold | 0.41 |

### 数据隔离验证

```text
sample users: 1000
training users: 5000
sample labels: 1000
training labels: 5000
```

- `data/sample/users.csv` 仍为 1,000 用户。
- `data/processed/labels.csv` 仍为 1,000 用户。
- 5,000 用户训练数据仅写入 `data/training/sample/` 与 `data/training/processed/`。

### ASCII scan

已确认 `src/`、`tests/`、`scripts/` 下 Python 文件无非 ASCII 字符。

### git status

训练后工作目录仅包含预期变更：

- 修改：`.gitignore`、`HANDOVER.md`、`PHASE2_MODELING_REPORT.md`、`README.md`、`scripts/train_churn_model.py`、`src/career_growth/features/model_features.py`
- 修改：`artifacts/churn_model.joblib`、`artifacts/model_metadata.json`（时间戳更新）
- 删除：`data/processed/model_features.csv`
- 新增：`tests/test_train_script.py`

`data/training/` 已被 `.gitignore` 忽略，未出现在 git status 中。

## 临时资源清理

已清理：

- `.pytest_cache`
- 全部 `__pycache__`
- `.ipynb_checkpoints`（不存在）

保留：

- `.venv/`
- `data/sample/` 与 `data/processed/labels.csv`（正式 1,000 用户 sample 数据）
- `data/training/`（本地 5,000 用户训练数据，被 git 忽略）
- `artifacts/` 正式产物
- 文档与 Notebook

## 未完成事项

- 未开始 API、数据库、前端或 Phase 3。
- 等待 Codex 最终确认本阻塞问题已解决。
