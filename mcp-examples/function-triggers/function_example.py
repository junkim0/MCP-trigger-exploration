"""
Function-based MCP trigger example showing decorator and direct function call approaches
"""
from mcp.server.fastmcp import FastMCP
from functools import wraps
from typing import Callable, Any, ParamSpec, TypeVar, Optional
from fastapi import FastAPI, HTTPException
import inspect
import uvicorn
import asyncio
from datetime import datetime

# Create MCP server
mcp = FastMCP("Function Triggers Demo")

# Type variables for generic function handling
P = ParamSpec('P')
R = TypeVar('R')

class MCPContext:
    def __init__(self, **kwargs):
        self.timestamp = datetime.utcnow()
        self.metadata = kwargs

class MCPTriggerConfig:
    def __init__(
        self,
        priority: int = 0,
        async_mode: bool = False,
        timeout: Optional[float] = None,
        retry_count: int = 0
    ):
        self.priority = priority
        self.async_mode = async_mode
        self.timeout = timeout
        self.retry_count = retry_count

def mcp_trigger(
    *,
    priority: int = 0,
    async_mode: bool = False,
    timeout: Optional[float] = None,
    retry_count: int = 0
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for MCP-triggered functions
    
    Args:
        priority: Execution priority (higher numbers = higher priority)
        async_mode: Whether to run the function asynchronously
        timeout: Maximum execution time in seconds
        retry_count: Number of retries on failure
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # Store MCP configuration in function metadata
        func._mcp_config = MCPTriggerConfig(
            priority=priority,
            async_mode=async_mode,
            timeout=timeout,
            retry_count=retry_count
        )
        
        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            context = MCPContext(**kwargs.pop('mcp_context', {}))
            
            try:
                if async_mode:
                    if timeout:
                        return await asyncio.wait_for(
                            func(*args, context=context, **kwargs),
                            timeout=timeout
                        )
                    return await func(*args, context=context, **kwargs)
                else:
                    if timeout:
                        return await asyncio.wait_for(
                            asyncio.to_thread(func, *args, context=context, **kwargs),
                            timeout=timeout
                        )
                    return await asyncio.to_thread(func, *args, context=context, **kwargs)
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=408,
                    detail=f"Function execution timed out after {timeout} seconds"
                )
            except Exception as e:
                if retry_count > 0:
                    for i in range(retry_count):
                        try:
                            if async_mode:
                                return await func(*args, context=context, **kwargs)
                            return await asyncio.to_thread(func, *args, context=context, **kwargs)
                        except Exception:
                            if i == retry_count - 1:
                                raise
                else:
                    raise
        
        return async_wrapper

    return decorator

# Example usage with different trigger configurations
@mcp_trigger(priority=1)
def basic_trigger(x: int, context: MCPContext) -> dict:
    """Basic MCP trigger example"""
    return {
        "result": x * 2,
        "timestamp": context.timestamp
    }

@mcp_trigger(priority=2, async_mode=True)
async def async_trigger(data: str, context: MCPContext) -> dict:
    """Async MCP trigger example"""
    await asyncio.sleep(1)  # Simulate async work
    return {
        "processed_data": data.upper(),
        "timestamp": context.timestamp
    }

@mcp_trigger(priority=3, timeout=5.0, retry_count=3)
def reliable_trigger(value: float, context: MCPContext) -> dict:
    """Reliable MCP trigger with timeout and retries"""
    # Simulate work that might fail
    if value < 0:
        raise ValueError("Value must be positive")
    return {
        "result": value ** 2,
        "metadata": context.metadata
    }

# FastAPI endpoints to invoke the triggers
@app.post("/trigger/basic/{x}")
async def trigger_basic(x: int):
    return await basic_trigger(x, mcp_context={"source": "api"})

@app.post("/trigger/async")
async def trigger_async(data: str):
    return await async_trigger(data, mcp_context={"source": "api"})

@app.post("/trigger/reliable/{value}")
async def trigger_reliable(value: float):
    return await reliable_trigger(value, mcp_context={"source": "api"})

if __name__ == "__main__":
    # Configure server settings
    mcp.settings.port = 8082
    mcp.run(transport="sse")

    app = FastAPI()
    uvicorn.run(app, host="0.0.0.0", port=8082) 