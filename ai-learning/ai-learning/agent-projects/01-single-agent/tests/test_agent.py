"""
tests/test_agent.py — Integration-level tests for the agent loop.

LEARNING NOTE:
    These tests mock the Anthropic API so you don't need a real key to run them.
    They verify that agent.py's LOGIC is correct:
      • Does it loop correctly on tool_use?
      • Does it stop on end_turn?
      • Does it handle errors gracefully?
      • Does it respect MAX_TURNS?

    For tests that actually call Claude, see evals/eval_runner.py.

Run:
    cd 01-single-agent
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import MagicMock, patch, call


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures: build fake Anthropic response objects
# ─────────────────────────────────────────────────────────────────────────────

def make_text_response(text: str = "The answer is 42."):
    """Build a fake 'end_turn' response containing a text block."""
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = text

    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [text_block]
    response.usage = MagicMock(input_tokens=100, output_tokens=50)
    return response


def make_tool_use_response(tool_name: str = "calculator",
                            tool_id: str = "toolu_abc",
                            tool_input: dict = None):
    """Build a fake 'tool_use' response requesting a tool call."""
    if tool_input is None:
        tool_input = {"expression": "2 + 2"}

    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.name = tool_name
    tool_block.id = tool_id
    tool_block.input = tool_input

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Let me calculate that."

    response = MagicMock()
    response.stop_reason = "tool_use"
    response.content = [text_block, tool_block]
    response.usage = MagicMock(input_tokens=80, output_tokens=30)
    return response


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAgentLoop:

    @patch("anthropic.Anthropic")
    def test_simple_end_turn(self, mock_anthropic_class):
        """Agent returns text when Claude responds with end_turn immediately."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("Paris is the capital.")
        mock_anthropic_class.return_value = mock_client

        from agent import run_agent
        result = run_agent("What is the capital of France?")

        assert "Paris" in result
        assert mock_client.messages.create.call_count == 1  # only one API call needed

    @patch("anthropic.Anthropic")
    def test_tool_use_then_end_turn(self, mock_anthropic_class):
        """Agent loops: tool_use response → execute tool → end_turn response."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        # First call: Claude requests a tool
        # Second call: Claude finishes with the result
        mock_client.messages.create.side_effect = [
            make_tool_use_response("calculator", "toolu_1", {"expression": "10 * 10"}),
            make_text_response("10 multiplied by 10 is 100."),
        ]
        mock_anthropic_class.return_value = mock_client

        from agent import run_agent
        result = run_agent("What is 10 times 10?")

        assert "100" in result
        # API should have been called twice
        assert mock_client.messages.create.call_count == 2

    @patch("anthropic.Anthropic")
    def test_multiple_tool_calls_in_sequence(self, mock_anthropic_class):
        """Agent handles a chain of tool calls correctly."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            make_tool_use_response("get_current_time", "toolu_1", {}),
            make_tool_use_response("calculator", "toolu_2", {"expression": "2025 - 1990"}),
            make_text_response("You are 35 years old."),
        ]
        mock_anthropic_class.return_value = mock_client

        from agent import run_agent
        result = run_agent("How old is someone born in 1990?")

        assert mock_client.messages.create.call_count == 3

    @patch("anthropic.Anthropic")
    def test_max_turns_respected(self, mock_anthropic_class):
        """Agent stops after MAX_TURNS even if Claude keeps requesting tools."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False
        original_max = config.MAX_TURNS
        config.MAX_TURNS = 3  # set low for this test

        mock_client = MagicMock()
        # Always return tool_use to simulate infinite loop
        mock_client.messages.create.return_value = make_tool_use_response()
        mock_anthropic_class.return_value = mock_client

        try:
            from agent import run_agent
            result = run_agent("Run forever")
            # Should return a "stopped" message
            assert "stopped" in result.lower() or "max" in result.lower()
            assert mock_client.messages.create.call_count <= config.MAX_TURNS
        finally:
            config.MAX_TURNS = original_max

    @patch("anthropic.Anthropic")
    def test_tool_result_includes_correct_id(self, mock_anthropic_class):
        """Verify tool results are sent back with matching tool_use_id."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            make_tool_use_response("calculator", "toolu_xyz", {"expression": "1+1"}),
            make_text_response("The result is 2."),
        ]
        mock_anthropic_class.return_value = mock_client

        from agent import run_agent
        run_agent("What is 1+1?")

        # Check the second API call's messages argument
        second_call_args = mock_client.messages.create.call_args_list[1]
        messages_sent = second_call_args[1]["messages"]  # kwargs['messages']

        # The last message should be a user message with tool_result content
        last_msg = messages_sent[-1]
        assert last_msg["role"] == "user"
        tool_result_block = last_msg["content"][0]
        assert tool_result_block["type"] == "tool_result"
        assert tool_result_block["tool_use_id"] == "toolu_xyz"


class TestAgentSession:

    @patch("anthropic.Anthropic")
    def test_session_preserves_history(self, mock_anthropic_class):
        """AgentSession sends growing history on each turn."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            make_text_response("My name is Claude."),
            make_text_response("You are testing me."),
        ]
        mock_anthropic_class.return_value = mock_client

        from agent import AgentSession
        session = AgentSession()
        session.chat("What is your name?")
        session.chat("What am I doing?")

        # Second call should have more messages than the first
        first_call_messages = mock_client.messages.create.call_args_list[0][1]["messages"]
        second_call_messages = mock_client.messages.create.call_args_list[1][1]["messages"]
        assert len(second_call_messages) > len(first_call_messages)

    @patch("anthropic.Anthropic")
    def test_session_reset_clears_history(self, mock_anthropic_class):
        """After reset(), history is empty again."""
        import config
        config.ANTHROPIC_API_KEY = "fake-key"
        config.VERBOSE = False

        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_text_response("Hello!")
        mock_anthropic_class.return_value = mock_client

        from agent import AgentSession
        session = AgentSession()
        session.chat("Hello")
        session.reset()
        assert session.messages == []
        assert session.turn_count == 0
