"""
UI-based MCP trigger example showing different ways to invoke specific MCPs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

app = FastAPI()

class MCPTrigger(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = None
    priority: Optional[int] = 0

@app.post("/trigger")
async def trigger_mcp(trigger: MCPTrigger):
    """
    Trigger an MCP command through the UI interface
    """
    try:
        # Process the command based on UI input
        result = process_command(trigger.command, trigger.context, trigger.priority)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def process_command(command: str, context: Optional[Dict[str, Any]], priority: int) -> Dict[str, Any]:
    """
    Process the MCP command with given context and priority
    """
    # Example command processing logic
    if command.startswith("/"):
        # Handle special commands
        return handle_special_command(command[1:], context)
    else:
        # Handle regular MCP triggers
        return {
            "command_processed": command,
            "context_applied": context,
            "priority_level": priority
        }

def handle_special_command(cmd: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Handle special UI commands starting with /
    """
    commands = {
        "help": lambda: {"available_commands": ["/help", "/status", "/clear"]},
        "status": lambda: {"system_status": "operational"},
        "clear": lambda: {"cleared": True}
    }
    
    if cmd in commands:
        return commands[cmd]()
    raise ValueError(f"Unknown special command: /{cmd}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 