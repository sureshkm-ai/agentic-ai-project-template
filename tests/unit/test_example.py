"""
Unit tests for example module
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.agents.base_agent import BaseAgent


class TestBaseAgent:
    """Test suite for BaseAgent"""
    
    @pytest.fixture
    def agent(self):
        """
        Fixture providing a BaseAgent instance for testing
        
        Returns:
            BaseAgent instance
        """
        return BaseAgent(name="test-agent", description="Test agent")
    
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
    
    @patch('src.agents.base_agent.logger')
    def test_logging(self, mock_logger, agent):
        """Test agent logging"""
        agent.log("Test message", level="info")
        
        mock_logger.info.assert_called_once()


class TestBaseAgentEdgeCases:
    """Test edge cases for BaseAgent"""
    
    def test_empty_name(self):
        """Test agent creation with empty name"""
        with pytest.raises(ValueError):
            BaseAgent(name="", description="Test")
    
    @pytest.mark.asyncio
    async def test_null_state(self):
        """Test processing with null state"""
        agent = BaseAgent(name="test", description="Test")
        
        with pytest.raises(TypeError):
            await agent.process(None)
