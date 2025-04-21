from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_delete_element_tool(mcp: FastMCP):
    """注册删除元素的工具"""
    
    @mcp.tool()
    def delete_element(element_ids: List[str]) -> Dict[str, Any]:
        """
        通过元素ID删除Revit模型中的一个或多个元素
        
        Args:
            element_ids: 要删除的元素ID列表
            
        Returns:
            包含操作结果的字典
        """
        # 准备参数
        params = {
            "elementIds": element_ids
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("delete_element", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"删除元素失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"删除元素失败: {str(e)}"
            } 