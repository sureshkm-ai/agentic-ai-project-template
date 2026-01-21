"""
Unit tests for example module
"""

from typing import Any, Dict
from unittest.mock import patch

import pytest

from src.agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing"""

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Simple stub implementation for testing"""
        return {"processed": True}


class TestBaseAgent:
    """Test suite for BaseAgent"""

    @pytest.fixture
    def agent(self):
        """
        Fixture providing a DummyAgent instance for testing

        Returns:
            DummyAgent instance
        """
        return DummyAgent(name="test-agent", description="Test agent")

    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent.name == "test-agent"
        assert agent.description == "Test agent"

    @pytest.mark.asyncio
    async def test_agent_process(self, agent):
        """Test agent processing"""
        state = {"input": "test"}
        result = await agent.process(state)

        assert result is not None
        assert isinstance(result, dict)

    def test_create_human_message(self, agent):
        """Test human message creation"""
        message = agent._create_human_message("Hello")

        assert message.content == "Hello"
        assert message.type == "human"

    @patch("src.agents.base_agent.logger")
    def test_logging(self, mock_logger, agent):
        """Test agent logging"""
        agent.log("Test message", level="info")

        mock_logger.info.assert_called_once()


class TestBaseAgentEdgeCases:
    """Test edge cases for BaseAgent"""

    def test_empty_name(self):
        """Test agent creation with empty name"""
        with pytest.raises(ValueError):
            DummyAgent(name="", description="Test")

    @pytest.mark.asyncio
    async def test_null_state(self):
        """Test processing with null state returns valid result"""
        agent = DummyAgent(name="test", description="Test")

        result = await agent.process(None)
        assert isinstance(result, dict)
