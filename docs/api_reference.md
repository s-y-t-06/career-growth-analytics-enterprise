# API Reference

Base URL: `http://localhost:8000`

Interactive docs are available at `http://localhost:8000/docs`.

## Health

### GET /health

Return backend, database, model, and metrics status.

**Response**

```json
{
  "status": "ok",
  "database": "ok",
  "model": "ok",
  "metrics": "ok"
}
```

## Overview

### GET /api/overview

Return platform and model overview.

**Response**

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

## Funnel

### GET /api/funnel

Return the core user lifecycle funnel.

**Response**

```json
{
  "steps": [
    {
      "step": "signup",
      "users": 1000,
      "conversion_rate": 1.0,
      "drop_off_rate": 0.0
    }
  ]
}
```

## Retention

### GET /api/retention

Return D1/D7/D14 retention and cohort retention.

**Response**

```json
{
  "d1_retention": 0.674,
  "d7_retention": 0.467,
  "d14_retention": 0.079,
  "cohorts": [
    {
      "signup_week": "2026-02-23/2026-03-01",
      "day": 1,
      "users": 50,
      "retained": 34,
      "retention_rate": 0.68
    }
  ]
}
```

## Experiment

### GET /api/experiment

Return onboarding A/B experiment analysis.

**Response**

```json
{
  "experiment_id": "exp_onboarding_v1",
  "sample_sizes": {"control": 400, "personalized": 300, "simplified": 300},
  "srm_chi2": 1.5,
  "srm_p_value": 0.4726,
  "metrics": {
    "onboarding_completion_rate": [
      {
        "variant_id": "control",
        "sample_size": 400,
        "conversions": 200,
        "conversion_rate": 0.5,
        "absolute_lift": null,
        "relative_lift": null,
        "p_value": null,
        "ci_lower": null,
        "ci_upper": null
      }
    ]
  }
}
```

## Model

### GET /api/model/metrics

Return model metrics from artifacts.

### GET /api/model/subgroups

Return subgroup evaluation metrics.

## Users

### GET /api/users

Return scored users with filters.

**Query parameters**

- `limit` (int, default 50)
- `sort_by` (string, default `risk`)
- `min_risk` (float, 0-1)
- `acquisition_channel` (string)
- `career_stage` (string)

### GET /api/users/{user_id}

Return detailed profile, risk, explanation, and timeline.

### POST /api/users/score

Score a single user.

**Request**

```json
{"user_id": "u123"}
```

**Response**

```json
{
  "user_id": "u123",
  "churn_probability": 0.83,
  "predicted_class": 1,
  "recommended_action": "send_reengagement_message",
  "channel": "email",
  "reason": "high churn risk with marketing consent"
}
```

## Next Best Action

### GET /api/nba/examples

Return example recommendations.

### POST /api/nba/recommend

Return a recommendation for a user.

**Request**

```json
{"user_id": "u123"}
```

**Response**

```json
{
  "user_id": "u123",
  "action_name": "send_reengagement_message",
  "channel": "email",
  "reason": "high churn risk with marketing consent"
}
```
