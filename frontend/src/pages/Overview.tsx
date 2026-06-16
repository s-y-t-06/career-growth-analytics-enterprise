import { useEffect, useState } from 'react'
import { fetchOverview } from '../api/client'
import type { Overview } from '../api/types'
import PageHeader from '../components/PageHeader'
import KpiCard from '../components/KpiCard'
import SectionCard from '../components/SectionCard'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}

function formatNumber(value: number): string {
  return value.toLocaleString()
}

export default function Overview() {
  const [overview, setOverview] = useState<Overview | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchOverview()
      .then(setOverview)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return (
      <ErrorState
        title="Overview unavailable"
        message={error.includes('fetch') ? 'Backend API is unavailable. Start FastAPI on http://localhost:8000.' : error}
      />
    )
  }
  if (!overview) return <LoadingState message="Loading overview..." />

  return (
    <div>
      <PageHeader
        title="Overview Dashboard"
        subtitle="Monitor activation, retention, experiment performance, churn risk, and next-best actions for an AI career platform."
      />

      <div className="kpi-grid">
        <KpiCard label="Users" value={formatNumber(overview.users)} helper="Total registered users in sample" />
        <KpiCard label="Events" value={formatNumber(overview.events)} helper="Tracked platform events" />
        <KpiCard
          label="Churn Rate"
          value={formatPercent(overview.churn_rate)}
          helper="Share inactive in days 8-21"
          variant="negative"
        />
        <KpiCard label="D7 Retention" value={formatPercent(overview.d7_retention)} helper="Users active 7 days after signup" />
        <KpiCard label="Selected Model" value={overview.selected_model} helper="Model chosen by validation PR-AUC" variant="highlight" />
        <KpiCard label="Test PR-AUC" value={overview.test_pr_auc.toFixed(4)} helper="Precision-recall AUC on test set" />
        <KpiCard label="Test ROC-AUC" value={overview.test_roc_auc.toFixed(4)} helper="Ranking quality on test set" />
        <KpiCard label="Test F1" value={overview.test_f1.toFixed(4)} helper="Precision-recall balance" />
      </div>

      <div className="two-column">
        <SectionCard title="What to watch">
          <ul className="watch-list">
            <li>
              <span className="watch-list-marker" />
              <div>
                <p className="watch-list-title">Activation funnel drop-off</p>
                <p className="watch-list-desc">Identify where users stop progressing after signup.</p>
              </div>
            </li>
            <li>
              <span className="watch-list-marker" />
              <div>
                <p className="watch-list-title">Early retention</p>
                <p className="watch-list-desc">D1 and D7 retention are leading indicators of long-term engagement.</p>
              </div>
            </li>
            <li>
              <span className="watch-list-marker" />
              <div>
                <p className="watch-list-title">High-risk users</p>
                <p className="watch-list-desc">Prioritize outreach before users leave the platform.</p>
              </div>
            </li>
            <li>
              <span className="watch-list-marker" />
              <div>
                <p className="watch-list-title">Recommended interventions</p>
                <p className="watch-list-desc">Match each user with the right channel and action.</p>
              </div>
            </li>
          </ul>
        </SectionCard>

        <SectionCard title="Demo flow">
          <p className="section-subtitle">Suggested video walkthrough order</p>
          <div className="demo-flow">
            <span className="demo-flow-step">Overview</span>
            <span className="demo-flow-arrow">-&gt;</span>
            <span className="demo-flow-step">Funnel</span>
            <span className="demo-flow-arrow">-&gt;</span>
            <span className="demo-flow-step">Retention</span>
            <span className="demo-flow-arrow">-&gt;</span>
            <span className="demo-flow-step">Experiment</span>
            <span className="demo-flow-arrow">-&gt;</span>
            <span className="demo-flow-step">Churn Risk</span>
            <span className="demo-flow-arrow">-&gt;</span>
            <span className="demo-flow-step">User Detail</span>
          </div>
        </SectionCard>
      </div>
    </div>
  )
}
