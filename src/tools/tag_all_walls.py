from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_tag_all_walls_tool(mcp: FastMCP):
    """注册为所有墙体添加标签的工具"""
    
    @mcp.tool()
    def tag_all_walls(
        use_leader: bool = False,
        tag_type_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        为当前活动视图中的所有墙体创建标签。标签将放置在每个墙体的中间点。
        
        Args:
            use_leader: 创建标签时是否使用引线
            tag_type_id: 要使用的特定墙体标签族类型的ID。如果未提供，将使用默认墙体标签类型
            
        Returns:
            包含标记操作结果的字典
        """
        # 准备参数
        params = {
            "useLeader": use_leader
        }
        
        # 仅当提供了标签类型ID时才添加该参数
        if tag_type_id:
            params["tagTypeId"] = tag_type_id
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("tag_walls", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"墙体标记失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"墙体标记失败: {str(e)}"
            } 