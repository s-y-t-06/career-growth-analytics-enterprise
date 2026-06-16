import { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import {
  Activity,
  BarChart3,
  Filter,
  Layers,
  Percent,
  Users,
} from 'lucide-react'
import { fetchHealth } from '../api/client'
import type { Health } from '../api/types'
import StatusBadge from './StatusBadge'

interface NavItem {
  to: string
  label: string
  icon: React.ReactNode
}

const navItems: NavItem[] = [
  { to: '/', label: 'Overview', icon: <Activity size={18} /> },
  { to: '/funnel', label: 'Funnel', icon: <Filter size={18} /> },
  { to: '/retention', label: 'Retention', icon: <Layers size={18} /> },
  { to: '/experiment', label: 'Experiment', icon: <Percent size={18} /> },
  { to: '/churn', label: 'Churn Risk', icon: <BarChart3 size={18} /> },
  { to: '/users', label: 'High-Risk Users', icon: <Users size={18} /> },
]

function healthToStatus(health: Health | null, error: string | null) {
  if (error || !health) {
    return { status: 'error' as const, label: 'API Offline' }
  }
  const allOk = health.status === 'ok' && health.database === 'ok' && health.model === 'ok' && health.metrics === 'ok'
  if (allOk) {
    return { status: 'ok' as const, label: 'API Online / Model Loaded / Data Ready' }
  }
  return { status: 'warning' as const, label: 'Service degraded' }
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const [health, setHealth] = useState<Health | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch((err) => setHealthError(err.message))
  }, [])

  const status = healthToStatus(health, healthError)

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <h1 className="sidebar-title">Career Growth Analytics</h1>
          <p className="sidebar-subtitle">AI Career Platform Lifecycle Growth System</p>
        </div>
        <nav>
          <ul className="sidebar-nav">
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink to={item.to} end={item.to === '/'}>
                  {item.icon}
                  <span>{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="sidebar-footer">
          Local enterprise analytics demo
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div className="topbar-brand">
            <p className="topbar-name">Career Growth Analytics</p>
            <p className="topbar-context">AI Career Platform Lifecycle Growth System</p>
          </div>
          <div className="topbar-health">
            <StatusBadge status={status.status} label={status.label} />
          </div>
        </header>
        {healthError && (
          <div className="offline-banner">
            Backend API is unavailable. Start FastAPI on http://localhost:8000.
          </div>
        )}
        <div className="content">{children}</div>
      </main>
    </div>
  )
}
