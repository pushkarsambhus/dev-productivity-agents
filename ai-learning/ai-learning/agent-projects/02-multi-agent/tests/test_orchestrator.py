"""
tests/test_orchestrator.py — Tests for the pipeline orchestration logic.

Run:
    cd 02-multi-agent
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import MagicMock, patch


class TestPipeline:

    @patch("agents.critic.run_critic")
    @patch("agents.writer.run_writer")
    @patch("agents.researcher.run_researcher")
    def test_pipeline_happy_path(self, mock_research, mock_write, mock_critic):
        """Pipeline completes with approved draft on first try."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False
        config.MAX_REVISION_ROUNDS = 2

        mock_research.return_value = "Research: AI is useful. Source: example.com"
        mock_write.return_value = "AI stands for Artificial Intelligence and is very useful."
        mock_critic.return_value = {"approve": True, "verdict": "APPROVE", "feedback": "Great work."}

        from orchestrator import run_pipeline
        state = run_pipeline("Explain AI")

        assert mock_research.call_count == 1
        assert mock_write.call_count == 1
        assert mock_critic.call_count == 1
        assert state.approved is True
        assert len(state.final_output) > 0

    @patch("agents.critic.run_critic")
    @patch("agents.writer.run_writer")
    @patch("agents.researcher.run_researcher")
    def test_pipeline_one_revision_then_approve(self, mock_research, mock_write, mock_critic):
        """Pipeline revises once then approves."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False
        config.MAX_REVISION_ROUNDS = 2

        mock_research.return_value = "Research brief."
        mock_write.side_effect = ["First draft.", "Revised draft."]
        mock_critic.side_effect = [
            {"approve": False, "verdict": "REVISE", "feedback": "Too short."},
            {"approve": True,  "verdict": "APPROVE", "feedback": ""},
        ]

        from orchestrator import run_pipeline
        state = run_pipeline("Write about AI")

        assert mock_write.call_count == 2   # initial + 1 revision
        assert mock_critic.call_count == 2
        assert state.revision_count == 1
        assert state.approved is True

    @patch("agents.critic.run_critic")
    @patch("agents.writer.run_writer")
    @patch("agents.researcher.run_researcher")
    def test_pipeline_hits_max_revisions(self, mock_research, mock_write, mock_critic):
        """Pipeline stops after MAX_REVISION_ROUNDS even without approval."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False
        config.MAX_REVISION_ROUNDS = 1  # only allow 1 revision

        mock_research.return_value = "Brief."
        mock_write.return_value = "Draft."
        mock_critic.return_value = {"approve": False, "verdict": "REVISE", "feedback": "Still bad."}

        from orchestrator import run_pipeline
        state = run_pipeline("Write about AI")

        # MAX_REVISION_ROUNDS=1 means initial write + 1 revision = 2 writes total
        assert mock_write.call_count == 2
        # Final output should still be set
        assert state.final_output

    @patch("agents.critic.run_critic")
    @patch("agents.writer.run_writer")
    @patch("agents.researcher.run_researcher")
    def test_pipeline_state_has_all_fields(self, mock_research, mock_write, mock_critic):
        """PipelineState is fully populated after a run."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False
        config.MAX_REVISION_ROUNDS = 2

        mock_research.return_value = "Research."
        mock_write.return_value = "Final document."
        mock_critic.return_value = {"approve": True, "verdict": "APPROVE", "feedback": "Good."}

        from orchestrator import run_pipeline, PipelineState
        state = run_pipeline("Test request")

        assert isinstance(state, PipelineState)
        assert state.user_request == "Test request"
        assert state.research_brief == "Research."
        assert len(state.drafts) >= 1
        assert len(state.steps) >= 3   # researcher + writer + critic
        assert state.final_output == "Final document."

    @patch("agents.critic.run_critic")
    @patch("agents.writer.run_writer")
    @patch("agents.researcher.run_researcher")
    def test_critic_feedback_passed_to_writer_on_revision(self, mock_research, mock_write, mock_critic):
        """When Critic says REVISE, the feedback must reach the Writer."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False
        config.MAX_REVISION_ROUNDS = 2

        mock_research.return_value = "Brief."
        mock_write.return_value = "Draft."
        mock_critic.side_effect = [
            {"approve": False, "verdict": "REVISE", "feedback": "Improve paragraph 2."},
            {"approve": True,  "verdict": "APPROVE", "feedback": ""},
        ]

        from orchestrator import run_pipeline
        run_pipeline("Write something")

        # Second call to writer should include the feedback
        second_writer_call = mock_write.call_args_list[1]
        assert second_writer_call[1].get("critic_feedback") == "Improve paragraph 2."


class TestPipelineState:

    def test_log_step(self):
        from orchestrator import PipelineState
        state = PipelineState(user_request="test")
        state.log_step("researcher", "gather", "Found 5 facts.")
        assert len(state.steps) == 1
        assert state.steps[0]["agent"] == "researcher"
        assert state.steps[0]["action"] == "gather"

    def test_summary_truncated(self):
        from orchestrator import PipelineState
        state = PipelineState(user_request="test")
        long_summary = "A" * 500
        state.log_step("writer", "draft", long_summary)
        assert len(state.steps[0]["summary"]) <= 200


class TestParallelResearch:

    @patch("agents.researcher.run_researcher")
    def test_all_topics_researched(self, mock_research):
        """Parallel research returns results for every input topic."""
        import config
        config.ANTHROPIC_API_KEY = "fake"
        config.VERBOSE = False

        mock_research.side_effect = lambda topic, **kwargs: f"Research on {topic}"

        from orchestrator import run_parallel_research
        topics = ["topic A", "topic B", "topic C"]
        results = run_parallel_research(topics)

        assert len(results) == 3
        assert mock_research.call_count == 3
        # Each result should reference its topic
        for result in results:
            assert "Research on" in result
