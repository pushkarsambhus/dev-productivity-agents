import { useState, useEffect, useCallback, useRef } from 'react'
import confetti from 'canvas-confetti'

function ProgressBar({ completed, total }) {
  const pct = total ? Math.round((completed / total) * 100) : 0
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm font-medium">
        <span className="text-gray-600">{completed} of {total} done</span>
        <span className="text-blue-600">{pct}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className="bg-gradient-to-r from-blue-500 to-green-500 h-4 rounded-full transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

function HintBox({ hint }) {
  return (
    <div className="hint-box animate-fade-in">
      <div className="flex items-start gap-2">
        <span className="text-blue-500 mt-0.5">💡</span>
        <p className="text-sm leading-relaxed">{hint.text}</p>
      </div>
    </div>
  )
}

function QuestionCard({ q, sessionId, onComplete }) {
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [checking, setChecking] = useState(false)
  const [requesting, setRequesting] = useState(false)
  const [hintsShown, setHintsShown] = useState(q.visible_hints || [])
  const [hintsSeen, setHintsSeen] = useState(q.hints_seen || 0)
  const [noMoreHints, setNoMoreHints] = useState(false)
  const answerRef = useRef(null)

  const hintsAvailable = q.hints_available || 0

  async function requestHint() {
    setRequesting(true)
    setNoMoreHints(false)
    try {
      const res = await fetch('/api/student/request-hint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, question_id: q.id }),
      })
      const data = await res.json()
      if (data.message === 'no_more_hints') {
        setNoMoreHints(true)
      } else {
        setHintsShown((prev) => [...prev, { level: data.level, text: data.text }])
        setHintsSeen(data.hints_seen)
      }
    } finally {
      setRequesting(false)
    }
  }

  async function submitAnswer(e) {
    e.preventDefault()
    if (!answer.trim()) return
    setChecking(true)
    setFeedback(null)
    try {
      const res = await fetch('/api/student/submit-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          question_id: q.id,
          answer: answer.trim(),
        }),
      })
      const data = await res.json()
      setFeedback(data)
      if (data.correct) {
        confetti({
          particleCount: 120,
          spread: 80,
          origin: { y: 0.6 },
          colors: ['#4ade80', '#60a5fa', '#f472b6', '#facc15'],
        })
        onComplete()
      }
    } finally {
      setChecking(false)
    }
  }

  if (q.completed) {
    return (
      <div className="card border-l-4 border-l-green-500 opacity-75">
        <div className="flex items-center gap-2">
          <span className="text-green-500 text-xl">✅</span>
          <div>
            <span className="text-xs font-semibold text-gray-400">Problem {q.number}</span>
            <p className="text-sm text-gray-600 line-clamp-1">{q.text}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card border-l-4 border-l-blue-400">
      <div className="mb-4">
        <span className="text-xs font-semibold bg-blue-100 text-blue-700 px-2 py-1 rounded">
          Problem {q.number}
        </span>
      </div>

      <p className="text-gray-900 text-base leading-relaxed whitespace-pre-wrap mb-5">
        {q.text}
      </p>

      {/* Hints */}
      {hintsShown.length > 0 && (
        <div className="space-y-3 mb-5">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Hints</p>
          {hintsShown.map((h) => <HintBox key={h.level} hint={h} />)}
        </div>
      )}

      {/* Hint button */}
      {!feedback?.correct && (
        <div className="mb-5">
          {hintsSeen < hintsAvailable ? (
            <button
              className="btn-secondary w-full text-sm"
              onClick={requestHint}
              disabled={requesting}
            >
              {requesting ? '…' : `🤔 I'm stuck — get a hint (${hintsSeen}/${hintsAvailable} used)`}
            </button>
          ) : hintsAvailable === 0 ? (
            <p className="text-xs text-gray-400 text-center">No hints available yet — ask your teacher!</p>
          ) : (
            <p className="text-xs text-amber-600 bg-amber-50 border border-amber-200 rounded-lg p-3 text-center">
              You've used all {hintsAvailable} hint{hintsAvailable !== 1 ? 's' : ''}. You've got this — give it your best try!
            </p>
          )}
          {noMoreHints && (
            <p className="text-xs text-gray-400 mt-2 text-center">No more hints available right now.</p>
          )}
        </div>
      )}

      {/* Answer form */}
      {!feedback?.correct && (
        <form onSubmit={submitAnswer} className="space-y-3">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Your answer</label>
            <input
              ref={answerRef}
              type="text"
              className="input"
              placeholder="Type your answer here…"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="btn-green w-full"
            disabled={checking || !answer.trim()}
          >
            {checking ? 'Checking…' : '✅ Submit Answer'}
          </button>
        </form>
      )}

      {/* Feedback */}
      {feedback && (
        <div className={`mt-4 rounded-xl p-4 border ${
          feedback.correct
            ? 'bg-green-50 border-green-300 text-green-900'
            : 'bg-orange-50 border-orange-300 text-orange-900'
        }`}>
          <div className="flex items-start gap-2">
            <span className="text-xl">{feedback.correct ? '🎉' : '💪'}</span>
            <div>
              <p className="font-semibold mb-1">
                {feedback.correct ? 'Correct!' : 'Not quite yet'}
              </p>
              <p className="text-sm">{feedback.feedback}</p>
              {!feedback.correct && (
                <button
                  className="mt-3 text-sm underline text-orange-700 hover:text-orange-900"
                  onClick={() => { setFeedback(null); answerRef.current?.focus() }}
                >
                  Try again →
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

const POLL_INTERVAL = 5000  // refresh every 5 seconds

export default function StudentView() {
  const [questions, setQuestions] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeIdx, setActiveIdx] = useState(0)
  const activeIdxRef = useRef(0)   // track without triggering re-renders

  const loadData = useCallback(async ({ silent = false } = {}) => {
    try {
      const res = await fetch('/api/student/questions')
      const data = await res.json()

      // Merge incoming data — preserve local hint/answer state on the active card
      setQuestions(prev => {
        if (prev.length === 0) return data
        return data.map((incoming, i) => {
          const existing = prev.find(p => p.id === incoming.id)
          // Always take latest hints_available / completed from server,
          // but don't clobber visible_hints the child already sees mid-session
          if (!existing) return incoming
          return {
            ...incoming,
            // keep whichever has more visible hints (server may have just released more)
            visible_hints: incoming.visible_hints.length >= existing.visible_hints.length
              ? incoming.visible_hints
              : existing.visible_hints,
          }
        })
      })

      if (data.length > 0) {
        setSessionId(data[0].session_id)
        const pRes = await fetch(`/api/progress/${data[0].session_id}`)
        setProgress(await pRes.json())

        // On first load only: jump to first incomplete question
        if (!silent) {
          const firstIncomplete = data.findIndex((q) => !q.completed)
          const idx = firstIncomplete >= 0 ? firstIncomplete : 0
          setActiveIdx(idx)
          activeIdxRef.current = idx
        }
      }
    } finally {
      if (!silent) setLoading(false)
    }
  }, [])

  // Initial load
  useEffect(() => { loadData() }, [loadData])

  // Poll every 5 s — silent refresh so UI doesn't flicker
  useEffect(() => {
    const id = setInterval(() => loadData({ silent: true }), POLL_INTERVAL)
    return () => clearInterval(id)
  }, [loadData])

  // Keep ref in sync with activeIdx so poll doesn't reset navigation
  const handleSetActiveIdx = (idx) => {
    activeIdxRef.current = idx
    setActiveIdx(idx)
  }

  async function handleComplete() {
    await loadData({ silent: true })
  }

  const allDone = questions.length > 0 && questions.every((q) => q.completed)

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-400">
        <div className="text-center">
          <div className="text-4xl mb-3 animate-pulse">🧮</div>
          <p>Loading your homework…</p>
        </div>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="card text-center max-w-sm">
          <div className="text-5xl mb-4">📚</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">No homework yet!</h2>
          <p className="text-gray-500 text-sm">Ask your teacher to upload a homework assignment.</p>
        </div>
      </div>
    )
  }

  if (allDone) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="card text-center max-w-sm">
          <div className="text-6xl mb-4">🏆</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Amazing work!</h2>
          <p className="text-gray-600">You completed all the problems! You're a math superstar! ⭐</p>
        </div>
      </div>
    )
  }

  const activeQ = questions[activeIdx]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-xl">🧮</span>
              <h1 className="font-bold text-gray-800">RSM Math Tutor</h1>
            </div>
            <span className="text-sm text-gray-500">
              {progress?.completed ?? 0}/{progress?.total ?? questions.length} done
            </span>
          </div>
          {progress && <ProgressBar completed={progress.completed} total={progress.total} />}
        </div>
      </header>

      <div className="max-w-2xl mx-auto p-4 space-y-4">
        {/* Question navigation tabs */}
        <div className="flex gap-2 overflow-x-auto pb-1">
          {questions.map((q, i) => (
            <button
              key={q.id}
              onClick={() => handleSetActiveIdx(i)}
              className={`shrink-0 w-10 h-10 rounded-lg text-sm font-semibold border transition-colors ${
                q.completed
                  ? 'bg-green-100 border-green-300 text-green-700'
                  : i === activeIdx
                  ? 'bg-blue-600 border-blue-600 text-white'
                  : 'bg-white border-gray-200 text-gray-600 hover:border-blue-300'
              }`}
            >
              {q.completed ? '✓' : q.number}
            </button>
          ))}
        </div>

        {/* Active question */}
        {activeQ && (
          <QuestionCard
            key={activeQ.id}
            q={activeQ}
            sessionId={sessionId}
            onComplete={handleComplete}
          />
        )}

        {/* Nav arrows */}
        <div className="flex justify-between">
          <button
            className="btn-secondary text-sm disabled:opacity-30"
            onClick={() => handleSetActiveIdx(Math.max(0, activeIdx - 1))}
            disabled={activeIdx === 0}
          >← Previous</button>
          <button
            className="btn-secondary text-sm disabled:opacity-30"
            onClick={() => handleSetActiveIdx(Math.min(questions.length - 1, activeIdx + 1))}
            disabled={activeIdx === questions.length - 1}
          >Next →</button>
        </div>
      </div>
    </div>
  )
}
