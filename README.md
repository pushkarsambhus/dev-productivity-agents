# Dev Productivity Agents

This repo explores how **AI/ML can transform developer productivity** by building lightweight agents that reduce manual toil in the software development lifecycle:
- **Build Fixer Agent** → triages noisy CI logs and suggests actionable fixes.
- **Test Suggestion Agent** → proposes tests from code diffs to improve coverage.

The focus is on blending **rule-based heuristics** with **optional AI enrichment** to provide reliable, scalable helpers for developers. The agents are simple prototypes, but they demonstrate how intelligent automation can accelerate common engineering workflows.

## Why This Project
- Engineers often spend significant time debugging builds and writing repetitive tests.
- These prototypes show how **automation + AI agents** can reduce friction and speed up delivery.

### Why This Matters
Build failures and pipeline issues often waste hours of developer time. By automating triage and test case suggestions, this project reduces manual toil, accelerates CI/CD cycles, and improves developer productivity across large teams.

### Trade-offs & Design Choices
- **Heuristics-first:** Designed to provide quick, offline answers; optional LLM integration adds richer suggestions but requires cost/API keys.
- **Slack + API integration:** Chosen for accessibility; in production, this would extend to other collaboration tools and dashboards.
- **Scope:** Prototype-level agent; production deployments would need stronger observability and caching.


![CI](https://github.com/pushkarsambhus/dev-productivity-agents/actions/workflows/ci.yml/badge.svg)

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# (Optional) set your API key
export OPENAI_API_KEY=sk-...

# Run the API
uvicorn app.main:app --reload
```

Example requests:
```bash
curl -X POST http://127.0.0.1:8000/triage -H "Content-Type: application/json" -d @examples/sample_logs/npm_fail.json
curl -X POST http://127.0.0.1:8000/suggest-tests -H "Content-Type: application/json" -d '{"repo":"example-service","diff":"added endpoint /users"}'
```

## Next Steps
- Integrate with Slack as a slash command (`/triage`)
- Expand to other ecosystems (Gradle, Docker builds, PyPI errors)
- Experiment with LangGraph for multi-agent orchestration
- Explore how this approach scales in enterprise CI/CD pipelines

---

**License**: MIT  
