import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Deals from './pages/Deals'
import DealDetail from './pages/DealDetail'
import { isLoggedIn } from './lib/api'

function Protected({ children }: { children: React.ReactNode }) {
  return isLoggedIn() ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/deals" element={<Protected><Deals /></Protected>} />
        <Route path="/deals/:id" element={<Protected><DealDetail /></Protected>} />
        <Route path="/" element={<Navigate to="/deals" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
