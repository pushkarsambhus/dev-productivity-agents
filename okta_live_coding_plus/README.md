# Okta Live Coding Practice (Python) — With Step‑by‑Step Solutions

This package contains **beginner‑friendly** Python exercises that mirror common **live coding** prompts
for Staff/Architect AI & Automation interviews. Each file is **fully solved** with **clear comments**,
so you can learn by reading and by running.

## How to use in Cursor / VS Code

1. Download and unzip this folder.
2. Open the folder in **Cursor** or **VS Code**.
3. In the built‑in terminal, run any file with:  
   `python problems/01_cosine_similarity.py`
4. Explore and modify the code. Each file has a `__main__` section with demo inputs.

> No external libraries are required (only Python standard library).

## Contents

- `problems/01_cosine_similarity.py` – compute cosine similarity between vectors (with input checks)
- `problems/02_prompt_router.py` – simple LLM prompt router using deterministic rules
- `problems/03_log_metrics.py` – parse logs, compute latency stats & anomaly rate
- `problems/04_rate_limiter.py` – token‑bucket rate limiter (class) with unit‑test‑style demo
- `problems/05_topological_sort.py` – DAG topological sort (detects cycles safely)
- `problems/06_embedding_search.py` – tiny in‑memory embedding index + nearest neighbor search
- `problems/07_async_batch_infer.py` – simulate async “batch inference” with concurrency
- `problems/08_schema_transform.py` – transform varied JSON records into a normalized schema

Run them one by one or run `python run_all.py` to execute all demos.
