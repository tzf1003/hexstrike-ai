#!/usr/bin/env python3
"""
HexStrike AI - MCP客户端实现
MCP Client Implementation

这个模块提供了与HexStrike AI API服务器通信的客户端，包括：
- 安全的HTTP请求处理
- 连接重试和故障恢复
- 中文化的日志记录
- 请求和响应的标准化处理
"""

import requests
import time
from typing import Dict, Any, Optional
from datetime import datetime

from ...config.logger_config import get_logger
from ...config.colors import HexStrikeColors
from .connection_manager import ConnectionManager

class HexStrikeMCPClient:
    """HexStrike AI MCP客户端 - 与API服务器通信的增强客户端"""
    
    def __init__(self, 
                 server_url: str, 
                 timeout: int = 300,
                 max_retries: int = 3):
        """初始化HexStrike AI MCP客户端
        
        Args:
            server_url: HexStrike AI API服务器URL
            timeout: 请求超时时间(秒)
            max_retries: 最大重试次数
        """
        self.server_url = server_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = get_logger('HexStrike-MCP-Client')
        
        # 创建连接管理器
        self.connection_manager = ConnectionManager(
            server_url=server_url,
            timeout=timeout,
            max_retries=max_retries
        )
        
        # 建立会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HexStrike-AI-MCP-Client/6.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 连接状态
        self.is_connected = False
        self.last_health_check = None
        self.server_info = {}
        
        # 统计信息
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'connection_retries': 0,
            'last_request_time': None
        }
        
        self.logger.info(f"🔗 初始化MCP客户端，目标服务器: {self.server_url}")
        
        # 尝试建立连接
        self._establish_connection()
    
    def _establish_connection(self):
        """建立与服务器的连接"""
        self.logger.info("🔄 正在建立与HexStrike AI服务器的连接...")
        
        connected = False
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"📡 连接尝试 {attempt}/{self.max_retries}...")
                
                # 执行健康检查
                health_result = self._perform_health_check()
                
                if health_result.get('success', False):
                    self.is_connected = True
                    self.server_info = health_result.get('data', {})
                    connected = True
                    
                    self.logger.success(f"✅ 成功连接到HexStrike AI服务器")
                    self.logger.info(f"📊 服务器状态: {self.server_info.get('status', '未知')}")
                    
                    # 显示服务器信息
                    if 'version' in self.server_info:
                        self.logger.info(f"🏷️  服务器版本: {self.server_info['version']}")
                    
                    if 'tools' in self.server_info:
                        available_tools = self.server_info['tools'].get('available_tools', 0)
                        total_tools = self.server_info['tools'].get('total_tools', 0)
                        self.logger.info(f"🛠️  可用工具: {available_tools}/{total_tools}")
                    
                    break
                    
                else:
                    error_msg = health_result.get('error', '未知错误')
                    self.logger.warning(f"⚠️  连接检查失败: {error_msg}")
                    
            except Exception as e:
                self.logger.warning(f"⚠️  连接尝试 {attempt} 失败: {e}")
                self.stats['connection_retries'] += 1
            
            if attempt < self.max_retries:
                wait_time = min(2 ** attempt, 10)  # 指数退避，最大10秒
                self.logger.info(f"⏳ 等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        if not connected:
            self.logger.error(f"❌ 在 {self.max_retries} 次尝试后仍无法连接到服务器")
            self.logger.warning("⚠️  MCP客户端将继续运行，但工具调用可能失败")
    
    def _perform_health_check(self) -> Dict[str, Any]:
        """执行服务器健康检查"""
        try:
            response = self.session.get(
                f"{self.server_url}/health",
                timeout=min(self.timeout, 10)  # 健康检查使用较短超时
            )
            response.raise_for_status()
            
            result = response.json()
            self.last_health_check = datetime.now()
            
            return {
                'success': True,
                'data': result.get('data', {}),
                'message': result.get('message', '健康检查成功')
            }
            
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': '无法连接到服务器，请确保HexStrike AI服务器正在运行'
            }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': '服务器响应超时'
            }
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP错误: {e.response.status_code}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'健康检查异常: {str(e)}'
            }
    
    def safe_get(self, 
                 endpoint: str, 
                 params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行安全的GET请求
        
        Args:
            endpoint: API端点路径(不带前导斜杠)
            params: 可选的查询参数
            
        Returns:
            响应数据字典
        """
        if params is None:
            params = {}
        
        url = f"{self.server_url}/{endpoint}"
        
        self.logger.debug(f"📡 发送GET请求: {url}")
        if params:
            self.logger.debug(f"📝 请求参数: {params}")
        
        try:
            self.stats['requests_total'] += 1
            self.stats['last_request_time'] = datetime.now()
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            self.stats['requests_success'] += 1
            
            self.logger.debug(f"✅ GET请求成功: {endpoint}")
            return result
            
        except requests.exceptions.RequestException as e:
            self.stats['requests_failed'] += 1
            error_msg = f"请求失败: {str(e)}"
            self.logger.error(f"❌ GET请求失败 {endpoint}: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "error_type": "request_error",
                "endpoint": endpoint
            }
            
        except Exception as e:
            self.stats['requests_failed'] += 1
            error_msg = f"意外错误: {str(e)}"
            self.logger.error(f"💥 GET请求异常 {endpoint}: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "error_type": "unexpected_error",
                "endpoint": endpoint
            }
    
    def safe_post(self, 
                  endpoint: str, 
                  json_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行安全的POST请求
        
        Args:
            endpoint: API端点路径(不带前导斜杠)
            json_data: 要发送的JSON数据
            
        Returns:
            响应数据字典
        """
        url = f"{self.server_url}/{endpoint}"
        
        self.logger.debug(f"📡 发送POST请求: {url}")
        self.logger.debug(f"📝 请求数据: {json_data}")
        
        try:
            self.stats['requests_total'] += 1
            self.stats['last_request_time'] = datetime.now()
            
            response = self.session.post(url, json=json_data, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            self.stats['requests_success'] += 1
            
            self.logger.debug(f"✅ POST请求成功: {endpoint}")
            return result
            
        except requests.exceptions.RequestException as e:
            self.stats['requests_failed'] += 1
            error_msg = f"请求失败: {str(e)}"
            self.logger.error(f"❌ POST请求失败 {endpoint}: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "error_type": "request_error",
                "endpoint": endpoint
            }
            
        except Exception as e:
            self.stats['requests_failed'] += 1
            error_msg = f"意外错误: {str(e)}"
            self.logger.error(f"💥 POST请求异常 {endpoint}: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "error_type": "unexpected_error",
                "endpoint": endpoint
            }
    
    def execute_command(self, 
                       command: str, 
                       use_cache: bool = True,
                       timeout: Optional[int] = None) -> Dict[str, Any]:
        """执行通用命令
        
        Args:
            command: 要执行的命令
            use_cache: 是否使用缓存
            timeout: 命令超时时间
            
        Returns:
            命令执行结果
        """
        self.logger.info(f"🚀 执行命令: {command}")
        
        request_data = {
            "command": command,
            "use_cache": use_cache
        }
        
        if timeout is not None:
            request_data["timeout"] = timeout
        
        result = self.safe_post("api/command", request_data)
        
        if result.get("success"):
            duration = result.get("duration", 0)
            self.logger.success(f"✅ 命令执行成功，耗时: {duration:.2f}秒")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 命令执行失败: {error}")
        
        return result
    
    def check_health(self) -> Dict[str, Any]:
        """检查服务器健康状态
        
        Returns:
            服务器健康状态信息
        """
        self.logger.debug("🔍 检查服务器健康状态...")
        result = self.safe_get("health")
        
        if result.get("success"):
            self.logger.debug("✅ 服务器健康检查通过")
            self.is_connected = True
            self.last_health_check = datetime.now()
        else:
            self.logger.warning("⚠️  服务器健康检查失败")
            self.is_connected = False
        
        return result
    
    def get_tools_status(self) -> Dict[str, Any]:
        """获取工具状态信息
        
        Returns:
            工具状态信息
        """
        self.logger.debug("🛠️  获取工具状态信息...")
        result = self.safe_get("api/tools/status")
        
        if result.get("success"):
            data = result.get("data", {})
            total_tools = data.get("total_tools", 0)
            available_tools = data.get("available_tools", 0)
            self.logger.info(f"📊 工具状态: {available_tools}/{total_tools} 可用")
        
        return result
    
    def get_client_stats(self) -> Dict[str, Any]:
        """获取客户端统计信息
        
        Returns:
            客户端统计信息
        """
        success_rate = 0
        if self.stats['requests_total'] > 0:
            success_rate = (self.stats['requests_success'] / self.stats['requests_total']) * 100
        
        return {
            'connected': self.is_connected,
            'server_url': self.server_url,
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'stats': {
                **self.stats,
                'success_rate': round(success_rate, 2),
                'last_request_time': self.stats['last_request_time'].isoformat() if self.stats['last_request_time'] else None
            },
            'server_info': self.server_info
        }
    
    def __del__(self):
        """析构函数 - 清理资源"""
        try:
            if hasattr(self, 'session'):
                self.session.close()
        except:
            pass