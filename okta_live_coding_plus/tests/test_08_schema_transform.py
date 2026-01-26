import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from problems._wrappers import m_08_schema_transform as mod  # type: ignore

class TestSchema(unittest.TestCase):
    def test_normalize(self):
        r = mod.normalize({"id":123,"mail":"a@x.com","yrs":"30"})
        self.assertEqual(r["user_id"], "123")
        self.assertEqual(r["email"], "a@x.com")
        self.assertEqual(r["age"], 30)

if __name__ == '__main__':
    unittest.main()
