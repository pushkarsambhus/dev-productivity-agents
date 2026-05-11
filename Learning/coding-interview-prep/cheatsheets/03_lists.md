# Lists

**Pattern: ORDERED COLLECTION** — Go-to structure for sequences. Master add/remove/slice/search — these appear in almost every interview.

---

## Creating and accessing

```python
nums = [1, 2, 3, 4, 5]
nums[0]     # 1    — first item   → Java: list.get(0)
nums[-1]    # 5    — last item    (no Java equivalent)
```

---

## Adding and removing

```python
nums.append(6)      # add to end           → Java: list.add(6)
nums.insert(1, 9)   # insert at index      → Java: list.add(1, 9)
nums.remove(3)      # remove by value      → Java: list.remove(Integer.valueOf(3))
nums.pop()          # remove & return last → Java: list.remove(list.size()-1)
nums.pop(1)         # remove & return at index
```

**Gotcha:** `pop()` returns the removed item, NOT the remaining list.

---

## Useful operations

```python
len(nums)           # length              → Java: list.size()
sum(nums)           # total of all items  (no direct Java equivalent)
max(nums)           # largest value
min(nums)           # smallest value
nums.count(3)       # count occurrences   → Java: Collections.frequency(list, 3)
nums.index(3)       # first index of value (crashes if not found — use `in` first)
3 in nums           # True/False          → Java: list.contains(3)
```

---

## Sorting

```python
sorted(nums)        # returns NEW sorted list — original unchanged
nums.sort()         # sorts IN PLACE — returns None
nums.reverse()      # reverses IN PLACE — returns None
```

**Gotcha:** `x = nums.sort()` → `x` is `None`. Never assign in-place methods.

---

## Slicing — same rules as strings

```python
nums[1:4]     # items at index 1, 2, 3 (stop exclusive)
nums[::-1]    # reversed list
nums[:3]      # first 3 items
nums[2:]      # from index 2 to end
```

---

## Combining lists

```python
a = [1, 2, 3]
b = [4, 5, 6]
a + b           # [1, 2, 3, 4, 5, 6] — creates new list
a.extend(b)     # adds b into a in place
" ".join(["a","b","c"])  # "a b c" — join list of strings
```

---

## List comprehension

```python
# Pattern: [what_to_keep   for x in iterable   if condition]
evens  = [x for x in range(1, 21) if x % 2 == 0]   # filter
squares = [x**2 for x in nums]                       # transform
doubled = [x * 2 for x in nums]                      # transform
```

**Gotcha:** `[x % 2 == 0 for x in nums]` gives booleans, not values — put the condition in the `if` clause.

---

## Gotchas summary

- `pop()` returns the item, not the remaining list
- `sort()` and `reverse()` return `None` — modify in place
- `index()` crashes if value not found — check with `in` first
- `len([1, [2,3], 4])` → `3` — counts top-level items only

---

## Interview trigger

> "Find max/min", "remove duplicates", "filter values", "reverse" → lists + built-ins
> "One-line filter or transform" → list comprehension
