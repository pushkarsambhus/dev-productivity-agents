import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_02_prompt_router as mod  # type: ignore

class TestRouter(unittest.TestCase):
    def test_finance(self):
        self.assertEqual(mod.route_prompt("What's the revenue this quarter?"), "claude")
    def test_security(self):
        self.assertEqual(mod.route_prompt("Explain Okta SSO and OAuth"), "gpt-4")
    def test_default(self):
        self.assertEqual(mod.route_prompt("Write a poem"), "gpt-4o-mini")

if __name__ == '__main__':
    unittest.main()
