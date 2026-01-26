"""
07_async_batch_infer.py
----------------------
Goal: Simulate asynchronous "batch inference" over many prompts with limited concurrency.

Why this matters:
- Platform engineers often have to control concurrency against external APIs.
- Shows comfort with asyncio primitives (Semaphore, gather).

We DO NOT call any external service here; we simulate latency with asyncio.sleep.
"""

import asyncio
from typing import List

async def fake_model_infer(prompt: str) -> str:
    """
    Simulate a model call that takes variable time.
    """
    # Variable sleep based on prompt length (just to simulate)
    await asyncio.sleep(0.01 + (len(prompt) % 5) * 0.02)
    return f"answer:{prompt[:10]}"

async def batch_infer(prompts: List[str], max_concurrency: int = 5) -> List[str]:
    """
    Run many inferences concurrently but cap the number of simultaneous tasks.
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _wrapped(p: str) -> str:
        async with semaphore:
            return await fake_model_infer(p)

    tasks = [asyncio.create_task(_wrapped(p)) for p in prompts]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    prompts = [f"prompt-{i}" for i in range(12)]
    answers = asyncio.run(batch_infer(prompts, max_concurrency=3))
    print(answers)
