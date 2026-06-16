import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { fetchFunnel } from '../api/client'
import type { FunnelResponse } from '../api/types'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

export default function Funnel() {
  const [data, setData] = useState<FunnelResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchFunnel()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <div className="error">Error: {error}</div>
  if (!data) return <div className="loading">Loading funnel...</div>

  return (
    <div>
      <h1 className="page-title">Funnel</h1>

      <div className="card">
        <h2>User Lifecycle Funnel</h2>
        <div style={{ height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.steps}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="step" tick={{ fontSize: 12 }} interval={0} angle={-20} textAnchor="end" />
              <YAxis />
              <Tooltip formatter={(value: number) => value.toLocaleString()} />
              <Bar dataKey="users" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h2>Funnel Breakdown</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Users</th>
              <th>Conversion Rate</th>
              <th>Drop-off Rate</th>
            </tr>
          </thead>
          <tbody>
            {data.steps.map((step) => (
              <tr key={step.step}>
                <td>{step.step}</td>
                <td>{step.users.toLocaleString()}</td>
                <td>{formatPercent(step.conversion_rate)}</td>
                <td>{formatPercent(step.drop_off_rate)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
