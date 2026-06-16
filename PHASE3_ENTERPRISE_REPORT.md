# Phase 3 Enterprise Report

## 1. Objective

Build a local, Enterprise-level full-stack system on top of the existing MVP analytics and churn prediction pipeline. The system exposes MVP capabilities through a FastAPI backend, persists data in SQLite, and visualizes insights through a React + Vite + TypeScript frontend.

## 2. Scope

- FastAPI backend with health, overview, funnel, retention, experiment, model, users, and NBA endpoints.
- SQLite database initialized from committed sample CSVs and artifacts.
- React + Vite + TypeScript frontend with six dashboard pages.
- Backend tests covering all public endpoints.
- Architecture and API reference documentation.

No cloud infrastructure, Kafka, Redis, Postgres, or Flink was introduced.

## 3. New Files

### Backend

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/schemas.py`
- `backend/app/services/data_service.py`
- `backend/app/services/analytics_service.py`
- `backend/app/services/model_service.py`
- `backend/app/services/nba_service.py`
- `backend/app/routers/health.py`
- `backend/app/routers/overview.py`
- `backend/app/routers/funnel.py`
- `backend/app/routers/retention.py`
- `backend/app/routers/experiment.py`
- `backend/app/routers/model.py`
- `backend/app/routers/users.py`
- `backend/app/routers/nba.py`
- `backend/scripts/init_db.py`
- `backend/tests/conftest.py`
- `backend/tests/test_health.py`
- `backend/tests/test_overview.py`
- `backend/tests/test_funnel.py`
- `backend/tests/test_retention.py`
- `backend/tests/test_experiment.py`
- `backend/tests/test_model.py`
- `backend/tests/test_users.py`
- `backend/tests/test_nba.py`
- `backend/tests/test_init_db.py`

### Frontend

- `frontend/index.html`
- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/tsconfig.app.json`
- `frontend/tsconfig.node.json`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/index.css`
- `frontend/src/api/client.ts`
- `frontend/src/api/types.ts`
- `frontend/src/components/Layout.tsx`
- `frontend/src/pages/Overview.tsx`
- `frontend/src/pages/Funnel.tsx`
- `frontend/src/pages/Retention.tsx`
- `frontend/src/pages/Experiment.tsx`
- `frontend/src/pages/ChurnRisk.tsx`
- `frontend/src/pages/UserDetail.tsx`

### Documentation

- `docs/enterprise_architecture.md`
- `docs/api_reference.md`
- `PHASE3_ENTERPRISE_REPORT.md`
- `docs/worklogs/2026-06-16_phase3_enterprise_system.md`

### Updated

- `README.md`
- `HANDOVER.md`
- `pyproject.toml`
- `.gitignore`

## 4. SQLite Schema

Tables created by `backend/scripts/init_db.py`:

- `users`
- `events`
- `experiment_assignments`
- `interventions`
- `labels`
- `model_scores`
- `nba_recommendations`

Database path: `data/app/career_growth.db`

## 5. Backend API List

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Backend, database, model, metrics health |
| GET | `/api/overview` | Platform and model KPIs |
| GET | `/api/funnel` | Lifecycle funnel |
| GET | `/api/retention` | D1/D7/D14 and cohort retention |
| GET | `/api/experiment` | Onboarding A/B experiment analysis |
| GET | `/api/model/metrics` | Model metrics from artifacts |
| GET | `/api/model/subgroups` | Subgroup evaluation |
| GET | `/api/users` | Scored user list with filters |
| GET | `/api/users/{user_id}` | User profile, risk, explanation, timeline |
| POST | `/api/users/score` | Score a single user |
| GET | `/api/nba/examples` | Example NBA recommendations |
| POST | `/api/nba/recommend` | Recommend action for a user |

Interactive docs: `http://localhost:8000/docs`

## 6. Frontend Pages

- **Overview Dashboard**: KPI cards, system health, model metrics.
- **Funnel**: Bar chart and funnel table.
- **Retention**: D1/D7/D14 cards and cohort table.
- **Experiment**: Variant comparison and SRM status.
- **Churn Risk**: Model metrics, risk distribution, subgroup table, high-risk user table.
- **User Detail**: Profile, churn probability, risk factors, NBA recommendation, event timeline.

## 7. Local Startup

### Backend

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```

### Frontend

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics\frontend
npm install
npm run dev
```

Open http://localhost:5173.

## 8. Test Results

### Python Tests

```powershell
$env:PYTHONPATH = "src;backend"
.venv\Scripts\python.exe -m pytest tests backend/tests -q
```

Result: **73 passed, 1 warning** in 537.57s.

### Frontend Build

```powershell
cd frontend
npm run build
```

Result: build succeeded, output in `frontend/dist/`.

## 9. API Example Responses

### GET /api/overview

```json
{
  "users": 1000,
  "events": 17856,
  "churn_rate": 0.39,
  "d1_retention": 0.674,
  "d7_retention": 0.467,
  "d14_retention": 0.079,
  "selected_model": "logistic_regression",
  "test_pr_auc": 0.5371,
  "test_roc_auc": 0.6942,
  "test_f1": 0.5884,
  "test_brier": 0.2227
}
```

### POST /api/users/score

```json
{
  "user_id": "fa911d87-a280-5f11-b1b5-c04820b1f6db",
  "churn_probability": 0.8375,
  "predicted_class": 1,
  "recommended_action": "send_reengagement_message",
  "channel": "in_app",
  "reason": "high churn risk without marketing consent"
}
```

## 10. Known Risks and Limitations

- The system is local-only; no authentication, authorization, or cloud deployment.
- Data is synthetic.
- Model explanations are associations, not causal effects.
- Frontend chunk size is large due to Recharts; acceptable for a local demo.
- The SQLite database is single-thread friendly but not suited for high concurrency.

## 11. Uncompleted Items

- Cloud deployment.
- Real-time event ingestion.
- Advanced model monitoring and drift detection.
- User authentication and role-based access control.

## 12. Git Commit Hash

`42dd34f feat: Phase 3 Enterprise-level local full-stack system`

## 13. Frontend Presentation Polish

After the initial Phase 3 acceptance, the frontend presentation was refined to make the dashboard read like a real internal analytics product for interviews and demos.

### 13.1 UX Improvements

- **Global layout**: topbar with system name "Career Growth Analytics" and product context "AI Career Platform Lifecycle Growth System"; backend health indicator (API Online / Model Loaded / Data Ready); improved sidebar brand and active navigation states; backend unavailable banner.
- **Overview**: subtitle explaining business purpose; KPI cards for Users, Events, Churn Rate, D7 Retention, Selected Model, Test PR-AUC, Test ROC-AUC, Test F1 with helper text; "What to watch" section; "Demo flow" walkthrough hint.
- **Funnel**: clearer bar chart; table with Step, Users, Conversion Rate, Drop-off Rate; highest drop-off step highlighted; auto-generated business insight.
- **Retention**: D1/D7/D14 KPI cards; cohort retention shown as a pivot table with color-coded retention levels.
- **Experiment**: experiment ID and SRM p-value summary; "Healthy allocation" / "Potential SRM risk" status; metric tables grouped into Activation, Profile, and Retention; explicit synthetic experiment demonstration notice.
- **Churn Risk**: model metric KPI cards (PR-AUC, ROC-AUC, Brier, F1, Threshold); risk distribution chart; subgroup performance table with precision, recall, F1, and small-sample flags; filters for min risk, acquisition channel, and career stage; high-risk user table with risk bars.
- **User Detail**: header showing user ID, churn probability, predicted class, recommended action, and channel; profile grid; Next Best Action block; top risk factors with direction labels; early event timeline.
- **States**: loading, error, empty, and backend-unavailable states added across pages.

### 13.2 New Frontend Components

- `frontend/src/components/PageHeader.tsx`
- `frontend/src/components/KpiCard.tsx`
- `frontend/src/components/SectionCard.tsx`
- `frontend/src/components/StatusBadge.tsx`
- `frontend/src/components/LoadingState.tsx`
- `frontend/src/components/ErrorState.tsx`
- `frontend/src/components/EmptyState.tsx`
- `frontend/src/components/RiskBar.tsx`

### 13.3 Updated Frontend Files

- `frontend/src/App.tsx` (routes unchanged)
- `frontend/src/components/Layout.tsx`
- `frontend/src/index.css`
- `frontend/src/pages/Overview.tsx`
- `frontend/src/pages/Funnel.tsx`
- `frontend/src/pages/Retention.tsx`
- `frontend/src/pages/Experiment.tsx`
- `frontend/src/pages/ChurnRisk.tsx`
- `frontend/src/pages/UserDetail.tsx`
- `frontend/src/api/types.ts`
- `frontend/src/api/client.ts` (unchanged)

### 13.4 Frontend Presentation Polish Test Results

Backend smoke tests:

```powershell
$env:PYTHONPATH = "src;backend"
.venv\Scripts\python.exe -m pytest backend\tests -q
```

Result: **15 passed, 1 warning** in 131.15s.

Frontend build:

```powershell
cd frontend
npm run build
```

Result: build succeeded, output in `frontend/dist/`.

ASCII scan:

```text
NON_ASCII_TRACKED_TEXT_FILES=0
NON_ASCII_OCCURRENCES=0
```

## 14. Temporary Resources Released

- `.pytest_cache`
- `__pycache__` directories
- `.ipynb_checkpoints`
- `_tmp_*` helper scripts
- Frontend build output `frontend/dist/` is generated on demand and not committed; `node_modules/` is ignored by git.
