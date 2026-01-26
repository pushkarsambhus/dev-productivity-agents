"""
03_log_metrics.py
-----------------
Goal: Parse text log lines and compute basic metrics:
- average latency (in milliseconds)
- p95 latency (simple approximate)
- error rate (% of lines with status != 200)
- anomaly rate (requests slower than a threshold)

This mirrors many "observability" exercises in interviews.
"""

from typing import List, Tuple

def parse_log_line(line: str) -> Tuple[int, int]:
    """
    Parse a simple log line of the form:
    "status=200 latency_ms=123"
    Returns (status:int, latency_ms:int). Lines that don't match are ignored by raising ValueError.
    """
    parts = line.strip().split()
    if len(parts) < 2:
        raise ValueError("Malformed log line")
    status = int(parts[0].split("=")[1])
    latency = int(parts[1].split("=")[1])
    return status, latency


def compute_metrics(lines: List[str], slow_threshold_ms: int = 500) -> dict:
    """
    Given a list of log lines, compute metrics safely.
    - We ignore malformed lines with a try/except so the function is robust.
    """
    latencies = []
    total = 0
    errors = 0
    slow = 0

    for line in lines:
        try:
            status, latency = parse_log_line(line)
            total += 1
            latencies.append(latency)
            if status != 200:
                errors += 1
            if latency > slow_threshold_ms:
                slow += 1
        except Exception:
            # Skip bad lines silently, but you could log this in real systems.
            continue

    if total == 0:
        return {"count": 0, "avg_ms": 0, "p95_ms": 0, "error_rate": 0.0, "anomaly_rate": 0.0}

    latencies.sort()
    avg = sum(latencies) / len(latencies)
    # p95 index (0-based). max with 0 in case of tiny lists.
    p95_index = max(0, int(round(0.95 * (len(latencies) - 1))))
    p95 = latencies[p95_index]

    return {
        "count": total,
        "avg_ms": round(avg, 2),
        "p95_ms": p95,
        "error_rate": round(errors / total, 4),
        "anomaly_rate": round(slow / total, 4),
    }


if __name__ == "__main__":
    sample = [
        "status=200 latency_ms=120",
        "status=200 latency_ms=80",
        "status=500 latency_ms=900",
        "status=200 latency_ms=510",
        "bad line",
    ]
    print(compute_metrics(sample, slow_threshold_ms=500))
