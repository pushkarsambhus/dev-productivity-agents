// ── State ─────────────────────────────────────────────────────────────────────
const chatState = {
  history: [],   // [{role, content}]
  streaming: false,
};

const state = {
  sessionId:     null,
  position:      null,
  numQuestions:  10,
  provider:      'anthropic',
  prepProvider:      'anthropic',  // provider for prep mode
  prepExtraQuestions: 0,           // extra AI-generated questions in prep mode
  concepts:          [],           // concept walkthroughs for current session
  conceptIdx:        0,            // current concept index
  questions:     [],   // from API (answers hidden)
  answers:       {},   // { idx: { is_correct, feedback, explanation, remember } }
  deferred:      new Set(), // question indices marked "do later"
  currentIdx:    0,
  bugEditor:     null, // Monaco instance for find_the_bug
  codeEditor:    null, // Monaco instance for coding
  selectedOpt:   null, // selected MCQ option text
  monacoReady:   false,
  mcbQueue:      [],   // callbacks waiting for Monaco
  selectedPacks: [],   // pack IDs toggled on the landing page
  mode:          'prep', // 'prep' | 'role'
};

// ── Positions ────────────────────────────────────────────────────────────────
// Pinned roles (your targets) shown first, then general roles
const POSITIONS = [
  // ── Your target roles ──────────────────────────────────────────────────────
  {
    icon: '🤖', name: 'AI / ML Engineer',
    desc: 'LLMs, fine-tuning, MLOps, model serving, PyTorch, evals',
    pinned: true,
  },
  {
    icon: '🎯', name: 'AI Platform & Evaluation',
    desc: 'Eval frameworks, benchmarking, RAG quality, LLM observability',
    pinned: true,
  },
  {
    icon: '🔴', name: 'Red Team Engineer',
    desc: 'Adversarial ML, prompt injection, jailbreaks, threat modeling, MITRE ATT&CK',
    pinned: true,
  },
  {
    icon: '🤝', name: 'Product Manager',
    desc: 'Roadmaps, PRDs, user stories, metrics, prioritisation, stakeholder mgmt',
    pinned: true,
  },
  {
    icon: '🧪', name: 'AI Automation Test Engineer',
    desc: 'LLM test harnesses, eval pipelines, pytest, property-based testing, CI',
    pinned: true,
  },
  {
    icon: '👔', name: 'Engineering Manager',
    desc: 'Team leadership, delivery, 1:1s, hiring, technical strategy, OKRs',
    pinned: true,
  },
  {
    icon: '📋', name: 'Technical Program Manager',
    desc: 'Cross-team programs, risk mgmt, roadmap alignment, exec communication',
    pinned: true,
  },
  // ── General roles ──────────────────────────────────────────────────────────
  { icon: '🎨', name: 'Frontend Developer',   desc: 'HTML, CSS, JS, React, DOM, performance' },
  { icon: '⚙️', name: 'Backend Developer',    desc: 'APIs, databases, caching, Python/Node' },
  { icon: '📊', name: 'Data Scientist',       desc: 'Python, statistics, ML, pandas, SQL' },
  { icon: '🛠️', name: 'DevOps Engineer',      desc: 'CI/CD, Docker, Kubernetes, cloud infra' },
  { icon: '☁️', name: 'Cloud Architect',      desc: 'AWS/GCP/Azure, microservices, distributed' },
  { icon: '🔒', name: 'Security Engineer',    desc: 'OWASP, crypto, network security, auth' },
  { icon: '💻', name: 'Software Engineer',    desc: 'DSA, OOP, system design, architecture' },
];

// ── Helpers ───────────────────────────────────────────────────────────────────
function $(id) { return document.getElementById(id); }

function showView(name) {
  ['landing','loading','question','summary'].forEach(v => {
    $(`view-${v}`).hidden = (v !== name);
  });
  // Show chat FAB only on the question view
  const chatFab = $('chat-fab');
  if (chatFab) {
    chatFab.hidden = (name !== 'question');
    if (name !== 'question') { const p = $('chat-panel'); if (p) p.hidden = true; }
  }
}

function whenMonaco(fn) {
  if (state.monacoReady) fn();
  else state.mcbQueue.push(fn);
}

function langSlug(q) {
  return (q.language || 'python').split('/')[0].toLowerCase();
}

function monacoLang(slug) {
  const map = { js: 'javascript', ts: 'typescript', bash: 'shell', yml: 'yaml', yaml: 'yaml' };
  return map[slug] || slug;
}

function updateScoreboard() {
  const realQs  = state.questions.filter(q => q.type !== 'concept');
  const answered = Object.keys(state.answers).length;
  const correct  = Object.values(state.answers).filter(a => a.is_correct).length;
  $('sb-score').textContent = `${correct} / ${answered}`;
  const pct = realQs.length ? answered / realQs.length * 100 : 0;
  $('score-fill').style.width = `${pct}%`;
}

function buildNavDots() {
  const nav = $('q-nav');
  nav.innerHTML = '';
  state.questions.forEach((q, i) => {
    const d = document.createElement('button');
    d.className = q.type === 'concept' ? 'nav-dot nav-dot--concept' : 'nav-dot';
    d.textContent = q.type === 'concept' ? '📖' : i + 1;
    d.title = q.type === 'concept' ? q.title : '';
    d.dataset.i = i;
    d.addEventListener('click', () => renderQuestion(i));
    nav.appendChild(d);
  });
}

function refreshNavDots() {
  document.querySelectorAll('.nav-dot').forEach(d => {
    const i = +d.dataset.i;
    const q = state.questions[i];
    if (q.type === 'concept') {
      d.className = 'nav-dot nav-dot--concept';
      if (i === state.currentIdx) d.classList.add('current');
      return;
    }
    d.className = 'nav-dot';
    if (i === state.currentIdx) d.classList.add('current');
    if (state.answers[i] !== undefined) {
      d.classList.add(state.answers[i].is_correct ? 'correct' : 'wrong');
    } else if (state.deferred.has(i)) {
      d.classList.add('deferred');
    }
  });
}

// ── Monaco setup ──────────────────────────────────────────────────────────────
require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs' } });
require(['vs/editor/editor.main'], () => {
  state.monacoReady = true;
  state.mcbQueue.forEach(fn => fn());
  state.mcbQueue = [];
});

function createOrUpdateEditor(containerId, code, lang) {
  const container = $(containerId);
  const mlang = monacoLang(lang);

  if (containerId === 'bug-editor') {
    if (!state.bugEditor) {
      state.bugEditor = monaco.editor.create(container, editorOptions(code, mlang));
    } else {
      const m = monaco.editor.createModel(code, mlang);
      state.bugEditor.setModel(m);
    }
    return state.bugEditor;
  } else {
    if (!state.codeEditor) {
      state.codeEditor = monaco.editor.create(container, editorOptions(code, mlang));
    } else {
      const m = monaco.editor.createModel(code, mlang);
      state.codeEditor.setModel(m);
    }
    return state.codeEditor;
  }
}

function editorOptions(value, language) {
  return {
    value,
    language,
    theme: 'vs-dark',
    fontSize: 13,
    fontFamily: "'JetBrains Mono', monospace",
    lineNumbers: 'on',
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    automaticLayout: true,
    padding: { top: 12, bottom: 12 },
    wordWrap: 'on',
  };
}

// ── Landing ───────────────────────────────────────────────────────────────────
function setMode(mode) {
  state.mode = mode;
  $('prep-section').hidden  = (mode !== 'prep');
  $('role-section').hidden  = (mode !== 'role');
  document.querySelectorAll('.mode-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.mode === mode);
  });
  // Clear selections when switching modes
  state.selectedPacks = [];
  state.position = null;
  document.querySelectorAll('.prep-pack-row').forEach(r => r.classList.remove('active'));
  document.querySelectorAll('.pos-card').forEach(c => c.classList.remove('active'));
}

function initLanding() {
  // Mode toggle
  document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => setMode(btn.dataset.mode));
  });
  // Default to prep mode
  setMode('prep');

  // ── Role mode setup ──────────────────────────────────────────────────────
  const grid = $('position-grid');
  const pinnedLabel = document.createElement('p');
  pinnedLabel.className = 'section-label';
  pinnedLabel.textContent = 'Your target roles';
  pinnedLabel.style.cssText = 'margin-bottom:10px';
  grid.before(pinnedLabel);

  const pinnedGrid  = document.createElement('div');
  pinnedGrid.className = 'position-grid pinned-grid';

  const generalLabel = document.createElement('p');
  generalLabel.className = 'section-label';
  generalLabel.style.cssText = 'margin: 20px 0 10px';
  generalLabel.textContent = 'Other roles';

  const generalGrid = document.createElement('div');
  generalGrid.className = 'position-grid';

  grid.replaceWith(pinnedGrid);
  pinnedGrid.after(generalLabel);
  generalLabel.after(generalGrid);

  POSITIONS.forEach(p => {
    const card = document.createElement('div');
    card.className = p.pinned ? 'pos-card pos-card--pinned' : 'pos-card';
    card.innerHTML = `
      <div class="pos-icon">${p.icon}</div>
      <div class="pos-name">${p.name}</div>
      <div class="pos-desc">${p.desc}</div>`;
    card.addEventListener('click', () => {
      document.querySelectorAll('.pos-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      state.position = p.name;
      $('custom-position').value = '';
    });
    (p.pinned ? pinnedGrid : generalGrid).appendChild(card);
  });

  $('num-btn-group').addEventListener('click', e => {
    const btn = e.target.closest('.count-btn');
    if (!btn) return;
    $('num-btn-group').querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.numQuestions = +btn.dataset.n;
  });

  $('provider-btn-group').addEventListener('click', e => {
    const btn = e.target.closest('.count-btn');
    if (!btn) return;
    $('provider-btn-group').querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.provider = btn.dataset.p;
    $('api-key').placeholder = state.provider === 'openai' ? 'sk-...' : 'sk-ant-...';
    updateRoleApiKeyVisibility();
  });

  $('custom-position').addEventListener('input', e => {
    document.querySelectorAll('.pos-card').forEach(c => c.classList.remove('active'));
    state.position = e.target.value.trim() || null;
  });

  $('btn-start').addEventListener('click', startSession);

  // ── Prep mode setup ──────────────────────────────────────────────────────
  $('prep-provider-btn-group').addEventListener('click', e => {
    const btn = e.target.closest('.count-btn');
    if (!btn) return;
    $('prep-provider-btn-group').querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.prepProvider = btn.dataset.p;
    $('prep-api-key').placeholder = state.prepProvider === 'openai' ? 'sk-...' : 'sk-ant-...';
    updatePrepApiKeyVisibility();
  });

  $('prep-num-btn-group').addEventListener('click', e => {
    const btn = e.target.closest('.count-btn');
    if (!btn) return;
    $('prep-num-btn-group').querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.prepExtraQuestions = +btn.dataset.n;
    updatePrepApiKeyVisibility();
  });

  // Defaults
  state.prepProvider = 'claude-cli';
  state.provider = 'claude-cli';
  updatePrepApiKeyVisibility();
  updateRoleApiKeyVisibility();

  $('btn-start-prep').addEventListener('click', startPrepSession);

  // ── Shared ───────────────────────────────────────────────────────────────
  $('btn-new-session').addEventListener('click', resetToLanding);
}

function updatePrepApiKeyVisibility() {
  const needsKey = state.prepProvider !== 'claude-cli' && state.prepExtraQuestions > 0;
  $('prep-apikey-row').hidden = !needsKey;
}

function updateRoleApiKeyVisibility() {
  $('role-apikey-row').hidden = state.provider === 'claude-cli';
}

async function startPrepSession() {
  if (!state.selectedPacks.length) {
    alert('Please select a topic pack first.');
    return;
  }

  const apiKey = state.prepProvider !== 'claude-cli' ? $('prep-api-key').value.trim() : '';
  if (state.prepProvider !== 'claude-cli' && state.prepExtraQuestions > 0 && !apiKey) {
    alert('Please enter your API key.'); return;
  }

  const packRow = document.querySelector('.prep-pack-row.active');
  const packName = packRow ? packRow.querySelector('.prep-pack-name').textContent : 'Coding Interview Prep';
  const packDesc = packRow ? packRow.querySelector('.prep-pack-desc').textContent : '';
  const numQ = state.prepExtraQuestions || 0;

  showView('loading');
  $('loading-pos').textContent = packName;

  let step = 1;
  const stepInterval = setInterval(() => {
    if (step > 1) $(`ls-${step - 1}`).classList.replace('active', 'done');
    if (step <= 4) { $(`ls-${step}`).classList.add('active'); step++; }
  }, 800);

  try {
    const res = await fetch('/api/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        position:        packName,
        num_questions:   numQ,
        custom_topics:   packDesc || null,
        question_packs:  state.selectedPacks,
        provider:        state.prepProvider,
        api_key:         apiKey,
      }),
    });

    clearInterval(stepInterval);
    [1,2,3,4].forEach(n => { $(`ls-${n}`).classList.add('done'); });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail || res.statusText);
    }

    const data = await res.json();
    state.sessionId = data.session_id;
    localStorage.setItem('interview_session_id', state.sessionId);

    state.concepts = data.concepts || [];
    await loadSession(state.sessionId);
  } catch (err) {
    clearInterval(stepInterval);
    showView('landing');
    alert(`Failed to start session: ${err.message}`);
  }
}

async function startSession() {
  const pos = state.position || $('custom-position').value.trim();
  if (!pos) { alert('Please select or enter a role first.'); return; }

  const apiKey = state.provider !== 'claude-cli' ? $('api-key').value.trim() : '';
  if (state.provider !== 'claude-cli' && !apiKey) { alert('Please enter your API key.'); return; }

  state.position = pos;
  const topics = $('custom-topics').value.trim() || null;

  showView('loading');
  $('loading-pos').textContent = pos;

  // Animate loading steps
  let step = 1;
  const stepInterval = setInterval(() => {
    if (step > 1) $(`ls-${step - 1}`).classList.replace('active', 'done');
    if (step <= 4) {
      $(`ls-${step}`).classList.add('active');
      step++;
    }
  }, 1800);

  try {
    const res = await fetch('/api/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        position:       pos,
        num_questions:  state.numQuestions,
        custom_topics:  topics,
        question_packs: state.selectedPacks,
        provider:       state.provider,
        api_key:        apiKey,
      }),
    });

    clearInterval(stepInterval);
    [1,2,3,4].forEach(n => { $(`ls-${n}`).classList.add('done'); });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail || res.statusText);
    }

    const data = await res.json();
    state.sessionId = data.session_id;
    localStorage.setItem('interview_session_id', state.sessionId);

    state.concepts = data.concepts || [];
    await loadSession(state.sessionId);
  } catch (err) {
    clearInterval(stepInterval);
    showView('landing');
    alert(`Failed to start session: ${err.message}`);
  }
}

async function loadSession(sessionId) {
  const res = await fetch(`/api/sessions/${sessionId}`);
  if (!res.ok) throw new Error('Failed to load session');

  const data = await res.json();
  state.sessionId  = data.session_id;
  state.position   = data.position;

  // Prepend concept cards before actual questions
  const conceptCards = (state.concepts || []).map((c, i) => ({
    type: 'concept', id: `concept-${i}`,
    title: c.title, explanation: c.explanation,
    gotchas: c.gotchas || [], videos: c.videos || [],
    difficulty: 'easy', topic: 'Concept',
  }));
  state.questions  = [...conceptCards, ...data.questions];
  state.answers    = {};
  state.deferred   = new Set();

  const conceptOffset = (state.concepts || []).length;
  data.answers.forEach(a => {
    // feedback is stored as JSON string in DB — parse it back
    let fb = {};
    if (a.feedback) {
      try { fb = JSON.parse(a.feedback); } catch { fb = { feedback: a.feedback }; }
    }
    state.answers[a.question_index + conceptOffset] = {
      is_correct:  !!a.is_correct,
      feedback:    fb.feedback   || '',
      explanation: fb.explanation || '',
      remember:    fb.remember   || '',
    };
  });
  data.deferred && data.deferred.forEach(i => state.deferred.add(i + conceptOffset));

  $('sb-position').textContent = state.position;
  showSessionId(state.sessionId);
  buildNavDots();
  updateScoreboard();

  // Find first unanswered non-deferred question; fall back to first deferred
  const firstUnanswered = state.questions.findIndex(
    (_, i) => state.answers[i] === undefined && !state.deferred.has(i)
  );
  const firstDeferred = state.questions.findIndex(
    (_, i) => state.answers[i] === undefined && state.deferred.has(i)
  );
  const startIdx = firstUnanswered >= 0 ? firstUnanswered : (firstDeferred >= 0 ? firstDeferred : 0);
  renderQuestion(startIdx);
  showView('question');
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function markdownToHtml(md) {
  return marked.parse(md || '');
}

function showSessionId(id) {
  const short = id.slice(0, 8) + '…';
  $('session-id-val').textContent = short;
  $('session-id-box').onclick = () => {
    navigator.clipboard.writeText(id).then(() => {
      $('session-id-copy').textContent = 'Copied!';
      setTimeout(() => { $('session-id-copy').textContent = 'Copy'; }, 1500);
    });
  };
}

// ── Render question ───────────────────────────────────────────────────────────
function renderQuestion(idx) {
  state.currentIdx  = idx;
  state.selectedOpt = null;
  // Reset chat history and messages for new question
  chatState.history = [];
  const msgs = $('chat-messages');
  if (msgs) msgs.innerHTML = '';
  const q = state.questions[idx];

  // Meta
  $('q-num').textContent  = `${idx + 1} / ${state.questions.length}`;
  $('q-text').textContent = q.type === 'concept' ? q.title : q.question;

  // Show topic + optional pack-source badge
  $('q-topic').textContent = q.topic || 'Concept';
  let srcBadge = $('q-source-badge');
  if (!srcBadge) {
    srcBadge = document.createElement('span');
    srcBadge.id = 'q-source-badge';
    $('q-topic').after(srcBadge);
  }
  if (q.source) {
    srcBadge.className   = 'source-badge';
    srcBadge.textContent = `📝 ${q.source.replace(/_/g, ' ')}`;
    srcBadge.hidden      = false;
  } else {
    srcBadge.hidden = true;
  }

  const typeBadge = $('q-type-badge');
  typeBadge.textContent = q.type === 'concept' ? 'Concept' : q.type === 'find_the_bug' ? 'Find the Bug' : q.type === 'coding' ? 'Coding' : 'MCQ';
  typeBadge.className   = `badge badge-${q.type}`;

  const diffBadge = $('q-diff-badge');
  diffBadge.textContent = q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1);
  diffBadge.className   = `badge badge-${q.difficulty}`;

  // Company hint badge
  let companyBadge = $('q-company-badge');
  if (!companyBadge) {
    companyBadge = document.createElement('span');
    companyBadge.id = 'q-company-badge';
    diffBadge.after(companyBadge);
  }
  if (q.company_hint) {
    companyBadge.className   = 'badge badge-company';
    companyBadge.textContent = `🏢 ${q.company_hint}`;
    companyBadge.hidden      = false;
  } else {
    companyBadge.hidden = true;
  }

  // Hide all sections
  $('sec-concept').hidden = true;
  $('sec-mcq').hidden    = true;
  $('sec-bug').hidden    = true;
  $('sec-coding').hidden = true;

  if (q.type === 'concept') {
    renderConceptInline(q);
    // Hide submit/defer for concept cards — just "Next →"
    $('q-actions').hidden      = true;
    $('feedback-panel').hidden = true;
    refreshNavDots();
    return;
  }

  if (q.type === 'mcq') {
    renderMCQ(q);
  } else if (q.type === 'find_the_bug') {
    renderBugEditor(q);
  } else {
    renderCodingEditor(q);
  }

  // Reset actions / feedback
  $('q-actions').hidden   = false;
  $('feedback-panel').hidden = true;
  $('btn-submit').disabled   = false;
  $('btn-submit').textContent = 'Submit Answer';

  // Show/hide Do Later button
  const btnDefer = $('btn-defer');
  const isDeferred = state.deferred.has(idx);
  const isAnswered = state.answers[idx] !== undefined;
  btnDefer.hidden = isAnswered;
  btnDefer.textContent = isDeferred ? 'Un-defer ↩' : 'Do Later ⏭';
  btnDefer.classList.toggle('btn-defer--active', isDeferred);

  refreshNavDots();

  // If already answered, re-show feedback (read-only)
  if (isAnswered) {
    showFeedback(state.answers[idx], true);
    lockQuestion(q, state.answers[idx]);
  }
}

function renderConceptInline(q) {
  $('sec-concept').hidden = false;
  const body = $('concept-inline-body');

  const videosHtml = (q.videos || []).map(v => {
    const sourceClass = v.source === 'Udemy' ? 'source-udemy' : 'source-youtube';
    const icon = v.source === 'Udemy' ? '🎓' : '▶';
    return `<a href="${escapeHtml(v.url)}" target="_blank" rel="noopener noreferrer" class="video-link">
      <span class="video-icon">${icon}</span>
      <span class="video-title">${escapeHtml(v.title)}</span>
      <span class="video-source ${sourceClass}">${escapeHtml(v.source)}</span>
    </a>`;
  }).join('');

  const gotchasHtml = (q.gotchas || []).map(g =>
    `<li class="gotcha-item"><span class="gotcha-icon">⚡</span><span>${escapeHtml(g)}</span></li>`
  ).join('');

  const isLastConcept = state.questions[state.currentIdx + 1]?.type !== 'concept';
  const nextLabel = isLastConcept ? 'Start Questions →' : 'Next Concept →';

  body.innerHTML = `
    <div class="ci-explanation">${markdownToHtml(q.explanation || '')}</div>
    ${gotchasHtml ? `<div class="ci-section ci-gotchas"><div class="ci-label">Gotchas to Remember</div><ul>${gotchasHtml}</ul></div>` : ''}
    ${videosHtml ? `<div class="ci-section"><div class="ci-label">Watch First</div><div class="video-list">${videosHtml}</div></div>` : ''}
    <div class="ci-footer">
      <button class="btn-primary ci-btn-next">${nextLabel}</button>
    </div>
  `;

  body.querySelector('.ci-btn-next').addEventListener('click', () => {
    const nextIdx = state.currentIdx + 1;
    if (nextIdx < state.questions.length) renderQuestion(nextIdx);
  });
}

function renderMCQ(q) {
  $('sec-mcq').hidden = false;
  const container = $('options-container');
  container.innerHTML = '';

  (q.options || []).forEach((opt, i) => {
    const letters = ['A','B','C','D','E'];
    // Strip leading "A) " / "A. " prefix if present — the letter badge already shows it
    const displayText = opt.replace(/^[A-Ea-e][).]\s*/, '');
    const btn = document.createElement('button');
    btn.className = 'option-card';
    const letterSpan = document.createElement('span');
    letterSpan.className = 'option-letter';
    letterSpan.textContent = letters[i] || i+1;
    const textSpan = document.createElement('span');
    textSpan.textContent = displayText;
    btn.appendChild(letterSpan);
    btn.appendChild(textSpan);
    btn.addEventListener('click', () => {
      if (btn.disabled) return;
      document.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
      btn.classList.add('selected');
      state.selectedOpt = opt;
    });
    container.appendChild(btn);
  });
}

// ── Draft persistence ─────────────────────────────────────────────────────────
function draftKey(idx) {
  return `draft_${state.sessionId}_${idx}`;
}
function saveDraft(idx, code) {
  try { localStorage.setItem(draftKey(idx), code); } catch (_) {}
}
function loadDraft(idx) {
  try { return localStorage.getItem(draftKey(idx)); } catch (_) { return null; }
}
function clearDraft(idx) {
  try { localStorage.removeItem(draftKey(idx)); } catch (_) {}
}

let _draftTimer = null;
function attachDraftSaver(editor, idx) {
  editor.onDidChangeModelContent(() => {
    clearTimeout(_draftTimer);
    _draftTimer = setTimeout(() => saveDraft(idx, editor.getValue()), 500);
  });
}

function renderBugEditor(q) {
  $('sec-bug').hidden = false;
  $('bug-run-output').hidden = true;
  const lang = langSlug(q);
  $('bug-lang').textContent = lang;
  const draft = loadDraft(state.currentIdx);
  whenMonaco(() => {
    const ed = createOrUpdateEditor('bug-editor', draft ?? q.code ?? '', lang);
    attachDraftSaver(ed, state.currentIdx);
    attachRunButton('btn-run-bug', 'bug-run-output', 'bug-run-output-body', 'bug-run-output-label', lang, () => ed.getValue());
  });
  $('btn-bug-run-close').onclick = () => { $('bug-run-output').hidden = true; };
}

function renderCodingEditor(q) {
  $('sec-coding').hidden = false;
  $('run-output').hidden = true;
  const lang = langSlug(q);
  $('coding-lang').textContent = lang;
  const draft = loadDraft(state.currentIdx);
  whenMonaco(() => {
    const ed = createOrUpdateEditor('coding-editor', draft ?? q.starter_code ?? '', lang);
    attachDraftSaver(ed, state.currentIdx);
    attachRunButton('btn-run-code', 'run-output', 'run-output-body', 'run-output-label', lang, () => ed.getValue());
  });
  $('btn-run-close').onclick = () => { $('run-output').hidden = true; };
}

function attachRunButton(btnId, outputId, bodyId, labelId, lang, getCode) {
  const btn = $(btnId);
  btn.onclick = async () => {
    const code = getCode();
    if (!code.trim()) return;
    btn.disabled = true;
    btn.textContent = '⏳ Running…';
    $(outputId).hidden = false;
    $(bodyId).className = '';
    $(bodyId).textContent = 'Running…';
    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language: lang }),
      });
      const data = await res.json();
      const out = (data.stdout || '') + (data.stderr ? (data.stdout ? '\n' : '') + data.stderr : '');
      $(bodyId).textContent = out || '(no output)';
      $(bodyId).className = data.exit_code !== 0 ? 'error' : '';
      $(labelId).textContent = data.exit_code === 0 ? 'Output' : 'Output (error)';
    } catch (e) {
      $(bodyId).textContent = 'Run failed: ' + e.message;
      $(bodyId).className = 'error';
    } finally {
      btn.disabled = false;
      btn.textContent = '▶ Run';
    }
  };
}

function lockQuestion(q, answer) {
  // Lock MCQ options
  if (q.type === 'mcq') {
    document.querySelectorAll('.option-card').forEach(btn => {
      btn.disabled = true;
      const optText = btn.querySelector('span:last-child').textContent;
      if (optText === q.correct_answer_display) btn.classList.add('correct');
    });
  }
  // Lock editors
  if (state.bugEditor)  state.bugEditor.updateOptions({ readOnly: true });
  if (state.codeEditor) state.codeEditor.updateOptions({ readOnly: true });

  $('btn-submit').disabled = true;
  $('q-actions').hidden    = true;
}

// ── Do Later ──────────────────────────────────────────────────────────────────
$('btn-defer').addEventListener('click', async () => {
  const idx = state.currentIdx;
  const isDeferred = state.deferred.has(idx);

  if (isDeferred) {
    // Un-defer
    await fetch(`/api/sessions/${state.sessionId}/defer/${idx}`, { method: 'DELETE' });
    state.deferred.delete(idx);
  } else {
    // Defer
    const res = await fetch(`/api/sessions/${state.sessionId}/defer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_index: idx - state.concepts.length }),
    });
    if (res.ok) state.deferred.add(idx);
  }

  refreshNavDots();

  if (!isDeferred) {
    // Move to next unanswered non-deferred question
    const next = state.questions.findIndex(
      (_, i) => i > idx && state.answers[i] === undefined && !state.deferred.has(i)
    );
    const first = state.questions.findIndex(
      (_, i) => state.answers[i] === undefined && !state.deferred.has(i)
    );
    if (next >= 0) renderQuestion(next);
    else if (first >= 0) renderQuestion(first);
    else {
      // Only deferred remain — ask if they want to attempt them
      const goDeferred = confirm(
        'All non-deferred questions answered!\n\nAttempt your deferred questions now?'
      );
      if (goDeferred) {
        const firstDeferred = state.questions.findIndex(
          (_, i) => state.answers[i] === undefined && state.deferred.has(i)
        );
        if (firstDeferred >= 0) renderQuestion(firstDeferred);
        else showSummary();
      } else {
        showSummary();
      }
    }
  } else {
    // Just toggled off — update button label
    const btnDefer = $('btn-defer');
    btnDefer.textContent = 'Do Later ⏭';
    btnDefer.classList.remove('btn-defer--active');
  }
});

// ── Submit ────────────────────────────────────────────────────────────────────
$('btn-submit').addEventListener('click', submitAnswer);

async function submitAnswer() {
  const q = state.questions[state.currentIdx];
  let userAnswer = '';

  if (q.type === 'mcq') {
    if (!state.selectedOpt) { alert('Please select an option.'); return; }
    userAnswer = state.selectedOpt;
  } else if (q.type === 'find_the_bug') {
    userAnswer = state.bugEditor ? state.bugEditor.getValue() : '';
    if (!userAnswer.trim()) { alert('Please write your fix in the editor.'); return; }
  } else {
    userAnswer = state.codeEditor ? state.codeEditor.getValue() : '';
    if (!userAnswer.trim()) { alert('Please write your solution in the editor.'); return; }
  }

  $('btn-submit').disabled    = true;
  $('btn-submit').textContent = 'Evaluating…';

  try {
    const res = await fetch(`/api/sessions/${state.sessionId}/answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_index: state.currentIdx - state.concepts.length, user_answer: userAnswer }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail);
    }

    const result = await res.json();
    state.answers[state.currentIdx] = result;
    clearDraft(state.currentIdx);  // answer submitted — no need to keep draft
    updateScoreboard();
    refreshNavDots();

    // Highlight MCQ result
    if (q.type === 'mcq') {
      document.querySelectorAll('.option-card').forEach(btn => {
        btn.disabled = true;
        const optText = btn.querySelector('span:last-child').textContent;
        const isSelected = optText === userAnswer;
        const isCorrect  = optText === result.correct_option || result.is_correct && isSelected;
        if (isSelected && !result.is_correct) btn.classList.add('wrong');
        if (isSelected &&  result.is_correct) btn.classList.add('correct');
      });
    }

    $('q-actions').hidden = true;
    showFeedback(result, false);

  } catch (err) {
    $('btn-submit').disabled    = false;
    $('btn-submit').textContent = 'Submit Answer';
    alert(`Evaluation error: ${err.message}`);
  }
}

function showFeedback(result, readOnly) {
  const panel = $('feedback-panel');
  panel.hidden = false;

  const icon  = $('fb-icon');
  const title = $('fb-title');
  const q = state.questions[state.currentIdx];

  if (result.is_correct) {
    icon.className  = 'fb-icon correct';
    icon.textContent = '✓';
    title.className  = 'fb-title correct';
    title.textContent = 'Correct!';
  } else {
    icon.className   = 'fb-icon wrong';
    icon.textContent = '✕';
    title.className   = 'fb-title wrong';
    title.textContent = 'Not quite…';
  }

  $('fb-sub').textContent         = result.feedback || '';
  $('fb-explanation').textContent = result.explanation || '';
  $('fb-remember').textContent    = result.remember || '';

  // Show retry button for any wrong answer (not readOnly)
  const canRetry = !readOnly && !result.is_correct && q;
  $('btn-retry-question').hidden = !canRetry;

  // Show "Similar Question" button for all answered non-concept questions (not readOnly)
  const canSimilar = !readOnly && q && q.type !== 'concept';
  $('btn-similar').hidden = !canSimilar;

  // Show "Next" or "Summary" button
  const allDone = state.questions.every((_, i) => state.answers[i] !== undefined || state.deferred.has(i));
  $('btn-finish').hidden = !allDone;
  $('btn-next').hidden   = allDone;

  if (readOnly) {
    $('btn-next').hidden   = true;
    $('btn-finish').hidden = true;
    $('btn-retry-question').hidden = true;
    $('btn-similar').hidden = true;
  }
}

$('btn-similar').addEventListener('click', async () => {
  const btn = $('btn-similar');
  btn.disabled = true;
  btn.textContent = 'Generating…';

  try {
    const qIdx = state.currentIdx - state.concepts.length;
    const res = await fetch(`/api/sessions/${state.sessionId}/similar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_index: qIdx }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail);
    }
    const data = await res.json();
    // Append the new question to local state (with concept offset)
    const newIdx = state.questions.length;
    state.questions.push(data.question);
    buildNavDots();
    btn.disabled = false;
    btn.textContent = '+ Similar Question';
    // Navigate to it
    renderQuestion(newIdx);
  } catch (err) {
    btn.disabled = false;
    btn.textContent = '+ Similar Question';
    alert(`Failed to generate similar question: ${err.message}`);
  }
});

$('btn-retry-question').addEventListener('click', async () => {
  const idx = state.currentIdx;
  // Delete answer from backend
  await fetch(`/api/sessions/${state.sessionId}/answer/${idx - state.concepts.length}`, { method: 'DELETE' });
  // Reset local state
  delete state.answers[idx];
  updateScoreboard();
  refreshNavDots();
  // Re-render the question (hides feedback, re-enables editor)
  renderQuestion(idx);
});

$('btn-next').addEventListener('click', () => {
  // Find next unanswered non-deferred question
  const next = state.questions.findIndex(
    (_, i) => i > state.currentIdx && state.answers[i] === undefined && !state.deferred.has(i)
  );
  if (next >= 0) {
    renderQuestion(next);
  } else {
    const first = state.questions.findIndex(
      (_, i) => state.answers[i] === undefined && !state.deferred.has(i)
    );
    if (first >= 0) renderQuestion(first);
    else showSummary();
  }
});

$('btn-finish').addEventListener('click', showSummary);

// ── Summary ───────────────────────────────────────────────────────────────────
async function showSummary() {
  try {
    const res = await fetch(`/api/sessions/${state.sessionId}/summary`);
    if (!res.ok) throw new Error('Failed to load summary');
    const data = await res.json();
    renderSummary(data);
    showView('summary');
  } catch (err) {
    alert(`Could not load summary: ${err.message}`);
  }
}

function renderSummary(data) {
  $('summary-pos').textContent    = data.position;
  $('summary-title').textContent  = getGrade(data.score_pct);
  $('circle-pct').textContent     = `${data.score_pct}%`;
  $('stat-correct').textContent   = data.correct;
  $('stat-wrong').textContent     = data.answered - data.correct;
  $('stat-deferred').textContent  = data.deferred || 0;
  $('stat-total').textContent     = data.total;

  // Animate circle
  const circumference = 2 * Math.PI * 52; // 326.7
  const offset = circumference - (data.score_pct / 100) * circumference;
  setTimeout(() => {
    $('circle-prog').style.strokeDashoffset = offset;
    const color = data.score_pct >= 70 ? '#16a34a' : data.score_pct >= 40 ? '#d97706' : '#dc2626';
    $('circle-prog').style.stroke = color;
  }, 100);

  // Review list
  renderReview(data.review, 'all');

  // Filter buttons
  document.querySelectorAll('.filter-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderReview(data.review, btn.dataset.f);
    });
  });
}

function getGrade(pct) {
  if (pct >= 90) return '🏆 Outstanding!';
  if (pct >= 75) return '🎉 Great Job!';
  if (pct >= 55) return '👍 Good Effort!';
  if (pct >= 35) return '📚 Keep Practicing!';
  return '💪 Don\'t Give Up!';
}

function renderReview(items, filter) {
  const list = $('review-list');
  list.innerHTML = '';

  items.forEach((item, i) => {
    const wrong = !item.is_correct;
    const isDeferred = !!item.deferred;
    if (filter === 'wrong' && (!wrong || isDeferred)) return;
    if (filter === 'deferred' && !isDeferred) return;

    const el = document.createElement('div');
    el.className = 'review-item';

    const typeLabel = item.type === 'find_the_bug' ? 'Find the Bug' : item.type === 'coding' ? 'Coding' : 'MCQ';
    const diffClass = `badge-${item.difficulty}`;

    let codeBlock = '';
    if (item.code) {
      codeBlock = `<pre class="review-code">${escHtml(item.code)}</pre>`;
    }

    let optionsBlock = '';
    if (item.options && item.type === 'mcq') {
      optionsBlock = `<div style="font-size:13px;color:var(--muted);margin-bottom:6px">Options: ${item.options.join(' · ')}</div>`;
    }

    el.innerHTML = `
      <div class="review-item-header">
        <div class="review-verdict ${item.is_correct ? 'correct' : isDeferred ? 'deferred' : 'wrong'}">${item.is_correct ? '✓' : isDeferred ? '⏭' : '✕'}</div>
        <span class="badge ${diffClass}" style="font-size:11px">${item.difficulty}</span>
        <span class="badge" style="font-size:11px">${typeLabel}</span>
        <span class="topic-tag" style="font-size:11px">${item.topic}</span>
        <span style="font-size:12px;color:var(--muted);margin-left:auto">Q${item.question_index + 1}</span>
      </div>
      <div class="review-q">${escHtml(item.question)}</div>
      ${codeBlock}
      ${optionsBlock}
      <div class="review-user-answer">
        <strong>Your answer:</strong> ${escHtml(truncate(item.user_answer, 200))}
      </div>
      ${wrong ? `
        <div class="review-explanation">
          <strong>✅ Correct answer:</strong> ${escHtml(truncate(item.correct_answer, 300))}<br/><br/>
          ${escHtml(item.explanation)}
        </div>
        <div class="review-remember">💡 <strong>Remember:</strong> ${escHtml(item.remember)}</div>
      ` : `
        <div class="review-explanation" style="background:#dcfce7;color:#166534">
          ${escHtml(item.explanation)}
        </div>
      `}`;

    list.appendChild(el);
  });

  if (list.children.length === 0) {
    list.innerHTML = '<div style="padding:32px;text-align:center;color:var(--muted)">No questions to show.</div>';
  }
}

function escHtml(str) {
  return String(str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function truncate(str, n) {
  str = String(str || '');
  return str.length > n ? str.slice(0, n) + '…' : str;
}

// ── Custom question packs ─────────────────────────────────────────────────────

// Prep pack IDs and their week groupings (must match filenames in custom_questions/)
const PREP_WEEKS = [
  {
    label: 'Week 1-2: Python Fundamentals',
    icon:  '🐍',
    packs: ['prep_week1_python_fundamentals'],
  },
  {
    label: 'Week 3: Python Advanced',
    icon:  '⚡',
    packs: ['prep_week3_python_advanced'],
  },
  {
    label: 'Week 4-5: DSA Fundamentals',
    icon:  '🧩',
    packs: ['prep_week4_dsa_fundamentals'],
  },
  {
    label: 'Week 6: Trees & Graphs',
    icon:  '🌳',
    packs: ['prep_week6_trees_graphs'],
  },
  {
    label: 'Week 7: System Design',
    icon:  '🏗️',
    packs: ['prep_week7_system_design'],
  },
  {
    label: 'Week 8: AI & Agents',
    icon:  '🤖',
    packs: ['prep_week8_ai_agents'],
  },
];

const PREP_PACK_IDS = new Set(PREP_WEEKS.flatMap(w => w.packs));

async function fetchAndRenderPacks() {
  try {
    const res = await fetch('/api/question-packs');
    if (!res.ok) return;
    const packs = await res.json();
    if (!packs.length) return;

    const packMap = {};
    packs.forEach(p => { packMap[p.id] = p; });

    // ── Coding Interview Prep section ────────────────────────────────────────
    const prepPacks = packs.filter(p => PREP_PACK_IDS.has(p.id));
    if (prepPacks.length) {
      const weeksContainer = $('prep-weeks');
      weeksContainer.innerHTML = '';

      PREP_WEEKS.forEach((week, wi) => {
        const weekEl = document.createElement('div');
        weekEl.className = 'prep-week';

        const weekPacks = week.packs.map(id => packMap[id]).filter(Boolean);
        const totalQs = weekPacks.reduce((s, p) => s + p.count, 0);

        weekEl.innerHTML = `
          <div class="prep-week-header">
            <span class="prep-week-icon">${week.icon}</span>
            <span class="prep-week-title">${week.label}</span>
            <span class="prep-week-meta">${totalQs} questions</span>
            <span class="prep-week-chevron">▶</span>
          </div>
          <div class="prep-week-body"></div>`;

        const header = weekEl.querySelector('.prep-week-header');
        const body   = weekEl.querySelector('.prep-week-body');

        // Open first week by default
        if (wi === 0) weekEl.classList.add('open');

        header.addEventListener('click', () => {
          weekEl.classList.toggle('open');
        });

        weekPacks.forEach(pack => {
          const row = document.createElement('div');
          row.className = 'prep-pack-row';
          row.dataset.id = pack.id;
          row.innerHTML = `
            <div class="prep-pack-radio"><div class="prep-pack-radio-dot"></div></div>
            <div class="prep-pack-info">
              <div class="prep-pack-name">${pack.name}</div>
              <div class="prep-pack-desc">${pack.description || ''}</div>
            </div>
            <span class="prep-pack-count">${pack.count}q</span>`;

          row.addEventListener('click', () => {
            // Radio-select: deselect all other prep packs
            document.querySelectorAll('.prep-pack-row').forEach(r => {
              r.classList.remove('active');
              const id = r.dataset.id;
              state.selectedPacks = state.selectedPacks.filter(p => !PREP_PACK_IDS.has(p));
            });
            row.classList.add('active');
            state.selectedPacks = state.selectedPacks.filter(p => !PREP_PACK_IDS.has(p));
            state.selectedPacks.push(pack.id);
          });

          body.appendChild(row);
        });

        weeksContainer.appendChild(weekEl);
      });

      $('prep-section').hidden = false;
    }

    // ── Other custom packs ────────────────────────────────────────────────────
    const otherPacks = packs.filter(p => !PREP_PACK_IDS.has(p.id));
    if (otherPacks.length) {
      const grid = $('packs-grid');
      grid.innerHTML = '';

      otherPacks.forEach(pack => {
        const card = document.createElement('div');
        card.className = 'pack-card';
        card.dataset.id = pack.id;

        const hasError = pack.load_error || (pack.errors && pack.errors.length);
        card.innerHTML = `
          <div class="pack-card-top">
            <span class="pack-icon">${pack.icon || '📝'}</span>
            <div class="pack-toggle" id="toggle-${pack.id}">
              <div class="toggle-knob"></div>
            </div>
          </div>
          <div class="pack-name">${pack.name}</div>
          <div class="pack-desc">${pack.description || ''}</div>
          <div class="pack-meta">
            <span class="pack-count">${pack.count} question${pack.count !== 1 ? 's' : ''}</span>
            ${hasError ? `<span class="pack-warn" title="${pack.load_error || pack.errors.join('; ')}">⚠ issues</span>` : ''}
          </div>`;

        card.addEventListener('click', () => {
          if (pack.count === 0) return;
          const active = card.classList.toggle('active');
          if (active) {
            state.selectedPacks.push(pack.id);
          } else {
            state.selectedPacks = state.selectedPacks.filter(id => id !== pack.id);
          }
        });

        grid.appendChild(card);
      });

      $('packs-section').hidden = false;
    }
  } catch (e) {
    // packs are optional — silently skip if unavailable
  }
}

// ── Saved sessions (localStorage list) ───────────────────────────────────────
const SESSIONS_KEY = 'interview_saved_sessions';

function getSavedSessions() {
  try { return JSON.parse(localStorage.getItem(SESSIONS_KEY) || '[]'); }
  catch { return []; }
}

function saveSessionToList(id, position, answered, total) {
  const sessions = getSavedSessions().filter(s => s.id !== id); // dedupe
  sessions.unshift({
    id,
    position,
    answered,
    total,
    date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
  });
  localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions.slice(0, 10))); // keep last 10
}

function removeSessionFromList(id) {
  const sessions = getSavedSessions().filter(s => s.id !== id);
  localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions));
}

function renderSavedSessions() {
  const sessions = getSavedSessions();
  const card = $('saved-sessions-card');
  const list  = $('saved-sessions-list');
  if (!sessions.length) { card.hidden = true; return; }

  card.hidden = false;
  list.innerHTML = '';
  sessions.forEach(s => {
    const row = document.createElement('div');
    row.className = 'saved-session-row';
    row.innerHTML = `
      <div class="saved-session-info">
        <div class="saved-session-pos">${escapeHtml(s.position)}</div>
        <div class="saved-session-meta">${s.date} · ${s.answered || 0}/${s.total || '?'} answered</div>
      </div>
      <div class="saved-session-actions">
        <button class="btn-outline btn-sm" data-id="${s.id}">Resume →</button>
        <button class="btn-ghost btn-sm saved-session-delete" data-id="${s.id}" title="Remove">✕</button>
      </div>`;

    row.querySelector('.btn-outline').addEventListener('click', async () => {
      try { await loadSession(s.id); }
      catch { alert('Could not load session — it may have expired.'); removeSessionFromList(s.id); renderSavedSessions(); }
    });
    row.querySelector('.saved-session-delete').addEventListener('click', () => {
      removeSessionFromList(s.id);
      renderSavedSessions();
    });
    list.appendChild(row);
  });
}

// ── Save-before-leave modal ───────────────────────────────────────────────────
let _pendingLeaveCallback = null;

function promptSaveSession(onLeave) {
  if (!state.sessionId) { onLeave(); return; }
  if ($('view-landing').hidden === false) { onLeave(); return; } // already on landing
  const answered = Object.keys(state.answers).length;
  if (!answered) { onLeave(); return; } // nothing to save

  _pendingLeaveCallback = onLeave;
  $('modal-session-desc').textContent =
    `"${state.position}" — ${answered}/${state.questions.length} questions answered.`;
  $('save-session-modal').hidden = false;
}

$('modal-btn-save').addEventListener('click', () => {
  saveSessionToList(
    state.sessionId,
    state.position,
    Object.keys(state.answers).length,
    state.questions.length,
  );
  $('save-session-modal').hidden = true;
  if (_pendingLeaveCallback) { _pendingLeaveCallback(); _pendingLeaveCallback = null; }
});

$('modal-btn-discard').addEventListener('click', () => {
  $('save-session-modal').hidden = true;
  if (_pendingLeaveCallback) { _pendingLeaveCallback(); _pendingLeaveCallback = null; }
});

$('modal-btn-cancel').addEventListener('click', () => {
  $('save-session-modal').hidden = true;
  _pendingLeaveCallback = null;
});

// ── Navigation helpers ────────────────────────────────────────────────────────
function doResetToLanding() {
  localStorage.removeItem('interview_session_id');
  state.sessionId  = null;
  state.position   = null;
  state.questions  = [];
  state.answers    = {};
  state.deferred   = new Set();
  state.currentIdx = 0;
  state.selectedOpt = null;

  if (state.bugEditor)  { state.bugEditor.dispose();  state.bugEditor  = null; }
  if (state.codeEditor) { state.codeEditor.dispose(); state.codeEditor = null; }

  state.selectedPacks = [];
  document.querySelectorAll('.prep-pack-row').forEach(r => r.classList.remove('active'));
  document.querySelectorAll('.pos-card').forEach(c => c.classList.remove('active'));

  renderSavedSessions();
  showView('landing');
  setMode(state.mode);
}

function resetToLanding() {
  promptSaveSession(doResetToLanding);
}

$('btn-retry').addEventListener('click', () => {
  promptSaveSession(() => {
    doResetToLanding();
  });
});
$('btn-home').addEventListener('click', resetToLanding);

// ── Init ──────────────────────────────────────────────────────────────────────
function init() {
  localStorage.removeItem('interview_session_id');
  $('save-session-modal').hidden = true; // ensure modal never shows on load
  initLanding();
  fetchAndRenderPacks();
  renderSavedSessions();
  initChat();
}

// ── Claude Chat ───────────────────────────────────────────────────────────────

function initChat() {
  $('chat-fab').addEventListener('click', openChat);
  $('chat-close').addEventListener('click', closeChat);
  $('chat-send').addEventListener('click', sendChat);
  $('chat-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
  });
  initVoiceInput();
}

function initVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const micBtn = $('chat-mic');
  if (!SpeechRecognition) {
    micBtn.title = 'Voice input not supported in this browser';
    micBtn.style.opacity = '0.4';
    micBtn.style.cursor = 'not-allowed';
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = true;
  recognition.continuous = false;

  let isRecording = false;
  let interimStart = 0; // char position where interim text starts

  micBtn.addEventListener('click', () => {
    if (isRecording) {
      recognition.stop();
    } else {
      recognition.start();
    }
  });

  recognition.onstart = () => {
    isRecording = true;
    micBtn.classList.add('recording');
    micBtn.title = 'Listening… click to stop';
    const input = $('chat-input');
    // Mark where we'll insert interim text
    interimStart = input.value.length;
    if (interimStart > 0 && !input.value.endsWith(' ')) {
      input.value += ' ';
      interimStart = input.value.length;
    }
  };

  recognition.onresult = e => {
    const input = $('chat-input');
    let interim = '';
    let final = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) final += e.results[i][0].transcript;
      else interim += e.results[i][0].transcript;
    }
    // Replace everything from interimStart onwards
    input.value = input.value.slice(0, interimStart) + (final || interim);
    if (final) interimStart = input.value.length;
  };

  recognition.onend = () => {
    isRecording = false;
    micBtn.classList.remove('recording');
    micBtn.title = 'Voice input';
    // Trim trailing space if nothing was spoken
    const input = $('chat-input');
    input.value = input.value.trimEnd();
    input.focus();
  };

  recognition.onerror = e => {
    isRecording = false;
    micBtn.classList.remove('recording');
    micBtn.title = 'Voice input';
    if (e.error !== 'aborted') console.warn('Speech recognition error:', e.error);
  };
}

function openChat() {
  $('chat-panel').hidden = false;
  $('chat-fab').hidden   = true;
  $('chat-input').focus();
}

function closeChat() {
  $('chat-panel').hidden = true;
  $('chat-fab').hidden   = false;
}

// Show/hide the FAB only when in the question view
function setChatVisible(visible) {
  $('chat-fab').hidden   = !visible;
  if (!visible) $('chat-panel').hidden = true;
}

function chatContext() {
  const q = state.questions[state.currentIdx];
  if (!q) return 'No question loaded.';
  if (q.type === 'concept') {
    return `Concept: ${q.title}\n\n${q.explanation || ''}`;
  }
  let ctx = `Question type: ${q.type}\nTopic: ${q.topic}\nDifficulty: ${q.difficulty}\n\n${q.question}`;
  if (q.code) ctx += `\n\nOriginal code:\n${q.code}`;
  if (q.starter_code) ctx += `\n\nStarter code:\n${q.starter_code}`;

  // Include whatever the user has typed in the editor right now
  const liveCode = q.type === 'find_the_bug'
    ? (state.bugEditor  && state.bugEditor.getValue())
    : (state.codeEditor && state.codeEditor.getValue());
  if (liveCode && liveCode.trim()) ctx += `\n\nUser's current code:\n${liveCode}`;

  return ctx;
}

function appendChatBubble(role, text, streaming) {
  const wrap = document.createElement('div');
  wrap.className = `chat-bubble chat-bubble--${role}`;
  if (streaming) wrap.id = 'chat-streaming-bubble';
  wrap.innerHTML = markdownToHtml(text);
  $('chat-messages').appendChild(wrap);
  $('chat-messages').scrollTop = $('chat-messages').scrollHeight;
  return wrap;
}

async function sendChat() {
  if (chatState.streaming) return;
  const input = $('chat-input');
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  chatState.history.push({ role: 'user', content: text });
  appendChatBubble('user', text);

  chatState.streaming = true;
  $('chat-send').disabled = true;

  const streamBubble = appendChatBubble('assistant', '…', true);
  let accumulated = '';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        context: chatContext(),
        messages: chatState.history,
      }),
    });

    if (!res.ok) throw new Error(await res.text());

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // keep incomplete line
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const payload = line.slice(6);
        if (payload === '[DONE]') break;
        try {
          const obj = JSON.parse(payload);
          if (obj.error) throw new Error(obj.error);
          if (obj.text) {
            accumulated += obj.text;
            streamBubble.innerHTML = markdownToHtml(accumulated);
            $('chat-messages').scrollTop = $('chat-messages').scrollHeight;
          }
        } catch (_) {}
      }
    }

    streamBubble.id = '';
    chatState.history.push({ role: 'assistant', content: accumulated });
  } catch (err) {
    streamBubble.innerHTML = `<em style="color:var(--error)">Error: ${err.message}</em>`;
    streamBubble.id = '';
  } finally {
    chatState.streaming = false;
    $('chat-send').disabled = false;
    input.focus();
  }
}

init();
