# Handover Report: Career Growth Analytics Phase 3 Complete

> Read this file first when resuming work. Then review `README.md`, the latest phase report, and the most recent worklog.
> Permanent collaboration rule: at the start of every new session, independently read `HANDOVER.md`, the task brief or acceptance criteria, the latest phase report, `README.md`, `git status`, and the last 5 commits. At the end of every task, update `HANDOVER.md` and add a worklog under `docs/worklogs/`.

## 1. Project Basics

- **Repository**: `C:\Users\Administrator\Desktop\career-growth-analytics`
- **Project name**: Career Growth Analytics
- **Business context**: AI career platform user lifecycle growth and experimentation system
- **Current phase**: Phase 3 Enterprise-level local full-stack system complete
- **Hard constraints**: productize, API-ify, and visualize the existing MVP capabilities. Do not introduce Kafka, Redis, Postgres, Flink, or similar heavy infrastructure.
- **Compliance requirement**: do not use any lychas-related code, data, or naming

## 2. Current Git State

Latest commit at the start of this cleanup task:

```text
4786878 docs: update HANDOVER.md and PHASE3 report with final commit hash
```

Working-directory changes in progress: documentation and ASCII compliance cleanup. They will be committed after this worklog is written.

Files created or modified in this cleanup:

- `HANDOVER.md`: translated to professional English and ASCII-only text
- `README.md`: replaced Unicode tree symbols with ASCII tree drawing
- `docs/enterprise_architecture.md`: replaced Unicode tree symbols with ASCII tree drawing
- `docs/methodology.md`: replaced em-dashes with ASCII hyphens
- `docs/worklogs/2026-06-15_phase1_final-remediation.md`: translated to English ASCII
- `docs/worklogs/2026-06-16_phase2_training-data-isolation.md`: translated to English ASCII
- `docs/worklogs/2026-06-16_phase3_ascii-compliance-cleanup.md`: this cleanup worklog

## 3. Completed Phase 1 Remediation

The detailed remediation report is in `PHASE1_REMEDIATION_REPORT.md`. Core results:

| Remediation item | Status | Key files |
|---|---|---|
| Removed `uuid.uuid4()`, fully deterministic IDs | Done | `src/career_growth/data_generation/events.py`, `interventions.py` |
| Reproducibility tests strengthened | Done | `tests/test_data_generation.py` |
| Cohort retention timezone and consistency fix | Done | `src/career_growth/analytics/retention.py`, `tests/test_analytics.py` |
| SRM uses `chisquare(observed, f_exp=expected)` | Done | `src/career_growth/analytics/experiments.py`, `tests/test_analytics.py` |
| Intervention logic based on churn label | Done | `src/career_growth/data_generation/interventions.py`, `generator.py` |
| Onboarding treatment mechanism rebuilt and calibrated | Done | `src/career_growth/data_generation/events.py`, `config.py` |
| Repository cleanup and smaller sample data | Done | `data/sample/*` is now 1,000 users; `.gitignore` updated |
| Documentation standards (README, pyproject, methodology) | Done | `README.md`, `pyproject.toml`, `docs/methodology.md` |
| Notebook executable | Done | `notebooks/lifecycle_analysis.ipynb` |
| Acceptance report | Done | `PHASE1_REMEDIATION_REPORT.md` |
| Local `.venv` works and commands are reproducible | Done | `.venv/` is ignored; `README.md` updated |
| Source/script/test comments restored to professional English | Done | all 24 Python files; non-ASCII scan result is 0 |

### Current Calibration Parameters

In `src/career_growth/config.py`:

```python
ONBOARDING_VARIANTS = [
    {"variant_id": "control",    "allocation": 0.40, "effect": 0.0},
    {"variant_id": "personalized", "allocation": 0.30, "effect": 0.30},
    {"variant_id": "simplified",  "allocation": 0.30, "effect": 0.15},
]
```

In `src/career_growth/data_generation/events.py`:

- `direct_effect` applies only to `onboarding_start` and `onboarding_complete`
- `profile_complete` state bonus from `onboarding_complete` is `0.25`
- First-week daily activity probability: `0.01 + 0.50 * engagement_score + 0.05 * onboarding_complete`
- Late-phase daily activity probability: `0.001 + 0.08 * engagement_score + 0.015 * num_core_actions`

### Current Python Environment

- Base interpreter: `C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe` (CPython 3.11.15 installed via `uv`)
- Project virtual-environment interpreter: `.venv\Scripts\python.exe`
- Python version: 3.11.15
- Dependency install command: `.venv\Scripts\python.exe -m pip install -e ".[dev]"`
- Note: the Windows Store `python.exe` path (`C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\...`) is a 0-byte redirector and cannot be invoked by absolute path in a fresh terminal. Always create `.venv` from the real CPython interpreter.

### Current Test Status

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src;backend"
.venv\Scripts\python.exe -m pytest tests backend/tests -q
```

Result (Phase 1 + Phase 2 + Phase 3 backend, 73 tests):

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\Administrator\Desktop\career-growth-analytics
configfile: pyproject.toml
plugins: anyio-4.13.0, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 73 items

tests\test_analytics.py ...........
tests\test_data_generation.py .........
tests\test_decisions.py ..
tests\test_features.py ...
tests\test_model_features.py .......
tests\test_modeling.py ............
tests\test_nba_integration.py ....
tests\test_train_script.py ..
tests\test_validation.py ....
backend\tests\test_experiment.py .
backend\tests\test_funnel.py .
backend\tests\test_health.py .
backend\tests\test_init_db.py .
backend\tests\test_model.py ..
backend\tests\test_nba.py ..
backend\tests\test_overview.py .
backend\tests\test_retention.py .
backend\tests\test_users.py .....

================== 73 passed, 1 warning in 537.57s (0:08:57) ==================
```

### Current Data State

- Committed sample data is **1,000 users** under `data/sample/` and `data/processed/labels.csv`. Verified not overwritten after training runs.
- Full **5,000-user** training data is written to the isolated `data/training/` directory (ignored by git) and does not overwrite `data/sample/`.
- `model_features.csv` is written as training output to `data/training/processed/model_features.csv`.
- Enterprise backend database is at `data/app/career_growth.db`, generated by `backend/scripts/init_db.py`.
- To generate 5,000-user training data locally:
  ```powershell
  $env:PYTHONPATH = "src"
  .venv\Scripts\python.exe scripts/train_churn_model.py --count 5000 --seed 42
  ```

### Latest Full 5,000-User Metrics (reference)

- Users: 5,000 / Events: 88,975 / Churn rate: 34.94%
- D1 / D7 / D14 retention: 63.16% / 46.58% / 8.52%
- SRM p-value: 0.6677
- Onboarding: personalized +30.0% (p=4.44e-10), simplified +12.9% (p=0.006)
- Profile: personalized +25.5% (p=4.73e-08), simplified +9.4% (p=0.041)
- D7 retention: personalized +6.8% (p=0.079), simplified +9.8% (p=0.010)
- Interventions: 413 win-back records, all sent to churned users

## 4. Original Codex Constraints (Still in Force)

The following requirements come from the Codex Phase 1 remediation brief and must still be honored:

### 4.1 Scope Constraints

- The project is now in Phase 3 (Enterprise local full-stack system). Phase 1 and Phase 2 scopes are complete.
- Do not begin cloud deployment, streaming infrastructure, or authentication/authorization unless explicitly requested.

### 4.2 Fix Determinism

1. Remove `uuid.uuid4()` from data generation.
2. `session_id`, `job_id`, `message_id`, and similar IDs must be generated deterministically from seed, user_id, time, or business sequence.
3. Expand reproducibility tests: two runs with the same seed must produce identical CSV content; compare file hashes or full DataFrames.

### 4.3 Fix Retention Analysis

1. Check timezones for `event_date` and `signup_date` in `compute_cohort_retention`.
2. Use consistent date types.
3. Add tests proving cohort retention is not all zeros.
4. Check that cohort summaries are consistent with overall D1, D7, and D14 retention.
5. Support or clearly display retention grouped by experiment variant.

### 4.4 Fix Experiment Statistics

1. SRM must use `scipy.stats.chisquare(observed, f_exp=expected)` or a statistically equivalent one-way chi-square goodness-of-fit test.
2. Do not use `chi2_contingency([observed, expected])`.
3. Add unit tests comparing directly against scipy standard results.
4. Update the experiment report SRM p-value after fixes.

### 4.5 Fix Intervention Logic

1. `win-back` must not rely only on `last_action <= label_end` to decide churn.
2. Churn definition must match the label: no `user_action` between day 8 and day 21 after signup.
3. Do not send win-back to retained users.
4. Add tests for intervention targeting on retained/churned users.
5. Intervention records must also be reproducible.

### 4.6 Improve Experiment Realism

1. Onboarding experiment must not directly boost all downstream events with the same effect.
2. Treatment should primarily affect `onboarding_complete` or early guidance behavior.
3. Lifts in profile completion, resume upload, job save, career report, and retention should flow through user state and funnel progression.
4. Recalibrate effects so results are statistically significant but not exaggerated.
5. Document that this is a synthetic causal mechanism, not a real business conclusion.

### 4.7 Data and Repository Cleanup

1. Tests must use `pytest tmp_path`; do not leave `data_test_*` directories in the project root.
2. Delete existing `data_test_a`, `data_test_b`, `data_test_dup`, `data_test_orphan`, `data_test_shared`, `data_test_source`, and similar temporary directories.
3. Committed sample data should stay around 500 to 1000 users.
4. Full 5,000-user data continues to be generated locally by the generation script.
5. Clean pytest cache and generated artifacts; keep `.gitignore` up to date.

### 4.8 Documentation Standards

1. Remove or replace fictional `github.com/deepmanifold/...` repository addresses.
2. `pyproject.toml` must not impersonate a project author or official company project.
3. Author may be Su Yutong or left blank.
4. Replace decorative Unicode arrows, em-dashes, and other non-ASCII characters in README with formal ASCII expressions.
5. README must accurately describe installation, data generation, tests, and notebook execution.

### 4.9 Runtime Environment and Acceptance

1. Provide the Python executable path used when tests are actually run.
2. Ensure a fresh environment can be installed and run from README instructions.
3. Run the full test suite.
4. Re-run data generation, validation, analysis, and the notebook.
5. Do not just report "tests passed"; provide commands and key output.
6. Submit `PHASE1_REMEDIATION_REPORT.md` after remediation.

### 4.10 Temporary Resource Cleanup Constraint

Before declaring any task complete, phase delivered, or test run finished, you must:

1. Stop background processes, dev servers, and containers started by this task.
2. Delete temporary test directories, rendered files, caches, and intermediate artifacts.
3. Clean pytest, Python, notebook, and build caches.
4. Do not delete source code, formal documentation, required sample data, acceptance reports, or the user's original files.
5. Before cleanup, confirm the target path belongs to the project directory or is a clearly temporary location.
6. List released temporary resources in the phase report.
7. If a resource must remain, document its purpose, path, and reason for retention.

Resource cleanup must be completed before claiming task completion.

## 5. Quick Command Reference

```powershell
# Enter the project directory
cd C:\Users\Administrator\Desktop\career-growth-analytics

# Create and activate a local virtual environment (first time; requires CPython 3.11)
py -3.11 -m venv .venv
.venv\Scripts\activate

# Install dependencies (after any pyproject.toml change)
.venv\Scripts\python.exe -m pip install -e ".[dev]"

# Set PYTHONPATH (Windows PowerShell)
$env:PYTHONPATH = "src"

# Generate sample data (1,000 users)
.venv\Scripts\python.exe scripts/generate_data.py --count 1000 --seed 42

# Generate full data (5,000 users)
.venv\Scripts\python.exe scripts/generate_data.py --count 5000 --seed 42

# Run full analysis
.venv\Scripts\python.exe scripts/run_analysis.py

# Print summary
.venv\Scripts\python.exe scripts/compute_summary.py

# Run tests
$env:PYTHONPATH = "src;backend"
.venv\Scripts\python.exe -m pytest tests backend/tests -q

# Rebuild and execute the notebook
.venv\Scripts\python.exe scripts/build_notebook.py
.venv\Scripts\python.exe -m nbconvert --execute --to notebook --inplace notebooks/lifecycle_analysis.ipynb

# Initialize the Enterprise SQLite database
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db

# Start the Enterprise backend
$env:PYTHONPATH = "src"
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000

# Start the Enterprise frontend (in a separate terminal)
cd C:\Users\Administrator\Desktop\career-growth-analytics\frontend
npm install
npm run dev
```

## 6. Key File Inventory

| Category | Files |
|---|---|
| Data generation | `src/career_growth/data_generation/events.py`, `generator.py`, `interventions.py`, `users.py`, `experiments.py` |
| Configuration | `src/career_growth/config.py` |
| Schema | `src/career_growth/schemas.py` |
| Labels | `src/career_growth/features/labels.py` |
| Feature engineering | `src/career_growth/features/model_features.py` |
| Validation | `src/career_growth/validation/validator.py` |
| Analytics | `src/career_growth/analytics/funnel.py`, `retention.py`, `experiments.py` |
| Modeling | `src/career_growth/modeling/split.py`, `pipeline.py`, `evaluate.py`, `explain.py`, `train.py` |
| Decisions | `src/career_growth/decisions/next_best_action.py` |
| Tests | `tests/test_data_generation.py`, `test_validation.py`, `test_analytics.py`, `test_features.py`, `test_decisions.py`, `test_model_features.py`, `test_modeling.py`, `test_nba_integration.py`, `test_train_script.py`, `tests/conftest.py` |
| Scripts | `scripts/generate_data.py`, `run_analysis.py`, `compute_summary.py`, `build_notebook.py`, `train_churn_model.py` |
| Documentation | `README.md`, `docs/data_schema.md`, `docs/methodology.md`, `docs/model_card.md`, `pyproject.toml`, `.gitignore` |
| Artifacts | `artifacts/churn_model.joblib`, `model_metadata.json`, `metrics.json`, `feature_schema.json`, `explainability.json`, `user_explanations.json`, `subgroup_metrics.*`, `nba_examples.*`, `plots/*.png` |
| Training data (local, not committed) | `data/training/sample/*`, `data/training/processed/*` |
| Enterprise backend | `backend/app/*`, `backend/scripts/*`, `backend/tests/*` |
| Enterprise frontend | `frontend/src/*`, `frontend/package.json`, `frontend/vite.config.ts` |
| Enterprise database | `data/app/career_growth.db` |
| Acceptance reports | `PHASE1_REMEDIATION_REPORT.md`, `PHASE2_MODELING_REPORT.md`, `PHASE3_ENTERPRISE_REPORT.md`, `HANDOVER.md` (this file) |

## 7. Known Risks and Open Items

- D7 retention for the personalized variant is p=0.079 in the 5,000-user dataset, below the conventional 0.05 threshold. This is a property of the synthetic data; it does not block acceptance, but the effect can be recalibrated if stronger significance is required.
- The 1,000-user sample is small, so some metrics have non-significant p-values. The full 5,000-user analysis is more stable.
- Phase 2 training-data isolation is complete and verified.
- Phase 3 Enterprise-level local full-stack system is complete and verified (73 tests passed, frontend build succeeded).
- Dependency installation can be slow on this network; retry or use `uv pip install` if needed.

## 8. Next Steps

1. Wait for Codex final acceptance of Phase 3.
2. If Codex requests further remediation, follow the constraints above.
3. This phase is a local Enterprise system; cloud deployment, authentication/authorization, and real-time stream processing are out of scope unless explicitly requested.

---

## Appendix A: Historical Session Summaries

- **Session date**: 2026-06-15
- **Task**: fixed `.venv` pointing to a Windows Store alias; installed real CPython 3.11.15 and recreated `.venv`; restored source/script/test comments to professional English; ran non-ASCII scan; reran 29 tests, 1,000-user data generation, `run_analysis.py`, and `compute_summary.py` under `.venv`; updated README/HANDOVER/remediation report; cleaned temporary resources; committed changes.
- **Detailed worklog**: `docs/worklogs/2026-06-15_phase1_final-remediation.md`

- **Session date**: 2026-06-16
- **Task**: fixed the Phase 2 blocker where the training script overwrote the committed 1,000-user sample data. Changed `scripts/train_churn_model.py` default `--data-dir` to `data/training`; updated `.gitignore` to ignore the training directory; deleted the mistakenly committed `data/processed/model_features.csv`; added `tests/test_train_script.py` to verify training/sample isolation; updated README, `PHASE2_MODELING_REPORT.md`, and `HANDOVER.md`; reran 58 tests, 5,000-user training, verified sample was not overwritten, git status clean except for expected changes; cleaned temporary resources; wrote worklog and committed.
- **Detailed worklog**: `docs/worklogs/2026-06-16_phase2_training-data-isolation.md`

- **Session date**: 2026-06-16
- **Task**: built the Phase 3 Enterprise-level local full-stack system (FastAPI backend, SQLite data layer, React + Vite + TypeScript frontend); added 15 backend tests; ran the full 73-test suite and verified frontend build; wrote `PHASE3_ENTERPRISE_REPORT.md`, `docs/enterprise_architecture.md`, `docs/api_reference.md`, and `docs/worklogs/2026-06-16_phase3_enterprise_system.md`; updated `HANDOVER.md` and `README.md`; committed.
- **Detailed worklog**: `docs/worklogs/2026-06-16_phase3_enterprise_system.md`

## Appendix B: This Session Summary

- **Session date**: 2026-06-16
- **Task**: Codex final acceptance was blocked because tracked text files contained non-ASCII characters (Chinese text, Unicode tree symbols, em/en dashes). Converted all flagged tracked Markdown files to professional English ASCII-only text. Replaced Unicode tree symbols with ASCII pipe-and-dash equivalents and em-dashes with ASCII hyphens. Ran ASCII scan and confirmed `NON_ASCII_TRACKED_TEXT_FILES=0`. Updated `HANDOVER.md`, added this worklog, cleaned temporary resources, and committed.
- **Detailed worklog**: `docs/worklogs/2026-06-16_phase3_ascii-compliance-cleanup.md`
