from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_get_available_family_types_tool(mcp: FastMCP):
    """注册获取可用族类型的工具"""
    
    @mcp.tool()
    def get_available_family_types(
        category_list: Optional[List[str]] = None,
        family_name_filter: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        获取当前Revit项目中可用的族类型。可以按类别和族名称进行过滤，并限制返回的类型数量。
        
        Args:
            category_list: 要过滤的Revit类别名称列表（例如'OST_Walls'、'OST_Doors'、'OST_Furniture'）
            family_name_filter: 按族名称过滤族类型（部分匹配）
            limit: 返回的族类型最大数量
            
        Returns:
            包含族类型信息的字典
        """
        # 准备参数
        params = {
            "categoryList": category_list or [],
            "familyNameFilter": family_name_filter or "",
            "limit": limit
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("get_available_family_types", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"获取可用族类型失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"获取可用族类型失败: {str(e)}"
            } 