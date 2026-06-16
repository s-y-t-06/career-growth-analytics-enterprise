import { useEffect, useMemo, useState } from 'react'
import { fetchRetention } from '../api/client'
import type { CohortRow, RetentionResponse } from '../api/types'
import PageHeader from '../components/PageHeader'
import KpiCard from '../components/KpiCard'
import SectionCard from '../components/SectionCard'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

function retentionClass(rate: number): string {
  if (rate < 0.2) return 'retention-low'
  if (rate < 0.5) return 'retention-medium'
  return 'retention-high'
}

interface CohortSummary {
  signup_week: string
  users: number
  d1: number | null
  d7: number | null
  d14: number | null
}

function buildCohortSummary(cohorts: CohortRow[]): CohortSummary[] {
  const map = new Map<string, CohortSummary>()
  for (const row of cohorts) {
    if (!map.has(row.signup_week)) {
      map.set(row.signup_week, {
        signup_week: row.signup_week,
        users: row.users,
        d1: null,
        d7: null,
        d14: null,
      })
    }
    const summary = map.get(row.signup_week)!
    if (row.day === 1) summary.d1 = row.retention_rate
    if (row.day === 7) summary.d7 = row.retention_rate
    if (row.day === 14) summary.d14 = row.retention_rate
  }
  return Array.from(map.values())
}

export default function Retention() {
  const [data, setData] = useState<RetentionResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchRetention()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  const cohortSummary = useMemo(() => {
    if (!data) return []
    return buildCohortSummary(data.cohorts)
  }, [data])

  if (error) return <ErrorState title="Retention unavailable" message={error} />
  if (!data) return <LoadingState message="Loading retention..." />

  return (
    <div>
      <PageHeader
        title="Retention"
        subtitle="Retention is measured from user_action events after signup."
      />

      <div className="kpi-grid">
        <KpiCard label="D1 Retention" value={formatPercent(data.d1_retention)} helper="Users active 1 day after signup" />
        <KpiCard label="D7 Retention" value={formatPercent(data.d7_retention)} helper="Users active 7 days after signup" />
        <KpiCard label="D14 Retention" value={formatPercent(data.d14_retention)} helper="Users active 14 days after signup" />
      </div>

      <SectionCard title="Cohort Retention">
        <table className="table cohort-table">
          <thead>
            <tr>
              <th>Cohort</th>
              <th>Users</th>
              <th>D1</th>
              <th>D7</th>
              <th>D14</th>
            </tr>
          </thead>
          <tbody>
            {cohortSummary.map((row) => (
              <tr key={row.signup_week}>
                <td>{row.signup_week}</td>
                <td>{row.users.toLocaleString()}</td>
                <td className={row.d1 !== null ? retentionClass(row.d1) : ''}>
                  {row.d1 !== null ? formatPercent(row.d1) : '-'}
                </td>
                <td className={row.d7 !== null ? retentionClass(row.d7) : ''}>
                  {row.d7 !== null ? formatPercent(row.d7) : '-'}
                </td>
                <td className={row.d14 !== null ? retentionClass(row.d14) : ''}>
                  {row.d14 !== null ? formatPercent(row.d14) : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </SectionCard>
    </div>
  )
}
