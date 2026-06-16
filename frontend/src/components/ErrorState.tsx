interface ErrorStateProps {
  title?: string
  message: string
}

export default function ErrorState({ title = 'Unable to load data', message }: ErrorStateProps) {
  return (
    <div className="state-container state-error">
      <p className="state-title">{title}</p>
      <p className="state-message">{message}</p>
    </div>
  )
}
