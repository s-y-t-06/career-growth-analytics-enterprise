import { useEffect, useMemo, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts'
import { fetchFunnel } from '../api/client'
import type { FunnelResponse, FunnelStep } from '../api/types'
import PageHeader from '../components/PageHeader'
import SectionCard from '../components/SectionCard'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

function maxDropOffStep(steps: FunnelStep[]) {
  return steps
    .filter((s) => s.step !== 'signup')
    .reduce<FunnelStep | null>((max, step) => {
      if (!max || step.drop_off_rate > max.drop_off_rate) return step
      return max
    }, null)
}

export default function Funnel() {
  const [data, setData] = useState<FunnelResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchFunnel()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  const insight = useMemo(() => {
    if (!data) return null
    const worst = maxDropOffStep(data.steps)
    if (!worst) return null
    return `The largest drop-off appears at "${worst.step}" (${formatPercent(worst.drop_off_rate)} of users do not progress), suggesting activation is the main growth lever.`
  }, [data])

  if (error) return <ErrorState title="Funnel unavailable" message={error} />
  if (!data) return <LoadingState message="Loading funnel..." />

  return (
    <div>
      <PageHeader
        title="Funnel"
        subtitle="See where users drop out of the signup-to-activation journey."
      />

      <SectionCard title="User Lifecycle Funnel">
        <div style={{ height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.steps} margin={{ bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
              <XAxis
                dataKey="step"
                tick={{ fontSize: 12, fill: '#6b7280' }}
                interval={0}
                angle={-20}
                textAnchor="end"
                stroke="#e5e7eb"
              />
              <YAxis tick={{ fontSize: 12, fill: '#6b7280' }} stroke="#e5e7eb" />
              <Tooltip formatter={(value: number) => value.toLocaleString()} />
              <Bar dataKey="users" radius={[4, 4, 0, 0]}>
                {data.steps.map((_, idx) => (
                  <Cell key={`cell-${idx}`} fill={idx === 0 ? '#2563eb' : '#3b82f6'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </SectionCard>

      <SectionCard title="Funnel Breakdown">
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
            {data.steps.map((step) => {
              const isWorst = step.step === maxDropOffStep(data.steps)?.step
              return (
                <tr key={step.step} className={isWorst ? 'row-highlight' : ''}>
                  <td>
                    <strong>{step.step}</strong>
                    {isWorst && <span className="badge badge-high" style={{ marginLeft: 8 }}>Highest drop-off</span>}
                  </td>
                  <td>{step.users.toLocaleString()}</td>
                  <td>{formatPercent(step.conversion_rate)}</td>
                  <td className="metric-negative">{formatPercent(step.drop_off_rate)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </SectionCard>

      {insight && (
        <div className="insight-box">
          <strong>Business insight:</strong> {insight}
        </div>
      )}
    </div>
  )
}
