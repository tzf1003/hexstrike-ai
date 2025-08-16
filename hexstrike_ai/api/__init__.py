#!/usr/bin/env python3
"""
HexStrike AI - API服务器模块
API Server Module

这个模块包含了HexStrike AI框架的Web API服务器相关功能，包括：
- Flask应用创建和配置
- REST API端点定义
- 请求处理和响应格式化
- 认证和安全控制
"""

from .server import create_flask_app, HexStrikeAPI
from .routes import register_routes

__all__ = [
    'create_flask_app',
    'HexStrikeAPI',
    'register_routes'
]