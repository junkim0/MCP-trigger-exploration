"""
Custom MCP trigger example showing how to create prioritized MCP triggers
"""
from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrioritizedMCP(FastMCP):
    def __init__(self, name: str):
        super().__init__(name)
        self.priority_tools: Dict[str, int] = {}
        self.default_priority = 0

    def priority_tool(self, priority: int = 1):
        """Decorator to register a tool with priority"""
        def decorator(func: Any) -> Any:
            tool_name = func.__name__
            self.priority_tools[tool_name] = priority
            return self.tool()(func)
        return decorator

    async def handle_tool_call(self, tool_name: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        """Override tool handling to check priorities"""
        priority = self.priority_tools.get(tool_name, self.default_priority)
        logger.info(f"Handling tool '{tool_name}' with priority {priority}")
        
        # Here you could implement priority-based queuing or immediate execution
        # For this example, we just log the priority
        return await super().handle_tool_call(tool_name, *args, **kwargs)

# Create prioritized MCP server
mcp = PrioritizedMCP("Custom Triggers Demo")

@mcp.priority_tool(priority=10)
def security_scan(code: str) -> str:
    """
    High-priority security scanning tool.
    This tool will be prioritized over others.
    """
    return f"Running priority security scan on: {code}"

@mcp.priority_tool(priority=5)
def performance_analysis(code: str) -> str:
    """
    Medium-priority performance analysis tool.
    """
    return f"Running performance analysis on: {code}"

@mcp.tool()  # Default priority (0)
def code_format(code: str) -> str:
    """
    Standard-priority code formatting tool.
    """
    return f"Formatting code: {code}"

# Custom trigger handler for specific MCP types
class MCPTriggerHandler:
    def __init__(self, mcp_type: str):
        self.mcp_type = mcp_type
        self.handlers: Dict[str, Any] = {}

    def register_handler(self, trigger: str, handler: Any) -> None:
        """Register a handler for a specific trigger"""
        self.handlers[trigger] = handler

    def handle_trigger(self, trigger: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        """Handle a specific trigger"""
        handler = self.handlers.get(trigger)
        if handler:
            logger.info(f"Handling {self.mcp_type} trigger: {trigger}")
            return handler(*args, **kwargs)
        return None

# Example usage of custom trigger handler
security_handler = MCPTriggerHandler("security")

@security_handler.register_handler("vulnerability_scan")
def handle_vulnerability_scan(code: str) -> str:
    return security_scan(code)

if __name__ == "__main__":
    # Configure server settings
    mcp.settings.port = 8083
    mcp.run(transport="sse") 