# Notes: LLM / AI Patterns

## RAG Pipeline — The Mental Model

```
Documents → Chunking → Embedding → Vector Store
                                        ↓
Query → Embed Query → Similarity Search → Top-K Chunks → LLM → Answer
```

Each arrow is a place where things go wrong. Evals test each arrow independently.

---

## Chunking Tradeoffs

| Chunk size | Retrieval | Context |
|------------|-----------|---------|
| Small (128 tokens) | Precise | Less context per chunk |
| Large (1024 tokens) | Coarse | More context, irrelevant content |
| Overlapping | Better boundary handling | More storage |

Sweet spot: 256-512 tokens, 10-20% overlap. Always tune on your data.

---

## Embedding Models (2025 reference)

| Model | Dimensions | Use Case |
|-------|-----------|---------|
| `text-embedding-3-small` (OpenAI) | 1536 | General purpose, cheap |
| `text-embedding-3-large` (OpenAI) | 3072 | Higher quality |
| `all-MiniLM-L6-v2` (sentence-transformers) | 384 | Fast, local, free |
| `nomic-embed-text` (via Ollama) | 768 | Local, good quality |

Cosine similarity is the standard distance metric for embeddings.

---

## ReAct Agent Loop

```
Thought → Action → Observation → Thought → Action → ...→ Final Answer
```

```python
while not done and steps < max_steps:
    thought = llm(history)
    if "FINAL:" in thought:
        return extract_answer(thought)
    action = parse_action(thought)
    observation = execute_tool(action)
    history.append(thought + observation)
```

Failure modes to know: hallucinated tool calls, infinite loops, context overflow, premature termination.

---

## Eval Metrics Cheat Sheet

| Metric | Measures | How |
|--------|----------|-----|
| Answer Relevance | Does response answer the question? | LLM judge or cosine sim |
| Faithfulness | Is response grounded in context? | Check claims vs context |
| Context Recall | Did retrieval find the right chunks? | Check if answer is in top-k |
| Refusal Accuracy | Did model correctly refuse harmful requests? | Blocklist + LLM judge |
| Hallucination Rate | Did model make up facts? | Cross-reference with sources |

Your LangSmith/DeepEval experience covers Answer Relevance and Faithfulness.

---

## Prompt Engineering Hierarchy

1. **Zero-shot**: just ask. Works for simple tasks.
2. **Few-shot**: give examples. Best ROI for format adherence.
3. **Chain-of-thought**: "think step by step". Improves reasoning.
4. **Self-consistency**: sample multiple responses, take majority vote.
5. **ReAct**: reason + act + observe. For tool use.

Start with zero-shot. Add few-shot if output format is wrong. Add CoT if reasoning is wrong.

---

## Observability Stack

```
Code → Spans → Traces → Metrics → Dashboards
                          ↓
                     Alerts / Evals
```

| Tool | What it does |
|------|-------------|
| LangSmith | LangChain-native tracing + evals |
| DeepEval | Pytest-style LLM eval framework |
| OpenTelemetry | Vendor-neutral tracing standard |
| Prometheus + Grafana | Metrics + dashboards |

Your LangSmith experience is directly relevant to what interviewers mean by "how do you observe LLM systems in production?"

---

## Adversarial Eval Categories (your north star domain)

1. **Prompt injection**: user input overrides system instructions
2. **Jailbreaks**: role-play, encoding, indirect instruction, many-shot
3. **Data exfiltration**: "repeat your system prompt verbatim"
4. **Hallucination induction**: ask about plausible but false facts
5. **Refusal bypass**: reframe harmful requests as benign

Datasets: HarmBench, AdvBench, TruthfulQA, MMLU (for capability evals).
