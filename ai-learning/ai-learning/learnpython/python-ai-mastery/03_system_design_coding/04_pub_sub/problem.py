"""
PHASE 3 | SYSTEM DESIGN CODING | 04 PUB/SUB
============================================
Topic: Publish-Subscribe pattern — the messaging backbone of distributed AI systems.
Kafka underpins large-scale LLM pipelines. This is the Python-level model.

Pattern:
  Publishers emit events to named topics.
  Subscribers register handlers for topics.
  The broker routes events to all interested subscribers.

Use cases in AI:
  - LLM response streaming (each token = an event)
  - Pipeline stage notifications (embedding_done → trigger retrieval)
  - Eval run completion alerts
  - Build failure detection events (your production LangChain work)
"""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable
import time


@dataclass
class Event:
    topic: str
    payload: dict
    timestamp: float = field(default_factory=time.time)
    event_id: str = ""

    def __post_init__(self):
        if not self.event_id:
            self.event_id = f"{self.topic}_{int(self.timestamp * 1000)}"


# ── Problem 1: In-Memory Event Broker ────────────────────────────────────────
class EventBroker:
    """
    Simple synchronous pub/sub broker.
    Handlers are called immediately when an event is published.
    """

    def __init__(self):
        # TODO: dict mapping topic → list of handler functions
        pass

    def subscribe(self, topic: str, handler: Callable[[Event], None]):
        """Register a handler for a topic."""
        # TODO
        pass

    def unsubscribe(self, topic: str, handler: Callable[[Event], None]):
        """Remove a handler. No error if handler not found."""
        # TODO: use list.remove() safely (try/except or check membership)
        pass

    def publish(self, topic: str, payload: dict) -> int:
        """
        Publish an event to all subscribers of this topic.
        Returns number of handlers called.
        """
        # TODO: create Event, call each handler, return count
        pass

    def subscriber_count(self, topic: str) -> int:
        pass


# ── Problem 2: Wildcard Subscription ─────────────────────────────────────────
# Support wildcard topics: "llm.*" matches "llm.request", "llm.response", etc.
# This is how Kafka topic patterns work.

class WildcardBroker(EventBroker):
    """
    Extends EventBroker with wildcard topic matching.
    Pattern "prefix.*" matches any topic starting with "prefix."
    Exact topics still work as before.
    """

    def publish(self, topic: str, payload: dict) -> int:
        """
        Publish to all exact-match AND wildcard-match subscribers.
        TODO:
        1. Exact match: same as EventBroker
        2. Wildcard match: check all subscribed topics ending in ".*"
           If topic starts with the prefix (without .*), call those handlers too
        """
        pass


# ── Problem 3: Event History / Replay ────────────────────────────────────────
class AuditedBroker(EventBroker):
    """
    Broker that records all published events.
    Supports replaying events to a new subscriber (catch-up pattern).
    Used in: LLM eval audit trails, pipeline observability.
    """

    def __init__(self):
        super().__init__()
        # TODO: list to store all published events
        pass

    def publish(self, topic: str, payload: dict) -> int:
        """Publish event AND record it in history."""
        # TODO: call super().publish(), also store the event
        pass

    def replay(self, topic: str, handler: Callable[[Event], None]):
        """
        Send all historical events for a topic to handler.
        Useful for a new subscriber that missed earlier events.
        """
        # TODO: filter history by topic, call handler for each
        pass

    def event_count(self, topic: str = None) -> int:
        """Count events. If topic given, count only that topic."""
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Basic Broker ===")
    broker = EventBroker()
    received = []

    def on_eval_done(event: Event):
        received.append(f"eval_handler: {event.payload}")

    def on_any_eval(event: Event):
        received.append(f"monitor: {event.payload.get('score')}")

    broker.subscribe("eval.complete", on_eval_done)
    broker.subscribe("eval.complete", on_any_eval)
    broker.subscribe("eval.failed", on_eval_done)

    n = broker.publish("eval.complete", {"run_id": "r1", "score": 0.92})
    print(f"Handlers called: {n}")        # 2
    broker.unsubscribe("eval.complete", on_any_eval)
    n = broker.publish("eval.complete", {"run_id": "r2", "score": 0.88})
    print(f"Handlers after unsub: {n}")   # 1
    print(f"Messages received: {len(received)}")  # 3

    print("\n=== Wildcard Broker ===")
    wbroker = WildcardBroker()
    wlog = []
    wbroker.subscribe("llm.*", lambda e: wlog.append(f"wildcard:{e.topic}"))
    wbroker.subscribe("llm.request", lambda e: wlog.append(f"exact:{e.topic}"))

    wbroker.publish("llm.request",  {"model": "claude"})   # both handlers
    wbroker.publish("llm.response", {"tokens": 120})        # wildcard only
    wbroker.publish("eval.done",    {"score": 0.9})         # no handlers
    print(f"Wildcard log: {wlog}")
    # ['wildcard:llm.request', 'exact:llm.request', 'wildcard:llm.response']

    print("\n=== Audited Broker ===")
    abroker = AuditedBroker()
    abroker.subscribe("pipeline.step", lambda e: None)
    abroker.publish("pipeline.step", {"step": "embed", "status": "done"})
    abroker.publish("pipeline.step", {"step": "retrieve", "status": "done"})
    abroker.publish("eval.complete",  {"score": 0.95})

    print(f"Total events: {abroker.event_count()}")              # 3
    print(f"Pipeline events: {abroker.event_count('pipeline.step')}")  # 2

    # New subscriber catches up
    replay_log = []
    abroker.replay("pipeline.step", lambda e: replay_log.append(e.payload["step"]))
    print(f"Replayed: {replay_log}")   # ['embed', 'retrieve']
