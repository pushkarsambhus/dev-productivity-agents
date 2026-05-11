"""
tests/test_tools.py — Unit tests for tool handlers.

LEARNING NOTE ON TESTING AGENTS:
    Agent tests fall into three tiers:
      1. Unit tests (this file) — test individual tool functions in isolation.
         Fast, no API calls, no real external services needed.
      2. Integration tests     — test the full agent loop with a real API key.
         Slower, cost money, but catch wiring bugs.
      3. Evals                 — measure output quality across many examples.
         See evals/eval_runner.py

Run:
    cd 01-single-agent
    python -m pytest tests/ -v
"""

import sys
import os
import math

# Make sure the parent directory is on the path so we can import tools/config
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import tools


# ─────────────────────────────────────────────────────────────────────────────
# Calculator tests — pure Python, no external dependencies
# ─────────────────────────────────────────────────────────────────────────────

class TestCalculator:

    def test_basic_addition(self):
        result = tools.handle_calculator("2 + 2")
        assert "4" in result

    def test_multiplication(self):
        result = tools.handle_calculator("6 * 7")
        assert "42" in result

    def test_power(self):
        result = tools.handle_calculator("2 ** 10")
        assert "1024" in result

    def test_sqrt(self):
        result = tools.handle_calculator("sqrt(144)")
        assert "12" in result

    def test_float_result(self):
        result = tools.handle_calculator("1 / 3")
        # Should contain a decimal result
        assert "." in result

    def test_math_module_access(self):
        result = tools.handle_calculator("math.pi")
        assert "3.14" in result

    def test_invalid_expression(self):
        result = tools.handle_calculator("import os; os.system('ls')")
        # Security test: forbidden builtins should cause an error, not execute
        assert "error" in result.lower() or "Error" in result

    def test_empty_expression(self):
        result = tools.handle_calculator("")
        # Should not crash; return an error message
        assert result  # non-empty

    def test_division_by_zero(self):
        result = tools.handle_calculator("1 / 0")
        assert "error" in result.lower() or "Error" in result or "ZeroDivision" in result

    def test_complex_expression(self):
        # Verify order of operations is respected
        result = tools.handle_calculator("2 + 3 * 4")
        assert "14" in result  # 2 + (3*4) = 14, not 20


# ─────────────────────────────────────────────────────────────────────────────
# Current time tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGetCurrentTime:

    def test_returns_string(self):
        result = tools.handle_get_current_time()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_date_like_string(self):
        result = tools.handle_get_current_time()
        # Should contain a year-like string (e.g., "2025" or "2026")
        import re
        assert re.search(r"20\d\d", result), f"No year found in: {result}"

    def test_contains_time_like_string(self):
        result = tools.handle_get_current_time()
        # Should contain HH:MM pattern
        import re
        assert re.search(r"\d\d:\d\d", result), f"No time found in: {result}"

    def test_timezone_param_accepted(self):
        # Should not raise even with an unknown timezone (graceful fallback)
        result = tools.handle_get_current_time("America/New_York")
        assert isinstance(result, str)


# ─────────────────────────────────────────────────────────────────────────────
# Simulated web search tests (no API key required)
# ─────────────────────────────────────────────────────────────────────────────

class TestWebSearch:

    def test_returns_string_without_key(self, monkeypatch):
        """With no API key, should return a helpful placeholder."""
        monkeypatch.setattr("config.SEARCH_API_KEY", "")
        result = tools.handle_web_search("test query")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_simulated_result_contains_query(self, monkeypatch):
        monkeypatch.setattr("config.SEARCH_API_KEY", "")
        result = tools.handle_web_search("artificial intelligence")
        assert "artificial intelligence" in result

    def test_simulated_result_with_num_results(self, monkeypatch):
        monkeypatch.setattr("config.SEARCH_API_KEY", "")
        # Should not crash with explicit num_results
        result = tools.handle_web_search("test", num_results=3)
        assert isinstance(result, str)


# ─────────────────────────────────────────────────────────────────────────────
# Tool dispatch tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDispatch:

    def test_dispatch_calculator(self):
        result = tools.dispatch_tool("calculator", {"expression": "10 + 5"})
        assert "15" in result

    def test_dispatch_get_current_time(self):
        result = tools.dispatch_tool("get_current_time", {})
        assert isinstance(result, str)

    def test_dispatch_unknown_tool(self):
        result = tools.dispatch_tool("nonexistent_tool", {})
        assert "Unknown tool" in result or "unknown" in result.lower()

    def test_all_schemas_have_required_fields(self):
        """Every schema must have name, description, and input_schema."""
        for schema in tools.TOOL_SCHEMAS:
            assert "name" in schema, f"Missing 'name' in schema: {schema}"
            assert "description" in schema, f"Missing 'description' in {schema['name']}"
            assert "input_schema" in schema, f"Missing 'input_schema' in {schema['name']}"

    def test_all_schemas_registered(self):
        """Every schema must have a matching handler in TOOL_REGISTRY."""
        for schema in tools.TOOL_SCHEMAS:
            name = schema["name"]
            assert name in tools.TOOL_REGISTRY, \
                f"Tool '{name}' has a schema but no handler in TOOL_REGISTRY"
