import os, sys, time, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_04_rate_limiter as mod  # type: ignore

class TestLimiter(unittest.TestCase):
    def test_rate(self):
        bucket = mod.TokenBucket(rate_per_sec=10, capacity=10)
        ok = sum(1 for _ in range(10) if bucket.try_acquire())
        self.assertEqual(ok, 10)
        time.sleep(0.15)
        self.assertTrue(bucket.try_acquire())

if __name__ == '__main__':
    unittest.main()
