"""
XML-style MCP trigger example showing structured control using XML-like tags
"""
from mcp.server.fastmcp import FastMCP
from typing import Dict, List

# Create MCP server
mcp = FastMCP("XML Triggers Demo")

@mcp.tool()
def code_review(params: Dict[str, str]) -> str:
    """
    Review code with specific parameters.
    Example XML trigger:
    <task type="code_review">
        <language>python</language>
        <focus>security</focus>
        <detail_level>high</detail_level>
    </task>
    """
    return f"Reviewing code with parameters: {params}"

@mcp.tool()
def system_prompt(role: str, expertise_level: str, focus_areas: List[str]) -> str:
    """
    Set system prompt with specific parameters.
    Example XML trigger:
    <system_prompt>
        <role>security_expert</role>
        <expertise_level>senior</expertise_level>
        <focus_areas>
            <area>penetration_testing</area>
            <area>code_analysis</area>
        </focus_areas>
    </system_prompt>
    """
    return f"Setting system prompt - Role: {role}, Level: {expertise_level}, Focus: {focus_areas}"

@mcp.tool()
def response_format(includes: List[str], excludes: List[str]) -> str:
    """
    Configure response format.
    Example XML trigger:
    <response_format>
        <include>code</include>
        <include>explanations</include>
        <exclude>warnings</exclude>
    </response_format>
    """
    return f"Setting response format - Include: {includes}, Exclude: {excludes}"

if __name__ == "__main__":
    # Configure server settings
    mcp.settings.port = 8081
    mcp.run(transport="sse") 