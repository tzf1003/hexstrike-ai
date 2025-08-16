#!/usr/bin/env python3
"""
HexStrike AI - MCP连接管理器
MCP Connection Manager

这个模块提供了MCP客户端的连接管理功能，包括：
- 连接池管理
- 自动重连机制
- 连接健康监控
- 故障检测和恢复
"""

import threading
import time
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ...config.logger_config import get_logger

class ConnectionStatus(Enum):
    """连接状态枚举"""
    DISCONNECTED = "已断开"
    CONNECTING = "连接中"
    CONNECTED = "已连接"
    RECONNECTING = "重连中"
    FAILED = "连接失败"

@dataclass
class ConnectionMetrics:
    """连接指标数据类"""
    total_attempts: int = 0
    successful_connections: int = 0
    failed_connections: int = 0
    reconnection_attempts: int = 0
    last_connection_time: Optional[datetime] = None
    last_failure_time: Optional[datetime] = None
    average_response_time: float = 0.0
    uptime_percentage: float = 0.0

class ConnectionManager:
    """MCP连接管理器 - 管理与HexStrike AI服务器的连接"""
    
    def __init__(self, 
                 server_url: str,
                 timeout: int = 30,
                 max_retries: int = 3,
                 health_check_interval: int = 60):
        """初始化连接管理器
        
        Args:
            server_url: 服务器URL
            timeout: 连接超时时间
            max_retries: 最大重试次数
            health_check_interval: 健康检查间隔(秒)
        """
        self.server_url = server_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.health_check_interval = health_check_interval
        
        self.logger = get_logger('ConnectionManager')
        
        # 连接状态
        self.status = ConnectionStatus.DISCONNECTED
        self.last_error = None
        self.connection_start_time = None
        
        # 连接指标
        self.metrics = ConnectionMetrics()
        
        # 回调函数
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        
        # 健康检查线程
        self.health_check_thread = None
        self.health_check_active = False
        
        # 线程锁
        self.lock = threading.RLock()
        
        self.logger.info(f"🔗 连接管理器初始化完成，目标: {server_url}")
    
    def start_health_monitoring(self):
        """启动健康监控"""
        with self.lock:
            if not self.health_check_active:
                self.health_check_active = True
                self.health_check_thread = threading.Thread(
                    target=self._health_check_loop,
                    daemon=True
                )
                self.health_check_thread.start()
                self.logger.info("💓 连接健康监控已启动")
    
    def stop_health_monitoring(self):
        """停止健康监控"""
        with self.lock:
            self.health_check_active = False
            if self.health_check_thread:
                self.health_check_thread.join(timeout=5)
            self.logger.info("💓 连接健康监控已停止")
    
    def _health_check_loop(self):
        """健康检查循环"""
        while self.health_check_active:
            try:
                self._perform_health_check()
                time.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"❌ 健康检查循环异常: {e}")
                time.sleep(self.health_check_interval)
    
    def _perform_health_check(self):
        """执行健康检查"""
        try:
            # 这里应该实际调用服务器健康检查
            # 暂时模拟健康检查
            current_time = datetime.now()
            
            if self.status == ConnectionStatus.CONNECTED:
                # 检查连接是否仍然有效
                if self.connection_start_time:
                    uptime = (current_time - self.connection_start_time).total_seconds()
                    if uptime > 0:
                        self.metrics.uptime_percentage = min(100.0, uptime / 3600 * 100)
                
                self.logger.debug("💓 连接健康检查通过")
            else:
                self.logger.debug("💓 连接未建立，跳过健康检查")
                
        except Exception as e:
            self.logger.warning(f"⚠️  健康检查失败: {e}")
            self._handle_connection_failure(str(e))
    
    def connect(self) -> bool:
        """建立连接
        
        Returns:
            是否连接成功
        """
        with self.lock:
            if self.status == ConnectionStatus.CONNECTED:
                self.logger.debug("🔗 连接已存在")
                return True
            
            self.logger.info(f"🔗 正在连接到服务器: {self.server_url}")
            self.status = ConnectionStatus.CONNECTING
            self.metrics.total_attempts += 1
            
            try:
                # 这里应该实现实际的连接逻辑
                # 暂时模拟连接过程
                success = self._attempt_connection()
                
                if success:
                    self.status = ConnectionStatus.CONNECTED
                    self.connection_start_time = datetime.now()
                    self.metrics.successful_connections += 1
                    self.metrics.last_connection_time = self.connection_start_time
                    
                    self.logger.success(f"✅ 成功连接到服务器")
                    
                    # 启动健康监控
                    self.start_health_monitoring()
                    
                    # 调用连接成功回调
                    if self.on_connected:
                        self.on_connected()
                    
                    return True
                else:
                    self._handle_connection_failure("连接尝试失败")
                    return False
                    
            except Exception as e:
                self._handle_connection_failure(str(e))
                return False
    
    def _attempt_connection(self) -> bool:
        """尝试连接 - 子类应该重写此方法"""
        # 这里应该实现实际的连接逻辑
        # 暂时模拟成功连接
        time.sleep(0.1)  # 模拟连接延迟
        return True
    
    def disconnect(self):
        """断开连接"""
        with self.lock:
            if self.status == ConnectionStatus.DISCONNECTED:
                return
            
            self.logger.info("🔌 正在断开服务器连接...")
            
            # 停止健康监控
            self.stop_health_monitoring()
            
            # 设置状态
            self.status = ConnectionStatus.DISCONNECTED
            self.connection_start_time = None
            
            # 调用断开连接回调
            if self.on_disconnected:
                self.on_disconnected()
            
            self.logger.info("🔌 服务器连接已断开")
    
    def reconnect(self) -> bool:
        """重新连接
        
        Returns:
            是否重连成功
        """
        with self.lock:
            self.logger.info("🔄 尝试重新连接...")
            self.status = ConnectionStatus.RECONNECTING
            self.metrics.reconnection_attempts += 1
            
            # 先断开现有连接
            self.disconnect()
            
            # 尝试重新连接
            for attempt in range(1, self.max_retries + 1):
                self.logger.info(f"🔄 重连尝试 {attempt}/{self.max_retries}")
                
                if self.connect():
                    self.logger.success("✅ 重连成功")
                    return True
                
                if attempt < self.max_retries:
                    wait_time = min(2 ** attempt, 30)  # 指数退避，最大30秒
                    self.logger.info(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
            
            self.logger.error(f"❌ 重连失败，已尝试 {self.max_retries} 次")
            self.status = ConnectionStatus.FAILED
            return False
    
    def _handle_connection_failure(self, error_message: str):
        """处理连接失败"""
        self.status = ConnectionStatus.FAILED
        self.last_error = error_message
        self.metrics.failed_connections += 1
        self.metrics.last_failure_time = datetime.now()
        
        self.logger.error(f"❌ 连接失败: {error_message}")
        
        # 调用错误回调
        if self.on_error:
            self.on_error(error_message)
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.status == ConnectionStatus.CONNECTED
    
    def get_status(self) -> ConnectionStatus:
        """获取连接状态"""
        return self.status
    
    def get_metrics(self) -> ConnectionMetrics:
        """获取连接指标"""
        return self.metrics
    
    def get_connection_info(self) -> Dict[str, Any]:
        """获取连接信息"""
        uptime = None
        if self.connection_start_time:
            uptime = (datetime.now() - self.connection_start_time).total_seconds()
        
        return {
            'server_url': self.server_url,
            'status': self.status.value,
            'connected': self.is_connected(),
            'uptime_seconds': uptime,
            'last_error': self.last_error,
            'metrics': {
                'total_attempts': self.metrics.total_attempts,
                'successful_connections': self.metrics.successful_connections,
                'failed_connections': self.metrics.failed_connections,
                'reconnection_attempts': self.metrics.reconnection_attempts,
                'success_rate': (self.metrics.successful_connections / max(1, self.metrics.total_attempts)) * 100,
                'last_connection_time': self.metrics.last_connection_time.isoformat() if self.metrics.last_connection_time else None,
                'last_failure_time': self.metrics.last_failure_time.isoformat() if self.metrics.last_failure_time else None
            }
        }
    
    def set_callbacks(self, 
                     on_connected: Optional[Callable] = None,
                     on_disconnected: Optional[Callable] = None,
                     on_error: Optional[Callable] = None):
        """设置回调函数
        
        Args:
            on_connected: 连接成功回调
            on_disconnected: 断开连接回调
            on_error: 错误回调
        """
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_error = on_error
        
        self.logger.debug("🔧 连接回调函数已设置")
    
    def __del__(self):
        """析构函数"""
        try:
            self.stop_health_monitoring()
            self.disconnect()
        except:
            pass