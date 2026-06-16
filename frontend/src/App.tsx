import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Overview from './pages/Overview'
import Funnel from './pages/Funnel'
import Retention from './pages/Retention'
import Experiment from './pages/Experiment'
import ChurnRisk from './pages/ChurnRisk'
import UserDetail from './pages/UserDetail'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/funnel" element={<Funnel />} />
        <Route path="/retention" element={<Retention />} />
        <Route path="/experiment" element={<Experiment />} />
        <Route path="/churn" element={<ChurnRisk />} />
        <Route path="/users" element={<ChurnRisk />} />
        <Route path="/users/:userId" element={<UserDetail />} />
      </Routes>
    </Layout>
  )
}
