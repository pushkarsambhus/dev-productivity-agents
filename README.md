# Dev Productivity Agents

[![CI](https://github.com/pushkarsambhus/dev-productivity-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/pushkarsambhus/dev-productivity-agents/actions/workflows/ci.yml)

Lightweight AI agents that cut developer toil in CI/CD pipelines. Two agents, heuristics-first with optional LLM enrichment:

- **Build Fixer Agent** — triages noisy CI logs and surfaces actionable root-cause suggestions
- **Test Suggestion Agent** — proposes test cases from code diffs to improve coverage

Inspired by a production system that reduced build failure triage from 20+ minutes to near-immediate results across 60+ engineering teams.

## Stack

Python · FastAPI · OpenAI API (optional)

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...   # optional — heuristics work without it

uvicorn app.main:app --reload
```

## Example requests

```bash
# Triage a CI log
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d @examples/sample_logs/npm_fail.json

# Suggest tests for a diff
curl -X POST http://localhost:8000/suggest-tests \
  -H "Content-Type: application/json" \
  -d '{"repo": "example-service", "diff": "added endpoint /users"}'
```

## Design notes

- **Heuristics-first** — fast, offline answers by default; LLM adds richer context when an API key is present
- **Prototype scope** — production deployments would add observability, caching, and multi-ecosystem support (Gradle, Docker, PyPI)

## License

MIT
