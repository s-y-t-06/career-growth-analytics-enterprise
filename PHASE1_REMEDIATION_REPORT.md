# Phase 1 Remediation Report

## 1. Python executable

```text
C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe
```

## 2. Modified files

### Source code
- `src/career_growth/config.py`
- `src/career_growth/data_generation/events.py`
- `src/career_growth/data_generation/generator.py`
- `src/career_growth/data_generation/interventions.py`
- `src/career_growth/analytics/retention.py`
- `src/career_growth/analytics/experiments.py`

### Tests
- `tests/conftest.py`
- `tests/test_data_generation.py`
- `tests/test_validation.py`
- `tests/test_analytics.py`

### Scripts
- `scripts/build_notebook.py`
- `scripts/capture_full_stats.py` (temporary helper, removed after report generation)

### Documentation
- `README.md`
- `docs/methodology.md`
- `pyproject.toml`
- `.gitignore`

### Sample data
- `data/sample/users.csv` (1,000 users)
- `data/sample/events.csv`
- `data/sample/experiment_assignments.csv`
- `data/sample/interventions.csv`
- `data/sample/metadata.json`
- `data/processed/labels.csv`

### Notebook
- `notebooks/lifecycle_analysis.ipynb` (rebuilt and re-executed)

## 3. Remediation details

### 3.1 Determinism and reproducibility
- Removed all `uuid.uuid4()` calls from the data pipeline.
- `event_id` and `session_id` continue to be generated with `uuid.uuid5` from `(seed, user_id, counter)`.
- `job_id` is now generated deterministically from `(seed, user_id, job_counter)` instead of `uuid.uuid4()`.
- `message_id` in interventions is now generated deterministically from `(seed, user_id, counter)`.
- Late-phase sessions (days 8-21) now reuse the same deterministic `next_session_id()` helper instead of `uuid.uuid4()`.
- `test_generation_reproducibility` was expanded to compare MD5 hashes of every generated CSV file between two runs with the same seed, and to assert full DataFrame equality for `users.csv`.

### 3.2 Retention analytics
- Added `_normalize_date()` helper in `retention.py` to strip timezone and floor both `event_timestamp` and `signup_timestamp` to calendar days before comparison.
- `compute_cohort_retention` now uses the same date normalization as `compute_day_retention`, eliminating the prior timezone mismatch warning.
- Added `compute_retention_by_variant()` to support retention analysis grouped by experiment variant.
- Added tests that prove cohort retention is not all-zero and that the cohort-weighted average matches the overall day-retention rate.

### 3.3 Experiment statistics
- Replaced `scipy.stats.chi2_contingency([observed, expected])` with `scipy.stats.chisquare(observed, f_exp=expected)` in `analytics/experiments.py`.
- Added `test_experiment_srm_matches_scipy`, which verifies the reported SRM p-value equals the result from `scipy.stats.chisquare` directly.
- The validator already used `chisquare`, so it remains consistent with the analytics module.

### 3.4 Intervention logic
- `generate_interventions` now accepts the churn `labels` DataFrame and uses `is_churned` to decide win-back eligibility.
- Win-back campaigns are sent only to churned users, after the label window ends (`label_end + 1 day`).
- Retained users can still receive incomplete-onboarding or low-engagement prompts, but never win-back.
- Added `test_intervention_win_back_targets_churned` and `test_intervention_reproducibility`.

### 3.5 Experiment realism
- The onboarding treatment effect is now applied only to `onboarding_start` and `onboarding_complete`.
- No direct treatment effect is added to `profile_complete`, `resume_upload`, `job_save`, `career_report_generate`, or late-phase retention.
- Downstream lifts emerge from state bonuses and from the higher activity associated with completing onboarding.
- Variant effects were recalibrated to `control=0.0`, `personalized=0.30`, `simplified=0.15`. This produces statistically significant but bounded effects.
- `docs/methodology.md` now explicitly describes the synthetic causal mechanism and states that the results are for pipeline demonstration, not real business conclusions.

### 3.6 Data and repository cleanup
- All `data_test_*` directories were removed.
- The sample dataset committed to the repository was reduced from 5,000 to 1,000 users.
- The full 5,000-user dataset continues to be generated locally via `python scripts/generate_data.py --count 5000 --seed 42`.
- Tests now use `pytest tmp_path` and `tmp_path_factory` fixtures; no temporary data directories are left in the project root after tests finish.
- `.gitignore` was extended to exclude `.mypy_cache/`, `.ruff_cache/`, `.coverage.*`, `data_tmp_grid/`, and similar artifacts.
- `__pycache__`, `.ipynb_checkpoints`, and `.pytest_cache` were removed.

### 3.7 Documentation cleanup
- Removed the fictional `github.com/deepmanifold/...` URLs from `pyproject.toml`.
- Set package author to `Su Yutong` in `pyproject.toml`.
- Replaced decorative Unicode arrows and em-dashes in `README.md` with ASCII equivalents (`->`, `--`).
- Updated `README.md` commands to explicitly set `PYTHONPATH="src"` on Windows and to cover data generation, analytics, tests, and notebook execution.
- Updated `docs/methodology.md` to reflect the new treatment-effect mechanism and to add the synthetic-data disclaimer.

## 4. Verification commands and results

### 4.1 Install and generate data

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
python scripts/generate_data.py --count 1000 --seed 42
```

Output:

```text
Generated 1000 users and 17856 events.
Churn rate: 39.00%
```

### 4.2 Run analytics

```powershell
$env:PYTHONPATH = "src"
python scripts/run_analysis.py
```

Validation passed: `True`.

Sample data metrics:

- Users: 1,000
- Events: 17,856
- Churn rate: 39.00%
- D1 retention: 67.40%
- D7 retention: 46.70%
- D14 retention: 7.90%
- D7 rolling retention: 76.30%
- SRM p-value: 0.3253

### 4.3 Run tests

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests -q
```

Output:

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-6.0
rootdir: C:\Users\Administrator\Desktop\career-growth-analytics
configfile: pyproject.toml
testpaths: tests
collected 29 items

tests\test_analytics.py ...........
tests\test_data_generation.py .........
tests\test_decisions.py ..
tests\test_features.py ...
tests\test_validation.py ....

============================= 29 passed in 29.19s =============================
```

### 4.4 Execute notebook

```powershell
$env:PYTHONPATH = "src"
python scripts/build_notebook.py
python -m nbconvert --execute --to notebook --inplace notebooks/lifecycle_analysis.ipynb
```

Output:

```text
Notebook written to notebooks/lifecycle_analysis.ipynb
[NbConvertApp] Writing 222094 bytes to notebooks\lifecycle_analysis.ipynb
```

## 5. Full 5,000-user dataset metrics

Generated with:

```powershell
$env:PYTHONPATH = "src"
python scripts/generate_data.py --count 5000 --seed 42
```

- Users: 5,000
- Events: 88,975
- Events per user: 17.8
- Churn rate: 34.94%

### Retention

- D1 retention: 63.16%
- D7 retention: 46.58%
- D14 retention: 8.52%
- D7 rolling retention: 78.50%

### Core funnel

| step | users | conversion_rate | drop_off_rate |
|------|------:|----------------:|--------------:|
| signup | 5000 | 1.0000 | 0.000000 |
| onboarding_complete | 1960 | 0.3920 | 0.608000 |
| profile_complete | 1165 | 0.2330 | 0.405612 |
| resume_upload | 606 | 0.1212 | 0.479828 |
| job_recommendation_view | 331 | 0.0662 | 0.453795 |
| job_save | 178 | 0.0356 | 0.462236 |
| career_report_generate | 85 | 0.0170 | 0.522472 |

### Sample data file sizes (1,000 users)

| file | size (bytes) |
|------|-------------:|
| data/sample/events.csv | 4,010,899 |
| data/sample/experiment_assignments.csv | 147,206 |
| data/sample/interventions.csv | 94,766 |
| data/sample/users.csv | 132,295 |
| data/processed/labels.csv | 144,077 |
| data/sample/metadata.json | 130 |

### A/B experiment results

SRM p-value: 0.6677 (no sample-ratio mismatch detected).

| metric | variant | n | rate | relative lift | p-value |
|--------|---------|---|------|---------------|---------|
| onboarding_completion_rate | control | 2019 | 34.77% | - | - |
| onboarding_completion_rate | personalized | 1471 | 45.21% | +30.0% | 4.44e-10 |
| onboarding_completion_rate | simplified | 1510 | 39.27% | +12.9% | 0.0060 |
| profile_completion_rate | control | 2019 | 35.91% | - | - |
| profile_completion_rate | personalized | 1471 | 45.07% | +25.5% | 4.73e-08 |
| profile_completion_rate | simplified | 1510 | 39.27% | +9.4% | 0.0410 |
| d7_retention_rate | control | 2019 | 44.38% | - | - |
| d7_retention_rate | personalized | 1471 | 47.38% | +6.8% | 0.0785 |
| d7_retention_rate | simplified | 1510 | 48.74% | +9.8% | 0.0101 |

### Interventions

| action_name | count |
|-------------|------:|
| complete_onboarding | 3040 |
| send_win_back | 413 |
| send_reengagement_message | 14 |

- Win-back sent to churned users: 413
- Win-back sent to retained users: 0

## 6. Git commit

Commit after remediation:

```text
3d8313c Phase 1 remediation: reproducibility, retention, SRM, interventions, realism, docs, cleanup
```

## 7. Remaining risks and limitations

- The synthetic causal mechanism is calibrated for demonstration; it should not be interpreted as a real product result.
- D7 retention shows positive but modest effects. The personalized variant is not statistically significant at alpha=0.05 (p=0.078), while the simplified variant is (p=0.010). This is acceptable for a synthetic pipeline but would require more power or a stronger treatment in a real experiment.
- The sample dataset (1,000 users) produces wider confidence intervals and non-significant p-values for some metrics; the full 5,000-user dataset is recommended for stable analytics.
- No model training, API, database, or frontend work was performed, per the Phase 1 scope.

## 8. Temporary resources released

- Removed directories: `data_test_a`, `data_test_b`, `data_test_dup`, `data_test_orphan`, `data_test_shared`, `data_test_source`, `data_tmp_grid`, `data_full`.
- Removed caches: `.pytest_cache`, all `__pycache__`, `.ipynb_checkpoints`.
- Removed temporary script: `scripts/capture_full_stats.py` after statistics were captured.
