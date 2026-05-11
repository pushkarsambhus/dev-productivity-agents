"""
Coding Interview Prep — Week 1-2: Python Fundamentals
======================================================
Covers: Variables & Types, Strings, Lists, Tuples & Sets, Dictionaries,
        Constructors (__init__), Classes & OOP, Inheritance, Encapsulation, Polymorphism

Java parallels woven into explanations for a Java-background developer.
Questions mirror the same concept order and gotchas tracked in progress.md.
"""

NAME        = "Week 1-2: Python Fundamentals"
DESCRIPTION = "Variables, strings, lists, tuples, sets, dicts, OOP — interview patterns"
ICON        = "🐍"

# ── Concept walkthroughs shown before questions ────────────────────────────────
# Each entry: title, explanation (markdown), gotchas (list), videos (list of {title, url, source})
CONCEPTS = [
    {
        "title": "Variables & Types",
        "explanation": """Python is **dynamically typed** — no type declarations, the interpreter figures it out at runtime. You are the compiler.

**The 4 basic types:**

| Type | Example | Java equivalent |
|------|---------|-----------------|
| `int` | `age = 25` | `int age = 25;` |
| `float` | `price = 9.99` | `double price = 9.99;` |
| `str` | `name = "Alice"` | `String name = "Alice";` |
| `bool` | `active = True` | `boolean active = true;` |

**Type casting:**
```python
str(25)        # → "25"
int(9.99)      # → 9   (truncates, never rounds)
float("3.14")  # → 3.14
type(25)       # → <class 'int'>
```

**f-strings (use these always):**
```python
name = "Alice"
print(f"Hello {name}!")   # Java: "Hello " + name + "!"
```""",
        "gotchas": [
            "type() returns <class 'int'>, not just 'int'",
            "int(3.7) → 3, always truncates toward zero, never rounds",
            "print('x:', val) adds a space between args — use f-strings instead",
            "True/False are capitalized in Python (not true/false like Java)",
        ],
        "videos": [
            {"title": "Python Variables & Data Types (Corey Schafer)", "url": "https://www.youtube.com/watch?v=khKv-8q7YmY", "source": "YouTube"},
            {"title": "Python for Beginners — Full Course (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw&t=360s", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Variables & Data Types", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Strings",
        "explanation": """Strings are **immutable sequences** in Python — same as Java. Learn the built-ins; don't reinvent them.

**Key methods:**
```python
s = "Hello, World!"
s.upper()            # "HELLO, WORLD!"   → Java: toUpperCase()
s.lower()            # "hello, world!"   → Java: toLowerCase()
s.strip()            # removes whitespace → Java: trim()
s.split(",")         # splits into list  → Java: split()
s.replace("a","b")  # replaces all      → Java: replace()
s.find("World")     # index or -1       → Java: indexOf()
len(s)              # length            → Java: s.length()
"World" in s        # True              → Java: contains()
```

**Slicing — Python only:**
```python
s[0:5]    # "Hello"   start inclusive, stop exclusive
s[-1]     # last char
s[::-1]   # reverse the string
s[::2]    # every other character
```
Rule: `[start : stop : step]`""",
        "gotchas": [
            "find() returns -1 if not found (safe). index() raises ValueError (crashes). Use find().",
            "s[::-1] reverses — this is the interview answer for 'reverse a string'",
            "Strings are immutable: s[0] = 'x' raises TypeError",
            "split() with no args handles multiple spaces; split(' ') does not",
        ],
        "videos": [
            {"title": "Python Strings (Corey Schafer)", "url": "https://www.youtube.com/watch?v=k9TUPpGqYTo", "source": "YouTube"},
            {"title": "String Methods in Python (Tech With Tim)", "url": "https://www.youtube.com/watch?v=Ctqi5Y4X-jA", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — String Manipulation", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Lists",
        "explanation": """Lists are **ordered, mutable sequences** — Python's version of Java's ArrayList.

**Creating & accessing:**
```python
nums = [1, 2, 3, 4, 5]
nums[0]      # 1 — first    → Java: list.get(0)
nums[-1]     # 5 — last     (no Java equivalent)
```

**Adding & removing:**
```python
nums.append(6)    # add to end         → Java: list.add(6)
nums.pop()        # remove & return last
nums.pop(1)       # remove & return at index
nums.remove(3)    # remove by value
```

**Sorting:**
```python
sorted(nums)   # returns NEW sorted list
nums.sort()    # sorts IN PLACE — returns None
nums.reverse() # reverses IN PLACE — returns None
```

**List comprehension:**
```python
evens = [x for x in nums if x % 2 == 0]
squares = [x**2 for x in nums]
```""",
        "gotchas": [
            "sort() and reverse() return None — they mutate in place. Never assign them.",
            "pop() returns the removed item, not the remaining list",
            "index() crashes if value not found — check with 'in' first",
            "len([1, [2,3], 4]) → 3 — counts top-level items only",
        ],
        "videos": [
            {"title": "Python Lists (Corey Schafer)", "url": "https://www.youtube.com/watch?v=W8KRzm-HUcc", "source": "YouTube"},
            {"title": "List Comprehensions in Python (Tech With Tim)", "url": "https://www.youtube.com/watch?v=3dt4OGnU5sM", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Lists & List Comprehension", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Tuples & Sets",
        "explanation": """**Tuples** — immutable, ordered. Like a `final List` in Java.
```python
t = (1, 2, 3)
t = (42,)       # single element — comma is REQUIRED
a, b, c = t     # unpacking
```
Use tuples as dict keys (lists can't be — they're mutable). Return multiple values from a function.

**Sets** — unordered, unique elements. Like Java's HashSet.
```python
s = {1, 2, 3}
s = set()        # empty set — NOT {}, that's a dict!
s.add(4)
s.discard(4)     # remove, no error if missing
4 in s           # O(1) lookup
s1 & s2          # intersection → Java: retainAll()
s1 | s2          # union        → Java: addAll()
s1 - s2          # difference   → Java: removeAll()
```""",
        "gotchas": [
            "(42) is just 42. You need (42,) for a single-element tuple — the comma matters.",
            "{} creates an empty dict, NOT a set. Empty set must be set().",
            "Sets are unordered — no indexing. s[0] will error.",
            "Set elements must be hashable — can't have a set of lists.",
        ],
        "videos": [
            {"title": "Python Tuples (Corey Schafer)", "url": "https://www.youtube.com/watch?v=MZfMO8mSKPk", "source": "YouTube"},
            {"title": "Python Sets (Corey Schafer)", "url": "https://www.youtube.com/watch?v=r3R3h5ly_8g", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Tuples, Sets & Dictionaries", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Dictionaries",
        "explanation": """Dicts are **key-value stores** — like Java's HashMap. O(1) average lookup.

```python
d = {"name": "Alice", "age": 30}
d["name"]           # "Alice" — raises KeyError if missing
d.get("name")       # "Alice" — returns None if missing (safe)
d.get("x", 0)       # 0 — default value
d["city"] = "NY"    # add/update
del d["age"]        # delete key

d.keys()            # → dict_keys(["name", "city"])
d.values()          # → dict_values(["Alice", "NY"])
d.items()           # → [("name","Alice"), ("city","NY")]
```

**Iteration:**
```python
for key, value in d.items():
    print(key, value)
```

**Frequency count pattern (memorize this):**
```python
counts = {}
for c in "hello":
    counts[c] = counts.get(c, 0) + 1
# {"h":1, "e":1, "l":2, "o":1}
```""",
        "gotchas": [
            "d[key] raises KeyError. d.get(key) returns None. Always use get() for safe access.",
            "Dicts are insertion-ordered in Python 3.7+ (unlike Java's HashMap).",
            "setdefault(key, []).append(val) is the grouping pattern — avoids if/else.",
        ],
        "videos": [
            {"title": "Python Dictionaries (Corey Schafer)", "url": "https://www.youtube.com/watch?v=daefaLgNkw0", "source": "YouTube"},
            {"title": "Python defaultdict (Tech With Tim)", "url": "https://www.youtube.com/watch?v=7abBWAEiGX4", "source": "YouTube"},
            {"title": "100 Days of Code: Python Bootcamp — Dictionaries", "url": "https://www.udemy.com/course/100-days-of-code/", "source": "Udemy"},
        ],
    },
    {
        "title": "Classes & OOP",
        "explanation": """Python OOP mirrors Java's — classes, constructors, inheritance, encapsulation, polymorphism.

**Class & constructor:**
```python
class Dog:
    def __init__(self, name, breed):   # constructor = Java's Dog(String name)
        self.name = name               # self = Java's this
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"

d = Dog("Rex", "Lab")   # no 'new' keyword needed
print(d.bark())
```

**Inheritance:**
```python
class Animal:
    def __init__(self, name):
        self.name = name

class Cat(Animal):          # Java: class Cat extends Animal
    def __init__(self, name, indoor):
        super().__init__(name)   # Java: super(name)
        self.indoor = indoor
```

**Encapsulation:**
```python
class BankAccount:
    def __init__(self):
        self._balance = 0       # convention: _name = protected
        self.__pin = 1234       # __name = private (name-mangled)
```""",
        "gotchas": [
            "self must be the first parameter of every instance method — it's explicit in Python, implicit in Java.",
            "Child __init__ must call super().__init__() or parent attributes won't be set.",
            "__init__ is the constructor. __str__ is toString(). __len__ is .length().",
            "No 'new' keyword in Python — just call the class: Dog('Rex').",
        ],
        "videos": [
            {"title": "Python OOP Tutorial (Corey Schafer — 6 parts)", "url": "https://www.youtube.com/watch?v=ZDa-Z5JzLYM", "source": "YouTube"},
            {"title": "Python Classes & Inheritance (Tech With Tim)", "url": "https://www.youtube.com/watch?v=RSl87lqOXDE", "source": "YouTube"},
            {"title": "Python Mega Course — OOP Section", "url": "https://www.udemy.com/course/the-python-mega-course/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # VARIABLES & TYPES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Variables & Types",
        "question": (
            "What does the following print?\n\n"
            "    x = 5\n"
            "    print(type(x))\n\n"
            "A) int\n"
            "B) <class 'int'>\n"
            "C) 'int'\n"
            "D) Integer"
        ),
        "options": [
            "A) int",
            "B) <class 'int'>",
            "C) 'int'",
            "D) Integer",
        ],
        "correct_answer": "B) <class 'int'>",
        "explanation": (
            "In Python, type() returns the class object itself, not just the name string. "
            "So type(5) returns <class 'int'> — the angle brackets and 'class' keyword are "
            "part of the output. In Java, getClass().getName() would return 'java.lang.Integer'. "
            "Python's type() is more like printing the class reference directly."
        ),
        "remember": "type() returns <class 'typename'>, not just the name. Use isinstance() for type checks in real code.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "easy",
        "topic": "Variables & Types",
        "question": "Find and fix the bug:",
        "language": "python",
        "code": (
            "name = 'Alice'\n"
            "age = 30\n"
            "print('Name:', name, 'Age:', age)\n"
            "# Expected: Name: Alice Age: 30\n"
            "# Actual output adds unwanted spaces — rewrite using f-string"
        ),
        "correct_answer": (
            "Use an f-string: print(f'Name: {name} Age: {age}')\n"
            "The comma-separated print adds a space between each argument, which can "
            "produce unintended spacing. f-strings give precise control."
        ),
        "explanation": (
            "print('Name:', name) inserts a space between 'Name:' and the value of name "
            "because Python's print() separates arguments with a space by default (sep=' '). "
            "f-strings are the preferred interview pattern: f'Name: {name} Age: {age}' "
            "produces exactly 'Name: Alice Age: 30' with no surprises. "
            "In Java this is analogous to String.format() vs concatenation with +."
        ),
        "remember": "print() comma = spaces you don't control. Always use f-strings for formatted output.",
    },

    # ══════════════════════════════════════════════════════════════════
    # STRINGS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Strings",
        "question": (
            "Which of the following correctly reverses the string s = 'hello'?"
        ),
        "options": [
            "A) s.reverse()",
            "B) reversed(s)",
            "C) s[::-1]",
            "D) s.sort(reverse=True)",
        ],
        "correct_answer": "C) s[::-1]",
        "explanation": (
            "Strings in Python are immutable sequences. s.reverse() and s.sort() don't exist on strings "
            "(they're list methods). reversed(s) returns an iterator, not a string. "
            "s[::-1] uses slice notation with step=-1 to walk the string backwards, returning a new string. "
            "Java equivalent: new StringBuilder(s).reverse().toString()."
        ),
        "remember": "Reverse a string with s[::-1]. slice[start:stop:step] — step=-1 walks backwards.",
    },
    {
        "type": "coding",
        "difficulty": "easy",
        "topic": "Strings",
        "question": (
            "Write a function that counts the number of words in a string.\n\n"
            "Examples:\n"
            "  word_count('hello world')       → 2\n"
            "  word_count('  spaces   here  ') → 2\n"
            "  word_count('')                  → 0"
        ),
        "language": "python",
        "starter_code": (
            "def word_count(s: str) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def word_count(s: str) -> int:\n"
            "    return len(s.split())\n"
        ),
        "explanation": (
            "str.split() with no arguments splits on any whitespace AND strips leading/trailing whitespace, "
            "returning a list of words. len() on that list gives the word count. "
            "A common mistake is s.split(' ') which does NOT strip extra spaces — "
            "it would count empty strings from consecutive spaces. "
            "In Java this is s.trim().split('\\\\s+').length."
        ),
        "remember": "split() with no args handles all whitespace. split(' ') does not — it leaves empty strings.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Strings",
        "question": "Find and fix the bug — the palindrome check fails for 'A man a plan a canal Panama':",
        "language": "python",
        "code": (
            "def is_palindrome(s):\n"
            "    cleaned = [c for c in s if c.isalnum()]\n"
            "    return cleaned == cleaned[::-1]"
        ),
        "correct_answer": (
            "The bug is missing .lower() — uppercase 'A' != lowercase 'a'.\n"
            "Fix: cleaned = [c.lower() for c in s if c.isalnum()]"
        ),
        "explanation": (
            "The function correctly filters non-alphanumeric characters and reverses the list, "
            "but it doesn't normalize case. 'A' and 'a' have different ASCII values so the "
            "comparison fails. Adding .lower() in the comprehension: "
            "[c.lower() for c in s if c.isalnum()] fixes this. "
            "In interviews, always normalize case before palindrome checks."
        ),
        "remember": "Palindrome check pattern: filter isalnum + lowercase, then compare to reverse.",
    },

    # ══════════════════════════════════════════════════════════════════
    # LISTS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Lists",
        "question": (
            "What is the output of the following?\n\n"
            "    nums = [3, 1, 2]\n"
            "    result = nums.sort()\n"
            "    print(result)"
        ),
        "options": [
            "A) [1, 2, 3]",
            "B) None",
            "C) [3, 1, 2]",
            "D) TypeError",
        ],
        "correct_answer": "B) None",
        "explanation": (
            "list.sort() sorts the list in-place and returns None. "
            "This is the single most common Python gotcha for Java developers — "
            "Java's Collections.sort() also returns void, but it's easy to forget in Python. "
            "To get a new sorted list, use sorted(nums) which does return the sorted list. "
            "Same trap applies to list.reverse() — modifies in-place, returns None."
        ),
        "remember": "sort() and reverse() return None — they mutate in place. Use sorted() / reversed() to get a new object.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "easy",
        "topic": "Lists",
        "question": "Find and fix the bug — the code tries to remove and print the last element:",
        "language": "python",
        "code": (
            "items = ['a', 'b', 'c']\n"
            "removed = items.remove(items[-1])\n"
            "print(f'Removed: {removed}')"
        ),
        "correct_answer": (
            "list.remove() returns None, not the removed item.\n"
            "Fix: use pop() instead.\n"
            "  removed = items.pop()   # removes AND returns the last item\n"
            "  print(f'Removed: {removed}')  # prints: Removed: c"
        ),
        "explanation": (
            "remove(x) finds and removes the first occurrence of value x, but returns None. "
            "pop(index) removes the item at the given index (default -1 = last) and returns it. "
            "For this use case — remove last item and get its value — pop() is the right method. "
            "Java's ArrayList.remove(index) actually returns the element, so this is a Python-specific trap."
        ),
        "remember": "pop() returns the removed item. remove() returns None. Use pop() when you need the value.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Lists",
        "question": (
            "Given a list of integers, return a new list with duplicates removed, preserving original order.\n\n"
            "Examples:\n"
            "  dedupe([1, 2, 2, 3, 1]) → [1, 2, 3]\n"
            "  dedupe([4, 4, 4])       → [4]\n"
            "  dedupe([])              → []"
        ),
        "language": "python",
        "starter_code": (
            "def dedupe(nums: list) -> list:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def dedupe(nums: list) -> list:\n"
            "    seen = set()\n"
            "    result = []\n"
            "    for n in nums:\n"
            "        if n not in seen:\n"
            "            seen.add(n)\n"
            "            result.append(n)\n"
            "    return result\n"
            "\n"
            "# One-liner alternative (Python 3.7+ preserves dict insertion order):\n"
            "# return list(dict.fromkeys(nums))\n"
        ),
        "explanation": (
            "The set-based approach is O(n) time and O(n) space. Using 'seen' as a set gives O(1) "
            "average lookup per element. list(set(nums)) is shorter but does NOT preserve order. "
            "dict.fromkeys(nums) preserves order because dicts are insertion-ordered in Python 3.7+. "
            "In interviews, clarify whether order matters before choosing the approach."
        ),
        "remember": "list(set(x)) dedupes but loses order. Use a seen-set + loop to preserve order.",
    },

    # ══════════════════════════════════════════════════════════════════
    # TUPLES & SETS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Tuples & Sets",
        "question": (
            "Which of the following creates a tuple with a single element 42?"
        ),
        "options": [
            "A) t = (42)",
            "B) t = (42,)",
            "C) t = tuple[42]",
            "D) t = {42}",
        ],
        "correct_answer": "B) t = (42,)",
        "explanation": (
            "(42) is just 42 — the parentheses are grouping, not a tuple. "
            "The trailing comma is what makes it a tuple: (42,). "
            "{42} creates a set, not a tuple. "
            "This is one of Python's most common syntax gotchas — there's no Java equivalent "
            "since Java doesn't have tuple literals."
        ),
        "remember": "Single-element tuple needs a trailing comma: (42,) not (42). The comma makes it a tuple.",
    },
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Tuples & Sets",
        "question": (
            "What does the following code print?\n\n"
            "    s = {}\n"
            "    print(type(s))"
        ),
        "options": [
            "A) <class 'set'>",
            "B) <class 'dict'>",
            "C) <class 'frozenset'>",
            "D) TypeError",
        ],
        "correct_answer": "B) <class 'dict'>",
        "explanation": (
            "{} creates an empty dict, NOT an empty set. "
            "To create an empty set you must use set(). "
            "{1, 2, 3} is a set literal (because there are no key:value pairs), "
            "but {} alone is always a dict. "
            "This trips up almost every Python beginner — remember: empty set = set(), not {}."
        ),
        "remember": "{} = empty dict. Empty set must be set(). {1,2,3} is a set literal only when non-empty.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Tuples & Sets",
        "question": (
            "Given two lists, return a sorted list of elements that appear in BOTH lists (intersection), "
            "with no duplicates.\n\n"
            "Examples:\n"
            "  common([1,2,3,4], [3,4,5,6]) → [3, 4]\n"
            "  common([1,1,2], [2,2,3])     → [2]\n"
            "  common([1,2], [3,4])          → []"
        ),
        "language": "python",
        "starter_code": (
            "def common(a: list, b: list) -> list:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def common(a: list, b: list) -> list:\n"
            "    return sorted(set(a) & set(b))\n"
        ),
        "explanation": (
            "Converting both lists to sets removes duplicates and enables O(1) average lookup. "
            "The & operator (or .intersection()) computes the set intersection. "
            "sorted() returns a new sorted list. "
            "Time complexity: O(n + m) for set construction, O(k log k) for sorting the result "
            "where k is the intersection size. In Java this is like using HashSet.retainAll()."
        ),
        "remember": "Set intersection: set(a) & set(b). Faster than nested loops. O(n+m) vs O(n*m).",
    },

    # ══════════════════════════════════════════════════════════════════
    # DICTIONARIES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Dictionaries",
        "question": (
            "What is the safest way to get a value from a dict without raising a KeyError "
            "if the key doesn't exist?"
        ),
        "options": [
            "A) d[key]",
            "B) d.get(key)",
            "C) d.fetch(key)",
            "D) d.value(key)",
        ],
        "correct_answer": "B) d.get(key)",
        "explanation": (
            "d[key] raises KeyError if key is missing — equivalent to Java's HashMap.get() "
            "which returns null (but Python raises an exception instead). "
            "d.get(key) returns None if missing, or d.get(key, default) returns the default value. "
            "In interviews, using get() shows awareness of safe access patterns. "
            "d.fetch() and d.value() don't exist."
        ),
        "remember": "d.get(key, default) — safe access, no KeyError. d[key] raises KeyError if missing.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Dictionaries",
        "question": (
            "Given a string, return a dictionary with the frequency count of each character.\n\n"
            "Examples:\n"
            "  char_count('hello') → {'h':1, 'e':1, 'l':2, 'o':1}\n"
            "  char_count('aaa')   → {'a':3}\n"
            "  char_count('')      → {}"
        ),
        "language": "python",
        "starter_code": (
            "def char_count(s: str) -> dict:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def char_count(s: str) -> dict:\n"
            "    counts = {}\n"
            "    for c in s:\n"
            "        counts[c] = counts.get(c, 0) + 1\n"
            "    return counts\n"
            "\n"
            "# Alternative with collections.Counter:\n"
            "# from collections import Counter\n"
            "# return dict(Counter(s))\n"
        ),
        "explanation": (
            "The get(key, 0) pattern initializes missing keys to 0 without needing an explicit check. "
            "This is the standard frequency-count pattern — memorize it. "
            "collections.Counter does the same thing and is preferred in production, "
            "but building it manually shows understanding in interviews. "
            "This pattern appears constantly: anagram detection, majority element, top-k problems."
        ),
        "remember": "Frequency count: counts[c] = counts.get(c, 0) + 1. Or use collections.Counter.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Dictionaries",
        "question": "Find and fix the bug — this should group words by their first letter:",
        "language": "python",
        "code": (
            "def group_by_first(words):\n"
            "    groups = {}\n"
            "    for word in words:\n"
            "        key = word[0]\n"
            "        groups[key].append(word)\n"
            "    return groups\n"
            "\n"
            "print(group_by_first(['apple', 'ant', 'banana', 'avocado']))"
        ),
        "correct_answer": (
            "groups[key] raises KeyError when key doesn't exist yet.\n"
            "Fix: initialize missing keys before appending.\n\n"
            "Option 1: if/else\n"
            "    if key not in groups:\n"
            "        groups[key] = []\n"
            "    groups[key].append(word)\n\n"
            "Option 2: setdefault\n"
            "    groups.setdefault(key, []).append(word)\n\n"
            "Option 3: defaultdict\n"
            "    from collections import defaultdict\n"
            "    groups = defaultdict(list)"
        ),
        "explanation": (
            "Accessing groups[key] when key doesn't exist raises KeyError. "
            "setdefault(key, []) is idiomatic Python — it inserts an empty list if the key is missing "
            "and returns the list either way. defaultdict(list) from collections is cleaner for this pattern. "
            "Grouping by key is a very common interview pattern — know all three approaches."
        ),
        "remember": "Grouping pattern: dict.setdefault(key, []).append(val) OR use defaultdict(list).",
    },

    # ══════════════════════════════════════════════════════════════════
    # OOP — CLASSES, CONSTRUCTORS, INHERITANCE
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Classes & Constructors",
        "question": (
            "In Python, what is the purpose of the 'self' parameter in a class method?\n\n"
            "    class Dog:\n"
            "        def __init__(self, name):\n"
            "            self.name = name"
        ),
        "options": [
            "A) It is a keyword that Python requires but ignores internally",
            "B) It is a reference to the current instance, like 'this' in Java",
            "C) It refers to the class itself, not the instance",
            "D) It must be named 'self' or Python raises a SyntaxError",
        ],
        "correct_answer": "B) It is a reference to the current instance, like 'this' in Java",
        "explanation": (
            "self is exactly like Java's 'this' — it refers to the specific object the method was called on. "
            "Unlike Java, Python requires you to explicitly declare it as the first parameter of every instance method. "
            "It does NOT have to be named 'self' (any name works), but self is the universal convention. "
            "Python passes the instance automatically when you call obj.method() — you never pass self yourself."
        ),
        "remember": "self = Java's 'this'. Must be first param of every instance method. Name is convention, not keyword.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Inheritance",
        "question": "Find and fix the bug — the child class should call the parent constructor:",
        "language": "python",
        "code": (
            "class Animal:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "\n"
            "class Dog(Animal):\n"
            "    def __init__(self, name, breed):\n"
            "        self.breed = breed\n"
            "\n"
            "d = Dog('Rex', 'Labrador')\n"
            "print(d.name)   # AttributeError: 'Dog' has no attribute 'name'"
        ),
        "correct_answer": (
            "Dog.__init__ overrides Animal.__init__ without calling it, so self.name is never set.\n"
            "Fix: call super().__init__(name) inside Dog.__init__.\n\n"
            "class Dog(Animal):\n"
            "    def __init__(self, name, breed):\n"
            "        super().__init__(name)   # calls Animal.__init__\n"
            "        self.breed = breed"
        ),
        "explanation": (
            "When a child class defines __init__, it completely overrides the parent's __init__. "
            "To also run the parent's initialization, you must explicitly call super().__init__(). "
            "This is identical to Java's super() call in a constructor. "
            "Forgetting super().__init__() is one of the most common OOP bugs in Python interviews "
            "— especially when the parent sets up required attributes."
        ),
        "remember": "Child __init__ must call super().__init__() to initialize parent attributes. Same as Java's super().",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Polymorphism & OOP",
        "question": (
            "Design a Shape hierarchy with polymorphic area() calculation.\n\n"
            "Requirements:\n"
            "- Base class Shape with an area() method that raises NotImplementedError\n"
            "- Circle(radius) and Rectangle(width, height) subclasses\n"
            "- A function total_area(shapes) that sums area() across any list of shapes\n\n"
            "Examples:\n"
            "  shapes = [Circle(5), Rectangle(3, 4)]\n"
            "  total_area(shapes)  →  ~90.54  (78.54 + 12)"
        ),
        "language": "python",
        "starter_code": (
            "import math\n\n\n"
            "class Shape:\n"
            "    pass\n\n\n"
            "class Circle(Shape):\n"
            "    pass\n\n\n"
            "class Rectangle(Shape):\n"
            "    pass\n\n\n"
            "def total_area(shapes: list) -> float:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "import math\n\n\n"
            "class Shape:\n"
            "    def area(self) -> float:\n"
            "        raise NotImplementedError('Subclasses must implement area()')\n\n\n"
            "class Circle(Shape):\n"
            "    def __init__(self, radius: float):\n"
            "        self.radius = radius\n\n"
            "    def area(self) -> float:\n"
            "        return math.pi * self.radius ** 2\n\n\n"
            "class Rectangle(Shape):\n"
            "    def __init__(self, width: float, height: float):\n"
            "        self.width = width\n"
            "        self.height = height\n\n"
            "    def area(self) -> float:\n"
            "        return self.width * self.height\n\n\n"
            "def total_area(shapes: list) -> float:\n"
            "    return sum(s.area() for s in shapes)\n"
        ),
        "explanation": (
            "This is the classic polymorphism pattern. The base class defines the interface (area()), "
            "subclasses provide implementations, and total_area() works on any Shape without knowing the type. "
            "Python doesn't have abstract classes by default — raising NotImplementedError is the simple pattern. "
            "For stricter enforcement, use ABC: 'from abc import ABC, abstractmethod' and decorate area() with @abstractmethod. "
            "In Java this would be an abstract class or interface."
        ),
        "remember": "Polymorphism: define method in base, override in subclasses. Python uses NotImplementedError or ABC for abstract methods.",
    },
]
