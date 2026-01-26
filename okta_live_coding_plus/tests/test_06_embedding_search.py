import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_06_embedding_search as mod  # type: ignore

class TestIndex(unittest.TestCase):
    def test_search(self):
        idx = mod.EmbeddingIndex()
        idx.add("a",[1,0]); idx.add("b",[0,1])
        res = idx.search([0.9,0.1], k=1)
        self.assertEqual(res[0][0],"a")

if __name__ == '__main__':
    unittest.main()
