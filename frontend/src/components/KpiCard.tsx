interface KpiCardProps {
  label: string
  value: string
  helper?: string
  variant?: 'neutral' | 'positive' | 'negative' | 'highlight'
}

export default function KpiCard({ label, value, helper, variant = 'neutral' }: KpiCardProps) {
  const valueClass = `kpi-value ${variant === 'positive' ? 'metric-positive' : ''} ${variant === 'negative' ? 'metric-negative' : ''} ${variant === 'highlight' ? 'metric-highlight' : ''}`

  return (
    <div className="kpi-card">
      <p className="kpi-label">{label}</p>
      <p className={valueClass}>{value}</p>
      {helper && <p className="kpi-helper">{helper}</p>}
    </div>
  )
}
