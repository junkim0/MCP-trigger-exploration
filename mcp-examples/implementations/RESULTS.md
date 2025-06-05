# MCP Trigger Methods - Example Outputs

This document shows the expected outputs from different MCP trigger methods. Each section includes example inputs and their corresponding outputs.

## 1. UI-Based Triggers

### Example 1: Setting Mode
**Input:**
```
/ui set_mode analytical
```
**Expected Output:**
```
2024-06-05 10:15:23,456 - INFO - Processing UI command: /ui set_mode analytical
Mode set to: analytical
```

### Example 2: Setting Context
**Input:**
```
/ui set_context technical
```
**Expected Output:**
```
2024-06-05 10:15:23,789 - INFO - Processing UI command: /ui set_context technical
Context set to: technical
```

## 2. XML-Style Triggers

### Example 1: Code Review Task
**Input:**
```xml
<task>
    <type>code_review</type>
    <language>python</language>
    <focus>security</focus>
</task>
```
**Expected Output:**
```json
{
    "config_applied": {
        "type": "code_review",
        "language": "python",
        "focus": "security"
    },
    "mode": "analytical",
    "context": "technical"
}
```

### Example 2: Analysis Task
**Input:**
```xml
<task>
    <type>analysis</type>
    <language>javascript</language>
    <focus>performance</focus>
</task>
```
**Expected Output:**
```json
{
    "config_applied": {
        "type": "analysis",
        "language": "javascript",
        "focus": "performance"
    },
    "mode": "analytical",
    "context": "technical"
}
```

## 3. Function-Based Triggers

### Example 1: Python Code Analysis
**Input:**
```python
analyze_code(language="python", focus="security")
```
**Expected Output:**
```json
{
    "function": "analyze_code",
    "args": {
        "language": "python",
        "focus": "security"
    },
    "mode": "analytical",
    "result": "Analyzing python code with security focus"
}
```

### Example 2: JavaScript Performance Analysis
**Input:**
```python
analyze_code(language="javascript", focus="performance")
```
**Expected Output:**
```json
{
    "function": "analyze_code",
    "args": {
        "language": "javascript",
        "focus": "performance"
    },
    "mode": "analytical",
    "result": "Analyzing javascript code with performance focus"
}
```

## 4. Custom Priority Triggers

### Example 1: High Priority Task
**Input:**
```python
@mcp.priority_tool(priority=2)
async def high_priority_task():
    return "High priority task executed"
```
**Expected Output:**
```
2024-06-05 10:15:24,123 - INFO - Executing high priority task
High priority task executed
```

### Example 2: Normal Priority Task
**Input:**
```python
@mcp.priority_tool(priority=1)
async def normal_task():
    return "Normal task executed"
```
**Expected Output:**
```
2024-06-05 10:15:24,456 - INFO - Executing normal task
Normal task executed
```

## Running the Tests

To see these outputs in action, run the test script:
```bash
python test_triggers.py
```

The script will generate both console output and a log file (`mcp_test_output.log`) containing all the results.

## Common Patterns in Outputs

1. All outputs include timestamps and logging levels
2. JSON responses maintain consistent structure
3. Error messages follow standard format
4. Priority levels are clearly indicated
5. Context and mode settings are preserved across calls

## Troubleshooting

If you don't see the expected outputs:
1. Check that the MCP server is running
2. Verify your Python environment
3. Check the log file for detailed error messages
4. Ensure all dependencies are installed correctly 