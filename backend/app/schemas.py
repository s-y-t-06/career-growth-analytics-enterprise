"""Pydantic schemas for API request and response models."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    database: str
    model: str
    metrics: str


class OverviewResponse(BaseModel):
    users: int
    events: int
    churn_rate: float
    d1_retention: float
    d7_retention: float
    d14_retention: float
    selected_model: str
    test_pr_auc: float
    test_roc_auc: float
    test_f1: float
    test_brier: float


class FunnelStep(BaseModel):
    step: str
    users: int
    conversion_rate: float
    drop_off_rate: float


class FunnelResponse(BaseModel):
    steps: list[FunnelStep]


class RetentionResponse(BaseModel):
    d1_retention: float
    d7_retention: float
    d14_retention: float
    cohorts: list[dict]


class ExperimentMetric(BaseModel):
    variant_id: str
    sample_size: int
    conversions: int
    conversion_rate: float
    absolute_lift: float | None
    relative_lift: float | None
    p_value: float | None
    ci_lower: float | None
    ci_upper: float | None


class ExperimentResponse(BaseModel):
    experiment_id: str
    sample_sizes: dict
    srm_chi2: float
    srm_p_value: float
    metrics: dict[str, list[ExperimentMetric]]


class ModelMetricsResponse(BaseModel):
    selected_model: str
    selected_threshold: float
    validation: dict
    test: dict
    confusion_matrix: dict


class SubgroupResponse(BaseModel):
    groups: list[dict]


class UserSummary(BaseModel):
    user_id: str
    acquisition_channel: str
    career_stage: str
    device_type: str
    churn_probability: float
    predicted_class: int
    recommended_action: str
    channel: str


class UserListResponse(BaseModel):
    users: list[UserSummary]
    total: int


class ModelExplanation(BaseModel):
    feature: str
    contribution: float


class UserDetailResponse(BaseModel):
    user_id: str
    profile: dict
    features: dict
    churn_probability: float
    predicted_class: int
    explanation: list[ModelExplanation]
    recommended_action: str
    channel: str
    reason: str
    timeline: list[dict]


class ScoreRequest(BaseModel):
    user_id: str = Field(..., min_length=1)


class ScoreResponse(BaseModel):
    user_id: str
    churn_probability: float
    predicted_class: int
    recommended_action: str
    channel: str
    reason: str


class NBARequest(BaseModel):
    user_id: str = Field(..., min_length=1)


class NBAResponse(BaseModel):
    user_id: str
    action_name: str
    channel: str
    reason: str
