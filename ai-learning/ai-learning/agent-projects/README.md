# AI Agent Learning Projects

Four end-to-end projects for learning how to build, evaluate, secure, and ship AI agents with the Anthropic Claude API. Each project is self-contained with working code, unit tests, eval runners, and an interactive architecture diagram.

---

## Projects

| # | Folder | Focus | Target Roles |
|---|--------|-------|-------------|
| 1 | `01-single-agent` | Tool-use agentic loop | AI/ML Engineer |
| 2 | `02-multi-agent` | Multi-agent pipelines | AI/ML Engineer |
| 3 | `03-red-team` | Attack suites + defence layers | Red Team / Security |
| 4 | `04-ai-product` | Cost, A/B testing, eval platform | PM / EM / TPM / AI Platform Eval |

---

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies for a project:

```bash
cd 01-single-agent
uv sync
# or, without a pyproject.toml:
uv pip install anthropic pytest pytest-mock
```

Set your API key (only needed for integration/eval runs — unit tests work without it):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Project 1 — Single Agent (`01-single-agent`)

**What it teaches:** The core agentic loop: send message → Claude decides to use a tool → execute tool → send result back → repeat until done.

```
agent-projects/01-single-agent/
├── config.py          # API key, model, system prompt, feature flags
├── tools.py           # Tool schemas + handlers (web_search, calculator, time, fetch_url)
├── agent.py           # Agentic loop, streaming variant, multi-turn session
├── tests/
│   ├── test_tools.py  # Unit tests — no API key needed
│   └── test_agent.py  # Mocked loop tests — no API key needed
├── evals/
│   ├── eval_cases.json
│   └── eval_runner.py # Requires ANTHROPIC_API_KEY
└── architecture.html  # Interactive diagram — open in browser
```

**Key concepts:**
- `stop_reason == "tool_use"` triggers tool execution
- Tool results sent back as `tool_result` content blocks
- `MAX_TURNS` guard prevents infinite loops

**Run tests:**
```bash
cd 01-single-agent
uv run pytest tests/ -v
```

**Run evals** (requires API key):
```bash
python evals/eval_runner.py
```

**View architecture:** Open `architecture.html` in any browser.

---

## Project 2 — Multi-Agent (`02-multi-agent`)

**What it teaches:** How to compose multiple agents into pipelines — hardcoded sequences, Claude-driven dynamic orchestration, and parallel fan-out.

```
agent-projects/02-multi-agent/
├── config.py              # Per-agent model config, revision limits
├── agents/
│   ├── researcher.py      # Web search + fetch, returns structured brief
│   ├── writer.py          # Drafts content from research brief
│   └── critic.py          # Reviews draft, returns {verdict, feedback, approve}
├── orchestrator.py        # Hardcoded pipeline, dynamic orchestration, parallel research
├── tests/
│   └── test_orchestrator.py
├── evals/
│   ├── eval_cases.json
│   └── eval_runner.py
└── architecture.html      # Toggle: Hardcoded Pipeline vs Dynamic Orchestrator
```

**Key concepts:**
- `PipelineState` dataclass carries full audit trail across agents
- Dynamic orchestration: Claude decides which agent to call next via tool use
- Parallel fan-out with `ThreadPoolExecutor` for independent research tasks
- Critic → Writer revision loop with `MAX_REVISION_ROUNDS` guard

**Run tests:**
```bash
cd 02-multi-agent
uv run pytest tests/ -v
```

---

## Project 3 — Red Team (`03-red-team`)

**What it teaches:** How LLMs can be attacked and how to defend them. Practical for red team roles, security reviews, and building safety-aware products.

```
agent-projects/03-red-team/
├── config.py
├── attacks/
│   ├── prompt_injection.py   # Direct + indirect injection (6 + 2 payloads)
│   ├── jailbreak.py          # DAN, base64, many-shot, roleplay, token smuggling
│   └── data_extraction.py    # 7 payloads trying to leak system prompt
├── defenses/
│   ├── input_sanitizer.py    # Regex-based scoring, blocks suspicious inputs
│   └── output_validator.py   # Checks responses for compliance violations + PII
├── red_team_runner.py         # Full assessment runner, Markdown report, CI-friendly exit codes
├── tests/
│   ├── test_defenses.py      # 20 tests — no API key needed
│   └── test_attacks.py       # Payload schema + judge logic tests
├── evals/
│   ├── eval_cases.json       # Pass criteria: bypass rates, severity counts
│   └── eval_runner.py
└── architecture.html
```

**Defence layers:**
1. Input Sanitizer — blocks high-risk inputs before they reach the model
2. Prompt Hardening — system prompt tells the model how to handle attacks
3. Tool Output Wrapping — labels tool results as DATA, not instructions
4. Output Validator — scans responses for compliance violations and PII leaks

**LLM-as-judge:** A separate Claude call evaluates each attack response with `VERDICT / SEVERITY / EXPLANATION`.

**Run tests:**
```bash
cd 03-red-team
uv run pytest tests/ -v
```

**Run full assessment** (requires API key):
```bash
python red_team_runner.py --hardened --report report.md
```

Exit codes: `0` = MEDIUM/LOW risk, `1` = CRITICAL/HIGH findings (pipe into CI).

---

## Project 4 — AI Product (`04-ai-product`)

**What it teaches:** Everything a PM, EM, TPM, or AI Platform Eval engineer needs to operate an AI product in production: cost tracking, latency SLAs, A/B model comparison, quality regression testing, and benchmarking.

```
agent-projects/04-ai-product/
├── config.py
├── tracking/
│   ├── cost_tracker.py     # Per-call cost: input_tokens × price + output_tokens × price
│   ├── latency_tracker.py  # P50/P95/P99, SLA breach rate, context manager for timing
│   └── usage_reporter.py   # Aggregated cost + latency reports, budget alerts
├── ab_testing/
│   ├── experiment.py       # Run Model A vs Model B on same prompts, judge winner
│   └── statistical_analysis.py  # Wilson CI, Cohen's d, significance test (no scipy)
├── platform_eval/
│   ├── llm_judge.py        # Score responses 1-10, head-to-head comparison, batch scoring
│   ├── regression_suite.py # Detect quality regressions between model versions
│   └── benchmark.py        # Category benchmarks: reasoning, factual, coding, safety
├── tests/
│   ├── test_cost_tracker.py
│   ├── test_ab_testing.py
│   └── test_llm_judge.py
├── evals/
│   ├── eval_cases.json
│   └── eval_runner.py      # --dry-run flag for testing without API key
└── architecture.html       # Tabs: A/B Flow | Eval Pipeline | Key Metrics | Model Decision Tree
```

**Model pricing (as of 2025):**

| Model | Input | Output |
|-------|-------|--------|
| `claude-haiku-4-5` | $0.80 / 1M tokens | $4.00 / 1M tokens |
| `claude-sonnet-4-6` | $3.00 / 1M tokens | $15.00 / 1M tokens |

**Key workflows:**

Track costs per call:
```python
from tracking.cost_tracker import CostTracker
tracker = CostTracker()
response = client.messages.create(...)
cost = tracker.record(model, response.usage)
print(f"This call cost ${cost.total_cost_usd:.4f}")
```

Run an A/B experiment:
```python
from ab_testing.experiment import run_experiment
result = run_experiment(prompts=["Explain quantum entanglement", ...])
print(result.recommendation)  # "USE_A", "USE_B", or "INCONCLUSIVE"
```

Detect regressions before shipping a new model:
```python
from platform_eval.regression_suite import run_regression, compare_regression_runs
baseline = run_regression("claude-sonnet-4-6")
candidate = run_regression("claude-opus-4-6")
diff = compare_regression_runs(baseline, candidate)
print(diff["regressions"])  # Cases that got worse
```

**Run tests:**
```bash
cd 04-ai-product
uv run pytest tests/ -v
```

**Run evals** (requires API key):
```bash
python evals/eval_runner.py
python evals/eval_runner.py --dry-run  # no API key needed
```

---

## Learning Path

```
01-single-agent   →  Understand the tool-use loop
       ↓
02-multi-agent    →  Compose agents into pipelines
       ↓
03-red-team       →  Attack and harden your agents
       ↓
04-ai-product     →  Measure cost, quality, and reliability
```

Each project builds on the previous. Start with 01, read the comments in every file, then run the tests to see the concepts in action.

---

## Running All Tests (no API key needed)

```bash
cd agent-projects
for project in 01-single-agent 02-multi-agent 03-red-team 04-ai-product; do
    echo "=== $project ==="
    (cd $project && uv pip install -r requirements.txt -q && uv run pytest tests/ -v --tb=short)
done
```

---

## Architecture Diagrams

Each project has an `architecture.html` — open it in any browser, no server needed:

```bash
open agent-projects/01-single-agent/architecture.html
open agent-projects/02-multi-agent/architecture.html
open agent-projects/03-red-team/architecture.html
open agent-projects/04-ai-product/architecture.html
```

Diagrams are interactive: click nodes to highlight data flow, hover for tooltips, switch tabs for different views.
