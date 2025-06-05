"""
Function-based MCP trigger example showing decorator and direct function call approaches
"""
from mcp.server.fastmcp import FastMCP
from functools import wraps
from typing import Callable, Any

# Create MCP server
mcp = FastMCP("Function Triggers Demo")

# Custom decorators for MCP control
def mcp_mode(mode: str) -> Callable:
    """Decorator to set MCP mode"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"Setting MCP mode to: {mode}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def mcp_context(context: str) -> Callable:
    """Decorator to set MCP context"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"Setting MCP context to: {context}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example usage of decorators
@mcp.tool()
@mcp_mode("analytical")
@mcp_context("technical")
def analyze_code(code_snippet: str) -> str:
    """Analyze code with predefined mode and context"""
    return f"Analyzing code: {code_snippet}"

# Direct function calls for MCP control
class MCPController:
    @staticmethod
    @mcp.tool()
    def set_mode(mode: str) -> str:
        """Set MCP mode directly"""
        return f"Setting mode to: {mode}"
    
    @staticmethod
    @mcp.tool()
    def set_context(context: str) -> str:
        """Set context directly"""
        return f"Setting context to: {context}"
    
    @staticmethod
    @mcp.tool()
    def set_parameters(params: dict) -> str:
        """Set parameters directly"""
        return f"Setting parameters: {params}"

# Context manager for MCP control
class MCPContext:
    def __init__(self, mode: str, context: str):
        self.mode = mode
        self.context = context
    
    def __enter__(self) -> 'MCPContext':
        print(f"Entering MCP context: mode={self.mode}, context={self.context}")
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print("Exiting MCP context")

if __name__ == "__main__":
    # Configure server settings
    mcp.settings.port = 8082
    mcp.run(transport="sse") 