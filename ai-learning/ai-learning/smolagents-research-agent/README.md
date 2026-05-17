# smolagents Research Agent

A command-line research tool that uses [smolagents](https://github.com/huggingface/smolagents) to answer questions by combining web search with autonomous code execution. It runs a `CodeAgent` backed by `DuckDuckGoSearchTool` and a Claude model via LiteLLM. You ask a question; the agent searches the web, optionally writes and runs Python code to process the results, and returns a clean, structured answer — all from your terminal.

---

## Prerequisites

- Python 3.10 or newer
- An [Anthropic API key](https://console.anthropic.com/) exported as an environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Installation

```bash
# 1. Clone the repo (or navigate to the project folder)
git clone https://github.com/pushkarsambhus/ai-learning.git
cd ai-learning/smolagents-research-agent

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate.bat     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

Make `main.py` executable (macOS / Linux):

```bash
chmod +x main.py
```

---

## Usage

### Basic

```bash
python main.py "your research question here"
```

### With flags

```bash
# Change the model
python main.py --model anthropic/claude-opus-4-5 "What is the state of quantum computing in 2025?"

# Increase the step limit for complex questions
python main.py --max-steps 25 "Summarise all major central bank rate decisions in Q1 2025"

# Show full agent reasoning and tool-call trace
python main.py --verbose "Compare Python and Rust performance benchmarks in 2025"
```

### Interactive mode

If you omit the question, the agent prompts you:

```bash
python main.py
# > Enter your research question: ...
```

### All flags

| Flag | Default | Description |
|---|---|---|
| `question` | (prompted) | The research question to answer |
| `--model` | `anthropic/claude-3-5-sonnet-20241022` | LiteLLM model ID |
| `--max-steps` | `15` | Max agent reasoning iterations |
| `--verbose` | off | Print full agent trace |

---

## How it works

```
User question
     │
     ▼
CodeAgent (smolagents)
     │
     ├─► DuckDuckGoSearchTool  ──► web results
     │
     ├─► Python code execution ──► computed results
     │
     └─► Final answer (Rich panel)
```

1. **LiteLLMModel** wraps Claude (or any LiteLLM-compatible model) and drives the agent's reasoning.
2. **DuckDuckGoSearchTool** performs free, unauthenticated web searches via the `duckduckgo-search` library.
3. **CodeAgent** orchestrates multi-step reasoning: it can call tools, inspect their outputs, write Python code, execute it in a sandboxed interpreter, and iterate until it has a confident answer.
4. **Rich** formats the terminal output with spinners, panels, and colour.

---

## Error handling

| Situation | What happens |
|---|---|
| Agent exceeds `--max-steps` | Friendly message with partial results + hint to raise the limit |
| DuckDuckGo tool fails | Tool name and error reason printed; suggests retrying |
| `ANTHROPIC_API_KEY` not set | Clear error before the agent starts |
| Anthropic API connection error | Network error message with retry hint |
| Anthropic rate limit hit | Rate-limit message with model-switch suggestion |
| Any other exception | Caught and displayed with the exception type |

---

## Example queries

```bash
python main.py "What are the top 3 programming languages in 2025 and their main use cases?"

python main.py "Compare the market cap of Apple and Microsoft as of early 2025 and calculate the percentage difference"

python main.py "What were the key AI model releases in the first half of 2025, and which company released the most?"

python main.py "What is the current price of gold per ounce and how has it changed year-over-year?"

python main.py "Summarise the key differences between React 19 and React 18"
```

---

## Examples directory

The `examples/` folder contains pre-written terminal traces showing realistic agent output for three sample queries:

- `examples/example1.txt` — Top programming languages in 2025
- `examples/example2.txt` — Apple vs. Microsoft market cap comparison (verbose mode)
- `examples/example3.txt` — Key AI model releases H1 2025 (multi-step search + code)

These illustrate the kind of reasoning trace and final-answer format you can expect.
