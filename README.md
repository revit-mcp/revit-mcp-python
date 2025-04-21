# revit-mcp-python

[English](README.md) | [简体中文](README_zh.md)

## Description

revit-mcp-python is a Python implementation of [revit-mcp](https://github.com/revit-mcp/revit-mcp), allowing you to interact with Revit using the MCP protocol (Model Context Protocol) through MCP-supported clients (such as Claude, Cline, etc.).

This project is the server side (providing Tools to AI), and you need to use revit-mcp-plugin (driving Revit) in conjunction.

## Features

* Allow AI to get data from the Revit project
* Allow AI to drive Revit to create, modify, and delete elements
* Send AI-generated code to Revit to execute (may not be successful, success rate is higher in simple scenarios with clear requirements)

## Requirements

* Python 3.11+
* uv package manager
* Running Revit application (with compatible MCP client plugin)

> The complete installation environment also needs to consider the requirements of revit-mcp-plugin, please refer to revit-mcp-plugin

## Installation

### 1. Install uv package manager

If you don't already have uv installed, install it according to the [official documentation](https://github.com/astral-sh/uv).

For Windows:
```
pip install uv
```

### 2. Setup the project

Clone the repository and navigate to the project directory.

Install dependencies with uv:
```
uv pip install -e .
```

### 3. Client configuration

**Claude client**

Claude client -> Settings > Developer > Edit Config > claude_desktop_config.json

```json
{
    "mcpServers": {
        "revit-mcp-python": {
            "command": "uv",
            "args": [
                "--directory",
                "<path to your project>",
                "run",
                "main.py"
            ]
        }
    }
}
```

Replace `<path to your project>` with the absolute path to your revit-mcp-python directory.

Restart the Claude client. When you see the hammer icon, it means the connection to the MCP service is normal.

## Extending Tools

You can extend the available tools by adding new Python files to the `src/tools` directory. Each tool file should follow this format:

```python
from mcp.server.fastmcp import FastMCP
from utils.connection_manager import with_revit_connection

def register_your_tool_name(mcp: FastMCP):
    """Register your tool"""
    
    @mcp.tool()
    def your_tool_name(...):
        """Tool description"""
        # Implementation code
        # Use with_revit_connection to communicate with Revit client
```

Note: Make sure the tool function and register function names match, so the dynamic registration system can recognize them correctly.

## Project Structure

- `main.py`: Main entry point that imports from src
- `src/`: Source code directory
  - `main.py`: Main server implementation
  - `tools/`: Directory containing all available tools
  - `utils/`: Utilities, including Socket client and connection manager

## License

MIT License
