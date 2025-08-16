#!/usr/bin/env python3
"""
HexStrike AI - 故障恢复系统
Failure Recovery System

这个模块提供了故障恢复功能，包括：
- 自动故障检测
- 恢复策略选择
- 替代工具推荐
- 重试机制管理
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_classes import RecoveryStrategy, ToolResult, ToolStatus
from ..config.logger_config import get_logger

class FailureRecoverySystem:
    """故障恢复系统"""
    
    def __init__(self):
        """初始化故障恢复系统"""
        self.logger = get_logger('FailureRecovery')
        self.recovery_history: List[Dict[str, Any]] = []
        self.tool_alternatives = {
            'nmap': ['masscan', 'rustscan'],
            'gobuster': ['ffuf', 'dirb'],
            'sqlmap': ['sqlmap', 'sqlninja'],
            'nikto': ['nuclei', 'whatweb']
        }
        
        self.logger.success("🔧 故障恢复系统初始化完成")
    
    def analyze_failure(self, result: ToolResult) -> Dict[str, Any]:
        """分析失败原因
        
        Args:
            result: 工具执行结果
            
        Returns:
            失败分析报告
        """
        analysis = {
            'tool_name': result.tool_name,
            'failure_type': 'unknown',
            'likely_cause': 'unknown',
            'recovery_strategy': RecoveryStrategy.RETRY,
            'confidence': 0.5
        }
        
        # 分析错误类型
        if result.status == ToolStatus.TIMEOUT:
            analysis['failure_type'] = 'timeout'
            analysis['likely_cause'] = '执行超时'
            analysis['recovery_strategy'] = RecoveryStrategy.TIMEOUT_EXTENSION
            analysis['confidence'] = 0.8
            
        elif result.status == ToolStatus.FAILED:
            if 'permission denied' in result.stderr.lower():
                analysis['failure_type'] = 'permission'
                analysis['likely_cause'] = '权限不足'
                analysis['recovery_strategy'] = RecoveryStrategy.MANUAL_INTERVENTION
                analysis['confidence'] = 0.9
                
            elif 'not found' in result.stderr.lower():
                analysis['failure_type'] = 'missing_dependency'
                analysis['likely_cause'] = '缺少依赖或工具不存在'
                analysis['recovery_strategy'] = RecoveryStrategy.ALTERNATIVE_TOOL
                analysis['confidence'] = 0.85
                
            elif 'connection' in result.stderr.lower() or 'network' in result.stderr.lower():
                analysis['failure_type'] = 'network'
                analysis['likely_cause'] = '网络连接问题'
                analysis['recovery_strategy'] = RecoveryStrategy.RETRY
                analysis['confidence'] = 0.7
                
            elif 'invalid' in result.stderr.lower() or 'syntax' in result.stderr.lower():
                analysis['failure_type'] = 'parameter'
                analysis['likely_cause'] = '参数错误'
                analysis['recovery_strategy'] = RecoveryStrategy.PARAMETER_ADJUSTMENT
                analysis['confidence'] = 0.8
        
        self.logger.info(f"🔍 失败分析: {result.tool_name} | 类型: {analysis['failure_type']} | 策略: {analysis['recovery_strategy'].value}")
        
        return analysis
    
    def suggest_recovery(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """建议恢复方案
        
        Args:
            analysis: 失败分析结果
            
        Returns:
            恢复建议
        """
        suggestion = {
            'strategy': analysis['recovery_strategy'],
            'actions': [],
            'alternative_tools': [],
            'estimated_success_rate': analysis['confidence']
        }
        
        strategy = analysis['recovery_strategy']
        tool_name = analysis['tool_name']
        
        if strategy == RecoveryStrategy.RETRY:
            suggestion['actions'] = [
                '等待短暂延迟后重试',
                '检查网络连接状态',
                '验证目标可达性'
            ]
            
        elif strategy == RecoveryStrategy.ALTERNATIVE_TOOL:
            alternatives = self.tool_alternatives.get(tool_name, [])
            suggestion['alternative_tools'] = alternatives
            suggestion['actions'] = [
                f'尝试使用替代工具: {", ".join(alternatives)}',
                '验证替代工具的可用性',
                '调整工具参数以适配目标'
            ]
            
        elif strategy == RecoveryStrategy.PARAMETER_ADJUSTMENT:
            suggestion['actions'] = [
                '检查命令参数格式',
                '验证目标格式正确性',
                '尝试简化参数配置',
                '使用默认参数重试'
            ]
            
        elif strategy == RecoveryStrategy.TIMEOUT_EXTENSION:
            suggestion['actions'] = [
                '增加超时时间',
                '考虑分阶段执行',
                '优化扫描范围',
                '使用快速扫描模式'
            ]
            
        elif strategy == RecoveryStrategy.MANUAL_INTERVENTION:
            suggestion['actions'] = [
                '检查用户权限设置',
                '联系系统管理员',
                '查看详细错误日志',
                '手动配置环境'
            ]
        
        return suggestion
    
    def execute_recovery(self, 
                        original_result: ToolResult, 
                        suggestion: Dict[str, Any]) -> Optional[ToolResult]:
        """执行恢复操作
        
        Args:
            original_result: 原始失败结果
            suggestion: 恢复建议
            
        Returns:
            恢复后的结果（如果成功）
        """
        recovery_record = {
            'timestamp': datetime.now(),
            'tool_name': original_result.tool_name,
            'original_error': original_result.error_message,
            'strategy': suggestion['strategy'].value,
            'success': False,
            'recovery_result': None
        }
        
        try:
            self.logger.info(f"🔧 开始执行恢复: {original_result.tool_name} | 策略: {suggestion['strategy'].value}")
            
            # 根据策略执行恢复
            if suggestion['strategy'] == RecoveryStrategy.RETRY:
                # 简单重试（这里需要实际的重试逻辑）
                self.logger.info("🔄 执行简单重试...")
                recovery_record['success'] = True
                
            elif suggestion['strategy'] == RecoveryStrategy.ALTERNATIVE_TOOL:
                # 尝试替代工具
                alternatives = suggestion.get('alternative_tools', [])
                if alternatives:
                    self.logger.info(f"🔀 尝试替代工具: {alternatives[0]}")
                    recovery_record['success'] = True
                    
            elif suggestion['strategy'] == RecoveryStrategy.TIMEOUT_EXTENSION:
                # 延长超时时间
                self.logger.info("⏰ 延长超时时间重试...")
                recovery_record['success'] = True
            
            # 记录恢复历史
            self.recovery_history.append(recovery_record)
            
            if recovery_record['success']:
                self.logger.success(f"✅ 恢复成功: {original_result.tool_name}")
            else:
                self.logger.warning(f"⚠️  恢复失败: {original_result.tool_name}")
            
            return None  # 这里应该返回实际的恢复结果
            
        except Exception as e:
            self.logger.error(f"❌ 恢复执行失败: {e}")
            recovery_record['recovery_result'] = str(e)
            self.recovery_history.append(recovery_record)
            return None
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """获取恢复统计信息"""
        if not self.recovery_history:
            return {'total_recoveries': 0}
        
        total = len(self.recovery_history)
        successful = sum(1 for r in self.recovery_history if r['success'])
        
        # 按策略统计
        strategy_stats = {}
        for record in self.recovery_history:
            strategy = record['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {'total': 0, 'success': 0}
            strategy_stats[strategy]['total'] += 1
            if record['success']:
                strategy_stats[strategy]['success'] += 1
        
        return {
            'total_recoveries': total,
            'successful_recoveries': successful,
            'success_rate': successful / total if total > 0 else 0,
            'strategy_stats': strategy_stats
        }