interface LoadingStateProps {
  message?: string
}

export default function LoadingState({ message = 'Loading...' }: LoadingStateProps) {
  return (
    <div className="state-container">
      <div className="loading-spinner" />
      <p className="state-message">{message}</p>
    </div>
  )
}
