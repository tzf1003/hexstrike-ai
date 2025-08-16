#!/usr/bin/env python3
"""
HexStrike AI - MCP (模型上下文协议) 模块
MCP (Model Context Protocol) Module

这个模块包含了HexStrike AI框架的MCP客户端功能，包括：
- AI代理通信接口
- FastMCP服务器集成
- 安全工具函数暴露
- 智能工作流管理
- 中文化的日志和错误处理
"""

from .client import HexStrikeMCPClient
from .server import create_mcp_server, MCPServerManager
from .tools import MCPToolsManager

__all__ = [
    'HexStrikeMCPClient',
    'create_mcp_server',
    'MCPServerManager',
    'MCPToolsManager'
]

# MCP模块版本信息
MCP_VERSION = "6.0.0"
MCP_DESCRIPTION = "HexStrike AI MCP客户端 - AI代理通信接口"

# MCP配置信息
MCP_CONFIG = {
    'name': 'hexstrike-ai-mcp',
    'version': MCP_VERSION,
    'description': MCP_DESCRIPTION,
    'default_server_url': 'http://127.0.0.1:8888',
    'default_timeout': 300,
    'max_retries': 3,
    'supported_protocols': ['mcp/1.0'],
    'capabilities': [
        'tools',  # 工具执行能力
        'prompts',  # 提示词管理
        'resources',  # 资源访问
        'logging'  # 日志记录
    ]
}

def get_mcp_info():
    """获取MCP模块信息"""
    return MCP_CONFIG