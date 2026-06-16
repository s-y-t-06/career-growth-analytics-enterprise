import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchUserDetail } from '../api/client'
import type { UserDetailResponse } from '../api/types'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

export default function UserDetail() {
  const { userId } = useParams<{ userId: string }>()
  const [data, setData] = useState<UserDetailResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!userId) return
    fetchUserDetail(userId)
      .then(setData)
      .catch((err) => setError(err.message))
  }, [userId])

  if (error) return <div className="error">Error: {error}</div>
  if (!data) return <div className="loading">Loading user detail...</div>

  const profile = data.profile

  return (
    <div>
      <h1 className="page-title">User Detail</h1>

      <div className="card">
        <h2>Profile</h2>
        <table className="table">
          <tbody>
            <tr>
              <td>User ID</td>
              <td>{data.user_id}</td>
            </tr>
            <tr>
              <td>Acquisition Channel</td>
              <td>{String(profile.acquisition_channel)}</td>
            </tr>
            <tr>
              <td>Career Stage</td>
              <td>{String(profile.career_stage)}</td>
            </tr>
            <tr>
              <td>Device Type</td>
              <td>{String(profile.device_type)}</td>
            </tr>
            <tr>
              <td>Intent Level</td>
              <td>{String(profile.user_intent_level)}</td>
            </tr>
            <tr>
              <td>Marketing Consent</td>
              <td>{profile.marketing_consent ? 'Yes' : 'No'}</td>
            </tr>
            <tr>
              <td>Signup Time</td>
              <td>{String(profile.signup_timestamp)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Churn Prediction</h2>
        <p>
          Risk:{' '}
          <strong className={data.predicted_class ? 'metric-negative' : 'metric-positive'}>
            {formatPercent(data.churn_probability)}
          </strong>
        </p>
        <p>
          Predicted class:{' '}
          <span className={data.predicted_class ? 'badge badge-high' : 'badge badge-low'}>
            {data.predicted_class ? 'High Risk' : 'Low Risk'}
          </span>
        </p>
        <p>
          Recommended Action: <strong>{data.recommended_action}</strong> via {data.channel}
        </p>
        <p>Reason: {data.reason}</p>
      </div>

      <div className="card">
        <h2>Top Risk Factors</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Contribution</th>
            </tr>
          </thead>
          <tbody>
            {data.explanation.map((item, idx) => (
              <tr key={idx}>
                <td>{item.feature}</td>
                <td>{item.contribution.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Early Event Timeline</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Event</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {data.timeline.map((event, idx) => (
              <tr key={idx}>
                <td>{String(event.event_timestamp)}</td>
                <td>{String(event.event_name)}</td>
                <td>{String(event.event_source)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
