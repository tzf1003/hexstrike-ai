#!/usr/bin/env python3
"""
HexStrike AI - 日志系统配置
Logging System Configuration

这个模块提供了完整的中文化日志系统，包括：
- 彩色日志格式化
- 多级别日志记录
- 文件和控制台输出
- 性能监控日志
- 错误追踪和调试
"""

import logging
import logging.handlers
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any
from .colors import HexStrikeColors

class ChineseColoredFormatter(logging.Formatter):
    """中文化彩色日志格式化器"""
    
    # 中文日志级别映射
    LEVEL_NAMES = {
        'DEBUG': '调试',
        'INFO': '信息',
        'WARNING': '警告',
        'ERROR': '错误',
        'CRITICAL': '严重错误'
    }
    
    # 日志级别颜色映射
    LEVEL_COLORS = {
        'DEBUG': HexStrikeColors.DEBUG,
        'INFO': HexStrikeColors.INFO,
        'WARNING': HexStrikeColors.WARNING,
        'ERROR': HexStrikeColors.ERROR,
        'CRITICAL': HexStrikeColors.CRITICAL
    }
    
    # 日志级别图标
    LEVEL_ICONS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }
    
    def __init__(self, use_colors: bool = True, use_icons: bool = True):
        """初始化格式化器
        
        Args:
            use_colors: 是否使用颜色
            use_icons: 是否使用图标
        """
        super().__init__()
        self.use_colors = use_colors
        self.use_icons = use_icons
        
        # 基础格式
        self.base_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        
        # 详细格式（包含文件和行号）
        self.detailed_format = '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录"""
        # 获取中文级别名称
        chinese_level = self.LEVEL_NAMES.get(record.levelname, record.levelname)
        
        # 添加图标
        if self.use_icons:
            icon = self.LEVEL_ICONS.get(record.levelname, '')
            chinese_level = f"{icon} {chinese_level}"
        
        # 创建新的记录副本以避免修改原记录
        new_record = logging.LogRecord(
            record.name, record.levelno, record.pathname, record.lineno,
            record.msg, record.args, record.exc_info, record.funcName
        )
        
        # 设置中文级别名称
        new_record.levelname = chinese_level
        new_record.created = record.created
        new_record.msecs = record.msecs
        
        # 格式化时间为中文格式
        dt = datetime.fromtimestamp(record.created)
        new_record.asctime = dt.strftime('%Y年%m月%d日 %H:%M:%S')
        
        # 使用基础格式
        formatter = logging.Formatter(self.base_format)
        formatted_message = formatter.format(new_record)
        
        # 添加颜色
        if self.use_colors:
            color = self.LEVEL_COLORS.get(record.levelname, HexStrikeColors.RESET)
            formatted_message = f"{color}{formatted_message}{HexStrikeColors.RESET}"
        
        return formatted_message

class SecurityEventFormatter(logging.Formatter):
    """安全事件专用格式化器"""
    
    def __init__(self):
        super().__init__()
        self.security_format = '%(asctime)s | 🔒 安全事件 | %(levelname)s | %(message)s'
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化安全相关日志"""
        dt = datetime.fromtimestamp(record.created)
        record.asctime = dt.strftime('%Y年%m月%d日 %H:%M:%S')
        
        formatter = logging.Formatter(self.security_format)
        return formatter.format(record)

class PerformanceFormatter(logging.Formatter):
    """性能监控专用格式化器"""
    
    def __init__(self):
        super().__init__()
        self.perf_format = '%(asctime)s | 📊 性能 | %(message)s'
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化性能相关日志"""
        dt = datetime.fromtimestamp(record.created)
        record.asctime = dt.strftime('%Y年%m月%d日 %H:%M:%S')
        
        formatter = logging.Formatter(self.perf_format)
        return formatter.format(record)

class HexStrikeLogger:
    """HexStrike AI 中文化日志管理器"""
    
    def __init__(self, name: str = 'HexStrike'):
        """初始化日志管理器
        
        Args:
            name: 日志器名称
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ChineseColoredFormatter(use_colors=True, use_icons=True)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器（主日志文件）
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                'hexstrike.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = ChineseColoredFormatter(use_colors=False, use_icons=True)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except PermissionError:
            self.logger.warning("⚠️  无法创建日志文件，仅使用控制台输出")
        
        # 错误日志文件处理器
        try:
            error_handler = logging.handlers.RotatingFileHandler(
                'hexstrike_errors.log',
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_formatter = ChineseColoredFormatter(use_colors=False, use_icons=True)
            error_handler.setFormatter(error_formatter)
            self.logger.addHandler(error_handler)
        except PermissionError:
            pass  # 静默处理错误日志文件创建失败
        
        # 安全事件日志处理器
        try:
            security_handler = logging.handlers.RotatingFileHandler(
                'hexstrike_security.log',
                maxBytes=20*1024*1024,  # 20MB
                backupCount=10,
                encoding='utf-8'
            )
            security_handler.setLevel(logging.INFO)
            security_formatter = SecurityEventFormatter()
            security_handler.setFormatter(security_formatter)
            
            # 创建安全日志过滤器
            security_filter = SecurityLogFilter()
            security_handler.addFilter(security_filter)
            
            self.logger.addHandler(security_handler)
        except PermissionError:
            pass
    
    def debug(self, message: str, **kwargs):
        """调试级别日志"""
        self.logger.debug(f"🔍 {message}", **kwargs)
    
    def info(self, message: str, **kwargs):
        """信息级别日志"""
        self.logger.info(f"ℹ️  {message}", **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告级别日志"""
        self.logger.warning(f"⚠️  {message}", **kwargs)
    
    def error(self, message: str, **kwargs):
        """错误级别日志"""
        self.logger.error(f"❌ {message}", **kwargs)
    
    def critical(self, message: str, **kwargs):
        """严重错误级别日志"""
        self.logger.critical(f"🚨 {message}", **kwargs)
    
    def success(self, message: str, **kwargs):
        """成功操作日志"""
        colored_msg = HexStrikeColors.colorize_text(f"✅ {message}", HexStrikeColors.SUCCESS)
        self.logger.info(colored_msg, **kwargs)
    
    def tool_start(self, tool_name: str, target: str = "", **kwargs):
        """工具启动日志"""
        msg = f"🚀 启动安全工具: {tool_name}"
        if target:
            msg += f" | 目标: {target}"
        colored_msg = HexStrikeColors.colorize_text(msg, HexStrikeColors.TOOL_RUNNING)
        self.logger.info(colored_msg, **kwargs)
    
    def tool_success(self, tool_name: str, duration: float = 0, **kwargs):
        """工具成功完成日志"""
        msg = f"✅ 工具执行成功: {tool_name}"
        if duration > 0:
            msg += f" | 耗时: {duration:.2f}秒"
        colored_msg = HexStrikeColors.colorize_text(msg, HexStrikeColors.TOOL_SUCCESS)
        self.logger.info(colored_msg, **kwargs)
    
    def tool_failed(self, tool_name: str, error: str = "", **kwargs):
        """工具执行失败日志"""
        msg = f"❌ 工具执行失败: {tool_name}"
        if error:
            msg += f" | 错误: {error}"
        colored_msg = HexStrikeColors.colorize_text(msg, HexStrikeColors.TOOL_FAILED)
        self.logger.error(colored_msg, **kwargs)
    
    def vulnerability_found(self, severity: str, vuln_type: str, target: str = "", **kwargs):
        """发现漏洞日志"""
        severity_cn = {
            'critical': '严重',
            'high': '高危',
            'medium': '中危',
            'low': '低危',
            'info': '信息'
        }.get(severity.lower(), severity)
        
        msg = f"🎯 发现{severity_cn}漏洞: {vuln_type}"
        if target:
            msg += f" | 目标: {target}"
        
        color = HexStrikeColors.get_vulnerability_color(severity)
        colored_msg = HexStrikeColors.colorize_text(msg, color)
        self.logger.warning(colored_msg, **kwargs)
    
    def ai_decision(self, decision: str, confidence: float = 0, **kwargs):
        """AI决策日志"""
        msg = f"🤖 AI决策: {decision}"
        if confidence > 0:
            msg += f" | 置信度: {confidence:.2f}"
        colored_msg = HexStrikeColors.colorize_text(msg, HexStrikeColors.AI_DECISION)
        self.logger.info(colored_msg, **kwargs)
    
    def performance(self, operation: str, duration: float, **kwargs):
        """性能监控日志"""
        msg = f"📊 性能统计: {operation} | 耗时: {duration:.2f}秒"
        self.logger.info(msg, **kwargs)
    
    def security_event(self, event_type: str, details: str = "", **kwargs):
        """安全事件日志"""
        msg = f"🔒 安全事件: {event_type}"
        if details:
            msg += f" | 详情: {details}"
        colored_msg = HexStrikeColors.colorize_text(msg, HexStrikeColors.HACKER_RED)
        self.logger.warning(colored_msg, **kwargs)

class SecurityLogFilter(logging.Filter):
    """安全日志过滤器 - 仅记录安全相关事件"""
    
    SECURITY_KEYWORDS = [
        '漏洞', '攻击', '入侵', '渗透', '爆破', '注入', 
        '提权', 'exploit', 'vulnerability', 'attack',
        'intrusion', 'penetration', 'injection', 'escalation'
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """过滤安全相关日志"""
        message = str(record.getMessage()).lower()
        return any(keyword.lower() in message for keyword in self.SECURITY_KEYWORDS)

class LoggerConfig:
    """日志配置管理器"""
    
    @staticmethod
    def setup_logging(
        level: str = 'INFO',
        enable_file_logging: bool = True,
        enable_colored_output: bool = True,
        log_file: str = 'hexstrike.log'
    ) -> HexStrikeLogger:
        """设置全局日志配置
        
        Args:
            level: 日志级别
            enable_file_logging: 是否启用文件日志
            enable_colored_output: 是否启用彩色输出
            log_file: 日志文件路径
            
        Returns:
            配置好的日志器实例
        """
        # 设置全局日志级别
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logging.getLogger().setLevel(numeric_level)
        
        # 创建主日志器
        logger = HexStrikeLogger('HexStrike-AI')
        
        # 输出配置信息
        logger.success("🔧 日志系统初始化完成")
        logger.info(f"📝 日志级别: {level}")
        logger.info(f"📁 文件日志: {'启用' if enable_file_logging else '禁用'}")
        logger.info(f"🎨 彩色输出: {'启用' if enable_colored_output else '禁用'}")
        
        return logger
    
    @staticmethod
    def get_log_stats() -> Dict[str, Any]:
        """获取日志统计信息"""
        stats = {
            'log_files': [],
            'total_size': 0,
            'last_modified': None
        }
        
        log_files = ['hexstrike.log', 'hexstrike_errors.log', 'hexstrike_security.log']
        
        for log_file in log_files:
            if os.path.exists(log_file):
                stat = os.stat(log_file)
                stats['log_files'].append({
                    'name': log_file,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
                stats['total_size'] += stat.st_size
                
                if stats['last_modified'] is None or stat.st_mtime > stats['last_modified']:
                    stats['last_modified'] = stat.st_mtime
        
        if stats['last_modified']:
            stats['last_modified'] = datetime.fromtimestamp(stats['last_modified']).strftime('%Y-%m-%d %H:%M:%S')
        
        return stats

# 全局日志器实例
logger = HexStrikeLogger('HexStrike-AI')

def get_logger(name: str = 'HexStrike-AI') -> HexStrikeLogger:
    """获取日志器实例"""
    return HexStrikeLogger(name)

def setup_logging(**kwargs) -> HexStrikeLogger:
    """设置日志系统的便捷函数"""
    return LoggerConfig.setup_logging(**kwargs)