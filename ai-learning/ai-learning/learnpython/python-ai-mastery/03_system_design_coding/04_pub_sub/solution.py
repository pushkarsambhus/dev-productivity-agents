"""
SOLUTION: Phase 3 | System Design Coding | 04 Pub/Sub
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


class EventBroker:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Event], None]):
        self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[Event], None]):
        try:
            self._subscribers[topic].remove(handler)
        except ValueError:
            pass   # handler not found — silent no-op

    def publish(self, topic: str, payload: dict) -> int:
        event = Event(topic=topic, payload=payload)
        handlers = self._subscribers.get(topic, [])
        for handler in handlers:
            handler(event)
        return len(handlers)

    def subscriber_count(self, topic: str) -> int:
        return len(self._subscribers.get(topic, []))


class WildcardBroker(EventBroker):
    def publish(self, topic: str, payload: dict) -> int:
        event = Event(topic=topic, payload=payload)
        called = set()   # track called handlers to avoid duplicates

        # Exact match
        for handler in self._subscribers.get(topic, []):
            handler(event)
            called.add(id(handler))

        # Wildcard match: find all subscriptions ending in ".*"
        for pattern, handlers in self._subscribers.items():
            if pattern.endswith(".*"):
                prefix = pattern[:-2]   # strip ".*"
                if topic.startswith(prefix + ".") or topic == prefix:
                    for handler in handlers:
                        if id(handler) not in called:
                            handler(event)
                            called.add(id(handler))

        return len(called)
        # id(handler) deduplication: if same function subscribed to both exact
        # and wildcard, only call it once.


class AuditedBroker(EventBroker):
    def __init__(self):
        super().__init__()
        self._history: list[Event] = []

    def publish(self, topic: str, payload: dict) -> int:
        event = Event(topic=topic, payload=payload)
        # Store before calling handlers (so replay order is correct)
        self._history.append(event)
        handlers = self._subscribers.get(topic, [])
        for handler in handlers:
            handler(event)
        return len(handlers)

    def replay(self, topic: str, handler: Callable[[Event], None]):
        for event in self._history:
            if event.topic == topic:
                handler(event)

    def event_count(self, topic: str = None) -> int:
        if topic is None:
            return len(self._history)
        return sum(1 for e in self._history if e.topic == topic)


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: How does this relate to Kafka?
A: Kafka adds: persistence (events survive restarts), consumer groups
   (multiple workers share a topic), offset tracking (replay from any point),
   and partitioning (parallelism). This in-memory broker is conceptually
   identical but lacks durability.

Q: Where does pub/sub fit in an AI pipeline?
A: Your build failure detection pipeline at Workday could be modeled as:
   - Publisher: CI system emits "build.failed" events with log data
   - Subscriber 1: LangChain classifier analyzes failure type
   - Subscriber 2: alerting service notifies on-call team
   - Subscriber 3: audit log records everything (like AuditedBroker)
   This is the event-driven architecture that makes pipelines decoupled.

Q: Sync vs async pub/sub?
A: This implementation is synchronous — handlers block the publisher.
   Production: handlers run in separate threads or async tasks.
   For LLM token streaming: asyncio + async generators are the norm.
"""

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
    n = broker.publish("eval.complete", {"run_id": "r1", "score": 0.92})
    print(f"Handlers called: {n}")
    broker.unsubscribe("eval.complete", on_any_eval)
    n = broker.publish("eval.complete", {"run_id": "r2", "score": 0.88})
    print(f"Handlers after unsub: {n}")
    print(f"Messages received: {len(received)}")

    print("\n=== Wildcard Broker ===")
    wbroker = WildcardBroker()
    wlog = []
    wbroker.subscribe("llm.*", lambda e: wlog.append(f"wildcard:{e.topic}"))
    wbroker.subscribe("llm.request", lambda e: wlog.append(f"exact:{e.topic}"))
    wbroker.publish("llm.request",  {"model": "claude"})
    wbroker.publish("llm.response", {"tokens": 120})
    wbroker.publish("eval.done",    {"score": 0.9})
    print(f"Wildcard log: {wlog}")

    print("\n=== Audited Broker ===")
    abroker = AuditedBroker()
    abroker.subscribe("pipeline.step", lambda e: None)
    abroker.publish("pipeline.step", {"step": "embed", "status": "done"})
    abroker.publish("pipeline.step", {"step": "retrieve", "status": "done"})
    abroker.publish("eval.complete",  {"score": 0.95})
    print(f"Total events: {abroker.event_count()}")
    print(f"Pipeline events: {abroker.event_count('pipeline.step')}")
    replay_log = []
    abroker.replay("pipeline.step", lambda e: replay_log.append(e.payload["step"]))
    print(f"Replayed: {replay_log}")
