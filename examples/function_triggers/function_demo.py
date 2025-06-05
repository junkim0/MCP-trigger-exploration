"""
Function-based MCP Triggers Examples
This file demonstrates various ways to trigger MCPs using function calls and decorators.
"""

# Decorator-based MCP triggers
def mcp_mode(mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Simulated MCP mode setting
            print(f"Setting MCP mode to: {mode}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def mcp_context(context):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Setting MCP context to: {context}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example usage of decorators
@mcp_mode("analytical")
@mcp_context("technical")
def analyze_code(code_snippet):
    return f"Analyzing code: {code_snippet}"

# Direct function calls for MCP control
class MCPController:
    @staticmethod
    def set_mode(mode):
        print(f"Setting mode to: {mode}")
    
    @staticmethod
    def set_context(context):
        print(f"Setting context to: {context}")
    
    @staticmethod
    def set_parameters(params):
        print(f"Setting parameters: {params}")

# Example usage
if __name__ == "__main__":
    # Using decorators
    result = analyze_code("def hello(): pass")
    
    # Using direct function calls
    controller = MCPController()
    controller.set_mode("creative")
    controller.set_context("development")
    controller.set_parameters({"temperature": 0.7})

# Function-based context managers
class MCPContext:
    def __init__(self, mode, context):
        self.mode = mode
        self.context = context
    
    def __enter__(self):
        print(f"Entering MCP context: mode={self.mode}, context={self.context}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting MCP context")

# Example usage of context manager
with MCPContext("analytical", "security"):
    print("Performing security analysis...") 