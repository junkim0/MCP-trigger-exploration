"""
Custom MCP trigger example showing how to create prioritized MCP triggers
"""
from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, Optional
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import uvicorn
from datetime import datetime
import asyncio
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TriggerPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

class TriggerType(Enum):
    COMMAND = "command"
    EVENT = "event"
    SCHEDULED = "scheduled"
    CONDITIONAL = "conditional"

@dataclass
class TriggerContext:
    timestamp: datetime
    priority: TriggerPriority
    type: TriggerType
    metadata: Dict[str, Any]

class TriggerHandler(ABC):
    @abstractmethod
    async def handle(self, context: TriggerContext, data: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def can_handle(self, trigger_type: TriggerType) -> bool:
        pass

class CommandTriggerHandler(TriggerHandler):
    async def handle(self, context: TriggerContext, data: Any) -> Dict[str, Any]:
        return {
            "type": "command_response",
            "command": data,
            "timestamp": context.timestamp,
            "priority": context.priority.name
        }

    def can_handle(self, trigger_type: TriggerType) -> bool:
        return trigger_type == TriggerType.COMMAND

class EventTriggerHandler(TriggerHandler):
    async def handle(self, context: TriggerContext, data: Any) -> Dict[str, Any]:
        return {
            "type": "event_processed",
            "event_data": data,
            "timestamp": context.timestamp,
            "priority": context.priority.name
        }

    def can_handle(self, trigger_type: TriggerType) -> bool:
        return trigger_type == TriggerType.EVENT

class ScheduledTriggerHandler(TriggerHandler):
    async def handle(self, context: TriggerContext, data: Any) -> Dict[str, Any]:
        return {
            "type": "scheduled_task",
            "task_data": data,
            "timestamp": context.timestamp,
            "priority": context.priority.name
        }

    def can_handle(self, trigger_type: TriggerType) -> bool:
        return trigger_type == TriggerType.SCHEDULED

class ConditionalTriggerHandler(TriggerHandler):
    async def handle(self, context: TriggerContext, data: Any) -> Dict[str, Any]:
        condition_met = await self.evaluate_condition(data)
        return {
            "type": "conditional_trigger",
            "condition_met": condition_met,
            "data": data,
            "timestamp": context.timestamp,
            "priority": context.priority.name
        }

    async def evaluate_condition(self, data: Any) -> bool:
        # Example condition evaluation
        if isinstance(data, dict):
            return data.get("condition", False)
        return False

    def can_handle(self, trigger_type: TriggerType) -> bool:
        return trigger_type == TriggerType.CONDITIONAL

class TriggerManager:
    def __init__(self):
        self.handlers: List[TriggerHandler] = [
            CommandTriggerHandler(),
            EventTriggerHandler(),
            ScheduledTriggerHandler(),
            ConditionalTriggerHandler()
        ]

    async def process_trigger(
        self,
        trigger_type: TriggerType,
        priority: TriggerPriority,
        data: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        context = TriggerContext(
            timestamp=datetime.utcnow(),
            priority=priority,
            type=trigger_type,
            metadata=metadata or {}
        )

        for handler in self.handlers:
            if handler.can_handle(trigger_type):
                return await handler.handle(context, data)

        raise HTTPException(
            status_code=400,
            detail=f"No handler found for trigger type: {trigger_type}"
        )

# Initialize trigger manager
trigger_manager = TriggerManager()

class TriggerRequest(BaseModel):
    type: TriggerType
    priority: TriggerPriority
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@app.post("/trigger")
async def handle_trigger(request: TriggerRequest):
    return await trigger_manager.process_trigger(
        request.type,
        request.priority,
        request.data,
        request.metadata
    )

@app.get("/trigger/types")
async def get_trigger_types():
    return {
        "types": [t.value for t in TriggerType],
        "priorities": [p.name for p in TriggerPriority]
    }

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
    uvicorn.run(app, host="0.0.0.0", port=8083) 