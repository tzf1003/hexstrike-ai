#!/usr/bin/env python3
"""
HexStrike AI - 颜色主题配置
Color Theme Configuration

这个模块定义了HexStrike AI框架的完整颜色方案，包括：
- 基础颜色定义
- 增强的红色黑客主题
- 漏洞严重性颜色
- 工具状态颜色
- 高亮显示颜色
"""

class HexStrikeColors:
    """HexStrike AI 增强颜色配置类 - 红色黑客主题"""
    
    # ========================================================================
    # 基础颜色 (向后兼容)
    # ========================================================================
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # ========================================================================
    # 核心增强颜色
    # ========================================================================
    MATRIX_GREEN = '\033[38;5;46m'      # 矩阵绿色
    NEON_BLUE = '\033[38;5;51m'         # 霓虹蓝色
    ELECTRIC_PURPLE = '\033[38;5;129m'  # 电紫色
    CYBER_ORANGE = '\033[38;5;208m'     # 赛博橙色
    HACKER_RED = '\033[38;5;196m'       # 黑客红色
    TERMINAL_GRAY = '\033[38;5;240m'    # 终端灰色
    BRIGHT_WHITE = '\033[97m'           # 亮白色
    RESET = '\033[0m'                   # 重置
    BOLD = '\033[1m'                    # 粗体
    DIM = '\033[2m'                     # 暗淡
    UNDERLINE = '\033[4m'               # 下划线
    BLINK = '\033[5m'                   # 闪烁
    REVERSE = '\033[7m'                 # 反显
    
    # ========================================================================
    # 增强红色系列 (黑客主题核心)
    # ========================================================================
    BLOOD_RED = '\033[38;5;124m'        # 血红色
    CRIMSON = '\033[38;5;160m'          # 深红色
    DARK_RED = '\033[38;5;88m'          # 暗红色
    FIRE_RED = '\033[38;5;202m'         # 火红色
    ROSE_RED = '\033[38;5;167m'         # 玫瑰红
    BURGUNDY = '\033[38;5;52m'          # 酒红色
    SCARLET = '\033[38;5;197m'          # 猩红色
    RUBY = '\033[38;5;161m'             # 红宝石色
    ORANGE_RED = '\033[38;5;196m'       # 橙红色
    
    # ========================================================================
    # 高亮显示颜色 (背景色)
    # ========================================================================
    HIGHLIGHT_RED = '\033[48;5;196m\033[38;5;15m'      # 红色背景，白色文字
    HIGHLIGHT_YELLOW = '\033[48;5;226m\033[38;5;16m'   # 黄色背景，黑色文字
    HIGHLIGHT_GREEN = '\033[48;5;46m\033[38;5;16m'     # 绿色背景，黑色文字
    HIGHLIGHT_BLUE = '\033[48;5;51m\033[38;5;16m'      # 蓝色背景，黑色文字
    HIGHLIGHT_PURPLE = '\033[48;5;129m\033[38;5;15m'   # 紫色背景，白色文字
    HIGHLIGHT_ORANGE = '\033[48;5;208m\033[38;5;16m'   # 橙色背景，黑色文字
    
    # ========================================================================
    # 状态颜色 (带红色基调)
    # ========================================================================
    SUCCESS = '\033[38;5;46m'           # 成功 - 亮绿色
    WARNING = '\033[38;5;208m'          # 警告 - 橙色
    ERROR = '\033[38;5;196m'            # 错误 - 亮红色
    CRITICAL = '\033[48;5;196m\033[38;5;15m\033[1m'  # 关键错误 - 红底白字粗体
    INFO = '\033[38;5;51m'              # 信息 - 青色
    DEBUG = '\033[38;5;240m'            # 调试 - 灰色
    
    # ========================================================================
    # 漏洞严重性颜色
    # ========================================================================
    VULN_CRITICAL = '\033[48;5;124m\033[38;5;15m\033[1m'  # 关键漏洞 - 暗红底白字粗体
    VULN_HIGH = '\033[38;5;196m\033[1m'                   # 高危漏洞 - 亮红粗体
    VULN_MEDIUM = '\033[38;5;208m\033[1m'                 # 中危漏洞 - 橙色粗体
    VULN_LOW = '\033[38;5;226m'                           # 低危漏洞 - 黄色
    VULN_INFO = '\033[38;5;51m'                           # 信息级漏洞 - 青色
    
    # ========================================================================
    # 工具状态颜色
    # ========================================================================
    TOOL_RUNNING = '\033[38;5;46m\033[5m'     # 工具运行中 - 闪烁绿色
    TOOL_SUCCESS = '\033[38;5;46m\033[1m'     # 工具成功 - 粗体绿色
    TOOL_FAILED = '\033[38;5;196m\033[1m'     # 工具失败 - 粗体红色
    TOOL_TIMEOUT = '\033[38;5;208m\033[1m'    # 工具超时 - 粗体橙色
    TOOL_RECOVERY = '\033[38;5;129m\033[1m'   # 工具恢复 - 粗体紫色
    TOOL_PENDING = '\033[38;5;240m'           # 工具等待 - 灰色
    TOOL_CANCELLED = '\033[38;5;124m'         # 工具取消 - 血红色
    
    # ========================================================================
    # 进度条颜色
    # ========================================================================
    PROGRESS_BAR = '\033[38;5;46m'            # 进度条 - 绿色
    PROGRESS_BAR_BG = '\033[48;5;240m'        # 进度条背景 - 灰色背景
    PROGRESS_PERCENT = '\033[38;5;51m\033[1m' # 进度百分比 - 粗体青色
    PROGRESS_ETA = '\033[38;5;208m'           # 预计时间 - 橙色
    
    # ========================================================================
    # AI代理颜色
    # ========================================================================
    AI_DECISION = '\033[38;5;129m\033[1m'     # AI决策 - 粗体紫色
    AI_ANALYSIS = '\033[38;5;51m\033[1m'      # AI分析 - 粗体青色
    AI_LEARNING = '\033[38;5;46m\033[1m'      # AI学习 - 粗体绿色
    AI_ERROR = '\033[38;5;196m\033[1m'        # AI错误 - 粗体红色
    
    # ========================================================================
    # 网络安全特定颜色
    # ========================================================================
    EXPLOIT_FOUND = '\033[48;5;196m\033[38;5;15m\033[1m'  # 发现漏洞利用 - 红底白字
    PAYLOAD_SUCCESS = '\033[38;5;46m\033[1m'              # 载荷成功 - 粗体绿色
    SHELL_ACCESS = '\033[38;5;226m\033[1m\033[5m'         # Shell访问 - 闪烁黄色粗体
    PRIVILEGE_ESCALATION = '\033[38;5;196m\033[1m'        # 权限提升 - 粗体红色
    DATA_EXFILTRATION = '\033[38;5;208m\033[1m'           # 数据窃取 - 粗体橙色
    
    # ========================================================================
    # 横幅和装饰颜色
    # ========================================================================
    BANNER_TITLE = '\033[38;5;196m\033[1m'      # 横幅标题 - 粗体红色
    BANNER_SUBTITLE = '\033[38;5;208m'          # 横幅副标题 - 橙色
    BANNER_BORDER = '\033[38;5;240m'            # 横幅边框 - 灰色
    SEPARATOR = '\033[38;5;124m'                # 分隔符 - 血红色
    
    @classmethod
    def get_vulnerability_color(cls, severity: str) -> str:
        """根据漏洞严重性获取相应颜色"""
        severity_map = {
            'critical': cls.VULN_CRITICAL,
            'high': cls.VULN_HIGH,
            'medium': cls.VULN_MEDIUM,
            'low': cls.VULN_LOW,
            'info': cls.VULN_INFO,
            'informational': cls.VULN_INFO
        }
        return severity_map.get(severity.lower(), cls.INFO)
    
    @classmethod
    def get_tool_status_color(cls, status: str) -> str:
        """根据工具状态获取相应颜色"""
        status_map = {
            'running': cls.TOOL_RUNNING,
            'success': cls.TOOL_SUCCESS,
            'completed': cls.TOOL_SUCCESS,
            'failed': cls.TOOL_FAILED,
            'error': cls.TOOL_FAILED,
            'timeout': cls.TOOL_TIMEOUT,
            'recovery': cls.TOOL_RECOVERY,
            'pending': cls.TOOL_PENDING,
            'cancelled': cls.TOOL_CANCELLED,
            'waiting': cls.TOOL_PENDING
        }
        return status_map.get(status.lower(), cls.INFO)
    
    @classmethod
    def colorize_text(cls, text: str, color: str, reset: bool = True) -> str:
        """为文本添加颜色"""
        if reset:
            return f"{color}{text}{cls.RESET}"
        return f"{color}{text}"
    
    @classmethod
    def create_gradient_text(cls, text: str, start_color: str, end_color: str) -> str:
        """创建渐变色文本 (简化版本)"""
        # 这是一个简化版本，实际实现需要更复杂的算法
        length = len(text)
        if length <= 1:
            return f"{start_color}{text}{cls.RESET}"
        
        mid_point = length // 2
        first_half = f"{start_color}{text[:mid_point]}"
        second_half = f"{end_color}{text[mid_point:]}{cls.RESET}"
        return first_half + second_half
    
    @classmethod
    def print_colored(cls, text: str, color: str = None, end: str = '\n'):
        """打印彩色文本"""
        if color:
            print(f"{color}{text}{cls.RESET}", end=end)
        else:
            print(text, end=end)
    
    @classmethod
    def get_all_colors(cls) -> dict:
        """获取所有颜色定义"""
        colors = {}
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and not callable(getattr(cls, attr_name)):
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, str) and attr_value.startswith('\033'):
                    colors[attr_name] = attr_value
        return colors

# 向后兼容性别名
Colors = HexStrikeColors

# 常用颜色快捷方式
def red(text: str) -> str:
    """红色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.HACKER_RED)

def green(text: str) -> str:
    """绿色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.MATRIX_GREEN)

def blue(text: str) -> str:
    """蓝色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.NEON_BLUE)

def yellow(text: str) -> str:
    """黄色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.YELLOW)

def purple(text: str) -> str:
    """紫色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.ELECTRIC_PURPLE)

def cyan(text: str) -> str:
    """青色文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.NEON_BLUE)

def bold(text: str) -> str:
    """粗体文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.BOLD)

def success(text: str) -> str:
    """成功状态文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.SUCCESS)

def warning(text: str) -> str:
    """警告状态文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.WARNING)

def error(text: str) -> str:
    """错误状态文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.ERROR)

def critical(text: str) -> str:
    """关键错误状态文本"""
    return HexStrikeColors.colorize_text(text, HexStrikeColors.CRITICAL)