"""
XML-style MCP trigger example showing structured control using XML-like tags
"""
from mcp.server.fastmcp import FastMCP
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import xml.etree.ElementTree as ET
import uvicorn

# Create MCP server
mcp = FastMCP("XML Triggers Demo")

app = FastAPI()

class XMLTrigger(BaseModel):
    xml_content: str
    validate: Optional[bool] = True

@app.post("/xml-trigger")
async def trigger_xml_mcp(trigger: XMLTrigger):
    """
    Trigger MCP using XML formatted input
    """
    try:
        # Parse and validate XML
        root = ET.fromstring(trigger.xml_content)
        if trigger.validate:
            validate_mcp_xml(root)
        
        # Process the XML trigger
        result = process_xml_trigger(root)
        return {"status": "success", "result": result}
    except ET.ParseError as e:
        raise HTTPException(status_code=400, detail=f"Invalid XML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def validate_mcp_xml(root: ET.Element):
    """
    Validate MCP XML structure
    """
    required_elements = ["command", "context"]
    for elem in required_elements:
        if root.find(elem) is None:
            raise ValueError(f"Missing required element: {elem}")

def process_xml_trigger(root: ET.Element) -> dict:
    """
    Process XML-based MCP trigger
    """
    command = root.find("command").text
    context = root.find("context").text
    priority = root.find("priority").text if root.find("priority") is not None else "0"
    
    # Example XML processing logic
    return {
        "command": command,
        "context": context,
        "priority": int(priority),
        "metadata": {
            "trigger_type": "xml",
            "schema_version": "1.0"
        }
    }

@app.get("/xml-schema")
async def get_xml_schema():
    """
    Return the XML schema for MCP triggers
    """
    return {
        "schema": """
        <mcp-trigger>
            <command>string</command>
            <context>string</context>
            <priority>integer</priority>
            <metadata>
                <key>value</key>
            </metadata>
        </mcp-trigger>
        """
    }

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
    uvicorn.run(app, host="0.0.0.0", port=8081) 