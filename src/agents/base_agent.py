"""
Base agent class template
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from loguru import logger


class BaseAgent(ABC):
    """
    Abstract base class for all agents
    
    All agents should inherit from this class and implement
    the process method.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            description: Agent description/purpose
        """
        self.name = name
        self.description = description
        logger.info(f"Initialized agent: {name}")
    
    @abstractmethod
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the current state and return updated state
        
        Args:
            state: Current state dictionary
            
        Returns:
            Updated state dictionary
        """
        pass
    
    def _create_human_message(self, content: str) -> HumanMessage:
        """Create a human message"""
        return HumanMessage(content=content)
    
    def _create_ai_message(self, content: str) -> AIMessage:
        """Create an AI message"""
        return AIMessage(content=content)
    
    def log(self, message: str, level: str = "info") -> None:
        """
        Log a message
        
        Args:
            message: Message to log
            level: Log level (debug, info, warning, error)
        """
        log_method = getattr(logger, level, logger.info)
        log_method(f"[{self.name}] {message}")
