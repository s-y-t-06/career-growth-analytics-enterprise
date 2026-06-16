import { NavLink } from 'react-router-dom'
import {
  Activity,
  BarChart3,
  Filter,
  Layers,
  Percent,
  Users,
} from 'lucide-react'

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
  { to: '/users', label: 'Users', icon: <Users size={18} /> },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="app">
      <aside className="sidebar">
        <h1 className="sidebar-title">Career Growth</h1>
        <nav>
          <ul className="sidebar-nav">
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink to={item.to}>
                  {item.icon}
                  <span>{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  )
}
