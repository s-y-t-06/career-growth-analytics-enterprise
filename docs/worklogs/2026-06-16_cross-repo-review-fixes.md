# Cross-Repo Review Fixes

## Date

2026-06-16

## Objective

Fix reviewer-facing reproducibility risks, documentation consistency, and a few high-value engineering details across the MVP and Enterprise repositories without adding new features, changing core logic, or altering model results.

## Repositories

- MVP: `C:\Users\Administrator\Desktop\career-growth-analytics-mvp-export`
- Enterprise: `C:\Users\Administrator\Desktop\career-growth-analytics`

## Changes

### 1. README clone/cd command alignment

- MVP `README.md`: added `git clone https://github.com/s-y-t-06/career-growth-analytics-mvp.git` and `cd career-growth-analytics-mvp`.
- Enterprise `README.md`: added `git clone https://github.com/s-y-t-06/career-growth-analytics-enterprise.git` and `cd career-growth-analytics-enterprise`.
- Removed local-machine paths from clone instructions.

### 2. Enterprise README environment setup

- Added virtual environment creation steps:
  - `python -m venv .venv`
  - `.venv\Scripts\python.exe -m pip install --upgrade pip`
  - `.venv\Scripts\python.exe -m pip install -e ".[dev]"`

### 3. Smoke test vs full test distinction

- MVP `README.md`: added Smoke test section (5 core test files, ~30-60s) and Full test section (`pytest tests -q`, ~8-10min).
- Enterprise `README.md`: added Smoke test section (`backend\tests -q`, ~2-3min) and Full test section (`tests backend\tests -q`, ~8-10min).
- Added frontend build verification command.

### 4. Schema documentation aligned with actual CSV fields

Updated `docs/data_schema.md` in both repos based on real CSV headers:

- `users.csv`: added `initial_plan_type`.
- `events.csv`: added `event_properties`, `page_name`, `platform`, `experiment_id`, `variant_id`.
- `experiment_assignments.csv`: renamed `assigned_at` to `assignment_time`; added `experiment_name`, `experiment_type`, `traffic_allocation`, `is_exposed`, `is_converted`.
- `interventions.csv`: replaced old fields with `message_id`, `action_name`, `channel`, `send_time`, `open_time`, `click_time`, `conversion_time`, `experiment_id`.
- `labels.csv`: renamed `label_window_start`/`label_window_end` to `label_start`/`label_end`; added `signup_timestamp` and `prediction_cutoff`.

### 5. NBA risk threshold clarification

- Extracted `HIGH_RISK_ACTION_THRESHOLD = 0.70` constant in `src/career_growth/decisions/next_best_action.py` for both repos.
- Added comments explaining that 0.41 is the model classification threshold (validation F1) and 0.70 is the operational business threshold to avoid over-messaging.
- Updated `docs/model_card.md` in both repos with a dedicated "模型阈值与 Next Best Action 阈值" section.

### 6. Enterprise SQLite startup experience

- Updated `README.md` and `HANDOVER.md` to state that `backend.scripts.init_db` must be run before starting the backend.
- Clarified that `data/app/career_growth.db` is a local SQLite file, not cloud deployment.
- Added low-risk auto-seed in `backend/app/main.py`: on startup, if the `users` table is empty, the app automatically calls `seed_database()`.

### 7. Frontend Churn Risk column labels

- Updated `frontend/src/pages/ChurnRisk.tsx` to rename the two "Channel" columns to "Acquisition Channel" and "Recommended Channel".

### 8. Experiment analysis caveat

- Added "实验分析说明" section to `docs/methodology.md` in both repos, noting the current analysis is exploratory, lacks multiple-testing correction, and that production experiments should pre-register primary metrics and apply Bonferroni/FDR or similar methods.

## Validation

### MVP

- Python syntax check: `python -m py_compile src/career_growth/decisions/next_best_action.py` passed.
- Smoke test: `python -m pytest tests\test_data_generation.py tests\test_validation.py tests\test_analytics.py tests\test_features.py tests\test_decisions.py -q` -> 29 passed.

### Enterprise

- Python syntax check:
  - `.venv\Scripts\python.exe -m py_compile src/career_growth/decisions/next_best_action.py` passed.
  - `.venv\Scripts\python.exe -m py_compile backend/app/main.py` passed.
- Backend smoke test: `.venv\Scripts\python.exe -m pytest backend\tests -q` -> 15 passed, 1 warning.
- Full test: `.venv\Scripts\python.exe -m pytest tests backend\tests -q` -> 73 passed, 1 warning in 727.75s.
- Frontend build: `npm run build` succeeded.

### Cross-repo checks

- Grep for `C:\Users\Administrator` in Markdown files: no matches in either repo.
- Temporary resources cleaned: `.pytest_cache`, `__pycache__`, `.ipynb_checkpoints`, `frontend/dist`, `data_test_*`, `data_tmp_*`.

## Commits

- MVP: `6871c652432dc0a8c40c132b10a5031cbb817db9`
- Enterprise: `17c980d841df1fc07e04328d88fed1b514b6307b`

## Notes

- No push to GitHub performed; awaiting Codex review.
- No model metrics, training logic, or API field semantics were changed.
