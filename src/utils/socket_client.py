import socket
import json
import time
import threading
import logging
from typing import Dict, Any, Callable, Optional, Union

logger = logging.getLogger(__name__)

class RevitClientConnection:
    """用于与Revit客户端通信的Socket客户端"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected = False
        self.response_callbacks = {}  # 存储响应回调函数
        self.buffer = ""  # 数据缓冲区
        self.lock = threading.Lock()  # 线程锁
        
    def connect(self) -> bool:
        """连接到Revit客户端"""
        if self.is_connected:
            return True
            
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            
            # 启动接收线程
            receive_thread = threading.Thread(target=self._receive_data)
            receive_thread.daemon = True
            receive_thread.start()
            
            logger.info(f"已连接到Revit客户端 {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"连接到Revit客户端失败: {str(e)}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """断开与Revit客户端的连接"""
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                logger.error(f"关闭Socket连接时出错: {str(e)}")
            finally:
                self.socket = None
                self.is_connected = False
                logger.info("已断开与Revit客户端的连接")
    
    def _receive_data(self) -> None:
        """接收数据线程"""
        while self.is_connected and self.socket:
            try:
                data = self.socket.recv(4096)
                if not data:
                    logger.warning("Revit客户端已关闭连接")
                    self.is_connected = False
                    break
                    
                # 将接收到的数据添加到缓冲区
                with self.lock:
                    self.buffer += data.decode('utf-8')
                    self._process_buffer()
            except Exception as e:
                logger.error(f"接收数据时出错: {str(e)}")
                self.is_connected = False
                break
    
    def _process_buffer(self) -> None:
        """处理缓冲区中的数据"""
        try:
            # 尝试解析JSON
            response = json.loads(self.buffer)
            # 如果成功解析，处理响应并清空缓冲区
            self._handle_response(self.buffer)
            self.buffer = ""
        except json.JSONDecodeError:
            # 数据不完整，继续等待更多数据
            pass
    
    def _generate_request_id(self) -> str:
        """生成唯一的请求ID"""
        return f"{int(time.time() * 1000)}_{hash(threading.current_thread())}"
    
    def _handle_response(self, response_data: str) -> None:
        """处理接收到的响应"""
        try:
            response = json.loads(response_data)
            # 从响应中获取ID
            request_id = response.get('id', 'default')
            
            # 查找并调用对应的回调函数
            callback = self.response_callbacks.pop(request_id, None)
            if callback:
                callback(response_data)
        except Exception as e:
            logger.error(f"处理响应时出错: {str(e)}")
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Any:
        """
        发送命令到Revit客户端
        
        Args:
            command: 要执行的命令名称
            params: 命令参数
            
        Returns:
            命令的执行结果
        """
        if params is None:
            params = {}
            
        # 确保已连接
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError("无法连接到Revit客户端")
        
        # 创建Future对象用于等待异步响应
        response_event = threading.Event()
        response_result = {'data': None, 'error': None}
        
        try:
            # 生成请求ID
            request_id = self._generate_request_id()
            
            # 创建符合JSON-RPC标准的请求对象
            command_obj = {
                "jsonrpc": "2.0",
                "method": command,
                "params": params,
                "id": request_id
            }
            
            # 定义回调函数
            def response_callback(response_data):
                try:
                    response = json.loads(response_data)
                    if 'error' in response:
                        response_result['error'] = response['error'].get('message', '未知错误')
                    else:
                        response_result['data'] = response.get('result')
                except Exception as e:
                    response_result['error'] = f"解析响应时出错: {str(e)}"
                finally:
                    response_event.set()  # 设置事件，通知等待线程
            
            # 存储回调函数
            self.response_callbacks[request_id] = response_callback
            
            # 发送命令
            command_string = json.dumps(command_obj)
            self.socket.sendall(command_string.encode('utf-8'))
            
            # 设置超时
            timeout_seconds = 120  # 2分钟超时
            if not response_event.wait(timeout_seconds):
                self.response_callbacks.pop(request_id, None)
                raise TimeoutError(f"命令超时: {command} (等待了 {timeout_seconds} 秒)")
            
            # 检查是否有错误
            if response_result['error']:
                raise Exception(response_result['error'])
                
            return response_result['data']
            
        except Exception as e:
            logger.error(f"发送命令时出错: {str(e)}")
            raise 