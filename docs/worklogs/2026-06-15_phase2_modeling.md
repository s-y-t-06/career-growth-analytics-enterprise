# Phase 2 Modeling Worklog

## Session

- Date: 2026-06-15
- Task: Implement Phase 2 churn prediction MVP for Career Growth Analytics

## Work Completed

1. Read required handoff documents:
   - `HANDOVER.md`
   - `PHASE1_REMEDIATION_REPORT.md`
   - `README.md`
   - `docs/methodology.md`
   - Verified git status and recent commits.

2. Implemented feature engineering:
   - `src/career_growth/features/model_features.py`
   - Pre-cutoff features for users, events, and experiment assignments.
   - Label attachment with leakage checks.

3. Implemented modeling modules:
   - `src/career_growth/modeling/split.py` -- chronological train/validation/test split.
   - `src/career_growth/modeling/pipeline.py` -- Logistic Regression and HistGradientBoosting pipelines.
   - `src/career_growth/modeling/evaluate.py` -- metrics, threshold selection, calibration.
   - `src/career_growth/modeling/explain.py` -- feature names, logistic coefficients, permutation importance.
   - `src/career_growth/modeling/train.py` -- train both models, select by validation PR-AUC, evaluate once on test.

4. Implemented training script:
   - `scripts/train_churn_model.py`
   - Generates or loads data, builds features, trains models, saves artifacts and plots.

5. Added tests:
   - `tests/test_model_features.py`
   - `tests/test_modeling.py`

6. Created documentation:
   - `notebooks/churn_modeling.ipynb`
   - `docs/model_card.md`
   - `PHASE2_MODELING_REPORT.md`
   - This worklog.

7. Updated exports:
   - `src/career_growth/features/__init__.py` now exposes feature-engineering helpers.

## Commands Used

```powershell
cd C:\Users\Administrator\Desktop\career-growth-analytics
$env:PYTHONPATH = "src"
.venv\Scripts\python.exe scripts/generate_data.py --count 5000 --seed 42
.venv\Scripts\python.exe scripts/train_churn_model.py --count 5000 --seed 42
.venv\Scripts\python.exe -m pytest tests -q
```

## 5,000-User Training Results

Selected model: `logistic_regression`
Operating threshold: `0.42`

Validation metrics:

- PR-AUC: 0.5562
- ROC-AUC: 0.7110
- Log loss: 0.6205
- Precision: 0.4926
- Recall: 0.8242
- F1: 0.6166
- Accuracy: 0.6270

Test metrics:

- PR-AUC: 0.5353
- ROC-AUC: 0.6926
- Log loss: 0.6375
- Precision: 0.4672
- Recall: 0.7830
- F1: 0.5852
- Accuracy: 0.5960

## Artifacts Produced

- `artifacts/churn_model.joblib`
- `artifacts/model_metadata.json`
- `artifacts/metrics.json`
- `artifacts/feature_schema.json`
- `artifacts/explainability.json`
- `artifacts/plots/*.png`

## Notes

- Phase 2 does not include API, database, or frontend work, per project constraints.
- All code and documentation use ASCII-only characters.
