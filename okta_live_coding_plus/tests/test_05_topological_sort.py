import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_05_topological_sort as mod  # type: ignore

class TestTopo(unittest.TestCase):
    def test_order(self):
        edges = [(0,2), (1,2), (2,3)]
        order = mod.topological_sort(4, edges)
        self.assertEqual(order[-1], 3)
        self.assertIn(order[0], (0,1))
    def test_cycle(self):
        with self.assertRaises(ValueError):
            mod.topological_sort(3, [(0,1),(1,2),(2,0)])

if __name__ == '__main__':
    unittest.main()
