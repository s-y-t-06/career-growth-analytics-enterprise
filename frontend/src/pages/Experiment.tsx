import { useEffect, useState } from 'react'
import { fetchExperiment } from '../api/client'
import type { ExperimentResponse } from '../api/types'

function formatPercent(value: number | null): string {
  if (value === null) return '-'
  return `${(value * 100).toFixed(1)}%`
}

export default function Experiment() {
  const [data, setData] = useState<ExperimentResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchExperiment()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <div className="error">Error: {error}</div>
  if (!data) return <div className="loading">Loading experiment...</div>

  const srmOk = data.srm_p_value >= 0.05

  return (
    <div>
      <h1 className="page-title">Experiment</h1>

      <div className="card">
        <h2>Onboarding A/B Test</h2>
        <p>
          Experiment ID: <strong>{data.experiment_id}</strong>
        </p>
        <p>
          SRM p-value:{' '}
          <span className={srmOk ? 'metric-positive' : 'metric-negative'}>
            {data.srm_p_value.toFixed(4)} {srmOk ? '(OK)' : '(Warning)'}
          </span>
        </p>
        <p>
          Sample sizes:{' '}
          {Object.entries(data.sample_sizes)
            .map(([variant, size]) => `${variant}: ${size}`)
            .join(', ')}
        </p>
      </div>

      {Object.entries(data.metrics).map(([metricName, variants]) => (
        <div className="card" key={metricName}>
          <h2>{metricName.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}</h2>
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
                  <td>{variant.variant_id}</td>
                  <td>{variant.sample_size}</td>
                  <td>{variant.conversions}</td>
                  <td>{formatPercent(variant.conversion_rate)}</td>
                  <td>{formatPercent(variant.absolute_lift)}</td>
                  <td>{formatPercent(variant.relative_lift)}</td>
                  <td>
                    {variant.p_value === null
                      ? '-'
                      : variant.p_value.toFixed(4)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  )
}
