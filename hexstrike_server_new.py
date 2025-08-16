#!/usr/bin/env python3
"""
HexStrike AI - 重构版高级渗透测试框架服务器
Refactored Advanced Penetration Testing Framework Server

重构后的中文化版本 v6.0
Enhanced with AI-Powered Intelligence & Automation
🚀 漏洞赏金 | CTF | 红队作战 | 安全研究

主要改进:
✅ 完整的模块化架构设计
✅ 中文化界面和详细日志系统  
✅ AI智能决策引擎和多Agent协作
✅ 现代化可视化终端界面
✅ 高级进程管理和资源监控
✅ 智能缓存和性能优化
✅ 150+安全工具集成
✅ 实时漏洞情报关联分析

架构说明: 
采用双脚本系统架构 (hexstrike_server_new.py + hexstrike_mcp.py)
Flask框架提供REST API，FastMCP协议实现AI代理通信
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from hexstrike_ai import display_banner, get_version_info
from hexstrike_ai.config import get_config, setup_logging, HexStrikeColors
from hexstrike_ai.core import ProcessManager, AdvancedCache, ResourceMonitor
from hexstrike_ai.visualization import ModernVisualEngine
from hexstrike_ai.api.server import create_flask_app
from hexstrike_ai.tools.manager import SecurityToolsManager
from hexstrike_ai.intelligence.decision_engine import IntelligentDecisionEngine

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='HexStrike AI - 高级AI驱动渗透测试框架',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 hexstrike_server_new.py                    # 使用默认配置启动
  python3 hexstrike_server_new.py --port 9999       # 指定端口启动
  python3 hexstrike_server_new.py --debug           # 启用调试模式
  python3 hexstrike_server_new.py --host 0.0.0.0    # 绑定所有网卡

配置检查:
  python3 hexstrike_server_new.py --check-tools     # 检查安全工具可用性
  python3 hexstrike_server_new.py --version         # 显示版本信息
        """
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='服务器监听地址 (默认: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8888,
        help='服务器监听端口 (默认: 8888)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式'
    )
    
    parser.add_argument(
        '--max-workers',
        type=int,
        default=10,
        help='最大工作线程数 (默认: 10)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='日志级别 (默认: INFO)'
    )
    
    parser.add_argument(
        '--config-file',
        help='配置文件路径'
    )
    
    parser.add_argument(
        '--check-tools',
        action='store_true',
        help='检查安全工具可用性并退出'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='显示版本信息并退出'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='禁用缓存系统'
    )
    
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='禁用AI智能功能'
    )
    
    return parser.parse_args()

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print(f"{HexStrikeColors.ERROR}❌ 错误: 需要Python 3.8或更高版本{HexStrikeColors.RESET}")
        print(f"   当前版本: {sys.version}")
        sys.exit(1)

def check_dependencies():
    """检查关键依赖"""
    required_modules = [
        'flask', 'requests', 'psutil', 'fastmcp',
        'beautifulsoup4', 'selenium', 'aiohttp', 'mitmproxy'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"{HexStrikeColors.ERROR}❌ 缺少必需的Python模块:{HexStrikeColors.RESET}")
        for module in missing_modules:
            print(f"   - {module}")
        print(f"\n{HexStrikeColors.INFO}💡 安装方法:{HexStrikeColors.RESET}")
        print(f"   pip install {' '.join(missing_modules)}")
        return False
    
    return True

def check_tools_availability():
    """检查安全工具可用性"""
    visual_engine = ModernVisualEngine()
    visual_engine.print_header("🔧 安全工具可用性检查", 1)
    
    tools_manager = SecurityToolsManager()
    available_tools, unavailable_tools = tools_manager.check_all_tools()
    
    # 显示可用工具
    if available_tools:
        visual_engine.print_header("✅ 可用工具", 2)
        for category, tools in available_tools.items():
            print(f"\n{HexStrikeColors.NEON_BLUE}📂 {category}:{HexStrikeColors.RESET}")
            for tool in tools:
                version_info = tool.get('version', '未知版本')
                visual_engine.print_success(f"{tool['name']} ({version_info})")
    
    # 显示不可用工具
    if unavailable_tools:
        visual_engine.print_header("❌ 不可用工具", 2) 
        for category, tools in unavailable_tools.items():
            print(f"\n{HexStrikeColors.CYBER_ORANGE}📂 {category}:{HexStrikeColors.RESET}")
            for tool in tools:
                visual_engine.print_warning(f"{tool['name']} - {tool.get('reason', '未找到')}")
    
    # 统计信息
    total_available = sum(len(tools) for tools in available_tools.values())
    total_unavailable = sum(len(tools) for tools in unavailable_tools.values())
    total_tools = total_available + total_unavailable
    
    print(f"\n{HexStrikeColors.BANNER_TITLE}📊 工具统计摘要:{HexStrikeColors.RESET}")
    print(f"   总计工具: {total_tools}")
    print(f"   可用工具: {HexStrikeColors.SUCCESS}{total_available}{HexStrikeColors.RESET}")
    print(f"   不可用工具: {HexStrikeColors.WARNING}{total_unavailable}{HexStrikeColors.RESET}")
    print(f"   可用率: {HexStrikeColors.NEON_BLUE}{(total_available/total_tools)*100:.1f}%{HexStrikeColors.RESET}")

def show_version_info():
    """显示版本信息"""
    version_info = get_version_info()
    visual_engine = ModernVisualEngine()
    
    visual_engine.show_banner("HexStrike AI 版本信息")
    
    print(f"{HexStrikeColors.NEON_BLUE}版本号:{HexStrikeColors.RESET} {version_info['version']}")
    print(f"{HexStrikeColors.NEON_BLUE}描述:{HexStrikeColors.RESET} {version_info['description']}")
    print(f"{HexStrikeColors.NEON_BLUE}作者:{HexStrikeColors.RESET} {version_info['author']}")
    print(f"{HexStrikeColors.NEON_BLUE}许可证:{HexStrikeColors.RESET} {version_info['license']}")
    print(f"{HexStrikeColors.NEON_BLUE}发布日期:{HexStrikeColors.RESET} {version_info['release_date']}")
    
    print(f"\n{HexStrikeColors.BANNER_TITLE}🚀 主要特性:{HexStrikeColors.RESET}")
    for feature in version_info['major_features']:
        print(f"   ✅ {feature}")

def initialize_system(args):
    """初始化系统组件"""
    visual_engine = ModernVisualEngine()
    
    # 显示启动横幅
    print(display_banner())
    
    visual_engine.print_header("🔧 系统初始化", 1)
    
    # 1. 设置日志系统
    visual_engine.print_info("正在初始化日志系统...")
    logger = setup_logging(
        level=args.log_level,
        enable_colored_output=True,
        enable_file_logging=True
    )
    
    # 2. 加载配置
    visual_engine.print_info("正在加载系统配置...")
    config = get_config()
    
    # 更新配置
    config.server.host = args.host
    config.server.port = args.port
    config.server.debug = args.debug
    config.server.max_workers = args.max_workers
    config.cache.enabled = not args.no_cache
    config.ai.decision_engine_enabled = not args.no_ai
    
    # 验证配置
    if not config.validate():
        visual_engine.print_error("配置验证失败，使用默认配置继续")
    
    # 3. 初始化核心组件
    visual_engine.print_info("正在初始化核心组件...")
    
    # 进程管理器
    process_manager = ProcessManager(max_concurrent_processes=args.max_workers)
    visual_engine.print_success("进程管理器已启动")
    
    # 缓存系统
    cache_system = None
    if config.cache.enabled:
        cache_system = AdvancedCache(
            max_size=config.cache.max_size,
            default_ttl=config.cache.default_ttl
        )
        visual_engine.print_success("缓存系统已启动")
    
    # 资源监控
    resource_monitor = ResourceMonitor()
    visual_engine.print_success("资源监控已启动")
    
    # 4. 初始化安全工具管理器
    visual_engine.print_info("正在初始化安全工具管理器...")
    tools_manager = SecurityToolsManager()
    available_count = tools_manager.initialize_tools()
    visual_engine.print_success(f"安全工具管理器已启动 (可用工具: {available_count})")
    
    # 5. 初始化AI决策引擎
    decision_engine = None
    if config.ai.decision_engine_enabled:
        visual_engine.print_info("正在初始化AI决策引擎...")
        decision_engine = IntelligentDecisionEngine()
        visual_engine.print_success("AI决策引擎已启动")
    
    # 6. 创建Flask应用
    visual_engine.print_info("正在创建Web API服务器...")
    app = create_flask_app(
        config=config,
        process_manager=process_manager,
        cache_system=cache_system,
        resource_monitor=resource_monitor,
        tools_manager=tools_manager,
        decision_engine=decision_engine
    )
    visual_engine.print_success("Web API服务器已创建")
    
    return {
        'app': app,
        'config': config,
        'logger': logger,
        'visual_engine': visual_engine,
        'process_manager': process_manager,
        'cache_system': cache_system,
        'resource_monitor': resource_monitor,
        'tools_manager': tools_manager,
        'decision_engine': decision_engine
    }

def run_server(components):
    """运行服务器"""
    app = components['app']
    config = components['config']
    logger = components['logger']
    visual_engine = components['visual_engine']
    
    visual_engine.print_header("🚀 启动HexStrike AI服务器", 1)
    
    # 显示服务器信息
    print(f"{HexStrikeColors.NEON_BLUE}服务器地址:{HexStrikeColors.RESET} http://{config.server.host}:{config.server.port}")
    print(f"{HexStrikeColors.NEON_BLUE}调试模式:{HexStrikeColors.RESET} {'启用' if config.server.debug else '禁用'}")
    print(f"{HexStrikeColors.NEON_BLUE}最大工作线程:{HexStrikeColors.RESET} {config.server.max_workers}")
    print(f"{HexStrikeColors.NEON_BLUE}缓存系统:{HexStrikeColors.RESET} {'启用' if config.cache.enabled else '禁用'}")
    print(f"{HexStrikeColors.NEON_BLUE}AI决策引擎:{HexStrikeColors.RESET} {'启用' if config.ai.decision_engine_enabled else '禁用'}")
    
    # 显示API端点信息
    print(f"\n{HexStrikeColors.BANNER_TITLE}📡 主要API端点:{HexStrikeColors.RESET}")
    endpoints = [
        ("/health", "服务器健康检查"),
        ("/api/tools/status", "工具状态查询"),
        ("/api/intelligence/analyze-target", "AI目标分析"),
        ("/api/processes/status", "进程状态管理"),
        ("/api/command", "命令执行接口")
    ]
    
    for endpoint, description in endpoints:
        print(f"   {HexStrikeColors.CYBER_ORANGE}GET/POST{HexStrikeColors.RESET} {endpoint} - {description}")
    
    print(f"\n{HexStrikeColors.SUCCESS}✅ 服务器启动完成，等待客户端连接...{HexStrikeColors.RESET}")
    print(f"{HexStrikeColors.WARNING}⚠️  使用 Ctrl+C 停止服务器{HexStrikeColors.RESET}")
    
    try:
        # 启动Flask服务器
        app.run(
            host=config.server.host,
            port=config.server.port,
            debug=config.server.debug,
            threaded=True,
            use_reloader=False  # 避免重复初始化
        )
    except KeyboardInterrupt:
        visual_engine.print_warning("收到停止信号，正在关闭服务器...")
        cleanup_system(components)
    except Exception as e:
        visual_engine.print_error(f"服务器运行错误: {e}")
        cleanup_system(components)
        sys.exit(1)

def cleanup_system(components):
    """清理系统资源"""
    visual_engine = components.get('visual_engine')
    if visual_engine:
        visual_engine.print_header("🧹 清理系统资源", 1)
    
    # 清理进程管理器
    process_manager = components.get('process_manager')
    if process_manager:
        cleaned_count = process_manager.cleanup_all_processes()
        if visual_engine:
            visual_engine.print_success(f"已清理 {cleaned_count} 个进程")
    
    # 清理缓存系统
    cache_system = components.get('cache_system')
    if cache_system:
        cache_system.clear()
        if visual_engine:
            visual_engine.print_success("缓存系统已清理")
    
    # 停止资源监控
    resource_monitor = components.get('resource_monitor')
    if resource_monitor:
        resource_monitor.stop_monitoring()
        if visual_engine:
            visual_engine.print_success("资源监控已停止")
    
    if visual_engine:
        visual_engine.print_success("🎯 系统清理完成，再见!")

def main():
    """主函数"""
    # 检查Python版本
    check_python_version()
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 显示版本信息
    if args.version:
        show_version_info()
        sys.exit(0)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查工具可用性
    if args.check_tools:
        check_tools_availability()
        sys.exit(0)
    
    try:
        # 初始化系统
        components = initialize_system(args)
        
        # 运行服务器
        run_server(components)
        
    except KeyboardInterrupt:
        print(f"\n{HexStrikeColors.WARNING}⚠️  用户中断，正在退出...{HexStrikeColors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{HexStrikeColors.ERROR}❌ 致命错误: {e}{HexStrikeColors.RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()