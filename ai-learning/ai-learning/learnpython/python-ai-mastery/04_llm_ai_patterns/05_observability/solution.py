"""
SOLUTION: Phase 4 | LLM / AI Patterns | 05 Observability
"""
import time
import uuid
from dataclasses import dataclass, field
from contextlib import contextmanager
from collections import defaultdict


@dataclass
class Span:
    span_id: str
    name: str
    start_time: float
    end_time: float = 0.0
    attributes: dict = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_ms(self) -> float:
        return round((self.end_time - self.start_time) * 1000, 2)

    @property
    def is_error(self) -> bool:
        return self.error is not None


@dataclass
class Trace:
    trace_id: str
    spans: list[Span] = field(default_factory=list)

    def add_span(self, span: Span):
        self.spans.append(span)

    @property
    def total_duration_ms(self) -> float:
        if not self.spans:
            return 0.0
        start = min(s.start_time for s in self.spans)
        end   = max(s.end_time for s in self.spans)
        return round((end - start) * 1000, 2)

    @property
    def has_error(self) -> bool:
        return any(s.is_error for s in self.spans)


# ── Problem 1 ─────────────────────────────────────────────────────────────────
class Tracer:
    def __init__(self):
        self._traces: dict[str, Trace] = {}
        self._current_trace_id: str | None = None

    def start_trace(self) -> str:
        trace_id = str(uuid.uuid4())
        self._traces[trace_id] = Trace(trace_id=trace_id)
        self._current_trace_id = trace_id
        return trace_id

    def end_trace(self, trace_id: str) -> Trace:
        return self._traces[trace_id]

    @contextmanager
    def span(self, name: str, **attributes):
        span = Span(
            span_id=str(uuid.uuid4()),
            name=name,
            start_time=time.perf_counter(),
            attributes=dict(attributes),
        )
        try:
            yield span              # caller can add attributes inside the with block
        except Exception as e:
            span.error = str(e)
            raise                   # re-raise so caller handles the exception
        finally:
            span.end_time = time.perf_counter()
            if self._current_trace_id:
                self._traces[self._current_trace_id].add_span(span)
            # finally always runs — ensures span is recorded even on error
            # This is why contextmanager + try/finally is the right pattern here.

    @property
    def current_trace(self) -> Trace | None:
        return self._traces.get(self._current_trace_id)


# ── Problem 2 ─────────────────────────────────────────────────────────────────
class MetricsCollector:
    def __init__(self):
        self._latencies: dict[str, list[float]] = defaultdict(list)
        self._tokens: dict[str, int] = defaultdict(int)
        self._errors: dict[str, int] = defaultdict(int)
        self._calls: dict[str, int] = defaultdict(int)

    def record_latency(self, operation: str, latency_ms: float):
        self._latencies[operation].append(latency_ms)
        self._calls[operation] += 1

    def record_tokens(self, model: str, tokens: int):
        self._tokens[model] += tokens

    def record_error(self, operation: str):
        self._errors[operation] += 1

    def _percentile(self, data: list[float], p: float) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * p)
        idx = min(idx, len(sorted_data) - 1)   # clamp to last element
        return round(sorted_data[idx], 2)

    def summary(self) -> dict:
        result = {}
        for op, latencies in self._latencies.items():
            result[f"{op}.p50_ms"]  = self._percentile(latencies, 0.50)
            result[f"{op}.p95_ms"]  = self._percentile(latencies, 0.95)
            result[f"{op}.p99_ms"]  = self._percentile(latencies, 0.99)
            total = self._calls[op]
            errors = self._errors.get(op, 0)
            result[f"{op}.error_rate"] = round(errors / total, 3) if total else 0.0
        for model, tokens in self._tokens.items():
            result[f"{model}.total_tokens"] = tokens
        return result


# ── Problem 3 ─────────────────────────────────────────────────────────────────
def traced_llm_call(
    prompt: str,
    tracer: Tracer,
    metrics: MetricsCollector,
    mock_response: str = "mocked response",
    mock_tokens: int = 50,
    should_fail: bool = False,
) -> str:
    start = time.perf_counter()
    with tracer.span("llm_call", prompt_length=len(prompt)) as span:
        time.sleep(0.01)   # simulate network latency
        if should_fail:
            metrics.record_error("llm_call")
            raise RuntimeError("LLM API timeout")
        span.attributes["response_length"] = len(mock_response)
        span.attributes["tokens"] = mock_tokens

    latency = (time.perf_counter() - start) * 1000
    metrics.record_latency("llm_call", latency)
    metrics.record_tokens("claude-3-sonnet", mock_tokens)
    return mock_response


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: How does this relate to LangSmith?
A: LangSmith wraps LangChain calls and records exactly this structure:
   runs (traces) contain child runs (spans). Each span has inputs, outputs,
   latency, token counts, and errors. Our Tracer is a simplified version.

Q: What's the difference between logging and tracing?
A: Logs: individual events with timestamps. Hard to correlate across services.
   Traces: end-to-end view of a single request, with causally linked spans.
   For LLM pipelines with 5+ steps, tracing is essential for debugging.

Q: What metrics matter most for LLM systems?
A: - Latency (p50/p95/p99) — users feel p95
   - Token usage — directly maps to cost
   - Error rate — reliability signal
   - Hallucination rate — eval metric, not just infra
   - Cache hit rate — cost optimization
   Your build failure pipeline reduced p50 from 20min → near-zero.
   That's the story: not just "it works" but "here are the metrics."
"""

if __name__ == "__main__":
    tracer = Tracer()
    metrics = MetricsCollector()

    print("=== Tracer ===")
    tid = tracer.start_trace()
    with tracer.span("retrieval", query="what is RAG") as s:
        time.sleep(0.02)
        s.attributes["chunks_retrieved"] = 3
    traced_llm_call("Explain RAG", tracer, metrics)
    trace = tracer.end_trace(tid)

    print(f"Spans: {len(trace.spans)}, Duration: {trace.total_duration_ms}ms, Error: {trace.has_error}")
    for span in trace.spans:
        print(f"  [{span.name}] {span.duration_ms}ms {span.attributes}")

    print("\n=== Error Tracing ===")
    tid2 = tracer.start_trace()
    try:
        traced_llm_call("risky", tracer, metrics, should_fail=True)
    except RuntimeError:
        pass
    trace2 = tracer.end_trace(tid2)
    print(f"has_error={trace2.has_error}, error='{trace2.spans[-1].error}'")

    for i in range(8):
        tid = tracer.start_trace()
        traced_llm_call(f"prompt {i}", tracer, metrics, mock_tokens=40+i*10)
        tracer.end_trace(tid)

    print("\n=== Metrics ===")
    for k, v in metrics.summary().items():
        print(f"  {k}: {v}")
