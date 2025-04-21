from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_get_current_view_info_tool(mcp: FastMCP):
    """注册获取当前视图信息的工具"""
    
    @mcp.tool()
    def get_current_view_info() -> Dict[str, Any]:
        """
        获取Revit当前活动视图的详细信息，包括视图类型、名称、比例等属性。
        
        Returns:
            包含当前视图信息的字典
        """
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("get_current_view_info", {})
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"获取当前视图信息失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"获取当前视图信息失败: {str(e)}"
            } 