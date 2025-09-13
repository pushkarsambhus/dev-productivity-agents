# utils/notebook_setup.py
import os
import sys
from openai import OpenAI

# --- Find project root dynamically ---
# This file lives in: <project_root>/utils/notebook_setup.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Make sure project root is importable (so `utils/` works in notebooks)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Optionally set the notebook's working directory to the project root.
# Toggle with env var NOTEBOOK_FORCE_PROJECT_CWD=0 if you DON'T want this behavior.
if os.environ.get("NOTEBOOK_FORCE_PROJECT_CWD", "1") == "1":
    try:
        os.chdir(PROJECT_ROOT)
    except Exception:
        # Don't crash import if chdir fails
        pass

# --- Initialize a ready-to-use OpenAI client pointed at local Ollama ---
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

print(f"✅ Notebook setup complete — client ready\n"
      f"   PROJECT_ROOT: {PROJECT_ROOT}\n"
      f"   CWD: {os.getcwd()}\n")