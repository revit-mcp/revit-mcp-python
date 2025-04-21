from mcp.server.fastmcp import FastMCP
import os
import sys
import importlib
import logging
from typing import List, Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建服务器实例
mcp = FastMCP("revit-mcp-python")

def register_tools():
    """动态注册tools目录下的所有工具"""
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    
    # 确保tools目录存在
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        logger.info(f"Created tools directory: {tools_dir}")
        return
    
    # 确保tools目录在Python路径中
    if tools_dir not in sys.path:
        sys.path.append(tools_dir)
    
    tool_files = [f for f in os.listdir(tools_dir) 
                 if f.endswith('.py') and 
                 not f.startswith('__') and
                 f != '__init__.py']
    
    for file_name in tool_files:
        module_name = file_name[:-3]
        try:
            # 动态导入模块
            module = importlib.import_module(f"src.tools.{module_name}")
            
            # 查找并执行注册函数
            register_func_name = None
            for name in dir(module):
                if name.startswith('register') and callable(getattr(module, name)):
                    register_func_name = name
                    break
            
            if register_func_name:
                register_func = getattr(module, register_func_name)
                register_func(mcp)
                logger.info(f"已注册工具: {module_name}")
            else:
                logger.warning(f"警告: 在文件 {file_name} 中未找到注册函数")
        except Exception as e:
            logger.error(f"注册工具 {file_name} 时出错: {str(e)}")

def main():
    # 注册所有工具
    register_tools()
    
    # 启动服务器
    logger.info("Revit MCP Python Server 启动中...")
    mcp.run()
    logger.info("Revit MCP Python Server 已关闭")

if __name__ == "__main__":
    main() 