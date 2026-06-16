import { useEffect, useState } from 'react'
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
import type { ModelMetricsResponse, SubgroupResponse, UserSummary } from '../api/types'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

export default function ChurnRisk() {
  const [users, setUsers] = useState<UserSummary[]>([])
  const [total, setTotal] = useState(0)
  const [metrics, setMetrics] = useState<ModelMetricsResponse | null>(null)
  const [subgroups, setSubgroups] = useState<SubgroupResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [minRisk, setMinRisk] = useState<number | ''>('')

  useEffect(() => {
    Promise.all([
      fetchUsers({ limit: 50, sort_by: 'risk' }),
      fetchModelMetrics(),
      fetchSubgroups(),
    ])
      .then(([u, m, s]) => {
        setUsers(u.users)
        setTotal(u.total)
        setMetrics(m)
        setSubgroups(s)
      })
      .catch((err) => setError(err.message))
  }, [])

  const handleFilter = () => {
    const params: { limit: number; sort_by: string; min_risk?: number } = {
      limit: 50,
      sort_by: 'risk',
    }
    if (typeof minRisk === 'number') params.min_risk = minRisk
    fetchUsers(params)
      .then((u) => {
        setUsers(u.users)
        setTotal(u.total)
      })
      .catch((err) => setError(err.message))
  }

  if (error) return <div className="error">Error: {error}</div>
  if (!metrics) return <div className="loading">Loading churn risk...</div>

  const distribution = [
    { range: '0-20%', count: users.filter((u) => u.churn_probability < 0.2).length },
    { range: '20-40%', count: users.filter((u) => u.churn_probability >= 0.2 && u.churn_probability < 0.4).length },
    { range: '40-60%', count: users.filter((u) => u.churn_probability >= 0.4 && u.churn_probability < 0.6).length },
    { range: '60-80%', count: users.filter((u) => u.churn_probability >= 0.6 && u.churn_probability < 0.8).length },
    { range: '80-100%', count: users.filter((u) => u.churn_probability >= 0.8).length },
  ]

  return (
    <div>
      <h1 className="page-title">Churn Risk</h1>

      <div className="card">
        <h2>Model Metrics</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Metric</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Selected Model</td>
              <td>{metrics.selected_model}</td>
            </tr>
            <tr>
              <td>Threshold</td>
              <td>{metrics.selected_threshold.toFixed(2)}</td>
            </tr>
            <tr>
              <td>PR-AUC</td>
              <td>{metrics.test.pr_auc.toFixed(4)}</td>
            </tr>
            <tr>
              <td>ROC-AUC</td>
              <td>{metrics.test.roc_auc.toFixed(4)}</td>
            </tr>
            <tr>
              <td>F1</td>
              <td>{metrics.test.f1_score.toFixed(4)}</td>
            </tr>
            <tr>
              <td>Brier</td>
              <td>{metrics.test.brier_score.toFixed(4)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Risk Distribution</h2>
        <div style={{ height: 240 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={distribution}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#dc2626" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {subgroups && (
        <div className="card">
          <h2>Subgroup Performance</h2>
          <table className="table">
            <thead>
              <tr>
                <th>Group</th>
                <th>Value</th>
                <th>Sample Size</th>
                <th>Churn Rate</th>
                <th>F1</th>
              </tr>
            </thead>
            <tbody>
              {subgroups.groups.map((g, idx) => (
                <tr key={idx}>
                  <td>{String(g.group_column)}</td>
                  <td>{String(g.group_value)}</td>
                  <td>{Number(g.sample_size).toLocaleString()}</td>
                  <td>{formatPercent(Number(g.churn_rate))}</td>
                  <td>{Number(g.f1_score).toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card">
        <h2>High-Risk Users</h2>
        <div className="filters">
          <input
            type="number"
            min={0}
            max={1}
            step={0.1}
            placeholder="Min risk"
            value={minRisk}
            onChange={(e) => setMinRisk(e.target.value === '' ? '' : Number(e.target.value))}
          />
          <button onClick={handleFilter}>Filter</button>
        </div>
        <p>Total: {total}</p>
        <table className="table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Channel</th>
              <th>Career Stage</th>
              <th>Device</th>
              <th>Risk</th>
              <th>Class</th>
              <th>Recommended Action</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.user_id}>
                <td>{user.user_id}</td>
                <td>{user.acquisition_channel}</td>
                <td>{user.career_stage}</td>
                <td>{user.device_type}</td>
                <td>{formatPercent(user.churn_probability)}</td>
                <td>
                  <span className={user.predicted_class ? 'badge badge-high' : 'badge badge-low'}>
                    {user.predicted_class ? 'High' : 'Low'}
                  </span>
                </td>
                <td>{user.recommended_action}</td>
                <td>
                  <Link to={`/users/${user.user_id}`}>Details</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
