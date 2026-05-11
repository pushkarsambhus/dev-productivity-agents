"""
PHASE 4 | LLM / AI PATTERNS | 05 OBSERVABILITY
================================================
Topic: Tracing, metrics, and logging for LLM pipelines.
Your LangSmith experience is directly relevant here — this module
builds the underlying patterns that LangSmith implements.

Production AI systems need:
  - Traces: end-to-end record of a pipeline run (like a call stack)
  - Spans: individual steps within a trace (LLM call, retrieval, tool call)
  - Metrics: aggregated stats (latency, token usage, error rate)
  - Structured logs: machine-readable events

This is what separates a prototype from a production system.
"""
import time
import uuid
from dataclasses import dataclass, field
from contextlib import contextmanager
from collections import defaultdict
from typing import Any


# ── Span & Trace data structures ───────────────────────────────────────────────
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


# ── Problem 1: Tracer ──────────────────────────────────────────────────────────
class Tracer:
    """
    Records traces of LLM pipeline runs.
    Modeled after OpenTelemetry / LangSmith tracing.
    """

    def __init__(self):
        # TODO: store traces dict (trace_id → Trace) and current_trace_id
        pass

    def start_trace(self) -> str:
        """Create a new trace. Returns trace_id."""
        # TODO: generate a UUID trace_id, create Trace, store it,
        # set as current, return trace_id
        pass

    def end_trace(self, trace_id: str) -> Trace:
        """Return the completed trace."""
        pass

    @contextmanager
    def span(self, name: str, **attributes):
        """
        Context manager that records a span.

        Usage:
            with tracer.span("llm_call", model="claude-3-sonnet") as span:
                result = call_llm(...)
                span.attributes["tokens"] = result.tokens

        TODO:
        1. Create a Span with start_time=now, span_id=uuid
        2. Add attributes from kwargs
        3. yield the span (so caller can add more attributes)
        4. On exit: set end_time
        5. If exception: record error message on span, re-raise
        6. Add span to current trace
        """
        pass

    @property
    def current_trace(self) -> Trace | None:
        pass


# ── Problem 2: Metrics Collector ──────────────────────────────────────────────
class MetricsCollector:
    """
    Aggregates metrics from pipeline runs.
    Think: LangSmith dashboard stats, but built from scratch.
    """

    def __init__(self):
        # TODO: store latencies, token_counts, error_counts as defaultdict
        pass

    def record_latency(self, operation: str, latency_ms: float):
        pass

    def record_tokens(self, model: str, tokens: int):
        pass

    def record_error(self, operation: str):
        pass

    def summary(self) -> dict:
        """
        Return a summary dict with:
        - latency_p50, latency_p95, latency_p99 per operation (in ms)
        - total_tokens per model
        - error_rate per operation (errors / total calls)

        TODO: compute percentiles using sorted list and index math.
        p50 = 50th percentile = value at index len*0.5
        p95 = value at index len*0.95
        """
        pass


# ── Problem 3: Pipeline with built-in observability ───────────────────────────
# Wire the Tracer and MetricsCollector together into a traced pipeline step.

def traced_llm_call(
    prompt: str,
    tracer: Tracer,
    metrics: MetricsCollector,
    mock_response: str = "mocked response",
    mock_tokens: int = 50,
    should_fail: bool = False,
) -> str:
    """
    Simulate an LLM call with full observability.
    TODO:
    1. Use tracer.span("llm_call", prompt_length=len(prompt))
    2. Inside span: simulate latency (time.sleep(0.01))
    3. Record tokens with metrics
    4. If should_fail: raise RuntimeError("LLM API timeout")
    5. Set span.attributes["response_length"] = len(mock_response)
    6. Record latency in metrics
    7. Return mock_response
    """
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tracer ===")
    tracer = Tracer()
    metrics = MetricsCollector()

    # Successful pipeline run
    tid = tracer.start_trace()
    with tracer.span("retrieval", query="what is RAG") as s:
        time.sleep(0.02)
        s.attributes["chunks_retrieved"] = 3

    result = traced_llm_call("Explain RAG", tracer, metrics)
    trace = tracer.end_trace(tid)

    print(f"Trace {tid[:8]}... has {len(trace.spans)} spans")
    print(f"Total duration: {trace.total_duration_ms}ms")
    print(f"Has error: {trace.has_error}")
    for span in trace.spans:
        print(f"  [{span.name}] {span.duration_ms}ms attrs={span.attributes}")

    # Failed run
    print("\n=== Error Tracing ===")
    tid2 = tracer.start_trace()
    try:
        traced_llm_call("risky prompt", tracer, metrics, should_fail=True)
    except RuntimeError:
        pass
    trace2 = tracer.end_trace(tid2)
    print(f"Error trace has_error: {trace2.has_error}")
    print(f"Error span: {trace2.spans[-1].error}")

    # Run a few more for metrics
    for i in range(8):
        tid = tracer.start_trace()
        traced_llm_call(f"prompt {i}", tracer, metrics, mock_tokens=40+i*10)
        tracer.end_trace(tid)

    print("\n=== Metrics Summary ===")
    summary = metrics.summary()
    for key, val in summary.items():
        print(f"  {key}: {val}")
