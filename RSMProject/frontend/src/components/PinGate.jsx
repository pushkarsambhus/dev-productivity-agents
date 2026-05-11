import { useState } from 'react'

export default function PinGate({ role, onSuccess }) {
  const [pin, setPin] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const isAdmin = role === 'admin'

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await fetch(`/api/auth/${role}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin }),
      })
      if (res.ok) {
        onSuccess()
      } else {
        setError('Wrong PIN. Please try again.')
        setPin('')
      }
    } catch {
      setError('Could not connect to server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="card w-full max-w-sm">
        <div className="text-center mb-6">
          <div className="text-5xl mb-3">{isAdmin ? '🎓' : '🧮'}</div>
          <h1 className="text-2xl font-bold text-gray-800">
            {isAdmin ? 'Admin Portal' : 'RSM Math Tutor'}
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            {isAdmin ? 'Parent / Teacher access' : 'Enter your PIN to start!'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {isAdmin ? 'Admin PIN' : 'Student PIN'}
            </label>
            <input
              type="password"
              inputMode="numeric"
              pattern="[0-9]*"
              maxLength={8}
              className="input text-center text-2xl tracking-widest"
              placeholder="••••"
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              autoFocus
            />
          </div>

          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            className="btn-primary w-full"
            disabled={loading || pin.length === 0}
          >
            {loading ? 'Checking…' : 'Enter'}
          </button>
        </form>

        {!isAdmin && (
          <p className="text-center mt-4 text-xs text-gray-400">
            <a href="/admin" className="underline hover:text-gray-600">Admin login</a>
          </p>
        )}
      </div>
    </div>
  )
}
