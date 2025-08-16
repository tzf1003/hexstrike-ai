#!/usr/bin/env python3
"""
HexStrike AI - 核心模块
Core Module

这个模块包含了HexStrike AI框架的核心功能组件，包括：
- 进程管理器
- 缓存系统
- 资源监控
- 故障恢复系统
- 基础工具类
"""

from .process_manager import ProcessManager, ProcessStatus
from .cache_system import AdvancedCache, CacheStats
from .resource_monitor import ResourceMonitor, SystemStats
from .failure_recovery import FailureRecoverySystem, RecoveryStrategy
from .base_classes import SecurityTool, ToolResult, ToolStatus

__all__ = [
    'ProcessManager',
    'ProcessStatus', 
    'AdvancedCache',
    'CacheStats',
    'ResourceMonitor',
    'SystemStats',
    'FailureRecoverySystem',
    'RecoveryStrategy',
    'SecurityTool',
    'ToolResult',
    'ToolStatus'
]