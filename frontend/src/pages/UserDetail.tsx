import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchUserDetail } from '../api/client'
import type { UserDetailResponse } from '../api/types'
import PageHeader from '../components/PageHeader'
import SectionCard from '../components/SectionCard'
import RiskBar from '../components/RiskBar'
import StatusBadge from '../components/StatusBadge'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatTimestamp(value: string): string {
  try {
    return new Date(value).toLocaleString()
  } catch {
    return value
  }
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

  if (error) {
    return (
      <ErrorState
        title="User not found"
        message={error.includes('404') ? `No user found for ID ${userId}.` : error}
      />
    )
  }
  if (!data) return <LoadingState message="Loading user detail..." />

  const profile = data.profile

  return (
    <div>
      <PageHeader title="User Detail" subtitle="Profile, churn risk, key drivers, and recommended action." />

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="profile-grid">
          <div className="profile-item">
            <span className="profile-label">User ID</span>
            <span className="profile-value">{data.user_id}</span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Churn Probability</span>
            <span className="profile-value">
              <RiskBar probability={data.churn_probability} />
            </span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Predicted Class</span>
            <span className="profile-value">
              {data.predicted_class ? (
                <StatusBadge status="error" label="High Risk" />
              ) : (
                <StatusBadge status="ok" label="Low Risk" />
              )}
            </span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Recommended Action</span>
            <span className="profile-value">{data.recommended_action}</span>
          </div>
          <div className="profile-item">
            <span className="profile-label">Channel</span>
            <span className="profile-value">{data.channel}</span>
          </div>
        </div>
      </div>

      <div className="two-column">
        <SectionCard title="Profile">
          <div className="profile-grid">
            <div className="profile-item">
              <span className="profile-label">Acquisition Channel</span>
              <span className="profile-value">{profile.acquisition_channel ?? '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Country</span>
              <span className="profile-value">{profile.country ?? '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Device Type</span>
              <span className="profile-value">{profile.device_type ?? '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Career Stage</span>
              <span className="profile-value">{profile.career_stage ?? '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Intent Level</span>
              <span className="profile-value">{profile.user_intent_level ?? '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Marketing Consent</span>
              <span className="profile-value">{profile.marketing_consent ? 'Yes' : 'No'}</span>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Next Best Action">
          <div className="profile-grid">
            <div className="profile-item">
              <span className="profile-label">Action</span>
              <span className="profile-value">{data.recommended_action}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Channel</span>
              <span className="profile-value">{data.channel}</span>
            </div>
            <div className="profile-item" style={{ gridColumn: '1 / -1' }}>
              <span className="profile-label">Reason</span>
              <span className="profile-value">{data.reason}</span>
            </div>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Top Risk Factors">
        <p className="section-subtitle">
          Features that push the model toward a high or low churn prediction.
        </p>
        <table className="table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Contribution</th>
              <th>Direction</th>
            </tr>
          </thead>
          <tbody>
            {data.explanation.map((item, idx) => (
              <tr key={idx}>
                <td>{item.feature}</td>
                <td>{item.contribution.toFixed(4)}</td>
                <td>
                  {item.contribution > 0 ? (
                    <span className="badge badge-high">Higher risk</span>
                  ) : item.contribution < 0 ? (
                    <span className="badge badge-low">Lower risk</span>
                  ) : (
                    <span className="badge badge-info">Neutral</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </SectionCard>

      <SectionCard title="Early Event Timeline">
        <p className="section-subtitle">Events before the 7-day prediction cutoff.</p>
        <table className="table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Event</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {data.timeline.length === 0 ? (
              <tr>
                <td colSpan={3} style={{ textAlign: 'center', color: '#6b7280' }}>
                  No events before cutoff.
                </td>
              </tr>
            ) : (
              data.timeline.map((event, idx) => (
                <tr key={idx}>
                  <td>{formatTimestamp(event.event_timestamp)}</td>
                  <td>{event.event_name}</td>
                  <td>{event.event_source}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </SectionCard>
    </div>
  )
}
