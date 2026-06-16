# Enterprise Architecture

## Overview

The Phase 3 Enterprise system turns the existing MVP analytics and churn prediction pipeline into a local, full-stack product. It exposes the data and model through a FastAPI backend, persists data in SQLite, and visualizes it through a React + Vite + TypeScript frontend.

## Components

```text
career-growth-analytics/
|-- backend/
|   |-- app/
|   |   |-- main.py                 # FastAPI app and router registration
|   |   |-- config.py               # Paths and constants
|   |   |-- database.py             # SQLite connection and schema creation
|   |   |-- schemas.py              # Pydantic request/response models
|   |   |-- services/               # Business logic
|   |   |   |-- data_service.py     # CSV/artifact loading and DB seeding
|   |   |   |-- analytics_service.py # Funnel, retention, experiment analytics
|   |   |   |-- model_service.py    # Model scoring and explanations
|   |   |   |-- nba_service.py      # Next Best Action service
|   |   |-- routers/                # API endpoints
|   |   |   |-- health.py
|   |   |   |-- overview.py
|   |   |   |-- funnel.py
|   |   |   |-- retention.py
|   |   |   |-- experiment.py
|   |   |   |-- model.py
|   |   |   |-- users.py
|   |   |   |-- nba.py
|   |-- scripts/
|   |   |-- init_db.py              # Initialize and seed SQLite database
|   |-- tests/                      # Backend pytest suite
|-- frontend/                       # React + Vite + TypeScript
|   |-- src/
|   |   |-- api/                    # API client and TypeScript types
|   |   |-- components/             # Layout, shared UI
|   |   |-- pages/                  # Dashboard pages
|   |   |-- App.tsx
|   |   |-- main.tsx
|   |-- package.json
|-- data/app/
|   |-- career_growth.db            # Local SQLite database
|-- artifacts/                      # Existing model artifacts
```

## Data Flow

1. The CSV sample data and artifacts are committed with the repository.
2. `backend/scripts/init_db.py` reads the CSVs and writes them into `data/app/career_growth.db`.
3. FastAPI routers load data either directly from CSVs/artifacts or from SQLite depending on the endpoint.
4. The model service loads `artifacts/churn_model.joblib` once and scores users on demand.
5. The frontend fetches JSON from the backend and renders charts and tables.

## Backend Services

### Data Service

- Loads `data/sample/*.csv` and `data/processed/labels.csv`.
- Loads model artifacts from `artifacts/`.
- Seeds SQLite tables: users, events, experiment_assignments, interventions, labels.

### Analytics Service

- Reuses the existing `career_growth.analytics` modules.
- Computes overview KPIs, funnel, retention, and experiment analysis.

### Model Service

- Loads the fitted scikit-learn pipeline.
- Rebuilds features with `career_growth.features.model_features.build_model_features`.
- Returns predicted probabilities, predicted classes, and explanations.
- Does not use the true `is_churned` label for recommendations.

### NBA Service

- Wraps `recommend_next_action` with the model score.
- Generates Next Best Action recommendations from user state and churn probability.

## Frontend Pages

- **Overview**: KPI cards, system health, model performance.
- **Funnel**: Bar chart and table of lifecycle conversion.
- **Retention**: D1/D7/D14 cards and cohort table.
- **Experiment**: Variant comparison and SRM status.
- **Churn Risk**: Risk distribution, subgroup metrics, high-risk user table.
- **User Detail**: Profile, prediction, explanation, event timeline.

## Design Decisions

- **SQLite**: Chosen to keep the system local and dependency-free. No Postgres, Redis, or Kafka.
- **FastAPI**: Lightweight, auto-generates OpenAPI docs at `/docs`.
- **React + Vite + TypeScript**: Fast dev server, type safety, simple build.
- **Recharts**: Lightweight charting library for funnel and risk distribution.
- **No hardcoded demo data**: All UI values come from the backend API.

## Limitations

- The system runs locally only.
- Data is synthetic.
- Model explanations are associations, not causal effects.
- No authentication or authorization.
