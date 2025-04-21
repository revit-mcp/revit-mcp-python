from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_get_current_view_elements_tool(mcp: FastMCP):
    """注册获取当前视图元素的工具"""
    
    @mcp.tool()
    def get_current_view_elements(
        model_category_list: Optional[List[str]] = None,
        annotation_category_list: Optional[List[str]] = None,
        include_hidden: bool = False,
        limit: int = 100
    ) -> dict:
        """
        获取Revit当前视图中的元素。可以通过模型类别（如墙、楼板）或注释类别（如标注、文本）进行过滤。
        使用include_hidden参数显示/隐藏不可见元素，使用limit控制返回元素的数量。
        
        Args:
            model_category_list: Revit模型类别名称列表 (如 'OST_Walls', 'OST_Doors', 'OST_Floors')
            annotation_category_list: Revit注释类别名称列表 (如 'OST_Dimensions', 'OST_WallTags', 'OST_TextNotes')
            include_hidden: 是否包含隐藏元素
            limit: 返回元素的最大数量
            
        Returns:
            包含元素信息的字典
        """
        # 准备参数
        params = {
            "modelCategoryList": model_category_list or [],
            "annotationCategoryList": annotation_category_list or [],
            "includeHidden": include_hidden,
            "limit": limit
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("get_current_view_elements", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"获取当前视图元素失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"获取当前视图元素失败: {str(e)}"
            } 