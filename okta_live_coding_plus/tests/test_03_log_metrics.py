import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_03_log_metrics as mod  # type: ignore

class TestLogs(unittest.TestCase):
    def test_metrics(self):
        lines = [
            "status=200 latency_ms=100",
            "status=500 latency_ms=900",
            "status=200 latency_ms=600",
            "bad line",
        ]
        m = mod.compute_metrics(lines, slow_threshold_ms=500)
        self.assertEqual(m["count"], 3)
        self.assertAlmostEqual(m["avg_ms"], 533.33, places=2)
        self.assertAlmostEqual(m["error_rate"], 1/3, places=4)

if __name__ == '__main__':
    unittest.main()
