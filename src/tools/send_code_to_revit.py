from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import logging
from src.utils.connection_manager import with_revit_connection

logger = logging.getLogger(__name__)

def register_send_code_to_revit_tool(mcp: FastMCP):
    """注册发送代码到Revit执行的工具"""
    
    @mcp.tool()
    def send_code_to_revit(
        code: str,
        parameters: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        发送C#代码到Revit执行。代码将被插入到一个有权访问Revit Document和参数的模板中。
        您的代码应该被编写为在模板的Execute方法内工作。
        
        Args:
            code: 要在Revit中执行的C#代码。这段代码将被插入到一个有权访问Document和参数的模板的Execute方法中。
            parameters: 可选的执行参数，将传递给您的代码
            
        Returns:
            包含代码执行结果的字典
        """
        # 准备参数
        params = {
            "code": code,
            "parameters": parameters or []
        }
        
        try:
            # 使用连接管理器连接到Revit客户端并发送命令
            response = with_revit_connection(
                lambda client: client.send_command("send_code_to_revit", params)
            )
            
            # 返回结果
            return {
                "success": True,
                "result": response
            }
            
        except Exception as e:
            logger.error(f"代码执行失败: {str(e)}")
            # 返回错误信息
            return {
                "success": False,
                "error": True,
                "message": f"代码执行失败: {str(e)}"
            } 