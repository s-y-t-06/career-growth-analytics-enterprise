import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { fetchModelMetrics, fetchSubgroups, fetchUsers } from '../api/client'
import type { ModelMetricsResponse, Subgroup, SubgroupResponse, UserSummary } from '../api/types'
import PageHeader from '../components/PageHeader'
import KpiCard from '../components/KpiCard'
import SectionCard from '../components/SectionCard'
import RiskBar from '../components/RiskBar'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import EmptyState from '../components/EmptyState'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

function buildDistribution(users: UserSummary[]) {
  return [
    { range: '0-20%', count: users.filter((u) => u.churn_probability < 0.2).length },
    { range: '20-40%', count: users.filter((u) => u.churn_probability >= 0.2 && u.churn_probability < 0.4).length },
    { range: '40-60%', count: users.filter((u) => u.churn_probability >= 0.4 && u.churn_probability < 0.6).length },
    { range: '60-80%', count: users.filter((u) => u.churn_probability >= 0.6 && u.churn_probability < 0.8).length },
    { range: '80-100%', count: users.filter((u) => u.churn_probability >= 0.8).length },
  ]
}

export default function ChurnRisk() {
  const [allUsers, setAllUsers] = useState<UserSummary[]>([])
  const [metrics, setMetrics] = useState<ModelMetricsResponse | null>(null)
  const [subgroups, setSubgroups] = useState<SubgroupResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [minRisk, setMinRisk] = useState<string>('')
  const [channelFilter, setChannelFilter] = useState<string>('')
  const [stageFilter, setStageFilter] = useState<string>('')

  useEffect(() => {
    Promise.all([
      fetchUsers({ limit: 1000, sort_by: 'risk' }),
      fetchModelMetrics(),
      fetchSubgroups(),
    ])
      .then(([u, m, s]) => {
        setAllUsers(u.users)
        setMetrics(m)
        setSubgroups(s)
      })
      .catch((err) => setError(err.message))
  }, [])

  const channels = useMemo(
    () => Array.from(new Set(allUsers.map((u) => u.acquisition_channel))).sort(),
    [allUsers]
  )
  const careerStages = useMemo(
    () => Array.from(new Set(allUsers.map((u) => u.career_stage))).sort(),
    [allUsers]
  )

  const filteredUsers = useMemo(() => {
    const min = minRisk === '' ? 0 : Number(minRisk)
    return allUsers.filter((u) => {
      if (u.churn_probability < min) return false
      if (channelFilter && u.acquisition_channel !== channelFilter) return false
      if (stageFilter && u.career_stage !== stageFilter) return false
      return true
    })
  }, [allUsers, minRisk, channelFilter, stageFilter])

  const displayedUsers = useMemo(() => filteredUsers.slice(0, 50), [filteredUsers])
  const distribution = useMemo(() => buildDistribution(filteredUsers), [filteredUsers])

  if (error) return <ErrorState title="Churn risk unavailable" message={error} />
  if (!metrics) return <LoadingState message="Loading churn risk..." />

  return (
    <div>
      <PageHeader
        title="Churn Risk"
        subtitle="Model performance, risk distribution, subgroup metrics, and high-risk users."
      />

      <div className="kpi-grid">
        <KpiCard label="PR-AUC" value={metrics.test.pr_auc.toFixed(4)} helper="Precision-recall AUC" />
        <KpiCard label="ROC-AUC" value={metrics.test.roc_auc.toFixed(4)} helper="Ranking discrimination" />
        <KpiCard label="Brier" value={metrics.test.brier_score.toFixed(4)} helper="Probability calibration" />
        <KpiCard label="F1" value={metrics.test.f1_score.toFixed(4)} helper="Precision-recall balance" />
        <KpiCard label="Threshold" value={metrics.selected_threshold.toFixed(2)} helper="Operating threshold" />
      </div>

      <SectionCard title="Risk Distribution">
        <div style={{ height: 240 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={distribution} margin={{ bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
              <XAxis dataKey="range" tick={{ fontSize: 12, fill: '#6b7280' }} stroke="#e5e7eb" />
              <YAxis tick={{ fontSize: 12, fill: '#6b7280' }} stroke="#e5e7eb" />
              <Tooltip />
              <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </SectionCard>

      {subgroups && (
        <SectionCard title="Subgroup Performance">
          <table className="table">
            <thead>
              <tr>
                <th>Group</th>
                <th>Segment</th>
                <th>Sample Size</th>
                <th>Churn Rate</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1</th>
                <th>Flag</th>
              </tr>
            </thead>
            <tbody>
              {subgroups.groups.map((g: Subgroup, idx: number) => (
                <tr key={idx}>
                  <td>{g.group_column}</td>
                  <td><strong>{g.group_value}</strong></td>
                  <td>{g.sample_size.toLocaleString()}</td>
                  <td>{formatPercent(g.churn_rate)}</td>
                  <td>{g.precision.toFixed(3)}</td>
                  <td>{g.recall.toFixed(3)}</td>
                  <td>{g.f1_score.toFixed(3)}</td>
                  <td>
                    {g.small_sample ? (
                      <span className="small-sample-flag">Small sample</span>
                    ) : (
                      <span className="metric-muted">-</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </SectionCard>
      )}

      <SectionCard title="High-Risk Users">
        <div className="filters">
          <div className="filter-group">
            <label>Min Risk</label>
            <input
              type="number"
              min={0}
              max={1}
              step={0.1}
              placeholder="0.0 - 1.0"
              value={minRisk}
              onChange={(e) => setMinRisk(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>Acquisition Channel</label>
            <select value={channelFilter} onChange={(e) => setChannelFilter(e.target.value)}>
              <option value="">All channels</option>
              {channels.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
          <div className="filter-group">
            <label>Career Stage</label>
            <select value={stageFilter} onChange={(e) => setStageFilter(e.target.value)}>
              <option value="">All stages</option>
              {careerStages.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <button
            className="button button-secondary"
            onClick={() => {
              setMinRisk('')
              setChannelFilter('')
              setStageFilter('')
            }}
          >
            Reset
          </button>
        </div>

        <p className="section-subtitle" style={{ marginTop: -8 }}>
          Showing {displayedUsers.length} of {filteredUsers.length} matching users
        </p>

        {displayedUsers.length === 0 ? (
          <EmptyState message="No users match the selected filters." />
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Risk</th>
                <th>Class</th>
                <th>Acquisition Channel</th>
                <th>Career Stage</th>
                <th>Recommended Action</th>
                <th>Recommended Channel</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {displayedUsers.map((user) => (
                <tr key={user.user_id}>
                  <td>{user.user_id}</td>
                  <td>
                    <RiskBar probability={user.churn_probability} />
                  </td>
                  <td>
                    <span className={user.predicted_class ? 'badge badge-high' : 'badge badge-low'}>
                      {user.predicted_class ? 'High' : 'Low'}
                    </span>
                  </td>
                  <td>{user.acquisition_channel}</td>
                  <td>{user.career_stage}</td>
                  <td>{user.recommended_action}</td>
                  <td>{user.channel}</td>
                  <td>
                    <Link to={`/users/${user.user_id}`} className="button detail-link-button">
                      Details
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </SectionCard>
    </div>
  )
}
