interface EmptyStateProps {
  message?: string
}

export default function EmptyState({ message = 'No data available.' }: EmptyStateProps) {
  return (
    <div className="state-container">
      <p className="state-message">{message}</p>
    </div>
  )
}
