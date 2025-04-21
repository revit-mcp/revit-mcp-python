from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_ai_element_filter_tool(mcp: FastMCP):
    """注册AI元素过滤工具"""
    
    @mcp.tool()
    def ai_element_filter(
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        专为AI助手设计的智能Revit元素查询工具，用于从Revit项目中检索详细的元素信息。
        该工具允许AI请求匹配特定条件（如类别、类型、可见性或空间位置）的元素，
        然后对返回的数据进行进一步分析，以回答有关Revit模型元素的复杂用户查询。
        
        例如：当用户询问"查找项目中高度超过5m的所有墙"时，AI会：
        1) 使用参数调用此工具：{"filterCategory": "OST_Walls", "includeInstances": true}
        2) 接收项目中所有墙实例的详细信息
        3) 处理返回的数据以筛选高度 > 5000mm的墙
        4) 向用户呈现带有相关详细信息的筛选结果
        
        Args:
            data: 配置参数字典，包含以下可能的键：
                - filterCategory: Revit中内置元素类别的枚举，用于筛选和识别特定元素类型
                - filterElementType: 用于按类或类型筛选特定元素的Revit元素类型名称
                - filterFamilySymbolId: Revit中特定FamilySymbol（类型）的ElementId
                - includeTypes: 确定是否在选择结果中包含元素类型（如墙类型、门类型等）
                - includeInstances: 确定是否在选择结果中包含元素实例（如放置的墙、门等）
                - filterVisibleInCurrentView: 确定是否仅返回当前视图中可见的元素
                - boundingBoxMin: 用于空间边界框筛选的最小点坐标（以mm为单位）
                - boundingBoxMax: 用于空间边界框筛选的最大点坐标（以mm为单位）
                - maxElements: 在单个工具调用中查找的最大元素数量
                
        Returns:
            包含元素信息的字典
        """
        # 准备参数（直接传递原始数据）
        params = data
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("ai_element_filter", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"获取元素信息失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"获取元素信息失败: {str(e)}"
            } 