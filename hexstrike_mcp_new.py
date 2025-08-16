#!/usr/bin/env python3
"""
HexStrike AI - MCP客户端入口程序 (重构版本)
HexStrike AI MCP Client Entry Point (Refactored Version)

这是HexStrike AI的MCP(Model Context Protocol)客户端重构版本，提供：
- 模块化的MCP架构设计
- 中文化的用户界面和日志输出
- 完整的AI代理通信协议支持
- 安全工具集成和智能决策引擎
- 故障恢复和监控功能

使用方法:
    python hexstrike_mcp_new.py                           # 使用默认设置启动
    python hexstrike_mcp_new.py --server-url http://192.168.1.100:8888
    python hexstrike_mcp_new.py --name my-mcp-server --debug

作者: HexStrike AI Team
版本: 6.0 (重构版本)
更新时间: 2024
"""

import os
import sys
import argparse
import signal
from typing import Optional
from datetime import datetime
import asyncio

# 在Windows系统中设置UTF-8编码
if sys.platform.startswith('win'):
    try:
        # 设置控制台编码为UTF-8
        os.system('chcp 65001 > nul')
        # 设置环境变量
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        # 重新配置stdout和stderr
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        # 如果设置失败，使用简化的输出
        pass

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from hexstrike_ai.config.logger_config import get_logger, setup_logging
from hexstrike_ai.config.colors import HexStrikeColors
from hexstrike_ai.mcp.server import MCPServerManager, create_mcp_server
from hexstrike_ai.mcp import MCP_VERSION, MCP_DESCRIPTION, MCP_CONFIG


class HexStrikeMCPApplication:
    """HexStrike AI MCP应用程序主类"""
    
    def __init__(self):
        """初始化MCP应用程序"""
        self.logger = get_logger('MCP-Application')
        self.server_manager: Optional[MCPServerManager] = None
        self.is_running = False
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理系统信号"""
        signal_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"
        self.logger.warning(f"⚠️  收到 {signal_name} 信号，正在优雅关闭MCP服务器...")
        self.is_running = False
        
        if self.server_manager:
            try:
                self.server_manager._cleanup()
            except Exception as e:
                self.logger.error(f"❌ 清理资源时出现异常: {e}")
        
        self.logger.info("✅ MCP应用程序已安全关闭")
        sys.exit(0)
    
    def display_banner(self):
        """显示程序启动横幅"""
        print(f"\n{HexStrikeColors.BANNER_TITLE}{'=' * 60}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.BANNER_TITLE}    HexStrike AI - MCP客户端 v{MCP_VERSION} (重构版本)    {HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.BANNER_TITLE}{'=' * 60}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.NEON_BLUE}🤖 AI代理通信协议接口{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.NEON_GREEN}🛡️  安全工具集成平台{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.NEON_YELLOW}🧠 智能决策引擎支持{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.SEPARATOR}{'─' * 60}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.DIM_WHITE}📄 描述: {MCP_DESCRIPTION}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.DIM_WHITE}🏗️  架构: 模块化设计，支持150+安全工具{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.DIM_WHITE}🌍 语言: 中文化界面和日志输出{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.SEPARATOR}{'─' * 60}{HexStrikeColors.RESET}\n")
    
    def display_capabilities(self):
        """显示MCP服务器功能"""
        capabilities = MCP_CONFIG['capabilities']
        
        print(f"{HexStrikeColors.NEON_BLUE}🚀 MCP服务器功能:{HexStrikeColors.RESET}")
        capability_descriptions = {
            'tools': '🛠️  工具函数: 150+安全工具函数',
            'prompts': '💬 提示模板: AI代理通信模板',
            'resources': '📚 资源管理: 动态资源分配',
            'logging': '📝 日志记录: 详细的中文日志'
        }
        
        for cap in capabilities:
            desc = capability_descriptions.get(cap, f'✨ {cap}: 高级功能')
            print(f"  {desc}")
        print()
    
    def check_dependencies(self):
        """检查系统依赖"""
        self.logger.info("🔍 检查系统依赖...")
        
        missing_deps = []
        
        try:
            from mcp.server.fastmcp import FastMCP
            self.logger.debug("✅ FastMCP库: 已安装")
        except ImportError:
            missing_deps.append("mcp (Model Context Protocol)")
        
        try:
            import requests
            self.logger.debug("✅ Requests库: 已安装")
        except ImportError:
            missing_deps.append("requests")
        
        if missing_deps:
            self.logger.error(f"❌ 缺少依赖: {', '.join(missing_deps)}")
            print(f"\n{HexStrikeColors.BRIGHT_RED}❌ 错误: 缺少必要的Python依赖{HexStrikeColors.RESET}")
            print(f"{HexStrikeColors.YELLOW}请运行以下命令安装依赖:{HexStrikeColors.RESET}")
            print(f"{HexStrikeColors.CYAN}pip install -r requirements.txt{HexStrikeColors.RESET}\n")
            return False
        
        self.logger.success("✅ 所有依赖检查通过")
        return True
    
    def validate_config(self, args):
        """验证配置参数"""
        self.logger.info("⚙️  验证配置参数...")
        
        # 验证服务器URL格式
        if not args.server_url.startswith(('http://', 'https://')):
            self.logger.error(f"❌ 无效的服务器URL格式: {args.server_url}")
            return False
        
        # 验证超时时间
        if args.timeout <= 0:
            self.logger.error(f"❌ 无效的超时时间: {args.timeout}")
            return False
        
        # 验证重试次数
        if args.max_retries < 0:
            self.logger.error(f"❌ 无效的重试次数: {args.max_retries}")
            return False
        
        self.logger.success("✅ 配置参数验证通过")
        return True
    
    def display_startup_info(self, args):
        """显示启动信息"""
        print(f"{HexStrikeColors.NEON_BLUE}🔧 启动配置:{HexStrikeColors.RESET}")
        print(f"  📍 MCP服务器名称: {HexStrikeColors.BRIGHT_WHITE}{args.name}{HexStrikeColors.RESET}")
        print(f"  🌐 HexStrike服务器: {HexStrikeColors.BRIGHT_WHITE}{args.server_url}{HexStrikeColors.RESET}")
        print(f"  ⏱️  请求超时时间: {HexStrikeColors.BRIGHT_WHITE}{args.timeout}秒{HexStrikeColors.RESET}")
        print(f"  🔄 最大重试次数: {HexStrikeColors.BRIGHT_WHITE}{args.max_retries}次{HexStrikeColors.RESET}")
        print(f"  🐛 调试模式: {HexStrikeColors.BRIGHT_WHITE}{'启用' if args.debug else '禁用'}{HexStrikeColors.RESET}")
        print(f"  📅 启动时间: {HexStrikeColors.BRIGHT_WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{HexStrikeColors.RESET}")
        print()
    
    def run(self, args):
        """运行MCP应用程序"""
        try:
            # 显示启动信息
            self.display_startup_info(args)
            
            # 检查依赖
            if not self.check_dependencies():
                return 1
            
            # 验证配置
            if not self.validate_config(args):
                return 1
            
            # 创建MCP服务器管理器
            self.logger.info("🚀 创建MCP服务器管理器...")
            self.server_manager = create_mcp_server(
                server_name=args.name,
                hexstrike_server_url=args.server_url
            )
            
            # 设置运行标志
            self.is_running = True
            
            # 显示就绪信息
            print(f"{HexStrikeColors.MATRIX_GREEN}✅ MCP服务器准备就绪{HexStrikeColors.RESET}")
            print(f"{HexStrikeColors.NEON_YELLOW}🎯 等待AI代理连接...{HexStrikeColors.RESET}")
            print(f"{HexStrikeColors.DIM_WHITE}💡 提示: 按 Ctrl+C 优雅关闭服务器{HexStrikeColors.RESET}\n")
            
            # 运行MCP服务器
            self.server_manager.run()
            
            return 0
            
        except KeyboardInterrupt:
            self.logger.warning("⚠️  用户中断，正在关闭...")
            return 0
        except Exception as e:
            self.logger.error(f"❌ MCP应用程序运行异常: {e}")
            print(f"\n{HexStrikeColors.ERROR}❌ 运行异常: {e}{HexStrikeColors.RESET}")
            return 1
        finally:
            if self.server_manager:
                self.server_manager._cleanup()


def parse_command_line_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='HexStrike AI MCP客户端 - AI代理通信协议接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{HexStrikeColors.NEON_BLUE}使用示例:{HexStrikeColors.RESET}
  {HexStrikeColors.WHITE}python hexstrike_mcp_new.py{HexStrikeColors.RESET}
    使用默认设置启动MCP服务器
    
  {HexStrikeColors.WHITE}python hexstrike_mcp_new.py --server-url http://192.168.1.100:8888{HexStrikeColors.RESET}
    连接到指定的HexStrike服务器
    
  {HexStrikeColors.WHITE}python hexstrike_mcp_new.py --name my-mcp-server --debug{HexStrikeColors.RESET}
    自定义服务器名称并启用调试模式
    
  {HexStrikeColors.WHITE}python hexstrike_mcp_new.py --timeout 600 --max-retries 5{HexStrikeColors.RESET}
    自定义超时时间和重试次数

{HexStrikeColors.YELLOW}配置文件:{HexStrikeColors.RESET}
  请参考 {HexStrikeColors.WHITE}hexstrike-ai-mcp.json{HexStrikeColors.RESET} 配置Claude Desktop集成

{HexStrikeColors.MATRIX_GREEN}更多信息:{HexStrikeColors.RESET}
  项目主页: https://github.com/hexstrike/hexstrike-ai
  文档: 查看 README.md 获取详细说明
        """
    )
    
    parser.add_argument(
        '--server-url',
        default='http://127.0.0.1:8888',
        help='HexStrike AI服务器URL地址 (默认: http://127.0.0.1:8888)'
    )
    
    parser.add_argument(
        '--name',
        default='hexstrike-ai-mcp',
        help='MCP服务器实例名称 (默认: hexstrike-ai-mcp)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='HTTP请求超时时间，单位秒 (默认: 300)'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='请求失败时的最大重试次数 (默认: 3)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式，显示详细的调试信息'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='设置日志级别 (默认: INFO)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'HexStrike AI MCP客户端 v{MCP_VERSION}',
        help='显示版本信息'
    )
    
    return parser.parse_args()


def setup_application_logging(args):
    """设置应用程序日志"""
    log_level = 'DEBUG' if args.debug else args.log_level
    setup_logging(level=log_level)
    
    logger = get_logger('MCP-Main')
    logger.info(f"🔧 日志系统初始化完成，级别: {log_level}")
    
    if args.debug:
        logger.debug("🐛 调试模式已启用，将显示详细的调试信息")


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_command_line_args()
        
        # 设置日志系统
        setup_application_logging(args)
        
        # 创建应用程序实例
        app = HexStrikeMCPApplication()
        
        # 显示启动横幅
        app.display_banner()
        
        # 显示功能列表
        app.display_capabilities()
        
        # 运行应用程序
        exit_code = app.run(args)
        
        # 退出
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"\n{HexStrikeColors.ERROR}❌ 启动失败: {e}{HexStrikeColors.RESET}")
        print(f"{HexStrikeColors.YELLOW}💡 提示: 使用 --debug 参数获取详细错误信息{HexStrikeColors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()