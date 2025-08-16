#!/usr/bin/env python3
"""
HexStrike AI - MCP客户端模块
MCP Client Module

这个模块包含了MCP客户端的核心功能，包括：
- HexStrike API服务器通信
- 请求重试和错误恢复
- 中文化的状态报告
"""

from .hexstrike_client import HexStrikeMCPClient
from .connection_manager import ConnectionManager

__all__ = [
    'HexStrikeMCPClient', 
    'ConnectionManager'
]