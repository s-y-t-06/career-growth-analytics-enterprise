# Career Growth Analytics

AI Career Platform Lifecycle Growth and Experimentation System -- MVP.

This repository contains the minimum viable product for analyzing user lifecycle growth in an AI-powered career planning and job recommendation product. It generates a realistic synthetic event stream, validates data quality, computes growth funnels and cohort retention, analyzes an onboarding A/B experiment, and produces rule-based Next Best Action recommendations.

## Project Scope

The MVP focuses on the core data and analytics pipeline:

- Synthetic user and event data generation.
- Data schema validation and quality checks.
- Growth funnel analysis.
- Cohort retention analysis.
- A/B experiment analysis with sample ratio mismatch detection.
- Churn label construction without data leakage.
- Rule-based Next Best Action engine.
- Churn prediction model training and evaluation (Phase 2).
- Automated tests.
- End-to-end Jupyter notebooks.

Model training is now included as Phase 2: a reproducible churn prediction pipeline with feature engineering, chronological train/validation/test splits, model selection, and evaluation.

Phase 3 adds an Enterprise-level local full-stack system: a FastAPI backend, SQLite data layer, and React + Vite + TypeScript frontend for interactive product analytics.

## Business Context

The simulated product helps university students and early-career professionals explore career paths, upload resumes, receive job recommendations, complete growth tasks, and generate career reports. The growth platform measures and optimizes the user journey from signup through activation and retention.

Core user journey:

```
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

## Repository Structure

```
career-growth-analytics/
├── backend/                   # FastAPI enterprise backend
│   ├── app/                   # Application code
│   │   ├── main.py            # FastAPI entry point
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── database.py        # SQLite utilities
│   │   └── schemas.py         # Pydantic models
│   ├── scripts/               # Backend CLI scripts
│   │   └── init_db.py         # Initialize SQLite database
│   └── tests/                 # Backend pytest suite
├── data/
│   ├── sample/                # Generated CSV files (users, events, experiments, interventions)
│   ├── processed/             # Derived outputs such as labels
│   ├── app/                   # Local SQLite database
│   └── training/              # Local 5,000-user training data (ignored by git)
├── docs/
│   ├── data_schema.md         # Full data schema
│   ├── methodology.md         # Generation and label methodology
│   ├── model_card.md          # Model card
│   ├── enterprise_architecture.md  # Enterprise system architecture
│   └── api_reference.md       # API reference
├── frontend/                  # React + Vite + TypeScript frontend
│   ├── src/
│   │   ├── api/               # API client and types
│   │   ├── components/        # Shared UI components
│   │   ├── pages/             # Dashboard pages
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── notebooks/
│   ├── lifecycle_analysis.ipynb   # End-to-end exploratory analysis
│   └── churn_modeling.ipynb       # Churn prediction modeling
├── scripts/
│   ├── generate_data.py       # CLI to regenerate synthetic data
│   ├── run_analysis.py        # CLI to run validation and analytics
│   ├── compute_summary.py     # CLI to print a concise summary
│   ├── build_notebook.py      # CLI to execute the notebook from the command line
│   └── train_churn_model.py   # CLI to train churn models
├── src/career_growth/         # Original MVP analytics package
├── tests/                     # Original pytest suite
├── pyproject.toml
├── README.md
└── LICENSE
```

## Technology Stack

- Python 3.10+
- pandas, numpy, scikit-learn, scipy
- matplotlib / seaborn
- pydantic
- pytest
- Jupyter
- FastAPI, uvicorn
- SQLite
- React, Vite, TypeScript
- Recharts, lucide-react

No external APIs, payment gateways, or cloud services are used. All data is generated locally.

## Installation

Create and activate a virtual environment in the repository root using a real CPython interpreter (not a Windows Store alias), then install the package in editable mode.

On Windows, use the `py` launcher with CPython 3.11 preinstalled:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

On macOS or Linux:

```bash
/path/to/real/python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -e ".[dev]"
```

The `.venv/` directory is ignored by Git (see `.gitignore`). Using the virtual environment's interpreter avoids relying on the Windows Store Python shim, which cannot be invoked by absolute path in a fresh terminal.

Verified base interpreter for this repository (CPython 3.11.15 installed via `uv`):

```text
C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe
```

## Generate Data

The repository includes a small sample dataset (1,000 users) under `data/sample/`. To regenerate it, or to generate a larger dataset locally, run:

```powershell
# Regenerate the sample dataset
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/generate_data.py --count 1000 --seed 42

# Generate the full 5,000-user dataset used for stable analytics
.venv\Scripts\python.exe scripts/generate_data.py --count 5000 --seed 42
```

Generated files:

- `data/sample/users.csv`
- `data/sample/events.csv`
- `data/sample/experiment_assignments.csv`
- `data/sample/interventions.csv`
- `data/processed/labels.csv`

## Run Analytics

After generating data, run the full analytics pipeline from the project root:

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/run_analysis.py
```

This executes validation, funnel, retention, cohort, experiment, and Next Best Action analysis.

## Train Churn Model

Train and evaluate churn prediction models on the full 5,000-user dataset:

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/train_churn_model.py --count 5000 --seed 42
```

This script:

- Generates synthetic data into a dedicated training directory (`data/training/` by default) so that the committed 1,000-user sample data under `data/sample/` is never overwritten.
- Builds pre-cutoff features and attaches churn labels.
- Saves the engineered feature matrix to `data/training/processed/model_features.csv`.
- Splits users chronologically into train/validation/test sets.
- Trains a Logistic Regression baseline and a HistGradientBoostingClassifier.
- Selects the best model by validation PR-AUC.
- Chooses an operating threshold on the validation set (F1 by default; Youden index also supported).
- Evaluates the selected model exactly once on the test set, including Brier score and confusion matrix.
- Outputs subgroup metrics by `acquisition_channel`, `career_stage`, and `device_type`.
- Produces global and user-level explanations, plus Next Best Action examples.
- Saves the model, metadata, metrics, feature schema, explainability artifacts, subgroup metrics, NBA examples, and plots under `artifacts/`.

To use existing data instead of regenerating it, add `--use-existing-data`.

## Model Artifacts

Formal artifacts under `artifacts/` are committed as deliverables. Key files include:

- `artifacts/churn_model.joblib` -- selected, fitted model
- `artifacts/model_metadata.json` -- model name, version, training timestamp, cutoff/window days, feature columns, threshold, split time ranges, sizes, churn rates, library versions
- `artifacts/metrics.json` -- candidate validation metrics, selected model, threshold, validation metrics, test metrics, confusion matrix
- `artifacts/feature_schema.json` -- separated categorical and numeric feature lists
- `artifacts/explainability.json` -- top coefficients, permutation importance, user explanations
- `artifacts/user_explanations.json` -- at least 3 user-level explanations
- `artifacts/subgroup_metrics.csv` / `subgroup_metrics.json` -- subgroup evaluation
- `artifacts/nba_examples.csv` / `nba_examples.json` -- Next Best Action examples
- `artifacts/plots/*.png` -- PR, ROC, calibration, confusion matrix, risk distribution, and feature importance plots

## Run Enterprise Application

### Initialize database

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe -m backend.scripts.init_db
```

### Start backend

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```

### Start frontend

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics\frontend
npm install
npm run dev
```

Open http://localhost:5173 in a browser.

## Run Tests

```powershell
$env:PYTHONPATH = "src;backend"
.venv\Scripts\python.exe -m pytest tests backend/tests -q
```

## Build Frontend

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics\frontend
npm run build
```

## Open Notebook

```powershell
.venv\Scripts\jupyter.exe notebook notebooks/lifecycle_analysis.ipynb
```

To execute the notebook non-interactively:

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/build_notebook.py
.venv\Scripts\python.exe -m nbconvert --execute --to notebook --inplace notebooks/lifecycle_analysis.ipynb
```

## Churn Label Definition

- Prediction cutoff: signup timestamp + 7 days.
- Label window: day 8 through day 21 after signup.
- `is_churned = 1` if the user has no `event_source == "user_action"` events in the label window.
- Only users with a complete 21-day observation window are included.

## A/B Experiment

`exp_onboarding_v1` compares three onboarding flows:

- `control` -- standard five-step onboarding (40%)
- `personalized` -- adaptive onboarding (30%)
- `simplified` -- two-step onboarding (30%)

Primary metrics: onboarding completion rate, profile completion rate, D7 retention rate.

The treatment effects are injected into the synthetic data through a causal mechanism: the onboarding variants directly influence onboarding completion (and the preceding onboarding start), and any downstream lift in profile completion, resume upload, or retention emerges from the resulting user state and funnel progression. This is a synthetic demonstration, not a claim about real product performance.

## Design Decisions

See `docs/methodology.md` for the full generative causal order, probability formulas, treatment effect injection, noise and anomaly injection, and leakage protection rules.

## License

MIT License -- see `LICENSE`.
