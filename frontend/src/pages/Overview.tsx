import { useEffect, useState } from 'react'
import { fetchHealth, fetchOverview } from '../api/client'
import type { Health, Overview } from '../api/types'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

export default function Overview() {
  const [health, setHealth] = useState<Health | null>(null)
  const [overview, setOverview] = useState<Overview | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([fetchHealth(), fetchOverview()])
      .then(([h, o]) => {
        setHealth(h)
        setOverview(o)
      })
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <div className="error">Error: {error}</div>
  if (!overview) return <div className="loading">Loading overview...</div>

  return (
    <div>
      <h1 className="page-title">Overview Dashboard</h1>

      {health && (
        <div className="card">
          <h2>System Health</h2>
          <p>
            Backend: <span className="metric-positive">{health.status}</span> | Database:{' '}
            <span className="metric-positive">{health.database}</span> | Model: {health.model} | Metrics:{' '}
            {health.metrics}
          </p>
        </div>
      )}

      <div className="kpi-grid">
        <div className="kpi-card">
          <p className="kpi-label">Users</p>
          <p className="kpi-value">{overview.users.toLocaleString()}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">Events</p>
          <p className="kpi-value">{overview.events.toLocaleString()}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">Churn Rate</p>
          <p className="kpi-value metric-negative">{formatPercent(overview.churn_rate)}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">D1 Retention</p>
          <p className="kpi-value">{formatPercent(overview.d1_retention)}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">D7 Retention</p>
          <p className="kpi-value">{formatPercent(overview.d7_retention)}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">D14 Retention</p>
          <p className="kpi-value">{formatPercent(overview.d14_retention)}</p>
        </div>
      </div>

      <div className="card">
        <h2>Model Performance</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Model</th>
              <th>PR-AUC</th>
              <th>ROC-AUC</th>
              <th>F1</th>
              <th>Brier</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{overview.selected_model}</td>
              <td>{overview.test_pr_auc.toFixed(4)}</td>
              <td>{overview.test_roc_auc.toFixed(4)}</td>
              <td>{overview.test_f1.toFixed(4)}</td>
              <td>{overview.test_brier.toFixed(4)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
