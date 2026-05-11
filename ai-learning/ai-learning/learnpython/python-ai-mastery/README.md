# 🐍 Python → AI Mastery

A self-paced, structured learning repo that takes you from Python basics to building and evaluating production AI systems.

Built for: Principal Engineers transitioning into AI/ML roles, with a focus on interview readiness.

---

## 📍 Learning Path

```
Phase 1: Core Python         → Syntax, idioms, data structures
Phase 2: Algorithms & DS     → Interview-level problem solving
Phase 3: System Design Code  → Queues, caches, schedulers, rate limiters
Phase 4: LLM / AI Patterns   → RAG, agents, evals, observability
Phase 5: Interview Problems  → Principal-level mock problems
```

Work through phases **in order**. Each folder has:
- `problem.py` — description + starter code
- `solution.py` — reference solution with explanation comments
- `notes.md` — key concepts, gotchas, interview tips

---

## 🗂 Structure

```
python-ai-mastery/
├── 01_core_python/
│   ├── 01_basics/
│   ├── 02_data_structures/
│   ├── 03_functions_and_scope/
│   ├── 04_oop/
│   └── 05_pythonic_idioms/
├── 02_algorithms_and_ds/
│   ├── 01_arrays_strings/
│   ├── 02_hashmaps_sets/
│   ├── 03_stacks_queues/
│   ├── 04_trees_graphs/
│   └── 05_sorting_searching/
├── 03_system_design_coding/
│   ├── 01_queues_schedulers/
│   ├── 02_caching/
│   ├── 03_rate_limiting/
│   └── 04_pub_sub/
├── 04_llm_ai_patterns/
│   ├── 01_prompt_engineering/
│   ├── 02_rag_basics/
│   ├── 03_agents_tools/
│   ├── 04_evals_testing/
│   └── 05_observability/
└── 05_interview_problems/
    ├── 01_easy/
    ├── 02_medium/
    └── 03_principal_level/
```

---

## ⚡ How to Use

1. Open a folder's `problem.py` — read the docstring, try to solve it
2. Run it: `python problem.py`
3. Stuck? Check `notes.md` for hints
4. Compare with `solution.py`
5. Move on only when the concept clicks

> **Rule:** Don't skip phases. Phase 1 idioms show up directly in Phase 4 AI code.

---

## 🎯 End Goal

By the end of this repo you should be able to:
- Write clean, idiomatic Python without hesitation
- Solve medium/hard DS&A problems in an interview setting
- Design and code system components (rate limiter, task queue, cache)
- Build a basic RAG pipeline and agent from scratch
- Write LLM evals and explain adversarial testing strategies
- Discuss all of the above at principal / staff engineer depth

---

## 🛠 Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📦 Requirements

See `requirements.txt` — starts minimal, grows as you reach Phase 4.
