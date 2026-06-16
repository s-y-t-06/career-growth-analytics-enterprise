export interface Health {
  status: string
  database: string
  model: string
  metrics: string
}

export interface Overview {
  users: number
  events: number
  churn_rate: number
  d1_retention: number
  d7_retention: number
  d14_retention: number
  selected_model: string
  test_pr_auc: number
  test_roc_auc: number
  test_f1: number
  test_brier: number
}

export interface FunnelStep {
  step: string
  users: number
  conversion_rate: number
  drop_off_rate: number
}

export interface FunnelResponse {
  steps: FunnelStep[]
}

export interface CohortRow {
  signup_week: string
  day: number
  users: number
  retained: number
  retention_rate: number
}

export interface RetentionResponse {
  d1_retention: number
  d7_retention: number
  d14_retention: number
  cohorts: CohortRow[]
}

export interface ExperimentMetric {
  variant_id: string
  sample_size: number
  conversions: number
  conversion_rate: number
  absolute_lift: number | null
  relative_lift: number | null
  p_value: number | null
  ci_lower: number | null
  ci_upper: number | null
}

export interface ExperimentResponse {
  experiment_id: string
  sample_sizes: Record<string, number>
  srm_chi2: number
  srm_p_value: number
  metrics: Record<string, ExperimentMetric[]>
}

export interface ModelMetricsResponse {
  selected_model: string
  selected_threshold: number
  validation: Record<string, number>
  test: Record<string, number>
  confusion_matrix: Record<string, number>
}

export interface Subgroup {
  group_column: string
  group_value: string
  sample_size: number
  churn_rate: number
  precision: number
  recall: number
  f1_score: number
  predicted_positive_rate: number
  small_sample: boolean
}

export interface SubgroupResponse {
  groups: Subgroup[]
}

export interface UserSummary {
  user_id: string
  acquisition_channel: string
  career_stage: string
  device_type: string
  churn_probability: number
  predicted_class: number
  recommended_action: string
  channel: string
}

export interface UserListResponse {
  users: UserSummary[]
  total: number
}

export interface UserProfile {
  acquisition_channel: string | null
  country: string | null
  device_type: string | null
  user_intent_level: string | null
  career_stage: string | null
  marketing_consent: boolean
  language: string | null
  timezone: string | null
  signup_timestamp: string
}

export interface ModelExplanation {
  feature: string
  contribution: number
}

export interface TimelineEvent {
  event_name: string
  event_timestamp: string
  event_source: string
}

export interface UserDetailResponse {
  user_id: string
  profile: UserProfile
  features: Record<string, unknown>
  churn_probability: number
  predicted_class: number
  explanation: ModelExplanation[]
  recommended_action: string
  channel: string
  reason: string
  timeline: TimelineEvent[]
}

export interface ScoreResponse {
  user_id: string
  churn_probability: number
  predicted_class: number
  recommended_action: string
  channel: string
  reason: string
}

export interface NBAResponse {
  user_id: string
  action_name: string
  channel: string
  reason: string
}
