"""
Coding Interview Prep — Week 3: Python Advanced
================================================
Covers: Conditionals & Loops, Functions/*args/**kwargs,
        Lambda/map/filter, Error Handling, Decorators,
        Generators, List Comprehensions
"""

NAME        = "Week 3: Python Advanced"
DESCRIPTION = "Functions, comprehensions, error handling, decorators, generators"
ICON        = "⚡"

CONCEPTS = [
    {
        "title": "Functions, *args & **kwargs",
        "explanation": """Functions in Python are first-class objects — you can pass them around, return them, store them in variables.

```python
def greet(name, greeting="Hello"):   # default argument
    return f"{greeting}, {name}!"

greet("Alice")              # "Hello, Alice!"
greet("Alice", "Hi")        # "Hi, Alice!"
greet(greeting="Hey", name="Bob")  # keyword args — order doesn't matter
```

**Variable arguments:**
```python
def total(*args):           # *args = tuple of positional args
    return sum(args)

def info(**kwargs):         # **kwargs = dict of keyword args
    for k, v in kwargs.items():
        print(k, v)

total(1, 2, 3)              # 6
info(name="Alice", age=30)  # name Alice / age 30
```

**Mutable default argument trap (memorize this):**
```python
# WRONG:
def add(item, lst=[]):      # lst created ONCE at definition time
    lst.append(item)
    return lst

# RIGHT:
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```""",
        "gotchas": [
            "*args = tuple (not list). **kwargs = dict.",
            "Mutable default arguments ([], {}) are shared across all calls — use None.",
            "Default args are evaluated once at definition time, not each call.",
        ],
        "videos": [
            {"title": "Python Functions (Corey Schafer)", "url": "https://www.youtube.com/watch?v=9Os0o3wzS_I", "source": "YouTube"},
            {"title": "*args and **kwargs in Python (Tech With Tim)", "url": "https://www.youtube.com/watch?v=nKQwtHEyLgI", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Functions", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Lambda, map & filter",
        "explanation": """**Lambda** — anonymous single-expression function:
```python
square = lambda x: x ** 2   # same as def square(x): return x**2
square(5)   # 25

# Common use: sort by key
pairs = [(1, 'b'), (2, 'a')]
pairs.sort(key=lambda x: x[1])   # sort by second element
```

**map()** — apply function to every element:
```python
nums = [1, 2, 3, 4]
list(map(lambda x: x * 2, nums))   # [2, 4, 6, 8]
# Same as: [x * 2 for x in nums]   ← prefer this in interviews
```

**filter()** — keep elements where function returns True:
```python
list(filter(lambda x: x % 2 == 0, nums))   # [2, 4]
# Same as: [x for x in nums if x % 2 == 0]  ← prefer this
```

Both return **iterators** — wrap in list() to materialize.""",
        "gotchas": [
            "map() and filter() return iterators, not lists — wrap in list().",
            "List comprehension is usually cleaner than map/filter in interviews.",
            "Lambda can only be a single expression — no statements, no loops.",
        ],
        "videos": [
            {"title": "Lambda, map, filter in Python (Corey Schafer)", "url": "https://www.youtube.com/watch?v=hYzwCsKGRrg", "source": "YouTube"},
            {"title": "Python map() and filter() (Tech With Tim)", "url": "https://www.youtube.com/watch?v=cKlnR-CB3tk", "source": "YouTube"},
            {"title": "Automate the Boring Stuff with Python — Functions", "url": "https://www.udemy.com/course/automate/", "source": "Udemy"},
        ],
    },
    {
        "title": "Error Handling",
        "explanation": """Python's try/except/finally is identical to Java's try/catch/finally.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero")
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
else:
    print("No error occurred")   # runs only if no exception
finally:
    print("Always runs")         # cleanup — like Java's finally
```

**Raising exceptions:**
```python
def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b
```

**Custom exceptions:**
```python
class InsufficientFundsError(Exception):
    def __init__(self, amount):
        super().__init__(f"Not enough funds: need {amount}")
```""",
        "gotchas": [
            "Never use bare except: — it catches everything including KeyboardInterrupt. Always be specific.",
            "finally always runs — even if there's a return inside try.",
            "else block runs only if NO exception was raised.",
            "Multiple exceptions in one handler: except (ValueError, TypeError):",
        ],
        "videos": [
            {"title": "Python Exception Handling (Corey Schafer)", "url": "https://www.youtube.com/watch?v=NIWwJbo-9_8", "source": "YouTube"},
            {"title": "Try Except in Python (Tech With Tim)", "url": "https://www.youtube.com/watch?v=6SPDvPK38tw", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Error Handling", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Decorators & Generators",
        "explanation": """**Decorators** — wrap a function to add behavior before/after it. Like Spring AOP in Java.
```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_fn():
    time.sleep(1)

# @timer is syntactic sugar for: slow_fn = timer(slow_fn)
```

**Generators** — lazy iterators using `yield`. Produce values one at a time instead of building the whole list in memory.
```python
def count_up(n):
    for i in range(n):
        yield i        # pauses here, resumes on next()

gen = count_up(3)
next(gen)   # 0
next(gen)   # 1
next(gen)   # 2

# Generator expression (lazy list comprehension):
squares = (x**2 for x in range(1000000))   # no memory used yet
```""",
        "gotchas": [
            "Decorators use closures — the wrapper captures the outer function's state.",
            "yield pauses the function — it resumes from the same line on next call.",
            "Generators are exhausted after one pass — you can't reuse them.",
            "() = generator expression (lazy). [] = list comprehension (eager, builds full list).",
        ],
        "videos": [
            {"title": "Python Decorators (Corey Schafer)", "url": "https://www.youtube.com/watch?v=FsAPt_9Bf3U", "source": "YouTube"},
            {"title": "Python Generators (Corey Schafer)", "url": "https://www.youtube.com/watch?v=bD05uGo_sVI", "source": "YouTube"},
            {"title": "Python: Beyond the Basics — Decorators & Generators", "url": "https://www.udemy.com/course/python-beyond-the-basics-object-oriented-programming/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # FUNCTIONS, *args, **kwargs
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Functions & *args/**kwargs",
        "question": (
            "What does the following function print when called as shown?\n\n"
            "    def greet(*args, **kwargs):\n"
            "        print(args)\n"
            "        print(kwargs)\n\n"
            "    greet('Alice', 'Bob', city='NY', age=30)"
        ),
        "options": [
            "A) ('Alice', 'Bob')  then  {'city': 'NY', 'age': 30}",
            "B) ['Alice', 'Bob']  then  {'city': 'NY', 'age': 30}",
            "C) ('Alice', 'Bob', 'NY', 30)  then  {}",
            "D) TypeError: too many arguments",
        ],
        "correct_answer": "A) ('Alice', 'Bob')  then  {'city': 'NY', 'age': 30}",
        "explanation": (
            "*args collects all positional arguments into a tuple (not a list). "
            "**kwargs collects all keyword arguments into a dict. "
            "Positional args come before keyword args in the call. "
            "In Java there's no direct equivalent — varargs (String... args) is closest to *args, "
            "but there's no **kwargs analog. This pattern is used heavily in decorators and wrappers."
        ),
        "remember": "*args = tuple of positional args. **kwargs = dict of keyword args. args first, kwargs second.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Functions — Mutable Default Arguments",
        "question": "Find and fix the subtle bug — this function behaves unexpectedly on repeated calls:",
        "language": "python",
        "code": (
            "def add_item(item, items=[]):\n"
            "    items.append(item)\n"
            "    return items\n"
            "\n"
            "print(add_item('a'))   # ['a']       — expected\n"
            "print(add_item('b'))   # ['a', 'b']  — NOT expected! Should be ['b']"
        ),
        "correct_answer": (
            "Mutable default arguments are created ONCE when the function is defined, "
            "not on each call. The same list object is reused across calls.\n\n"
            "Fix: use None as default and create a new list inside:\n\n"
            "def add_item(item, items=None):\n"
            "    if items is None:\n"
            "        items = []\n"
            "    items.append(item)\n"
            "    return items"
        ),
        "explanation": (
            "Python evaluates default argument values once at function definition time. "
            "When the default is mutable (list, dict, set), that same object persists across calls. "
            "This is one of Python's most famous gotchas — no Java equivalent since Java doesn't have default parameter values. "
            "The fix: always use None as the default for mutable arguments, then initialize inside the function."
        ),
        "remember": "Never use mutable defaults ([], {}, set()). Use None + initialize inside. Called once at definition time.",
    },

    # ══════════════════════════════════════════════════════════════════
    # LAMBDA, MAP, FILTER
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Lambda, map, filter",
        "question": (
            "What does this code produce?\n\n"
            "    nums = [1, 2, 3, 4, 5]\n"
            "    result = list(filter(lambda x: x % 2 == 0, nums))\n"
            "    print(result)"
        ),
        "options": [
            "A) [1, 3, 5]",
            "B) [2, 4]",
            "C) [False, True, False, True, False]",
            "D) filter object",
        ],
        "correct_answer": "B) [2, 4]",
        "explanation": (
            "filter(function, iterable) returns an iterator of elements where function(element) is True. "
            "The lambda x: x % 2 == 0 returns True for even numbers. "
            "filter() returns a lazy iterator — you need list() to materialize it. "
            "Java equivalent: nums.stream().filter(x -> x % 2 == 0).collect(Collectors.toList()). "
            "In interviews, list comprehension [x for x in nums if x % 2 == 0] is often cleaner than filter()."
        ),
        "remember": "filter() returns an iterator — wrap in list(). Lambda is single-expression anonymous function.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Lambda, map, filter",
        "question": (
            "Given a list of strings, return a new list with each string:\n"
            "1. Stripped of whitespace\n"
            "2. Converted to lowercase\n"
            "3. Only keeping strings with length >= 3 after stripping\n\n"
            "Use a single list comprehension.\n\n"
            "Examples:\n"
            "  clean(['  Hello ', 'WORLD', 'hi', '  OK  ']) → ['hello', 'world']\n"
            "  clean(['  a  ', 'Python']) → ['python']"
        ),
        "language": "python",
        "starter_code": (
            "def clean(strings: list) -> list:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def clean(strings: list) -> list:\n"
            "    return [s.strip().lower() for s in strings if len(s.strip()) >= 3]\n"
        ),
        "explanation": (
            "List comprehensions with a filter condition are [expression for item in iterable if condition]. "
            "Note s.strip() is called twice here — once for the length check, once in the expression. "
            "To avoid this, assign inside the comprehension using a walrus operator (Python 3.8+): "
            "[stripped.lower() for s in strings if len(stripped := s.strip()) >= 3]. "
            "Both are valid in interviews. The walrus operator := is worth knowing."
        ),
        "remember": "List comprehension with filter: [expr for x in iterable if condition]. Walrus := avoids double computation.",
    },

    # ══════════════════════════════════════════════════════════════════
    # ERROR HANDLING
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Error Handling",
        "question": (
            "What is the output of this code?\n\n"
            "    try:\n"
            "        x = 1 / 0\n"
            "    except ZeroDivisionError:\n"
            "        print('caught')\n"
            "    finally:\n"
            "        print('finally')"
        ),
        "options": [
            "A) caught",
            "B) finally",
            "C) caught\nfinally",
            "D) ZeroDivisionError",
        ],
        "correct_answer": "C) caught\nfinally",
        "explanation": (
            "The finally block ALWAYS runs — whether an exception occurred or not, "
            "whether it was caught or not. Here: ZeroDivisionError is caught (prints 'caught'), "
            "then finally runs (prints 'finally'). "
            "Java's try/catch/finally works identically. "
            "finally is used for cleanup: closing files, releasing locks, closing DB connections."
        ),
        "remember": "finally always runs — caught or not. Use for cleanup (close files, DB connections).",
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Error Handling",
        "question": "Find and fix the bug — this exception handler is too broad:",
        "language": "python",
        "code": (
            "def safe_divide(a, b):\n"
            "    try:\n"
            "        return a / b\n"
            "    except:\n"
            "        return 0\n"
            "\n"
            "# Problem: this silently swallows ALL errors including bugs\n"
            "print(safe_divide(10, 0))    # 0  — OK\n"
            "print(safe_divide('x', 2))   # 0  — hides a bug!"
        ),
        "correct_answer": (
            "Bare except: catches everything including KeyboardInterrupt, SystemExit, and genuine bugs.\n"
            "Fix: catch only the specific exception you expect.\n\n"
            "def safe_divide(a, b):\n"
            "    try:\n"
            "        return a / b\n"
            "    except ZeroDivisionError:\n"
            "        return 0"
        ),
        "explanation": (
            "Bare except: or except Exception: are anti-patterns in production code. "
            "They catch everything — including bugs you should see, and system signals like Ctrl+C. "
            "Always catch the most specific exception type you expect. "
            "In interviews, catching specific exceptions shows maturity. "
            "Multiple exceptions: except (ValueError, TypeError): is valid syntax."
        ),
        "remember": "Never use bare except. Catch specific exceptions: except ZeroDivisionError. Multiple: except (A, B).",
    },

    # ══════════════════════════════════════════════════════════════════
    # LIST COMPREHENSIONS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "List Comprehensions",
        "question": (
            "Use a nested list comprehension to flatten a 2D matrix into a 1D list.\n\n"
            "Examples:\n"
            "  flatten([[1,2],[3,4],[5,6]]) → [1, 2, 3, 4, 5, 6]\n"
            "  flatten([[1],[2,3,4],[]])    → [1, 2, 3, 4]"
        ),
        "language": "python",
        "starter_code": (
            "def flatten(matrix: list) -> list:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def flatten(matrix: list) -> list:\n"
            "    return [x for row in matrix for x in row]\n"
        ),
        "explanation": (
            "Nested list comprehension reads left to right: [x for row in matrix for x in row]. "
            "The outer loop 'for row in matrix' comes first, then 'for x in row'. "
            "This is the opposite of how you'd write nested for-loops (outer before inner — same here). "
            "A common mistake is writing it backwards: [x for x in row for row in matrix] which fails. "
            "Remember: read it like English — 'give me x, for each row in matrix, for each x in that row'."
        ),
        "remember": "Nested comprehension: [x for outer in collection for x in outer]. Same order as nested for-loops.",
    },

    # ══════════════════════════════════════════════════════════════════
    # GENERATORS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Generators",
        "question": (
            "What is the key advantage of a generator function over a regular function "
            "that returns a list, when processing a large dataset?"
        ),
        "options": [
            "A) Generators are always faster to execute",
            "B) Generators produce values lazily — one at a time — consuming O(1) memory instead of O(n)",
            "C) Generators can be called multiple times without re-computation",
            "D) Generators support parallel execution automatically",
        ],
        "correct_answer": "B) Generators produce values lazily — one at a time — consuming O(1) memory instead of O(n)",
        "explanation": (
            "A generator with yield pauses execution and produces one value at a time. "
            "It doesn't build the full result in memory — ideal for large files, streams, or infinite sequences. "
            "If you return a list of 1 million items, all 1 million are in memory at once. "
            "A generator holds only the current state. "
            "Java equivalent: Iterator<T> or Stream<T> with lazy evaluation. "
            "Generator expression: (x for x in range(n)) vs list comprehension [x for x in range(n)]."
        ),
        "remember": "yield = lazy evaluation. Generator uses O(1) memory regardless of dataset size. Great for streaming/large data.",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Generators & Decorators",
        "question": (
            "Write a decorator that caches the result of a function call (memoization).\n"
            "If called again with the same arguments, return the cached result.\n\n"
            "Examples:\n"
            "    @memoize\n"
            "    def slow_square(n):\n"
            "        return n * n\n\n"
            "    slow_square(4)   # computes\n"
            "    slow_square(4)   # returns cached — function body NOT called again"
        ),
        "language": "python",
        "starter_code": (
            "def memoize(func):\n"
            "    pass\n\n\n"
            "@memoize\n"
            "def slow_square(n):\n"
            "    print(f'computing {n}^2')\n"
            "    return n * n\n\n"
            "print(slow_square(4))  # computing 4^2 / 16\n"
            "print(slow_square(4))  # 16 (no 'computing' printed)\n"
            "print(slow_square(5))  # computing 5^2 / 25\n"
        ),
        "correct_answer": (
            "def memoize(func):\n"
            "    cache = {}\n"
            "    def wrapper(*args):\n"
            "        if args not in cache:\n"
            "            cache[args] = func(*args)\n"
            "        return cache[args]\n"
            "    return wrapper\n"
        ),
        "explanation": (
            "A decorator is a function that takes a function and returns a new function (wrapper). "
            "The cache dict is closed over by wrapper — it persists across calls. "
            "args is a tuple (tuples are hashable, so they can be dict keys). "
            "Python's standard library provides functools.lru_cache which does this more robustly. "
            "In interviews: understanding decorators = understanding closures + higher-order functions. "
            "Java equivalent: method wrapping via Proxy or AspectJ."
        ),
        "remember": "Decorator = function wrapping function. Closure captures state (cache) across calls. functools.lru_cache does this built-in.",
    },
]
