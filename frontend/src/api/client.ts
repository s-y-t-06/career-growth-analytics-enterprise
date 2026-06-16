import type {
  ExperimentResponse,
  FunnelResponse,
  Health,
  ModelMetricsResponse,
  NBAResponse,
  Overview,
  RetentionResponse,
  ScoreResponse,
  SubgroupResponse,
  UserDetailResponse,
  UserListResponse,
} from './types'

const API_BASE = '/api'

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`)
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

export async function fetchHealth(): Promise<Health> {
  const response = await fetch('/health')
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json() as Promise<Health>
}

export const fetchOverview = () => get<Overview>('/overview')
export const fetchFunnel = () => get<FunnelResponse>('/funnel')
export const fetchRetention = () => get<RetentionResponse>('/retention')
export const fetchExperiment = () => get<ExperimentResponse>('/experiment')
export const fetchModelMetrics = () => get<ModelMetricsResponse>('/model/metrics')
export const fetchSubgroups = () => get<SubgroupResponse>('/model/subgroups')

export function fetchUsers(params: {
  limit?: number
  sort_by?: string
  min_risk?: number
  acquisition_channel?: string
  career_stage?: string
}): Promise<UserListResponse> {
  const search = new URLSearchParams()
  if (params.limit !== undefined) search.set('limit', String(params.limit))
  if (params.sort_by) search.set('sort_by', params.sort_by)
  if (params.min_risk !== undefined) search.set('min_risk', String(params.min_risk))
  if (params.acquisition_channel) search.set('acquisition_channel', params.acquisition_channel)
  if (params.career_stage) search.set('career_stage', params.career_stage)
  return get<UserListResponse>(`/users?${search.toString()}`)
}

export const fetchUserDetail = (userId: string) => get<UserDetailResponse>(`/users/${userId}`)
export const scoreUser = (userId: string) => post<ScoreResponse>('/users/score', { user_id: userId })
export const recommendNBA = (userId: string) => post<NBAResponse>('/nba/recommend', { user_id: userId })
