"""
SOLUTION: Phase 2 | Algorithms & DS | 03 Stacks & Queues
"""
from collections import deque


# ── Problem 1 ─────────────────────────────────────────────────────────────────
def is_valid_brackets(s: str) -> bool:
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0
    # Stack stores open brackets. When we see a close bracket, check if
    # the top of stack is its matching open. If not → invalid.
    # Empty stack at end → all brackets matched.


# ── Problem 2 ─────────────────────────────────────────────────────────────────
class LLMRequestQueue:
    def __init__(self, max_size: int = 100):
        self._queue = deque()
        self.max_size = max_size
        # deque: O(1) for both append (right) and popleft (left)
        # list would be O(n) for pop(0) — bad for queues

    def enqueue(self, request: dict) -> bool:
        if len(self._queue) >= self.max_size:
            return False
        self._queue.append(request)
        return True

    def dequeue(self) -> dict | None:
        return self._queue.popleft() if self._queue else None

    def peek(self) -> dict | None:
        return self._queue[0] if self._queue else None

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    @property
    def size(self) -> int:
        return len(self._queue)


# ── Problem 3 ─────────────────────────────────────────────────────────────────
class PromptEditor:
    def __init__(self):
        self._content = ""
        self._undo_stack = []   # stack of previous states
        self._redo_stack = []   # stack of undone states

    def type(self, text: str):
        self._undo_stack.append(self._content)   # save current before changing
        self._content += text
        self._redo_stack.clear()                 # new action invalidates redo history

    def undo(self):
        if self._undo_stack:
            self._redo_stack.append(self._content)
            self._content = self._undo_stack.pop()

    def redo(self):
        if self._redo_stack:
            self._undo_stack.append(self._content)
            self._content = self._redo_stack.pop()

    def current_text(self) -> str:
        return self._content


if __name__ == "__main__":
    print("=== Brackets ===")
    print(is_valid_brackets("{[()]}"))
    print(is_valid_brackets("([)]"))
    print(is_valid_brackets("{[}"))
    print(is_valid_brackets(""))

    print("\n=== LLM Queue ===")
    q = LLMRequestQueue(max_size=3)
    q.enqueue({"id": 1, "prompt": "Hello"})
    q.enqueue({"id": 2, "prompt": "Summarize this"})
    print(f"Size: {q.size}")
    print(f"Peek: {q.peek()}")
    print(f"Dequeue: {q.dequeue()}")
    print(f"Size: {q.size}")

    print("\n=== Prompt Editor ===")
    editor = PromptEditor()
    editor.type("You are ")
    editor.type("a helpful ")
    editor.type("assistant.")
    print(editor.current_text())
    editor.undo()
    print(editor.current_text())
    editor.undo()
    print(editor.current_text())
    editor.redo()
    print(editor.current_text())
