# Makes 'agents' a Python package.
from .researcher import run_researcher
from .writer import run_writer
from .critic import run_critic

__all__ = ["run_researcher", "run_writer", "run_critic"]
