# Phase 2 Modeling Report: Churn Prediction

## 1. Objective

Build a reproducible churn-prediction MVP that scores users at the end of their first week and identifies the most impactful pre-cutoff behavioral signals.

## 2. Label Definition

- Prediction cutoff: `signup_timestamp + 7 days`.
- Label window: days 8-21 after signup (inclusive).
- `is_churned = 1` if the user has zero `event_source == "user_action"` events in the label window.

## 3. Feature Engineering

Features are computed in `src/career_growth/features/model_features.py` and are strictly limited to pre-cutoff events:

- Static user attributes: `acquisition_channel`, `country`, `device_type`, `user_intent_level`, `career_stage`, `marketing_consent`.
- Temporal signals: `signup_hour`, `signup_day_of_week`.
- Experiment feature: `onboarding_variant`.
- Core funnel indicators: `onboarding_started`, `onboarding_complete`, `profile_complete`, `resume_upload`, `job_recommendation_view`, `job_save`, `growth_task_complete`, `career_report_generate`.
- Behavioral aggregates: `num_core_actions_completed`, `num_sessions`, `num_user_actions`, `num_days_active`, `num_email_sent`, `num_push_sent`, `num_in_app_sent`, `avg_events_per_session`, `max_events_in_session`, `total_user_actions_in_sessions`.

Leakage guardrails:

- `check_label_leakage` rejects forbidden prefixes (`future_`, `post_`, `label_`) and columns such as `last_active_date`, `days_since_last_active`, `is_churned`.
- Hidden propensity variables are never persisted or used as features.

## 4. Data Split

Chronological 60% / 20% / 20% split by `signup_timestamp`:

- No user overlap across splits.
- Training set precedes validation set; validation set precedes test set.
- This mirrors a real deployment where models are trained on older users and scored on newer users.

## 5. Models

Two scikit-learn pipelines are trained:

1. **Logistic Regression baseline**:
   - OneHotEncoder (`handle_unknown="infrequent_if_exist"`, `min_frequency=0.01`).
   - StandardScaler for numeric features.
   - `class_weight="balanced"`.

2. **HistGradientBoostingClassifier**:
   - OneHotEncoder for categorical features.
   - Native tree boosting for numeric features.
   - Early stopping with `n_iter_no_change=10`.

## 6. Selection and Evaluation Protocol

- Selection metric: PR-AUC on the validation set.
- Operating threshold: chosen on the validation set using F1 score (configurable via `--threshold-criterion`).
- Final evaluation: computed exactly once on the held-out test set.
- Metrics reported: PR-AUC, ROC-AUC, log loss, precision, recall, F1, accuracy.
- Calibration assessed with a reliability diagram.

## 7. Artifacts

The training script `scripts/train_churn_model.py` produces:

- `artifacts/churn_model.joblib`
- `artifacts/model_metadata.json`
- `artifacts/metrics.json`
- `artifacts/feature_schema.json`
- `artifacts/explainability.json`
- `artifacts/plots/pr_curve.png`
- `artifacts/plots/roc_curve.png`
- `artifacts/plots/calibration.png`
- `artifacts/plots/feature_importance.png`

## 8. Explainability

- Logistic-regression coefficients are reported when the linear model is selected.
- Permutation importance (drop in PR-AUC) is computed on the validation set for both models.

## 9. Limitations and Next Steps

- Data is synthetic; causal effects are calibrated for pipeline demonstration only.
- No API, database, or frontend is introduced in this phase.
- Future work may include hyper-parameter tuning, real-data retraining, subgroup fairness analysis, and integration with the Next Best Action engine via a lightweight scoring service.
