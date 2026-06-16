# Phase 2 Modeling Worklog

## Session

- Date: 2026-06-15
- Task: Complete Phase 2 churn prediction MVP after scope review

## Work Completed

1. Read required handoff documents and current code.
2. Added missing features to `src/career_growth/features/model_features.py`:
   - `language`, `timezone`
   - `unique_event_type_count`, `first_day_event_count`, `last_2_days_event_count`
   - `hours_to_first_action`, `hours_since_last_action_at_cutoff`
   - `ai_assistant_interaction_count`, `job_detail_view_count`, `return_visit_count`
   - Time-based features use NaN for inactive users and are imputed in the pipeline.
3. Added boundary test proving post-cutoff events do not influence features.
4. Updated pipelines to use `SimpleImputer(strategy="median")` for numeric features.
5. Enhanced evaluation (`src/career_growth/modeling/evaluate.py`):
   - Added Brier score.
   - Added confusion matrix helper.
   - Fixed Youden threshold selection.
6. Updated `TrainingResult` and `train_and_select_model` to save candidate validation metrics.
7. Fixed `feature_schema.json` and `model_metadata.json` output.
8. Added subgroup evaluation (`src/career_growth/modeling/subgroup.py`).
9. Added user-level explanations (`src/career_growth/modeling/explain.py`).
10. Added Next Best Action integration (`src/career_growth/modeling/nba_integration.py`).
11. Updated `scripts/train_churn_model.py` to output all required artifacts.
12. Updated `.gitignore` to commit formal artifacts.
13. Updated `notebooks/churn_modeling.ipynb` with all required sections.
14. Updated `README.md`, `HANDOVER.md`, `PHASE2_MODELING_REPORT.md`, `docs/model_card.md`, and this worklog.

## Commands Used

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/generate_data.py --count 1000 --seed 42
.venv\Scripts\python.exe scripts/train_churn_model.py --count 5000 --seed 42
.venv\Scripts\python.exe -m pytest tests -q
.venv\Scripts\python.exe -m nbconvert --execute --to notebook --inplace notebooks/churn_modeling.ipynb
```

## 5,000-User Training Results

Selected model: `logistic_regression`
Operating threshold: `0.41`

Candidate validation metrics:

| Model | PR-AUC | ROC-AUC | Brier score |
|---|---|---|---|
| logistic_regression | 0.5515 | 0.7079 | 0.2167 |
| hist_gradient_boosting | 0.5203 | 0.6860 | 0.2119 |

Final test metrics:

| Metric | Value |
|---|---|
| PR-AUC | 0.5371 |
| ROC-AUC | 0.6942 |
| Brier score | 0.2227 |
| Precision | 0.4636 |
| Recall | 0.8049 |
| F1 score | 0.5884 |
| Accuracy | 0.5900 |

Confusion matrix:

| | Predicted 0 | Predicted 1 |
|---|---|---|
| Actual 0 | 297 | 339 |
| Actual 1 | 71 | 293 |

## Artifacts Produced

- `artifacts/churn_model.joblib`
- `artifacts/model_metadata.json`
- `artifacts/metrics.json`
- `artifacts/feature_schema.json`
- `artifacts/explainability.json`
- `artifacts/user_explanations.json`
- `artifacts/subgroup_metrics.csv` / `subgroup_metrics.json`
- `artifacts/nba_examples.csv` / `nba_examples.json`
- `artifacts/plots/*.png`
- `data/processed/model_features.csv`

## Notes

- Phase 2 does not include API, database, or frontend work.
- All Python code uses ASCII-only characters.
