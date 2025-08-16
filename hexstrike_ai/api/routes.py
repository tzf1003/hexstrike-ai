#!/usr/bin/env python3
"""
HexStrike AI - API路由定义
API Routes Definition

这个模块定义了HexStrike AI框架的所有API路由，包括：
- 工具执行相关路由
- 进程管理路由
- AI智能分析路由
- 系统管理路由
"""

from flask import request
from ..config.logger_config import get_logger

logger = get_logger('API-Routes')

def register_routes(app, api):
    """注册所有API路由
    
    Args:
        app: Flask应用实例
        api: HexStrike API管理器实例
    """
    
    # 工具相关路由
    @app.route('/api/tools/status', methods=['GET'])
    @api.log_request
    def get_tools_status():
        """获取所有工具状态"""
        if not api.tools_manager:
            return api.create_response(
                success=False,
                message="工具管理器未初始化",
                status_code=503
            )
        
        try:
            status = api.tools_manager.get_all_tools_status()
            return api.create_response(
                success=True,
                message="工具状态获取成功",
                data=status
            )
        except Exception as e:
            return api.create_response(
                success=False,
                message=f"获取工具状态失败: {e}",
                status_code=500
            )
    
    @app.route('/api/command', methods=['POST'])
    @api.log_request
    @api.require_auth
    def execute_command():
        """执行命令"""
        if not api.process_manager:
            return api.create_response(
                success=False,
                message="进程管理器未初始化",
                status_code=503
            )
        
        try:
            data = request.get_json()
            if not data or 'command' not in data:
                return api.create_response(
                    success=False,
                    message="缺少必需的参数: command",
                    status_code=400
                )
            
            command = data['command']
            timeout = data.get('timeout', 300)
            
            logger.info(f"🚀 执行命令请求: {command}")
            
            result = api.process_manager.execute_command(command, timeout=timeout)
            
            return api.create_response(
                success=True,
                message="命令执行完成",
                data=result
            )
            
        except Exception as e:
            return api.create_response(
                success=False,
                message=f"命令执行失败: {e}",
                status_code=500
            )
    
    @app.route('/api/processes/status', methods=['GET'])
    @api.log_request
    def get_processes_status():
        """获取进程状态"""
        if not api.process_manager:
            return api.create_response(
                success=False,
                message="进程管理器未初始化",
                status_code=503
            )
        
        try:
            processes = api.process_manager.get_all_processes()
            process_info = []
            
            for process in processes:
                process_info.append({
                    'pid': process.pid,
                    'command': process.command,
                    'status': process.status.value,
                    'start_time': process.start_time.isoformat(),
                    'duration': process.duration,
                    'cpu_usage': process.cpu_usage,
                    'memory_usage': process.memory_usage
                })
            
            return api.create_response(
                success=True,
                message="进程状态获取成功",
                data={'processes': process_info}
            )
            
        except Exception as e:
            return api.create_response(
                success=False,
                message=f"获取进程状态失败: {e}",
                status_code=500
            )
    
    @app.route('/api/intelligence/analyze-target', methods=['POST'])
    @api.log_request
    @api.require_auth
    def analyze_target():
        """AI目标分析"""
        if not api.decision_engine:
            return api.create_response(
                success=False,
                message="AI决策引擎未启用",
                status_code=503
            )
        
        try:
            data = request.get_json()
            if not data or 'target' not in data:
                return api.create_response(
                    success=False,
                    message="缺少必需的参数: target",
                    status_code=400
                )
            
            target = data['target']
            analysis_type = data.get('analysis_type', 'basic')
            
            # 验证目标
            if not api.validate_target(target):
                return api.create_response(
                    success=False,
                    message="目标地址不合法或被禁止",
                    status_code=400
                )
            
            logger.info(f"🧠 AI目标分析请求: {target} (类型: {analysis_type})")
            
            # 这里应该调用AI决策引擎进行分析
            # 暂时返回模拟结果
            analysis_result = {
                'target': target,
                'analysis_type': analysis_type,
                'risk_level': 'medium',
                'recommended_tools': ['nmap', 'nuclei'],
                'confidence': 0.85,
                'estimated_scan_time': '15-30分钟'
            }
            
            return api.create_response(
                success=True,
                message="AI目标分析完成",
                data=analysis_result
            )
            
        except Exception as e:
            return api.create_response(
                success=False,
                message=f"AI目标分析失败: {e}",
                status_code=500
            )
    
    logger.success("🛣️  所有API路由注册完成")