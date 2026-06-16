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

export interface RetentionResponse {
  d1_retention: number
  d7_retention: number
  d14_retention: number
  cohorts: Array<Record<string, unknown>>
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

export interface SubgroupResponse {
  groups: Array<Record<string, unknown>>
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

export interface UserDetailResponse {
  user_id: string
  profile: Record<string, unknown>
  features: Record<string, unknown>
  churn_probability: number
  predicted_class: number
  explanation: Array<{ feature: string; contribution: number }>
  recommended_action: string
  channel: string
  reason: string
  timeline: Array<Record<string, unknown>>
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
