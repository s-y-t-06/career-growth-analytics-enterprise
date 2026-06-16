import { useEffect, useState } from 'react'
import { fetchRetention } from '../api/client'
import type { RetentionResponse } from '../api/types'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

export default function Retention() {
  const [data, setData] = useState<RetentionResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchRetention()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <div className="error">Error: {error}</div>
  if (!data) return <div className="loading">Loading retention...</div>

  return (
    <div>
      <h1 className="page-title">Retention</h1>

      <div className="kpi-grid">
        <div className="kpi-card">
          <p className="kpi-label">D1 Retention</p>
          <p className="kpi-value">{formatPercent(data.d1_retention)}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">D7 Retention</p>
          <p className="kpi-value">{formatPercent(data.d7_retention)}</p>
        </div>
        <div className="kpi-card">
          <p className="kpi-label">D14 Retention</p>
          <p className="kpi-value">{formatPercent(data.d14_retention)}</p>
        </div>
      </div>

      <div className="card">
        <h2>Cohort Retention</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Cohort</th>
              <th>Users</th>
              <th>Day</th>
              <th>Retained</th>
              <th>Retention Rate</th>
            </tr>
          </thead>
          <tbody>
            {data.cohorts.map((row, idx) => (
              <tr key={idx}>
                <td>{String(row.signup_week)}</td>
                <td>{Number(row.users).toLocaleString()}</td>
                <td>{String(row.day)}</td>
                <td>{Number(row.retained).toLocaleString()}</td>
                <td>{formatPercent(Number(row.retention_rate))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
