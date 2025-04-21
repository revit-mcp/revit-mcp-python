from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_color_elements_tool(mcp: FastMCP):
    """注册为元素着色的工具"""
    
    @mcp.tool()
    def color_elements(
        category_name: str,
        parameter_name: str,
        use_gradient: bool = False,
        custom_colors: Optional[List[Dict[str, int]]] = None
    ) -> Dict[str, Any]:
        """
        基于类别和参数值为当前视图中的元素着色。每个唯一的参数值都会分配一个不同的颜色。
        
        Args:
            category_name: Revit类别的名称（例如'Walls'、'Doors'、'Rooms'）
            parameter_name: 用于分组和为元素着色的参数名称
            use_gradient: 是否使用渐变色方案而不是随机颜色
            custom_colors: 用于特定参数值的自定义RGB颜色数组（可选）
            
        Returns:
            包含着色操作结果的字典
        """
        # 准备参数
        params = {
            "categoryName": category_name,
            "parameterName": parameter_name,
            "useGradient": use_gradient,
            "customColors": custom_colors
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("color_splash", params)
            )
            
            # 格式化结果为更加用户友好的输出
            if response.get("success", False):
                colored_groups = response.get("results", [])
                
                result = {
                    "success": True,
                    "total_elements": response.get("totalElements", 0),
                    "colored_groups": response.get("coloredGroups", 0),
                    "groups": []
                }
                
                # 格式化每个颜色组的信息
                for group in colored_groups:
                    rgb = group.get("color", {})
                    result["groups"].append({
                        "parameter_value": group.get("parameterValue", ""),
                        "count": group.get("count", 0),
                        "color": {
                            "r": rgb.get("r", 0),
                            "g": rgb.get("g", 0),
                            "b": rgb.get("b", 0)
                        }
                    })
                
                return result
            else:
                return {
                    "success": False,
                    "error": True,
                    "message": response.get("message", "着色操作失败")
                }
            
        except Exception as e:
            logger.error(f"着色操作失败: {str(e)}")
            return {
                "success": False,
                "error": True,
                "message": f"着色操作失败: {str(e)}"
            } 