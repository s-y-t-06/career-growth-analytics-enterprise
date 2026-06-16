import type { ReactNode } from 'react'

interface SectionCardProps {
  title: string
  children: ReactNode
  className?: string
}

export default function SectionCard({ title, children, className = '' }: SectionCardProps) {
  return (
    <div className={`card ${className}`}>
      <h2 className="section-title">{title}</h2>
      {children}
    </div>
  )
}
