import { useEffect, useState } from 'react'
import { fetchExperiment } from '../api/client'
import type { ExperimentMetric, ExperimentResponse } from '../api/types'
import PageHeader from '../components/PageHeader'
import SectionCard from '../components/SectionCard'
import StatusBadge from '../components/StatusBadge'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatPercent(value: number | null): string {
  if (value === null) return '-'
  return `${(value * 100).toFixed(1)}%`
}

function formatPValue(value: number | null): string {
  if (value === null) return '-'
  if (value < 0.001) return '<0.001'
  return value.toFixed(3)
}

const METRIC_GROUPS: Record<string, string[]> = {
  Activation: ['onboarding_completion_rate'],
  Profile: ['profile_completion_rate'],
  Retention: ['d7_retention_rate'],
}

function metricDisplayName(name: string): string {
  return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

function VariantTable({ variants }: { variants: ExperimentMetric[] }) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>Variant</th>
          <th>Sample Size</th>
          <th>Conversions</th>
          <th>Rate</th>
          <th>Absolute Lift</th>
          <th>Relative Lift</th>
          <th>p-value</th>
        </tr>
      </thead>
      <tbody>
        {variants.map((variant) => (
          <tr key={variant.variant_id}>
            <td><strong>{variant.variant_id}</strong></td>
            <td>{variant.sample_size.toLocaleString()}</td>
            <td>{variant.conversions.toLocaleString()}</td>
            <td>{formatPercent(variant.conversion_rate)}</td>
            <td className={variant.absolute_lift && variant.absolute_lift > 0 ? 'metric-positive' : ''}>
              {formatPercent(variant.absolute_lift)}
            </td>
            <td className={variant.relative_lift && variant.relative_lift > 0 ? 'metric-positive' : ''}>
              {formatPercent(variant.relative_lift)}
            </td>
            <td>{formatPValue(variant.p_value)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default function Experiment() {
  const [data, setData] = useState<ExperimentResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchExperiment()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorState title="Experiment unavailable" message={error} />
  if (!data) return <LoadingState message="Loading experiment..." />

  const srmOk = data.srm_p_value >= 0.05

  return (
    <div>
      <PageHeader
        title="Experiment"
        subtitle="Onboarding A/B test analysis with sample ratio mismatch check."
      />

      <div className="notice">
        This is a synthetic experiment demonstration. Reported lifts and p-values are generated from simulated data and should not be interpreted as causal claims about a real product.
      </div>

      <SectionCard title="Experiment Summary">
        <div className="profile-grid" style={{ marginBottom: 16 }}>
          <div className="profile-item">
            <span className="profile-label">Experiment ID</span>
            <span className="profile-value">{data.experiment_id}</span>
          </div>
          <div className="profile-item">
            <span className="profile-label">SRM p-value</span>
            <span className="profile-value">{data.srm_p_value.toFixed(4)}</span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Allocation Status</span>
            <span className="profile-value">
              {srmOk ? (
                <StatusBadge status="ok" label="Healthy allocation" />
              ) : (
                <StatusBadge status="warning" label="Potential SRM risk" />
              )}
            </span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Sample Sizes</span>
            <span className="profile-value">
              {Object.entries(data.sample_sizes)
                .map(([variant, size]) => `${variant}: ${size}`)
                .join(', ')}
            </span>
          </div>
        </div>
      </SectionCard>

      {Object.entries(METRIC_GROUPS).map(([groupName, metricKeys]) => (
        <SectionCard key={groupName} title={groupName}>
          {metricKeys.map((metricKey) => {
            const variants = data.metrics[metricKey]
            if (!variants) return null
            return (
              <div key={metricKey} style={{ marginBottom: 20 }}>
                <h3 className="section-title" style={{ fontSize: 14, marginBottom: 12 }}>
                  {metricDisplayName(metricKey)}
                </h3>
                <VariantTable variants={variants} />
              </div>
            )
          })}
        </SectionCard>
      ))}
    </div>
  )
}
