#!/usr/bin/env python3
"""
HexStrike AI - 资源监控器
Resource Monitor

这个模块提供了系统资源监控功能，包括：
- CPU和内存使用率监控
- 磁盘空间监控
- 网络IO监控
- 性能统计分析
"""

import psutil
import threading
import time
from datetime import datetime
from typing import Dict, List

from .base_classes import SystemStats
from ..config.logger_config import get_logger

class ResourceMonitor:
    """系统资源监控器"""
    
    def __init__(self, interval: int = 5):
        """初始化资源监控器
        
        Args:
            interval: 监控间隔（秒）
        """
        self.interval = interval
        self.monitoring = False
        self.monitor_thread = None
        self.current_stats = SystemStats()
        self.history: List[SystemStats] = []
        self.max_history = 100  # 保持最近100个记录
        self.logger = get_logger('ResourceMonitor')
        
        # 启动监控
        self.start_monitoring()
    
    def start_monitoring(self):
        """启动监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.logger.success(f"📊 资源监控器启动 (间隔: {self.interval}秒)")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("📊 资源监控器已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                self._collect_stats()
                time.sleep(self.interval)
            except Exception as e:
                self.logger.error(f"❌ 资源监控错误: {e}")
                time.sleep(self.interval)
    
    def _collect_stats(self):
        """收集系统统计信息"""
        try:
            # CPU使用率
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # 网络IO
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # 活跃进程数
            active_processes = len(psutil.pids())
            
            # 创建统计对象
            stats = SystemStats(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                active_processes=active_processes,
                timestamp=datetime.now()
            )
            
            self.current_stats = stats
            
            # 添加到历史记录
            self.history.append(stats)
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            # 记录警告级别的资源使用
            if cpu_usage > 80:
                self.logger.warning(f"⚠️  CPU使用率较高: {cpu_usage:.1f}%")
            
            if memory_usage > 85:
                self.logger.warning(f"⚠️  内存使用率较高: {memory_usage:.1f}%")
            
            if disk_usage > 90:
                self.logger.warning(f"⚠️  磁盘使用率较高: {disk_usage:.1f}%")
                
        except Exception as e:
            self.logger.error(f"❌ 收集系统统计信息失败: {e}")
    
    def get_current_stats(self) -> SystemStats:
        """获取当前统计信息"""
        return self.current_stats
    
    def get_average_stats(self, minutes: int = 5) -> Dict[str, float]:
        """获取平均统计信息
        
        Args:
            minutes: 统计的分钟数
            
        Returns:
            平均统计信息
        """
        if not self.history:
            return {}
        
        # 计算需要的记录数
        records_needed = min(minutes * 60 // self.interval, len(self.history))
        recent_stats = self.history[-records_needed:] if records_needed > 0 else self.history
        
        if not recent_stats:
            return {}
        
        # 计算平均值
        avg_cpu = sum(s.cpu_usage for s in recent_stats) / len(recent_stats)
        avg_memory = sum(s.memory_usage for s in recent_stats) / len(recent_stats)
        avg_disk = sum(s.disk_usage for s in recent_stats) / len(recent_stats)
        avg_processes = sum(s.active_processes for s in recent_stats) / len(recent_stats)
        
        return {
            'cpu_usage': round(avg_cpu, 2),
            'memory_usage': round(avg_memory, 2),
            'disk_usage': round(avg_disk, 2),
            'active_processes': round(avg_processes, 0),
            'sample_count': len(recent_stats),
            'time_range_minutes': minutes
        }
    
    def get_peak_stats(self) -> Dict[str, float]:
        """获取峰值统计信息"""
        if not self.history:
            return {}
        
        return {
            'max_cpu': max(s.cpu_usage for s in self.history),
            'max_memory': max(s.memory_usage for s in self.history),
            'max_disk': max(s.disk_usage for s in self.history),
            'max_processes': max(s.active_processes for s in self.history)
        }
    
    def is_system_overloaded(self) -> bool:
        """检查系统是否过载"""
        stats = self.current_stats
        return (stats.cpu_usage > 90 or 
                stats.memory_usage > 95 or 
                stats.disk_usage > 95)