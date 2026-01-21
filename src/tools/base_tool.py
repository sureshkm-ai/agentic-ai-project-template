"""
Base tool class template
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from loguru import logger


class BaseToolInput(BaseModel):
    """Base model for tool inputs"""

    pass


class BaseToolOutput(BaseModel):
    """Base model for tool outputs"""

    success: bool = Field(description="Whether the tool execution was successful")
    result: Any = Field(description="Tool execution result")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class BaseTool(ABC):
    """
    Abstract base class for all tools

    All tools should inherit from this class and implement
    the execute method.
    """

    def __init__(self, name: str, description: str):
        """
        Initialize base tool

        Args:
            name: Tool name
            description: Tool description/purpose
        """
        self.name = name
        self.description = description
        logger.info(f"Initialized tool: {name}")

    @abstractmethod
    async def execute(self, input_data: BaseToolInput) -> BaseToolOutput:
        """
        Execute the tool with given input

        Args:
            input_data: Tool input data

        Returns:
            Tool output data
        """
        pass

    def _success(self, result: Any) -> BaseToolOutput:
        """Create a successful tool output"""
        return BaseToolOutput(success=True, result=result)

    def _error(self, error_message: str) -> BaseToolOutput:
        """Create an error tool output"""
        return BaseToolOutput(success=False, result=None, error=error_message)

    def log(self, message: str, level: str = "info") -> None:
        """
        Log a message

        Args:
            message: Message to log
            level: Log level (debug, info, warning, error)
        """
        log_method = getattr(logger, level, logger.info)
        log_method(f"[{self.name}] {message}")
