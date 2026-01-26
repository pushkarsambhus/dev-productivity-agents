import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_01_cosine_similarity as mod  # type: ignore

class TestCosine(unittest.TestCase):
    def test_identical(self):
        self.assertAlmostEqual(mod.cosine_similarity([1,0,0],[1,0,0]), 1.0)
    def test_orthogonal(self):
        self.assertAlmostEqual(mod.cosine_similarity([1,0],[0,1]), 0.0)
    def test_zero_vector(self):
        self.assertEqual(mod.cosine_similarity([0,0],[1,1]), 0.0)

if __name__ == '__main__':
    unittest.main()
