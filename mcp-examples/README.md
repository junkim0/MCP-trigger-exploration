# MCP Trigger Methods Documentation

This repository demonstrates different methods to trigger and interact with Model Context Protocol (MCP) in both Claude and Cursor environments. Each method has its own advantages and use cases.

## 1. UI-Based Triggers (`ui-triggers/`)

UI-based triggers use command-line style interfaces to control MCP behavior. These are direct and intuitive for users.

Example commands:
```
/ui set_mode analytical
/ui set_context technical
/ui format markdown
```

Key features:
- Simple command-line interface
- Direct control over model behavior
- Immediate feedback
- No programming required

## 2. XML-Style Triggers (`xml-triggers/`)

XML-style triggers use structured XML-like tags to define complex behaviors and configurations.

Example structure:
```xml
<task type="code_review">
    <language>python</language>
    <focus>security</focus>
    <detail_level>high</detail_level>
</task>
```

Key features:
- Structured data format
- Nested configurations
- Clear hierarchy of settings
- Good for complex configurations

## 3. Function-Based Triggers (`function-triggers/`)

Function-based triggers use Python decorators and function calls to control MCP behavior programmatically.

Example usage:
```python
@mcp_mode("analytical")
@mcp_context("technical")
def analyze_code(code_snippet):
    return f"Analyzing code: {code_snippet}"
```

Key features:
- Programmatic control
- Type safety
- Integration with existing code
- Flexible and extensible

## 4. Custom Priority Triggers (`custom-triggers/`)

Custom triggers demonstrate how to create prioritized MCP handlers and custom trigger systems.

Example usage:
```python
@mcp.priority_tool(priority=10)
def security_scan(code):
    return f"Running priority security scan on: {code}"
```

Key features:
- Priority-based execution
- Custom trigger handlers
- Specialized MCP types
- Advanced control flow

## Usage

Each example can be run independently on different ports:

1. UI Triggers: Port 8080
2. XML Triggers: Port 8081
3. Function Triggers: Port 8082
4. Custom Triggers: Port 8083

To run an example:
```bash
python ui-triggers/ui_example.py
```

## Integration with Claude and Cursor

These trigger methods can be used with both Claude and Cursor:

1. **Claude Integration**:
   - Use the UI triggers directly in chat
   - XML triggers in system prompts
   - Function triggers via API

2. **Cursor Integration**:
   - All trigger methods via extension API
   - Direct integration with code editor
   - Custom trigger support

## Best Practices

1. Choose the appropriate trigger method based on your use case:
   - UI triggers for direct user interaction
   - XML triggers for complex configurations
   - Function triggers for programmatic control
   - Custom triggers for specialized needs

2. Consider security implications:
   - Validate all inputs
   - Use appropriate authentication
   - Monitor trigger usage

3. Handle errors gracefully:
   - Provide clear error messages
   - Implement fallback behavior
   - Log important events

## Contributing

Feel free to add more trigger methods or improve existing ones. Please follow these guidelines:
1. Add clear documentation
2. Include usage examples
3. Follow Python best practices
4. Add appropriate tests 