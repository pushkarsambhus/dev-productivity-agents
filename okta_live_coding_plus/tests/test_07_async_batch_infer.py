import os, sys, unittest, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_07_async_batch_infer as mod  # type: ignore

class TestAsync(unittest.TestCase):
    def test_batch(self):
        prompts = [f"p{i}" for i in range(10)]
        out = asyncio.run(mod.batch_infer(prompts, max_concurrency=3))
        self.assertEqual(len(out), 10)

if __name__ == '__main__':
    unittest.main()
