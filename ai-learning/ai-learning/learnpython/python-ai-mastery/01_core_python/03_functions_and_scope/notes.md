# Notes: Functions & Scope

## Decorator Template (memorize this)

```python
from functools import wraps

def my_decorator(fn):
    @wraps(fn)          # preserves fn.__name__ and fn.__doc__
    def wrapper(*args, **kwargs):
        # before
        result = fn(*args, **kwargs)
        # after
        return result
    return wrapper
```

`@wraps` is non-optional in production — without it, debugging tools and introspection break.

---

## Closure Rules (LEGB)

Python looks up names in this order:
1. **L**ocal — inside the current function
2. **E**nclosing — enclosing function's scope (closures)
3. **G**lobal — module level
4. **B**uilt-in — `len`, `print`, etc.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)   # prints "enclosing" — found in E before G
    inner()
```

---

## Mutable Default Argument (Classic Bug)

```python
# BUG — cache is shared across ALL calls
def embed(text, cache={}):
    ...

# FIX
def embed(text, cache=None):
    if cache is None:
        cache = {}
    ...
```

This catches out experienced engineers too. Interviewers love it.

---

## *args and **kwargs

```python
def fn(*args, **kwargs):
    # args is a tuple: (1, 2, 3)
    # kwargs is a dict: {'a': 1, 'b': 2}
    pass

fn(1, 2, 3, a=1, b=2)

# Forwarding:
def wrapper(*args, **kwargs):
    return real_fn(*args, **kwargs)   # * and ** unpack on call side
```

---

## Lambda Gotcha

```python
# Creating lambdas in a loop — all share the same `i`
fns = [lambda: i for i in range(3)]
fns[0]()   # returns 2, not 0!

# Fix: capture i at creation time
fns = [lambda i=i: i for i in range(3)]
fns[0]()   # returns 0 ✓
```

---

## Interview Tip
Decorators are asked at senior+ level to test understanding of closures and higher-order functions. Know: `@timer`, `@retry`, `@cache` (`functools.lru_cache`). For `@lru_cache` specifically: it's a built-in memoization decorator — know when to reach for it.
