
import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if __name__ == "__main__":
    unittest.main(module=None, defaultTest="discover",
                  argv=["ignored", "discover", "-s", os.path.dirname(__file__)], verbosity=2)
