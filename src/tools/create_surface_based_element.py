from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_create_surface_based_element_tool(mcp: FastMCP):
    """注册创建基于面的元素工具"""
    
    @mcp.tool()
    def create_surface_based_element(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        在Revit中创建一个或多个基于面的元素，例如楼板、天花板或屋顶。
        支持批量创建，具有详细参数，包括族类型ID、边界线、厚度和楼层信息。所有单位均为毫米(mm)。
        
        Args:
            data: 要创建的基于面的元素数组，每个元素包含以下内容：
                - name: 元素描述（例如楼板、天花板）
                - typeId: 要创建的族类型的ID（可选）
                - boundary: 边界定义，包括外环：
                    - outerLoop: 定义边界的线段数组，每个线段包含：
                        - p0: 起点坐标（x, y, z）
                        - p1: 终点坐标（x, y, z）
                - thickness: 元素厚度
                - baseLevel: 基准标高高度
                - baseOffset: 与基准标高的偏移量
                
        Returns:
            包含创建结果的字典
        """
        # 准备参数
        params = {
            "data": data
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("create_surface_based_element", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"创建基于面的元素失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"创建基于面的元素失败: {str(e)}"
            } 