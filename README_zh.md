# revit-mcp-python

[English](README.md) | [简体中文](README_zh.md)

## 简介

revit-mcp-python 是 [revit-mcp](https://github.com/revit-mcp/revit-mcp) 的Python实现，允许你通过MCP协议（Model Context Protocol）使用MCP支持的客户端（如Claude、Cline等）与Revit进行交互。

本项目是服务器端（为AI提供工具），需要配合 revit-mcp-plugin（驱动Revit）一起使用。

## 特性

* 允许AI从Revit项目中获取数据
* 允许AI驱动Revit创建、修改和删除元素
* 发送AI生成的代码到Revit执行（可能不一定成功，在需求明确的简单场景中成功率较高）

## 系统要求

* Python 3.11+
* uv 包管理器
* 运行中的Revit应用程序（带有兼容的MCP客户端插件）

> 完整安装环境还需要考虑 revit-mcp-plugin 的需求，请参考 revit-mcp-plugin

## 安装

### 1. 安装 uv 包管理器

如果你还没有安装 uv，请按照[官方文档](https://github.com/astral-sh/uv)进行安装。

对于 Windows：
```
pip install uv
```

### 2. 设置项目

克隆仓库并导航到项目目录。

使用 uv 安装依赖：
```
uv pip install -e .
```

### 3. 客户端配置

**Claude客户端**

Claude客户端 -> 设置 > 开发者 > 编辑配置 > claude_desktop_config.json

```json
{
    "mcpServers": {
        "revit-mcp-python": {
            "command": "uv",
            "args": [
                "--directory",
                "<项目路径>",
                "run",
                "main.py"
            ]
        }
    }
}
```

将 `<项目路径>` 替换为 revit-mcp-python 目录的绝对路径。

重启Claude客户端。当你看到锤子图标时，表示与MCP服务的连接正常。

## 扩展工具

您可以通过在`src/tools`目录中添加新的Python文件来扩展可用工具。每个工具文件应遵循以下格式:

```python
from mcp.server.fastmcp import FastMCP
from utils.connection_manager import with_revit_connection

def register_your_tool_name(mcp: FastMCP):
    """注册您的工具"""
    
    @mcp.tool()
    def your_tool_name(...):
        """工具描述"""
        # 实现代码
        # 使用 with_revit_connection 与Revit客户端通信
```

注意: 确保工具函数和注册函数的名称匹配，这样动态注册系统才能正确识别它们。

## 项目结构

- `main.py`: 主入口点，从src导入
- `src/`: 源代码目录
  - `main.py`: 主服务器实现
  - `tools/`: 包含所有可用工具的目录
  - `utils/`: 实用工具，包括Socket客户端和连接管理器

## 许可证

MIT 许可证 