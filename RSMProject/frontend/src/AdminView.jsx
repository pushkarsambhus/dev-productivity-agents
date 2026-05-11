import { useState, useEffect, useCallback, useRef } from 'react'

const PROVIDER_LABELS = {
  'anthropic': '🟠 Anthropic (Claude)',
  'openai': '🟢 OpenAI (GPT-4o)',
  'claude-cli': '🔵 Claude Subscription (CLI)',
}

function ProviderPanel() {
  const [settings, setSettings] = useState(null)
  const [provider, setProvider] = useState('anthropic')
  const [anthropicKey, setAnthropicKey] = useState('')
  const [openaiKey, setOpenaiKey] = useState('')
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    fetch('/api/settings').then(r => r.json()).then(s => {
      setSettings(s)
      setProvider(s.provider)
    })
  }, [])

  async function save() {
    setSaving(true)
    setSaved(false)
    const body = { provider, anthropic_key: anthropicKey, openai_key: openaiKey }
    await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    const s = await fetch('/api/settings').then(r => r.json())
    setSettings(s)
    setAnthropicKey('')
    setOpenaiKey('')
    setSaving(false)
    setSaved(true)
    setTimeout(() => setSaved(false), 2500)
  }

  if (!settings) return null

  return (
    <div className="card">
      <h2 className="font-semibold text-gray-800 mb-3">AI Provider</h2>

      <div className="space-y-2 mb-4">
        {Object.entries(PROVIDER_LABELS).map(([val, label]) => (
          <label key={val} className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${provider === val ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}`}>
            <input
              type="radio"
              name="provider"
              value={val}
              checked={provider === val}
              onChange={() => setProvider(val)}
              className="accent-blue-600"
            />
            <span className="text-sm font-medium">{label}</span>
          </label>
        ))}
      </div>

      {provider === 'claude-cli' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-xs text-blue-800 mb-3">
          Uses your Claude subscription via the local <code>claude</code> CLI — no API key needed.
          Make sure Claude Code is installed and logged in.
        </div>
      )}

      {provider === 'anthropic' && (
        <div className="mb-3">
          <label className="text-xs font-medium text-gray-600 block mb-1">
            Anthropic API Key {settings.anthropic_key_set && <span className="text-green-600">({settings.anthropic_key_preview} saved)</span>}
          </label>
          <input
            type="password"
            className="input text-sm"
            placeholder={settings.anthropic_key_set ? 'Leave blank to keep existing key' : 'sk-ant-...'}
            value={anthropicKey}
            onChange={e => setAnthropicKey(e.target.value)}
          />
        </div>
      )}

      {provider === 'openai' && (
        <div className="mb-3">
          <label className="text-xs font-medium text-gray-600 block mb-1">
            OpenAI API Key {settings.openai_key_set && <span className="text-green-600">({settings.openai_key_preview} saved)</span>}
          </label>
          <input
            type="password"
            className="input text-sm"
            placeholder={settings.openai_key_set ? 'Leave blank to keep existing key' : 'sk-...'}
            value={openaiKey}
            onChange={e => setOpenaiKey(e.target.value)}
          />
        </div>
      )}

      <button
        className="btn-primary w-full text-sm"
        onClick={save}
        disabled={saving}
      >
        {saving ? 'Saving…' : saved ? '✓ Saved!' : 'Save Settings'}
      </button>

      <p className="text-xs text-gray-400 mt-2 text-center">
        Currently using: <strong>{PROVIDER_LABELS[settings.provider]}</strong>
      </p>
    </div>
  )
}

function ProgressBar({ completed, total }) {
  const pct = total ? Math.round((completed / total) * 100) : 0
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm text-gray-600">
        <span>{completed} / {total} completed</span>
        <span>{pct}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className="bg-green-500 h-3 rounded-full transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

// Detect if a question is just a textbook reference with no real problem text
function isReference(text) {
  if (!text || text.trim().length < 3) return true
  // Matches patterns like "Ch.4: 148", "4006", "Ch.4: 22. d." etc.
  return /^(ch\.\s*\d+\s*:\s*\d+[\w.\s]*|\d{3,5}[\w.\s]*)$/i.test(text.trim())
}

function ImagePasteArea({ onExtracted, cardId }) {
  const [image, setImage] = useState(null)
  const [extracting, setExtracting] = useState(false)
  const [error, setError] = useState('')
  const [pasting, setPasting] = useState(false)

  function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) return
    const reader = new FileReader()
    reader.onload = (e) => {
      const dataUrl = e.target.result
      setImage({ b64: dataUrl.split(',')[1], mediaType: file.type, previewUrl: dataUrl })
      setError('')
    }
    reader.readAsDataURL(file)
  }

  async function readClipboard() {
    setPasting(true)
    setError('')
    try {
      const items = await navigator.clipboard.read()
      for (const item of items) {
        const imageType = item.types.find(t => t.startsWith('image/'))
        if (imageType) {
          const blob = await item.getType(imageType)
          handleFile(new File([blob], 'screenshot.png', { type: imageType }))
          return
        }
      }
      setError('No image found in clipboard. Take a screenshot first (⌘⇧4), then click this button.')
    } catch {
      setError('Clipboard access denied. Use the "Upload file" option below instead.')
    } finally {
      setPasting(false)
    }
  }

  function onDrop(e) {
    e.preventDefault()
    handleFile(e.dataTransfer.files[0])
  }

  async function extract() {
    if (!image) return
    setExtracting(true)
    setError('')
    try {
      const res = await fetch('/api/extract-from-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_b64: image.b64, media_type: image.mediaType }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Extraction failed')
      onExtracted(data.text)
      setImage(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setExtracting(false)
    }
  }

  return (
    <div className="space-y-2">
      {!image ? (
        <div
          onDrop={onDrop}
          onDragOver={e => e.preventDefault()}
          className="border-2 border-dashed border-amber-300 bg-amber-50 rounded-lg p-4 space-y-3"
        >
          {/* Primary: clipboard button */}
          <button
            className="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors text-sm"
            onClick={readClipboard}
            disabled={pasting}
          >
            {pasting ? 'Reading clipboard…' : '📋 Paste Screenshot from Clipboard'}
          </button>

          <div className="flex items-center gap-2 text-xs text-gray-400">
            <div className="flex-1 h-px bg-gray-200" />
            <span>or</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          {/* Fallback: file upload */}
          <label className="flex items-center justify-center gap-2 w-full border border-gray-300 bg-white hover:bg-gray-50 text-gray-700 font-medium py-2 px-4 rounded-lg cursor-pointer text-sm transition-colors">
            <span>📁 Upload image file</span>
            <input type="file" accept="image/*" className="hidden"
              onChange={e => handleFile(e.target.files[0])} />
          </label>

          <p className="text-xs text-amber-600 text-center">
            Tip: use <strong>⌘⇧4</strong> to screenshot the textbook, then click Paste above
          </p>
        </div>
      ) : (
        <div
          onDrop={onDrop}
          onDragOver={e => e.preventDefault()}
          className="border-2 border-amber-300 rounded-lg p-3 bg-amber-50"
        >
          <img src={image.previewUrl} alt="Problem" className="max-h-52 mx-auto rounded object-contain mb-3" />
          <div className="flex gap-2">
            <button className="btn-primary text-sm flex-1" onClick={extract} disabled={extracting}>
              {extracting ? '🔍 Reading problem…' : '🔍 Extract Problem Text'}
            </button>
            <button className="btn-secondary text-sm px-3" onClick={() => setImage(null)}>✕ Redo</button>
          </div>
        </div>
      )}
      {error && <p className="text-red-500 text-xs bg-red-50 border border-red-200 rounded p-2">{error}</p>}
    </div>
  )
}

function QuestionCard({ q, sessionId, onUpdate }) {
  const needsText = isReference(q.text)
  const [editing, setEditing] = useState(needsText)   // auto-open if reference-only
  const [editText, setEditText] = useState(q.text)
  const [generating, setGenerating] = useState(false)
  const [generatingSimilar, setGeneratingSimilar] = useState(false)
  const [expanded, setExpanded] = useState(false)
  const [showImagePaste, setShowImagePaste] = useState(needsText)

  // Keep editText fresh if the question updates via polling while not editing
  useEffect(() => {
    if (!editing) setEditText(q.text)
  }, [q.text])

  async function saveEdit() {
    await fetch(`/api/sessions/${sessionId}/questions/${q.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: editText }),
    })
    setEditing(false)
    onUpdate()
  }

  async function generateHints() {
    setGenerating(true)
    try {
      await fetch(`/api/sessions/${sessionId}/questions/${q.id}/generate-hints`, {
        method: 'POST',
      })
      onUpdate()
    } finally {
      setGenerating(false)
    }
  }

  async function generateSimilar() {
    setGeneratingSimilar(true)
    try {
      await fetch(`/api/sessions/${sessionId}/questions/${q.id}/generate-similar`, {
        method: 'POST',
      })
      onUpdate()
    } finally {
      setGeneratingSimilar(false)
    }
  }

  async function toggleActive() {
    await fetch(`/api/sessions/${sessionId}/questions/${q.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ active: !q.active }),
    })
    onUpdate()
  }

  async function releaseHint(level) {
    await fetch(`/api/sessions/${sessionId}/questions/${q.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hints_released: level }),
    })
    onUpdate()
  }

  const released = q.hints_released || 0

  return (
    <div className={`card border-l-4 ${needsText ? 'border-l-amber-400' : q.active ? 'border-l-blue-500' : 'border-l-gray-300'}`}>

      {/* Reference-only warning */}
      {needsText && (
        <div className="mb-3 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 flex items-start gap-2 text-amber-800 text-xs">
          <span className="text-base">📖</span>
          <div>
            <p className="font-semibold">Textbook reference only</p>
            <p>This PDF lists problem numbers from the RSM textbook. Paste the actual problem text below so Claude can generate hints.</p>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
              #{q.number}
            </span>
            {!q.active && (
              <span className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">Hidden</span>
            )}
            {q.hints_generated && (
              <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">✓ Hints ready</span>
            )}
          </div>

          {editing ? (
            <div className="space-y-2">
              {/* Toggle between image paste and text entry — available for ALL cards */}
              <div className="flex gap-2 mb-1">
                <button
                  className={`text-xs px-3 py-1 rounded-lg border font-medium transition-colors ${showImagePaste ? 'bg-amber-100 border-amber-400 text-amber-800' : 'bg-gray-100 border-gray-300 text-gray-600'}`}
                  onClick={() => setShowImagePaste(true)}
                >📸 Paste Image</button>
                <button
                  className={`text-xs px-3 py-1 rounded-lg border font-medium transition-colors ${!showImagePaste ? 'bg-blue-100 border-blue-400 text-blue-800' : 'bg-gray-100 border-gray-300 text-gray-600'}`}
                  onClick={() => setShowImagePaste(false)}
                >⌨️ Type Text</button>
              </div>

              {showImagePaste ? (
                <ImagePasteArea cardId={q.id} onExtracted={(text) => { setEditText(text); setShowImagePaste(false) }} />
              ) : (
                <textarea
                  className="input text-sm h-32 resize-y"
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                  placeholder={needsText
                    ? "Problem text will appear here after image extraction, or type it manually…"
                    : "Edit the problem text…"}
                  autoFocus={!needsText}
                />
              )}

              {!showImagePaste && (
                <div className="flex gap-2">
                  <button className="btn-primary text-sm py-1 px-3" onClick={saveEdit} disabled={!editText.trim() || editText === q.text}>Save</button>
                  <button className="btn-secondary text-sm py-1 px-3" onClick={() => { setEditing(false); setEditText(q.text) }}>Cancel</button>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">{q.text}</p>
          )}
        </div>

        <div className="flex flex-col gap-1 shrink-0">
          <button
            className="text-xs btn-secondary py-1 px-2"
            onClick={() => { setEditText(q.text); setEditing(!editing) }}
          >Edit</button>
          <button
            className={`text-xs py-1 px-2 rounded-lg font-semibold transition-colors ${q.active ? 'bg-yellow-100 hover:bg-yellow-200 text-yellow-800' : 'bg-green-100 hover:bg-green-200 text-green-800'}`}
            onClick={toggleActive}
          >{q.active ? 'Hide' : 'Show'}</button>
        </div>
      </div>

      {/* Hints section */}
      <div className="mt-4 border-t border-gray-100 pt-4 space-y-3">
        {!q.hints_generated ? (
          <button
            className="btn-primary text-sm w-full"
            onClick={generateHints}
            disabled={generating || !q.text.trim()}
          >
            {generating ? '⏳ Generating hints & solution…' : '✨ Generate Hints & Solution'}
          </button>
        ) : (
          <>
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-gray-700">Hints released to student</span>
              <div className="flex gap-1">
                {[0, 1, 2, 3].map((n) => (
                  <button
                    key={n}
                    onClick={() => releaseHint(n)}
                    className={`w-8 h-8 rounded-lg text-xs font-bold border transition-colors ${
                      released === n
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400'
                    }`}
                  >
                    {n === 0 ? '🚫' : n}
                  </button>
                ))}
              </div>
            </div>

            <button
              className="text-sm text-blue-600 hover:text-blue-800 underline"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? '▲ Hide hints & solution' : '▼ Preview hints & solution'}
            </button>

            {expanded && (
              <div className="space-y-3 text-sm">
                {[1, 2, 3].map((n) => (
                  <div key={n} className="hint-box">
                    <p className="font-semibold mb-1 text-blue-700">Hint {n}</p>
                    <p>{q[`hint${n}`]}</p>
                  </div>
                ))}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-green-900">
                  <p className="font-semibold mb-1 text-green-700">Full Solution</p>
                  <p className="whitespace-pre-wrap">{q.solution}</p>
                </div>
              </div>
            )}
          </>
        )}

        {/* Generate similar practice question — only for real questions with text */}
        {!needsText && (
          <div className="pt-3 border-t border-dashed border-gray-200">
            <button
              className="w-full text-sm py-2 px-3 rounded-lg border border-purple-300 bg-purple-50 hover:bg-purple-100 text-purple-800 font-medium transition-colors disabled:opacity-50"
              onClick={generateSimilar}
              disabled={generatingSimilar || !q.text.trim()}
            >
              {generatingSimilar ? '⏳ Generating practice question…' : '🔁 Generate Similar Practice Question'}
            </button>
            {q.is_practice && (
              <p className="text-xs text-purple-500 text-center mt-1">AI-generated practice • based on {q.source_id}</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function AdminView() {
  const [sessions, setSessions] = useState([])
  const [activeSession, setActiveSession] = useState(null)
  const [questions, setQuestions] = useState([])
  const [progress, setProgress] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [selectedSession, setSelectedSession] = useState(null)

  const loadSessions = useCallback(async () => {
    const [sessRes, activeRes] = await Promise.all([
      fetch('/api/sessions'),
      fetch('/api/sessions/active'),
    ])
    const sessData = await sessRes.json()
    setSessions(sessData)
    if (activeRes.ok) {
      const act = await activeRes.json()
      setActiveSession(act)
    }
  }, [])

  useEffect(() => { loadSessions() }, [loadSessions])

  async function loadSessionDetail(session) {
    setSelectedSession(session)
    const [qRes, pRes] = await Promise.all([
      fetch(`/api/sessions/${session.id}/questions`),
      fetch(`/api/progress/${session.id}`),
    ])
    setQuestions(await qRes.json())
    setProgress(await pRes.json())
  }

  async function refreshQuestions() {
    if (!selectedSession) return
    const [qRes, pRes] = await Promise.all([
      fetch(`/api/sessions/${selectedSession.id}/questions`),
      fetch(`/api/progress/${selectedSession.id}`),
    ])
    setQuestions(await qRes.json())
    setProgress(await pRes.json())
  }

  async function handleUpload(e) {
    const file = e.target.files[0]
    if (!file) return
    setUploadError('')
    setUploading(true)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch('/api/upload', { method: 'POST', body: form })
      if (!res.ok) {
        const err = await res.json()
        setUploadError(err.detail || 'Upload failed')
        return
      }
      const session = await res.json()
      await loadSessions()
      await loadSessionDetail(session)
    } catch {
      setUploadError('Upload failed — is the backend running?')
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  async function activateSession(sessionId) {
    const res = await fetch(`/api/sessions/${sessionId}/activate`, { method: 'POST' })
    const updated = await res.json()
    await loadSessions()
    // Keep selectedSession in sync
    setSelectedSession(prev => prev?.id === sessionId ? updated : prev)
  }

  async function deleteSession(sessionId) {
    if (!confirm('Delete this session and all its questions?')) return
    await fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' })
    if (selectedSession?.id === sessionId) {
      setSelectedSession(null)
      setQuestions([])
      setProgress(null)
    }
    await loadSessions()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top bar */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🎓</span>
          <div>
            <h1 className="text-xl font-bold text-gray-900">RSM Admin Portal</h1>
            <p className="text-xs text-gray-500">Manage homework sessions</p>
          </div>
        </div>
        <a href="/student" className="text-sm text-blue-600 hover:underline">→ Student view</a>
      </header>

      <div className="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left: Provider + Sessions + Upload */}
        <div className="space-y-4">
          <ProviderPanel />

          <div className="card">
            <h2 className="font-semibold text-gray-800 mb-3">Upload Homework PDF</h2>
            <label className={`block cursor-pointer border-2 border-dashed rounded-xl p-6 text-center transition-colors ${uploading ? 'border-blue-300 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'}`}>
              <input type="file" accept=".pdf" className="hidden" onChange={handleUpload} disabled={uploading} />
              <div className="text-3xl mb-2">📄</div>
              <p className="text-sm font-medium text-gray-700">
                {uploading ? 'Processing…' : 'Click to upload PDF'}
              </p>
              <p className="text-xs text-gray-400 mt-1">Claude will extract all problems</p>
            </label>
            {uploadError && <p className="text-red-500 text-sm mt-2">{uploadError}</p>}
          </div>

          <div className="card">
            <h2 className="font-semibold text-gray-800 mb-3">Sessions</h2>
            {sessions.length === 0 ? (
              <p className="text-gray-400 text-sm">No sessions yet. Upload a PDF.</p>
            ) : (
              <div className="space-y-2">
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedSession?.id === s.id
                        ? 'border-blue-400 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => loadSessionDetail(s)}
                  >
                    <div className="flex items-center justify-between gap-1">
                      <span className="text-sm font-medium text-gray-800 truncate">{s.filename}</span>
                      <div className="flex items-center gap-1 shrink-0">
                        {s.active && <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">✓ Active</span>}
                        <button
                          className="text-xs text-red-400 hover:text-red-600 px-1"
                          onClick={(e) => { e.stopPropagation(); deleteSession(s.id) }}
                          title="Delete session"
                        >🗑</button>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-0.5">{s.questions?.length ?? 0} questions · ID: {s.id}</p>
                    {!s.active && (
                      <button
                        className="mt-2 text-xs btn-primary py-1 px-2"
                        onClick={(e) => { e.stopPropagation(); activateSession(s.id) }}
                      >▶ Set active for students</button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: Questions + Progress */}
        <div className="lg:col-span-2 space-y-4">
          {selectedSession ? (
            <>
              {/* Out-of-sync warning — use live sessions array, not stale selectedSession snapshot */}
              {!sessions.find(s => s.id === selectedSession.id)?.active && (
                <div className="bg-red-50 border border-red-300 rounded-xl px-4 py-3 flex items-start gap-3">
                  <span className="text-xl mt-0.5">⚠️</span>
                  <div className="flex-1">
                    <p className="font-semibold text-red-800 text-sm">Students are NOT seeing this session</p>
                    <p className="text-red-700 text-xs mt-0.5">You're editing session <code>{selectedSession.id}</code>, but a different session is currently active. Click below to make this the one students see.</p>
                    <button
                      className="mt-2 text-xs bg-red-600 hover:bg-red-700 text-white font-semibold py-1.5 px-3 rounded-lg"
                      onClick={() => activateSession(selectedSession.id)}
                    >▶ Make this session active for students</button>
                  </div>
                </div>
              )}

              <div className="card">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="font-semibold text-gray-800">{selectedSession.filename}</h2>
                  <span className="text-xs text-gray-400">ID: {selectedSession.id}</span>
                </div>
                {progress && <ProgressBar completed={progress.completed} total={progress.total} />}
              </div>

              {questions.map((q) => (
                <QuestionCard
                  key={q.id}
                  q={q}
                  sessionId={selectedSession.id}
                  onUpdate={refreshQuestions}
                />
              ))}
            </>
          ) : (
            <div className="card flex flex-col items-center justify-center py-20 text-gray-400">
              <div className="text-4xl mb-3">📂</div>
              <p>Select a session or upload a PDF to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
