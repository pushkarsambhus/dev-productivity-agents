
from typing import List, Tuple, Dict, Optional

def mean(values: List[float]) -> float:
    return sum(values)/len(values)

def safe_get(d: Dict[str, int], key: str, default: Optional[int] = None) -> Optional[int]:
    return d.get(key, default)

def split_even_odd(nums: List[int]) -> Tuple[List[int], List[int]]:
    evens = [n for n in nums if n % 2 == 0]
    odds = [n for n in nums if n % 2 == 1]
    return evens, odds

if __name__ == "__main__":
    print(mean([1.0,2.0,3.0]))
    print(safe_get({"a":1},"b"))
    print(split_even_odd([1,2,3,4,5]))
