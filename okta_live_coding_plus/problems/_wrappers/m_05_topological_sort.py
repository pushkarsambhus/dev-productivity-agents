# Auto-generated thin wrapper to import a problem module by filename.
import importlib.util, os, sys
HERE = os.path.dirname(__file__)
TARGET = os.path.join(os.path.dirname(HERE), "05_topological_sort.py")
spec = importlib.util.spec_from_file_location("wrapped_m_05_topological_sort", TARGET)
_mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(_mod)  # type: ignore
for k in dir(_mod):
    if not k.startswith("__"):
        globals()[k] = getattr(_mod, k)
