import logging
import threading
import time
from typing import Any, Callable, TypeVar, Generic
from .socket_client import RevitClientConnection

logger = logging.getLogger(__name__)

# 定义泛型类型
T = TypeVar('T')

def with_revit_connection(operation: Callable[[RevitClientConnection], T], 
                          host: str = "localhost", 
                          port: int = 8080,
                          timeout: int = 5) -> T:
    """
    连接到Revit客户端并执行操作
    
    Args:
        operation: 连接成功后要执行的操作函数
        host: Revit客户端主机地址，默认为localhost
        port: Revit客户端端口，默认为8080
        timeout: 连接超时时间（秒），默认为5秒
        
    Returns:
        操作的结果
        
    Raises:
        ConnectionError: 无法连接到Revit客户端
        TimeoutError: 连接超时
        Exception: 操作执行过程中的其他错误
    """
    revit_client = RevitClientConnection(host, port)
    
    try:
        # 连接到Revit客户端
        if not revit_client.is_connected:
            connect_success = revit_client.connect()
            
            if not connect_success:
                raise ConnectionError("无法连接到Revit客户端")
            
            # 等待连接建立
            connection_time = 0
            check_interval = 0.1  # 100ms
            
            while not revit_client.is_connected and connection_time < timeout:
                time.sleep(check_interval)
                connection_time += check_interval
                
            if not revit_client.is_connected:
                raise TimeoutError(f"连接Revit客户端超时（{timeout}秒）")
                
        # 执行操作
        return operation(revit_client)
        
    except Exception as e:
        logger.error(f"与Revit客户端交互时出错: {str(e)}")
        raise
        
    finally:
        # 无论操作是否成功，都断开连接
        revit_client.disconnect() 