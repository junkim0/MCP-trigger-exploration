# MCP Triggers Tutorial

This tutorial will guide you through implementing and using different MCP (Model Control Protocol) trigger methods. Each section includes practical examples and points where you should take screenshots for visual reference.

## Prerequisites
- Python 3.8 or higher
- Basic understanding of Python programming
- A text editor or IDE (VS Code recommended)

## Setup

1. Create a new directory for your MCP project:
```bash
mkdir mcp-project
cd mcp-project
```
📸 **Screenshot Opportunity**: Show the terminal with the created directory

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```
📸 **Screenshot Opportunity**: Show the activated virtual environment

3. Install required packages:
```bash
pip install fastmcp aiohttp python-dotenv
```

## 1. UI-Based Triggers

### Implementation Steps:

1. Create a new file `ui_trigger_demo.py`:
```python
from fastmcp import FastMCP

mcp = FastMCP("UI Demo")

# Register a command handler
@mcp.command()
async def set_mode(mode: str):
    print(f"Setting mode to: {mode}")
    return f"Mode set to {mode}"

# Start the MCP server
if __name__ == "__main__":
    mcp.run()
```
📸 **Screenshot Opportunity**: Show the code in your editor

2. Run the demo:
```bash
python ui_trigger_demo.py
```
📸 **Screenshot Opportunity**: Show the running server

3. Test UI triggers:
```
/ui set_mode analytical
/ui set_context technical
```
📸 **Screenshot Opportunity**: Show the command output

## 2. XML-Style Triggers

### Implementation Steps:

1. Create `xml_trigger_demo.py`:
```python
from fastmcp import FastMCP
from typing import Dict

mcp = FastMCP("XML Demo")

@mcp.tool()
async def process_xml_config(config: Dict):
    """
    Handle XML-style configuration
    Example input:
    <task>
        <type>code_review</type>
        <focus>security</focus>
    </task>
    """
    task_type = config.get('type')
    focus = config.get('focus')
    return f"Processing {task_type} task with {focus} focus"

if __name__ == "__main__":
    mcp.run()
```
📸 **Screenshot Opportunity**: Show the XML trigger implementation

2. Test XML triggers:
```xml
<task>
    <type>code_review</type>
    <focus>security</focus>
</task>
```
📸 **Screenshot Opportunity**: Show the XML configuration and response

## 3. Function-Based Triggers

### Implementation Steps:

1. Create `function_trigger_demo.py`:
```python
from fastmcp import FastMCP
from functools import wraps

mcp = FastMCP("Function Demo")

def mcp_mode(mode):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"Setting MCP mode to: {mode}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@mcp_mode("analytical")
async def analyze_code(code: str):
    return f"Analyzing code in analytical mode: {code}"

if __name__ == "__main__":
    mcp.run()
```
📸 **Screenshot Opportunity**: Show the function-based implementation

2. Test function triggers:
```python
result = await analyze_code("def hello(): pass")
print(result)
```
📸 **Screenshot Opportunity**: Show the function call and output

## 4. Custom Priority Triggers

### Implementation Steps:

1. Create `priority_trigger_demo.py`:
```python
from fastmcp import FastMCP
from typing import Dict

class PriorityMCP(FastMCP):
    def __init__(self, name: str):
        super().__init__(name)
        self.priorities: Dict[str, int] = {}

    def priority_tool(self, priority: int = 1):
        def decorator(func):
            self.priorities[func.__name__] = priority
            return self.tool()(func)
        return decorator

mcp = PriorityMCP("Priority Demo")

@mcp.priority_tool(priority=2)
async def high_priority_task():
    return "High priority task executed"

@mcp.priority_tool(priority=1)
async def normal_task():
    return "Normal task executed"

if __name__ == "__main__":
    mcp.run()
```
📸 **Screenshot Opportunity**: Show the priority implementation

## Testing Your Implementation

1. Run each demo file separately and test the triggers
2. Observe the outputs and logging
3. Try combining different trigger methods
4. Experiment with different priorities and configurations

📸 **Screenshot Opportunity**: Show a combined test with multiple trigger types

## Common Issues and Solutions

1. **Connection Issues**
   - Ensure the MCP server is running
   - Check port availability
   - Verify network settings

2. **Configuration Errors**
   - Double-check XML syntax
   - Verify function decorators
   - Check priority values

3. **Performance Considerations**
   - Monitor response times
   - Use appropriate priority levels
   - Consider async/await patterns

## Next Steps

1. Explore more complex trigger combinations
2. Implement error handling
3. Add custom logging
4. Create your own trigger patterns

📸 **Screenshot Opportunity**: Show your final working implementation

## Resources

- FastMCP Documentation
- Python AsyncIO Documentation
- XML Processing Guidelines
- MCP Best Practices Guide 