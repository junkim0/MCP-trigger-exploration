# MCP Trigger Exploration

This repository contains examples and implementations of different Model Context Protocol (MCP) trigger methods for Claude and Cursor integration.

## Project Structure

```
mcp-examples/
├── ui-triggers/      # UI-based command-line style triggers
├── xml-triggers/     # XML-style structured triggers
├── function-triggers/# Python decorator-based triggers
├── custom-triggers/  # Specialized priority-based triggers
├── implementations/  # Working implementations with demos
└── tutorial/         # Step-by-step tutorial with examples

examples/            # Additional example code
```

## Trigger Types

### UI Triggers (Port 8080)
Command-line style interface for triggering MCPs through UI interactions.

### XML Triggers (Port 8081)
Structured XML-based approach for defining and triggering MCPs.

### Function Triggers (Port 8082)
Python decorator-based system for seamless MCP integration.

### Custom Triggers (Port 8083)
Priority-based custom trigger system with specialized handlers.

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run examples:
```bash
python -m mcp_examples.implementations.test_triggers
```

3. Check results in `implementations/RESULTS.md`

## Documentation

Detailed documentation for each trigger type and implementation details can be found in the respective directories.

## Tutorial

Follow the tutorial in `tutorial/MCP_Tutorial.md` for a step-by-step guide with practical examples. 