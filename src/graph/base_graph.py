"""
Base graph template for LangGraph workflows
"""

from typing import TypedDict, Annotated, Sequence, Any, Optional, cast
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from loguru import logger
import operator


class BaseGraphState(TypedDict):
    """
    Base state schema for graph workflows

    Extend this for your specific use case
    """

    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_agent: str
    final_response: str


class BaseGraph:
    """
    Base class for creating LangGraph workflows
    """

    def __init__(self, name: str = "base-graph"):
        """
        Initialize base graph

        Args:
            name: Graph name for logging
        """
        self.name = name
        # annotate workflow so type checkers do not infer `None` only
        self.workflow: Optional[Any] = None
        logger.info(f"Initialized graph: {name}")

    def create_workflow(self) -> Any:
        """
        Create and return the workflow graph

        Override this method to define your specific workflow

        Returns:
            Compiled StateGraph (concrete type depends on langgraph)
        """
        workflow = StateGraph(BaseGraphState)

        # Add nodes
        # workflow.add_node("node_name", node_function)

        # Add edges
        # workflow.add_edge("node1", "node2")
        # workflow.add_conditional_edges("node", routing_function)

        # Set entry point
        # workflow.set_entry_point("first_node")

        # Set finish point
        # workflow.add_edge("last_node", END)

        return workflow.compile()

    async def run(self, initial_state: BaseGraphState) -> BaseGraphState:
        """
        Run the workflow with initial state

        Args:
            initial_state: Initial state to start workflow

        Returns:
            Final state after workflow completion
        """
        if self.workflow is None:
            self.workflow = self.create_workflow()

        logger.info(f"Running workflow: {self.name}")
        # cast the result of ainvoke to the declared return type so type checkers are satisfied
        final_state = cast(BaseGraphState, await self.workflow.ainvoke(initial_state))
        logger.info(f"Workflow completed: {self.name}")

        return final_state
