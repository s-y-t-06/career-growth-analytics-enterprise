interface RiskBarProps {
  probability: number
}

export default function RiskBar({ probability }: RiskBarProps) {
  const percent = Math.max(0, Math.min(1, probability)) * 100
  let level = 'low'
  if (probability >= 0.7) level = 'high'
  else if (probability >= 0.4) level = 'medium'

  return (
    <div className="risk-bar">
      <div className="risk-bar-track">
        <div className={`risk-bar-fill risk-${level}`} style={{ width: `${percent}%` }} />
      </div>
      <span className="risk-bar-label">{percent.toFixed(0)}%</span>
    </div>
  )
}
