from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Any
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_get_selected_elements_tool(mcp: FastMCP):
    """注册获取当前选中元素的工具"""
    
    @mcp.tool()
    def get_selected_elements() -> Dict[str, Any]:
        """
        获取Revit中当前选中的元素
        
        Returns:
            包含选中元素信息的字典
        """
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("get_selected_elements", {})
            )
            
            # 格式化响应
            result = {
                "success": True,
                "elements": response.get("elements", []),
                "count": len(response.get("elements", []))
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取选中元素失败: {str(e)}")
            return {
                "error": True,
                "message": f"获取选中元素失败: {str(e)}"
            } 