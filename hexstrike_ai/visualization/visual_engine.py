#!/usr/bin/env python3
"""
HexStrike AI - 现代化可视化引擎
Modern Visual Engine

这个模块提供了美观的终端输出功能，包括：
- 红色黑客主题的终端界面
- 实时进度条和状态显示
- 彩色格式化输出
- 表格和横幅显示
"""

import sys
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import shutil

from ..config.colors import HexStrikeColors
from ..config.logger_config import get_logger

class ProgressBar:
    """现代化进度条类"""
    
    def __init__(self, 
                 total: int, 
                 title: str = "进度",
                 width: int = 40,
                 show_eta: bool = True,
                 show_percent: bool = True):
        """初始化进度条
        
        Args:
            total: 总数量
            title: 进度条标题
            width: 进度条宽度
            show_eta: 是否显示预计完成时间
            show_percent: 是否显示百分比
        """
        self.total = total
        self.current = 0
        self.title = title
        self.width = width
        self.show_eta = show_eta
        self.show_percent = show_percent
        self.start_time = datetime.now()
        self.last_update = self.start_time
        
    def update(self, amount: int = 1, message: str = ""):
        """更新进度
        
        Args:
            amount: 增加的数量
            message: 显示的消息
        """
        self.current += amount
        if self.current > self.total:
            self.current = self.total
            
        self._render(message)
    
    def set_progress(self, current: int, message: str = ""):
        """设置当前进度
        
        Args:
            current: 当前数量
            message: 显示的消息
        """
        self.current = current
        if self.current > self.total:
            self.current = self.total
            
        self._render(message)
    
    def _render(self, message: str = ""):
        """渲染进度条"""
        now = datetime.now()
        elapsed = (now - self.start_time).total_seconds()
        
        # 计算百分比
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        
        # 计算预计完成时间
        eta_str = ""
        if self.show_eta and self.current > 0 and elapsed > 0:
            rate = self.current / elapsed
            if rate > 0:
                remaining = (self.total - self.current) / rate
                eta = now + timedelta(seconds=remaining)
                eta_str = f" | ETA: {eta.strftime('%H:%M:%S')}"
        
        # 构建进度条
        filled = int((self.current / self.total) * self.width) if self.total > 0 else 0
        bar = "█" * filled + "░" * (self.width - filled)
        
        # 构建显示文本
        percent_str = f" {percent:6.1f}%" if self.show_percent else ""
        count_str = f" [{self.current}/{self.total}]"
        message_str = f" | {message}" if message else ""
        
        # 输出进度条
        output = (
            f"\r{HexStrikeColors.NEON_BLUE}{self.title}:{HexStrikeColors.RESET} "
            f"{HexStrikeColors.PROGRESS_BAR}[{bar}]{HexStrikeColors.RESET}"
            f"{HexStrikeColors.PROGRESS_PERCENT}{percent_str}{HexStrikeColors.RESET}"
            f"{count_str}"
            f"{HexStrikeColors.PROGRESS_ETA}{eta_str}{HexStrikeColors.RESET}"
            f"{message_str}"
        )
        
        print(output, end="", flush=True)
        
        # 如果完成，换行
        if self.current >= self.total:
            print()
    
    def finish(self, message: str = "完成"):
        """完成进度条"""
        self.current = self.total
        self._render(message)

class StatusDisplay:
    """状态显示类"""
    
    def __init__(self):
        self.logger = get_logger('StatusDisplay')
    
    def show_banner(self, title: str, subtitle: str = "", width: int = 80):
        """显示横幅
        
        Args:
            title: 主标题
            subtitle: 副标题
            width: 横幅宽度
        """
        # 计算居中位置
        title_padding = (width - len(title) - 4) // 2
        subtitle_padding = (width - len(subtitle) - 4) // 2 if subtitle else 0
        
        # 构建横幅
        border = "═" * width
        empty_line = "║" + " " * (width - 2) + "║"
        title_line = "║" + " " * title_padding + title + " " * (width - len(title) - title_padding - 2) + "║"
        
        print(f"{HexStrikeColors.BANNER_BORDER}╔{border}╗{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.BANNER_BORDER}{empty_line}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.BANNER_BORDER}║{HexStrikeColors.BANNER_TITLE}{' ' * title_padding}{title}{' ' * (width - len(title) - title_padding - 2)}{HexStrikeColors.BANNER_BORDER}║{HexStrikeColors.RESET}")
        
        if subtitle:
            subtitle_line = "║" + " " * subtitle_padding + subtitle + " " * (width - len(subtitle) - subtitle_padding - 2) + "║"
            print(f"{HexStrikeColors.BANNER_BORDER}║{HexStrikeColors.BANNER_SUBTITLE}{' ' * subtitle_padding}{subtitle}{' ' * (width - len(subtitle) - subtitle_padding - 2)}{HexStrikeColors.BANNER_BORDER}║{HexStrikeColors.RESET}")
        
        print(f"{HexStrikeColors.BANNER_BORDER}{empty_line}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.BANNER_BORDER}╚{border}╝{HexStrikeColors.RESET}")
    
    def show_table(self, 
                   headers: List[str], 
                   rows: List[List[str]], 
                   title: str = "",
                   max_width: int = 120):
        """显示表格
        
        Args:
            headers: 表头列表
            rows: 数据行列表
            title: 表格标题
            max_width: 最大宽度
        """
        if not headers or not rows:
            return
        
        # 计算列宽
        col_widths = []
        for i, header in enumerate(headers):
            max_width_col = len(header)
            for row in rows:
                if i < len(row):
                    max_width_col = max(max_width_col, len(str(row[i])))
            col_widths.append(min(max_width_col + 2, max_width // len(headers)))
        
        # 显示标题
        if title:
            print(f"\n{HexStrikeColors.BANNER_TITLE}📊 {title}{HexStrikeColors.RESET}")
            print(f"{HexStrikeColors.SEPARATOR}{'─' * sum(col_widths)}{HexStrikeColors.RESET}")
        
        # 显示表头
        header_line = ""
        for i, header in enumerate(headers):
            header_line += f"{HexStrikeColors.NEON_BLUE}{header:<{col_widths[i]}}{HexStrikeColors.RESET}"
        print(header_line)
        
        # 显示分隔线
        separator = ""
        for width in col_widths:
            separator += "─" * width
        print(f"{HexStrikeColors.TERMINAL_GRAY}{separator}{HexStrikeColors.RESET}")
        
        # 显示数据行
        for row in rows:
            row_line = ""
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    cell_str = str(cell)[:col_widths[i]-1]
                    row_line += f"{cell_str:<{col_widths[i]}}"
            print(row_line)
    
    def show_status_grid(self, 
                        items: List[Dict[str, Any]], 
                        title: str = "状态概览",
                        columns: int = 4):
        """显示状态网格
        
        Args:
            items: 状态项列表
            title: 网格标题
            columns: 列数
        """
        if not items:
            return
        
        print(f"\n{HexStrikeColors.BANNER_TITLE}📋 {title}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.SEPARATOR}{'─' * 60}{HexStrikeColors.RESET}")
        
        # 按列排列项目
        rows = []
        for i in range(0, len(items), columns):
            rows.append(items[i:i+columns])
        
        for row in rows:
            line = ""
            for item in row:
                name = item.get('name', '未知')
                status = item.get('status', '未知')
                icon = item.get('icon', '●')
                
                # 根据状态选择颜色
                color = self._get_status_color(status)
                
                item_str = f"{color}{icon} {name}: {status}{HexStrikeColors.RESET}"
                line += f"{item_str:<30}"
            
            print(line)
    
    def _get_status_color(self, status: str) -> str:
        """根据状态获取颜色"""
        status_colors = {
            '运行中': HexStrikeColors.TOOL_RUNNING,
            '成功': HexStrikeColors.TOOL_SUCCESS,
            '完成': HexStrikeColors.TOOL_SUCCESS,
            '失败': HexStrikeColors.TOOL_FAILED,
            '错误': HexStrikeColors.TOOL_FAILED,
            '超时': HexStrikeColors.TOOL_TIMEOUT,
            '等待': HexStrikeColors.TOOL_PENDING,
            '取消': HexStrikeColors.TOOL_CANCELLED,
            '可用': HexStrikeColors.SUCCESS,
            '不可用': HexStrikeColors.ERROR
        }
        
        return status_colors.get(status, HexStrikeColors.INFO)
    
    def show_vulnerability_summary(self, vulnerabilities: List[Dict[str, Any]]):
        """显示漏洞摘要
        
        Args:
            vulnerabilities: 漏洞列表
        """
        if not vulnerabilities:
            print(f"{HexStrikeColors.SUCCESS}✅ 未发现安全漏洞{HexStrikeColors.RESET}")
            return
        
        # 统计漏洞严重性
        severity_count = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'info').lower()
            if severity in severity_count:
                severity_count[severity] += 1
        
        print(f"\n{HexStrikeColors.BANNER_TITLE}🎯 漏洞发现摘要{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.SEPARATOR}{'─' * 50}{HexStrikeColors.RESET}")
        
        # 显示统计
        total = len(vulnerabilities)
        print(f"总计发现漏洞: {HexStrikeColors.HACKER_RED}{total}{HexStrikeColors.RESET} 个")
        
        severity_labels = {
            'critical': '严重',
            'high': '高危',
            'medium': '中危', 
            'low': '低危',
            'info': '信息'
        }
        
        for severity, count in severity_count.items():
            if count > 0:
                color = HexStrikeColors.get_vulnerability_color(severity)
                label = severity_labels[severity]
                print(f"  {color}● {label}: {count} 个{HexStrikeColors.RESET}")

class ModernVisualEngine:
    """现代化可视化引擎"""
    
    def __init__(self):
        """初始化可视化引擎"""
        self.logger = get_logger('VisualEngine')
        self.terminal_width = self._get_terminal_width()
        self.status_display = StatusDisplay()
        
        # 启动消息
        self.logger.info("🎨 现代化可视化引擎已启动")
    
    def _get_terminal_width(self) -> int:
        """获取终端宽度"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80  # 默认宽度
    
    def create_progress_bar(self, 
                           total: int, 
                           title: str = "进度",
                           **kwargs) -> ProgressBar:
        """创建进度条
        
        Args:
            total: 总数量
            title: 进度条标题
            **kwargs: 其他参数
            
        Returns:
            进度条实例
        """
        return ProgressBar(total, title, **kwargs)
    
    def print_header(self, text: str, level: int = 1):
        """打印标题
        
        Args:
            text: 标题文本
            level: 标题级别 (1-3)
        """
        colors = [
            HexStrikeColors.BANNER_TITLE,
            HexStrikeColors.HACKER_RED,
            HexStrikeColors.NEON_BLUE
        ]
        
        icons = ["🔥", "🎯", "📋"]
        
        color = colors[min(level-1, len(colors)-1)]
        icon = icons[min(level-1, len(icons)-1)]
        
        print(f"\n{color}{icon} {text}{HexStrikeColors.RESET}")
        
        if level == 1:
            print(f"{HexStrikeColors.SEPARATOR}{'═' * len(text)}{HexStrikeColors.RESET}")
        else:
            print(f"{HexStrikeColors.SEPARATOR}{'─' * len(text)}{HexStrikeColors.RESET}")
    
    def print_success(self, message: str, prefix: str = "✅"):
        """打印成功消息"""
        print(f"{HexStrikeColors.SUCCESS}{prefix} {message}{HexStrikeColors.RESET}")
    
    def print_error(self, message: str, prefix: str = "❌"):
        """打印错误消息"""
        print(f"{HexStrikeColors.ERROR}{prefix} {message}{HexStrikeColors.RESET}")
    
    def print_warning(self, message: str, prefix: str = "⚠️"):
        """打印警告消息"""
        print(f"{HexStrikeColors.WARNING}{prefix} {message}{HexStrikeColors.RESET}")
    
    def print_info(self, message: str, prefix: str = "ℹ️"):
        """打印信息消息"""
        print(f"{HexStrikeColors.INFO}{prefix} {message}{HexStrikeColors.RESET}")
    
    def print_tool_status(self, tool_name: str, status: str, details: str = ""):
        """打印工具状态
        
        Args:
            tool_name: 工具名称
            status: 状态
            details: 详细信息
        """
        color = HexStrikeColors.get_tool_status_color(status)
        status_icons = {
            'running': '🚀',
            'success': '✅',
            'completed': '✅',
            'failed': '❌',
            'error': '❌',
            'timeout': '⏰',
            'pending': '⏳',
            'cancelled': '🛑'
        }
        
        icon = status_icons.get(status.lower(), '●')
        details_str = f" | {details}" if details else ""
        
        print(f"{color}{icon} {tool_name}: {status}{details_str}{HexStrikeColors.RESET}")
    
    def print_vulnerability(self, 
                           vuln_type: str, 
                           severity: str, 
                           target: str = "",
                           description: str = ""):
        """打印漏洞信息
        
        Args:
            vuln_type: 漏洞类型
            severity: 严重性
            target: 目标
            description: 描述
        """
        color = HexStrikeColors.get_vulnerability_color(severity)
        severity_icons = {
            'critical': '🚨',
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'info': 'ℹ️'
        }
        
        icon = severity_icons.get(severity.lower(), '●')
        target_str = f" | 目标: {target}" if target else ""
        desc_str = f" | {description}" if description else ""
        
        print(f"{color}{icon} 漏洞发现: {vuln_type} ({severity}){target_str}{desc_str}{HexStrikeColors.RESET}")
    
    def clear_screen(self):
        """清屏"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def wait_for_input(self, message: str = "按回车键继续...") -> str:
        """等待用户输入"""
        return input(f"{HexStrikeColors.NEON_BLUE}{message}{HexStrikeColors.RESET}")
    
    def show_banner(self, title: str, subtitle: str = ""):
        """显示横幅"""
        self.status_display.show_banner(title, subtitle, self.terminal_width)
    
    def show_table(self, headers: List[str], rows: List[List[str]], title: str = ""):
        """显示表格"""
        self.status_display.show_table(headers, rows, title)
    
    def show_status_grid(self, items: List[Dict[str, Any]], title: str = ""):
        """显示状态网格"""
        self.status_display.show_status_grid(items, title)
    
    def show_vulnerability_summary(self, vulnerabilities: List[Dict[str, Any]]):
        """显示漏洞摘要"""
        self.status_display.show_vulnerability_summary(vulnerabilities)