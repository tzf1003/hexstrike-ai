#!/usr/bin/env python3
"""
HexStrike AI - Flask API服务器
Flask API Server

这个模块提供了HexStrike AI的Web API服务器实现，包括：
- Flask应用创建和配置
- 中间件和错误处理
- 安全控制和访问控制
- API响应格式统一
"""

import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps

from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException

from ..config.logger_config import get_logger
from ..config.colors import HexStrikeColors

class HexStrikeAPI:
    """HexStrike AI API管理器"""
    
    def __init__(self, 
                 config=None,
                 process_manager=None,
                 cache_system=None,
                 resource_monitor=None,
                 tools_manager=None,
                 decision_engine=None):
        """初始化API管理器"""
        self.config = config
        self.process_manager = process_manager
        self.cache_system = cache_system
        self.resource_monitor = resource_monitor
        self.tools_manager = tools_manager
        self.decision_engine = decision_engine
        self.logger = get_logger('HexStrike-API')
        
        # 统计信息
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'start_time': datetime.now()
        }
    
    def create_response(self, 
                       success: bool = True, 
                       message: str = "",
                       data: Any = None,
                       error_code: str = None,
                       status_code: int = 200) -> tuple:
        """创建标准API响应
        
        Args:
            success: 是否成功
            message: 响应消息
            data: 响应数据
            error_code: 错误代码
            status_code: HTTP状态码
            
        Returns:
            (响应字典, HTTP状态码)
        """
        response = {
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        if not success and error_code:
            response['error_code'] = error_code
        
        # 更新统计
        if success:
            self.stats['requests_success'] += 1
        else:
            self.stats['requests_error'] += 1
        
        return jsonify(response), status_code
    
    def require_auth(self, f):
        """认证装饰器"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.config or not self.config.security.require_authorization:
                return f(*args, **kwargs)
            
            # 检查API密钥
            api_key = request.headers.get(self.config.security.api_key_header)
            if not api_key:
                self.logger.warning("❌ 缺少API密钥的访问尝试")
                return self.create_response(
                    success=False,
                    message="缺少API密钥",
                    error_code="AUTH_MISSING_KEY",
                    status_code=401
                )
            
            # 这里可以添加API密钥验证逻辑
            # 暂时允许所有带密钥的请求
            
            return f(*args, **kwargs)
        return decorated_function
    
    def log_request(self, f):
        """请求日志装饰器"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 记录请求开始
            start_time = datetime.now()
            client_ip = request.remote_addr
            method = request.method
            path = request.path
            
            self.logger.info(f"📨 API请求: {method} {path} | 客户端: {client_ip}")
            
            # 更新统计
            self.stats['requests_total'] += 1
            
            try:
                # 执行请求
                result = f(*args, **kwargs)
                
                # 记录请求完成
                duration = (datetime.now() - start_time).total_seconds()
                self.logger.success(f"✅ API响应: {method} {path} | 耗时: {duration:.3f}秒")
                
                return result
                
            except Exception as e:
                # 记录请求错误
                duration = (datetime.now() - start_time).total_seconds()
                self.logger.error(f"❌ API错误: {method} {path} | 错误: {e} | 耗时: {duration:.3f}秒")
                raise
        
        return decorated_function
    
    def validate_target(self, target: str) -> bool:
        """验证目标地址是否合法"""
        if not target or not target.strip():
            return False
        
        # 检查是否在阻止列表中
        if (self.config and 
            self.config.security.blocked_targets and
            any(blocked in target.lower() for blocked in self.config.security.blocked_targets)):
            return False
        
        # 检查是否在允许列表中（如果设置了允许列表）
        if (self.config and 
            self.config.security.allowed_targets and
            not any(allowed in target.lower() for allowed in self.config.security.allowed_targets)):
            return False
        
        return True
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        status = {
            'service': 'HexStrike AI API',
            'version': '6.0.0',
            'status': 'running',
            'uptime': str(datetime.now() - self.stats['start_time']),
            'stats': self.stats.copy()
        }
        
        # 添加组件状态
        if self.process_manager:
            process_stats = self.process_manager.get_process_count()
            status['processes'] = process_stats
        
        if self.cache_system:
            cache_stats = self.cache_system.get_stats()
            status['cache'] = {
                'enabled': True,
                'entries': cache_stats.total_entries,
                'hit_rate': cache_stats.hit_rate,
                'memory_usage_mb': cache_stats.memory_usage / 1024 / 1024
            }
        else:
            status['cache'] = {'enabled': False}
        
        if self.resource_monitor:
            resource_stats = self.resource_monitor.get_current_stats()
            status['resources'] = {
                'cpu_usage': resource_stats.cpu_usage,
                'memory_usage': resource_stats.memory_usage,
                'disk_usage': resource_stats.disk_usage
            }
        
        if self.tools_manager:
            tool_stats = self.tools_manager.get_tools_summary()
            status['tools'] = tool_stats
        
        if self.decision_engine:
            ai_stats = self.decision_engine.get_stats()
            status['ai_engine'] = {
                'enabled': True,
                'decisions_made': ai_stats.get('decisions_made', 0),
                'average_confidence': ai_stats.get('average_confidence', 0)
            }
        else:
            status['ai_engine'] = {'enabled': False}
        
        return status

def create_flask_app(config=None,
                    process_manager=None,
                    cache_system=None,
                    resource_monitor=None,
                    tools_manager=None,
                    decision_engine=None) -> Flask:
    """创建Flask应用实例
    
    Args:
        config: 配置对象
        process_manager: 进程管理器
        cache_system: 缓存系统
        resource_monitor: 资源监控器
        tools_manager: 工具管理器
        decision_engine: AI决策引擎
        
    Returns:
        配置好的Flask应用实例
    """
    app = Flask(__name__)
    
    # 基础配置
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_AS_ASCII'] = False  # 支持中文字符
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    if config:
        app.config['MAX_CONTENT_LENGTH'] = config.server.max_request_size
    
    # 创建API管理器
    api = HexStrikeAPI(
        config=config,
        process_manager=process_manager,
        cache_system=cache_system,
        resource_monitor=resource_monitor,
        tools_manager=tools_manager,
        decision_engine=decision_engine
    )
    
    # 将API管理器附加到应用
    app.hexstrike_api = api
    
    # 注册错误处理器
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """HTTP异常处理器"""
        return api.create_response(
            success=False,
            message=f"HTTP错误: {e.description}",
            error_code=f"HTTP_{e.code}",
            status_code=e.code
        )
    
    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """通用异常处理器"""
        error_msg = str(e)
        api.logger.error(f"❌ 未处理的异常: {error_msg}")
        api.logger.debug(f"异常详情: {traceback.format_exc()}")
        
        return api.create_response(
            success=False,
            message=f"内部服务器错误: {error_msg}",
            error_code="INTERNAL_ERROR",
            status_code=500
        )
    
    # 请求预处理
    @app.before_request
    def before_request():
        """请求预处理"""
        g.start_time = datetime.now()
        g.client_ip = request.remote_addr
    
    # 响应后处理
    @app.after_request
    def after_request(response):
        """响应后处理"""
        # 添加CORS头
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-HexStrike-API-Key'
        
        # 添加安全头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 添加服务器信息
        response.headers['X-Powered-By'] = 'HexStrike AI v6.0'
        
        return response
    
    # 注册基础路由
    @app.route('/health', methods=['GET'])
    @api.log_request
    def health_check():
        """健康检查端点"""
        status = api.get_system_status()
        return api.create_response(
            success=True,
            message="服务器运行正常",
            data=status
        )
    
    @app.route('/version', methods=['GET'])
    @api.log_request
    def version_info():
        """版本信息端点"""
        from hexstrike_ai import get_version_info
        version = get_version_info()
        return api.create_response(
            success=True,
            message="版本信息",
            data=version
        )
    
    @app.route('/stats', methods=['GET'])
    @api.log_request
    def get_stats():
        """统计信息端点"""
        stats = api.get_system_status()
        return api.create_response(
            success=True,
            message="系统统计信息",
            data=stats
        )
    
    # 注册主要路由
    from .routes import register_routes
    register_routes(app, api)
    
    api.logger.success("🌐 Flask API服务器创建完成")
    
    return app