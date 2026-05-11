import { Routes, Route, Navigate } from 'react-router-dom'
import { useState } from 'react'
import AdminView from './AdminView.jsx'
import StudentView from './StudentView.jsx'
import PinGate from './components/PinGate.jsx'

export default function App() {
  const [adminAuth, setAdminAuth] = useState(false)
  const [studentAuth, setStudentAuth] = useState(false)

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/student" replace />} />

      <Route
        path="/admin"
        element={
          adminAuth ? (
            <AdminView />
          ) : (
            <PinGate
              role="admin"
              onSuccess={() => setAdminAuth(true)}
            />
          )
        }
      />

      <Route
        path="/student"
        element={
          studentAuth ? (
            <StudentView />
          ) : (
            <PinGate
              role="student"
              onSuccess={() => setStudentAuth(true)}
            />
          )
        }
      />
    </Routes>
  )
}
