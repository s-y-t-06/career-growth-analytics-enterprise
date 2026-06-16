# Worklog: Phase 2 Wrap-Up - Training Data Directory Isolation

## Session Information

- **Date**: 2026-06-16
- **Project phase**: Phase 2 churn prediction modeling
- **Task type**: Blocker fix (do not enter Phase 3)
- **Execution environment**: Windows PowerShell
- **Real base Python**: `C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe`
- **Project virtual environment**: `C:\Users\Administrator\Desktop\career-growth-analytics\.venv\Scripts\python.exe`
- **Commit hash**: `bf08265 fix: isolate 5,000-user training data from committed sample data`

## Problem Description

Codex Phase 2 core acceptance had already passed: 56/56 tests passed, 5,000-user training succeeded, notebook executed successfully, ASCII scan clean, artifacts present.

The only blocker: running

```powershell
.venv\Scripts\python.exe scripts\train_churn_model.py --count 5000 --seed 42
```

wrote the generated 5,000-user data into `data/sample/` and `data/processed/labels.csv`, overwriting the committed 1,000-user sample data.

## Remediation Content

1. **Modify `scripts/train_churn_model.py`**
   - Changed `--data-dir` default from `"data"` to `"data/training"`.
   - Updated help text to explain that the default training directory does not overwrite committed sample data.
   - Added optional `argv` parameter to `parse_args()` so unit tests can inject an empty argument list.

2. **Modify `src/career_growth/features/model_features.py`**
   - Changed `save_model_features` default output path from `data/processed/model_features.csv` to `data/training/processed/model_features.csv`, matching the training script default directory.

3. **Update `.gitignore`**
   - Added `data/training/` ignore rule with explanation.

4. **Remove Contaminated File**
   - Deleted the committed `data/processed/model_features.csv` (it was actually a 5,000-user training output and did not belong to the 1,000-user sample data).
   - Future `model_features.csv` outputs are written uniformly to `data/training/processed/model_features.csv`.

5. **Add Test `tests/test_train_script.py`**
   - `test_default_data_dir_is_training`: verifies the training script default data directory is `data/training`.
   - `test_training_script_respects_data_dir_and_does_not_touch_sample`: runs the training script as a subprocess with 200 users, verifies generated data is written only to the configured `data-dir`, and verifies that `data/sample/users.csv` and `data/processed/labels.csv` remain unchanged.

6. **Update Documentation**
   - `README.md`: training command description now states training data is written to `data/training/`; `model_features.csv` path updated to `data/training/processed/model_features.csv`.
   - `PHASE2_MODELING_REPORT.md`: section 7 artifact description updated.
   - `HANDOVER.md`: data state and key file inventory updated.

## Re-verification Commands and Results

### Full Tests

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m pytest tests -q
```

Result:

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
tests\test_model_features.py .......
tests\test_modeling.py ............
tests\test_nba_integration.py ....
tests\test_train_script.py ..
tests\test_validation.py ....

======================= 58 passed in 351.85s (0:05:51) ========================
```

### 5,000-User Training

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts\train_churn_model.py --count 5000 --seed 42
```

Result:

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

Training metrics are identical to before the fix:

| Metric | Value |
|---|---|
| PR-AUC | 0.5371 |
| ROC-AUC | 0.6942 |
| Brier score | 0.2227 |
| F1 score | 0.5884 |
| Threshold | 0.41 |

### Data Isolation Verification

```text
sample users: 1000
training users: 5000
sample labels: 1000
training labels: 5000
```

- `data/sample/users.csv` remains 1,000 users.
- `data/processed/labels.csv` remains 1,000 users.
- 5,000-user training data is written only to `data/training/sample/` and `data/training/processed/`.

### ASCII Scan

Confirmed that Python files under `src/`, `tests/`, and `scripts/` contain no non-ASCII characters.

### Git Status

After training, the working directory contained only expected changes:

- Modified: `.gitignore`, `HANDOVER.md`, `PHASE2_MODELING_REPORT.md`, `README.md`, `scripts/train_churn_model.py`, `src/career_growth/features/model_features.py`
- Modified: `artifacts/churn_model.joblib`, `artifacts/model_metadata.json` (timestamp updated)
- Deleted: `data/processed/model_features.csv`
- Added: `tests/test_train_script.py`

`data/training/` is ignored by `.gitignore` and does not appear in `git status`.

## Temporary Resource Cleanup

Cleaned:

- `.pytest_cache`
- All `__pycache__` directories
- `.ipynb_checkpoints` (did not exist)

Retained:

- `.venv/`
- `data/sample/` and `data/processed/labels.csv` (committed 1,000-user sample data)
- `data/training/` (local 5,000-user training data, ignored by git)
- `artifacts/` formal deliverables
- Documentation and notebooks

## Open Items

- API, database, frontend, and Phase 3 were not started.
- Waiting for Codex final confirmation that this blocker is resolved.
