"""
UI-based MCP trigger example showing different ways to invoke specific MCPs
"""
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("UI Triggers Demo")

@mcp.tool()
def analyze_code(code: str, mode: str = "security") -> str:
    """
    Analyze code with specific mode.
    Demonstrates UI command trigger: /ui set_mode security
    """
    return f"Analyzing code in {mode} mode: {code}"

@mcp.tool()
def process_data(data: str, context: str = "technical") -> str:
    """
    Process data with specific context.
    Demonstrates UI command trigger: /ui set_context technical
    """
    return f"Processing data in {context} context: {data}"

@mcp.tool()
def format_response(text: str, format: str = "markdown") -> str:
    """
    Format response in specific style.
    Demonstrates UI command trigger: /ui format markdown
    """
    return f"Formatting response in {format}: {text}"

if __name__ == "__main__":
    # Configure server settings
    mcp.settings.port = 8080
    mcp.run(transport="sse")  # Using SSE transport for UI interaction 