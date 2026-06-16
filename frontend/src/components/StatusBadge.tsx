interface StatusBadgeProps {
  status: 'ok' | 'warning' | 'error' | 'info'
  label: string
}

export default function StatusBadge({ status, label }: StatusBadgeProps) {
  return <span className={`status-badge status-${status}`}>{label}</span>
}
