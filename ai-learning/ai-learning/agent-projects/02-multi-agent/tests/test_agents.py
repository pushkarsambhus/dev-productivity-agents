"""
tests/test_agents.py — Unit tests for individual sub-agents.

Run:
    cd 02-multi-agent
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import MagicMock, patch


# ─────────────────────────────────────────────────────────────────────────────
# Shared fixture
# ─────────────────────────────────────────────────────────────────────────────

def make_text_response(text: str = "Test response."):
    block = MagicMock()
    block.type = "text"
    block.text = text
    resp = MagicMock()
    resp.stop_reason = "end_turn"
    resp.content = [block]
    resp.usage = MagicMock(input_tokens=100, output_tokens=50)
    return resp


def make_tool_use_response(name: str, tid: str, tinput: dict, text: str = ""):
    tb = MagicMock()
    tb.type = "tool_use"
    tb.name = name
    tb.id = tid
    tb.input = tinput
    resp = MagicMock()
    resp.stop_reason = "tool_use"
    resp.content = [tb]
    if text:
        txt_b = MagicMock()
        txt_b.type = "text"
        txt_b.text = text
        resp.content.insert(0, txt_b)
    resp.usage = MagicMock(input_tokens=80, output_tokens=30)
    return resp


# ─────────────────────────────────────────────────────────────────────────────
# Researcher tests
# ─────────────────────────────────────────────────────────────────────────────

class TestResearcher:

    @patch("anthropic.Anthropic")
    def test_returns_string(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response(
            "Key findings:\n- Fact 1: AI is useful.\n- Source: example.com"
        )
        mock_cls.return_value = mock_client

        from agents.researcher import run_researcher
        result = run_researcher("What is AI?")
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("anthropic.Anthropic")
    def test_uses_tool_on_tool_use_response(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            make_tool_use_response("web_search", "t1", {"query": "AI overview"}),
            make_text_response("Research complete: AI is a broad field."),
        ]
        mock_cls.return_value = mock_client

        from agents.researcher import run_researcher
        result = run_researcher("Overview of AI")
        assert mock_client.messages.create.call_count == 2
        assert "AI" in result

    @patch("anthropic.Anthropic")
    def test_context_passed_to_first_message(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("Done.")
        mock_cls.return_value = mock_client

        from agents.researcher import run_researcher
        run_researcher("AI", context="Focus on safety aspects")

        first_call = mock_client.messages.create.call_args_list[0]
        messages = first_call[1]["messages"]
        assert "Focus on safety aspects" in messages[0]["content"]


# ─────────────────────────────────────────────────────────────────────────────
# Writer tests
# ─────────────────────────────────────────────────────────────────────────────

class TestWriter:

    @patch("anthropic.Anthropic")
    def test_returns_string(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response(
            "AI is a branch of computer science..."
        )
        mock_cls.return_value = mock_client

        from agents.writer import run_writer
        result = run_writer(
            user_request="Write a short explanation of AI",
            research_brief="Fact: AI stands for Artificial Intelligence.",
        )
        assert isinstance(result, str)
        assert "AI" in result

    @patch("anthropic.Anthropic")
    def test_only_one_api_call(self, mock_cls):
        """Writer does not use tools — should be exactly one API call."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("Draft text.")
        mock_cls.return_value = mock_client

        from agents.writer import run_writer
        run_writer("Write about AI", "Research brief here")

        assert mock_client.messages.create.call_count == 1

    @patch("anthropic.Anthropic")
    def test_critic_feedback_included_in_prompt(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("Revised draft.")
        mock_cls.return_value = mock_client

        from agents.writer import run_writer
        run_writer(
            user_request="Write about AI",
            research_brief="Brief",
            critic_feedback="Paragraph 2 is too technical. Simplify.",
        )

        call_messages = mock_client.messages.create.call_args[1]["messages"]
        prompt_text = call_messages[0]["content"]
        assert "Simplify" in prompt_text


# ─────────────────────────────────────────────────────────────────────────────
# Critic tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCritic:

    @patch("anthropic.Anthropic")
    def test_approve_verdict(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response(
            "SECTION 1 — VERDICT\nAPPROVE\n\nSECTION 3 — STRENGTHS\nClear writing."
        )
        mock_cls.return_value = mock_client

        from agents.critic import run_critic
        result = run_critic("Write about AI", "Research brief", "Good draft here.")
        assert result["approve"] is True
        assert result["verdict"] == "APPROVE"

    @patch("anthropic.Anthropic")
    def test_revise_verdict(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response(
            "SECTION 1 — VERDICT\nREVISE\n\nSECTION 2 — ISSUES\n1. Introduction too vague."
        )
        mock_cls.return_value = mock_client

        from agents.critic import run_critic
        result = run_critic("Write about AI", "Brief", "Draft text here.")
        assert result["approve"] is False
        assert result["verdict"] == "REVISE"

    @patch("anthropic.Anthropic")
    def test_feedback_key_present(self, mock_cls):
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("APPROVE. Great work.")
        mock_cls.return_value = mock_client

        from agents.critic import run_critic
        result = run_critic("Request", "Brief", "Draft")
        assert "feedback" in result
        assert isinstance(result["feedback"], str)
