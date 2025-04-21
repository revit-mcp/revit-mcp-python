from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Union
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_operate_element_tool(mcp: FastMCP):
    """注册对Revit元素操作的工具"""
    
    @mcp.tool()
    def operate_element(
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        通过执行诸如select、selectionBox、setColor、setTransparency、delete、hide等操作来操作Revit元素。
        
        Args:
            data: 操作参数字典，包含以下内容：
                - elementIds: 要执行指定操作的Revit元素ID数组
                - action: 要对元素执行的操作。有效值：
                    - Select: 在活动视图中启用直接元素选择
                    - SelectionBox: 允许通过在视图中绘制矩形窗口来选择元素
                    - SetColor: 更改元素的颜色（需要colorValue参数）
                    - SetTransparency: 调整元素透明度（需要transparencyValue参数）
                    - Highlight: 将元素设置为红色的便捷操作（内部调用SetColor并使用红色）
                    - Delete: 从项目中永久删除元素
                    - Hide: 使元素在当前视图中不可见，直到明确显示
                    - TempHide: 暂时隐藏当前视图中的元素
                    - Isolate: 仅显示选定元素，同时隐藏所有其他元素
                    - Unhide: 显示先前隐藏的元素
                    - ResetIsolate: 将视图恢复为正常可见性
                - transparencyValue: SetTransparency操作的透明度值（0-100）。较高的值会增加透明度。
                - colorValue: SetColor操作的RGB颜色值。默认值为红色[255, 0, 0]。
                
        Returns:
            包含操作结果的字典
        """
        # 准备参数（直接传递原始数据）
        params = data
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("operate_element", params)
            )
            
            # 返回结果
            return response
            
        except Exception as e:
            logger.error(f"操作元素失败: {str(e)}")
            # 返回错误信息
            return {
                "error": True,
                "message": f"操作元素失败: {str(e)}"
            } 