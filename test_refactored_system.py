#!/usr/bin/env python3
"""
HexStrike AI - 重构系统测试脚本
Refactored System Test Script

这个脚本用于测试重构后的HexStrike AI系统的基本功能，包括：
- 模块导入测试
- 配置系统测试
- 日志系统测试
- 核心组件初始化测试
- API服务器创建测试
"""

import sys
import os
import traceback
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """测试基础模块导入"""
    print("测试基础模块导入...")
    
    try:
        # 测试主包导入
        import hexstrike_ai
        print(f"成功导入 hexstrike_ai 包 (版本: {hexstrike_ai.__version__})")
        
        # 测试配置模块导入
        from hexstrike_ai.config import get_config, setup_logging, HexStrikeColors
        print("成功导入配置模块")
        
        # 测试核心模块导入
        from hexstrike_ai.core import ProcessManager, AdvancedCache, ResourceMonitor
        print("成功导入核心模块")
        
        # 测试可视化模块导入
        from hexstrike_ai.visualization import ModernVisualEngine
        print("成功导入可视化模块")
        
        # 测试API模块导入
        from hexstrike_ai.api import create_flask_app, HexStrikeAPI
        print("成功导入API模块")
        
        # 测试工具管理器导入
        from hexstrike_ai.tools import SecurityToolsManager
        print("成功导入工具管理器")
        
        # 测试智能引擎导入
        from hexstrike_ai.intelligence import IntelligentDecisionEngine
        print("成功导入智能决策引擎")
        
        return True
        
    except Exception as e:
        print(f"模块导入失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return False

def test_configuration_system():
    """测试配置系统"""
    print("\n🔧 测试配置系统...")
    
    try:
        from hexstrike_ai.config import get_config
        
        # 获取配置实例
        config = get_config()
        print("✅ 成功获取配置实例")
        
        # 测试配置验证
        is_valid = config.validate()
        if is_valid:
            print("✅ 配置验证通过")
        else:
            print("⚠️  配置验证有警告，但可以继续")
        
        # 显示关键配置信息
        print(f"📊 服务器配置: {config.server.host}:{config.server.port}")
        print(f"📊 缓存状态: {'启用' if config.cache.enabled else '禁用'}")
        print(f"📊 AI引擎: {'启用' if config.ai.decision_engine_enabled else '禁用'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        return False

def test_logging_system():
    """测试日志系统"""
    print("\n📝 测试日志系统...")
    
    try:
        from hexstrike_ai.config import setup_logging
        
        # 初始化日志系统
        logger = setup_logging(level='INFO', enable_colored_output=True)
        print("✅ 成功初始化日志系统")
        
        # 测试各种日志级别
        logger.info("测试信息级别日志")
        logger.success("测试成功状态日志")
        logger.warning("测试警告级别日志")
        logger.debug("测试调试级别日志")
        
        # 测试专用日志方法
        logger.tool_start("test-tool", "example.com")
        logger.tool_success("test-tool", 1.5)
        logger.ai_decision("测试AI决策日志", 0.85)
        logger.vulnerability_found("high", "SQL注入", "example.com")
        
        print("✅ 各种日志类型测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 日志系统测试失败: {e}")
        return False

def test_core_components():
    """测试核心组件"""
    print("\n⚙️  测试核心组件...")
    
    try:
        from hexstrike_ai.core import ProcessManager, AdvancedCache, ResourceMonitor
        
        # 测试进程管理器
        print("🔄 测试进程管理器...")
        process_manager = ProcessManager(max_concurrent_processes=5)
        stats = process_manager.get_process_count()
        print(f"✅ 进程管理器创建成功 (当前进程: {stats['total']})")
        
        # 测试缓存系统
        print("💾 测试缓存系统...")
        cache = AdvancedCache(max_size=100, default_ttl=300)
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        if value == "test_value":
            print("✅ 缓存系统工作正常")
        else:
            print("⚠️  缓存系统异常")
        
        # 测试资源监控
        print("📊 测试资源监控器...")
        monitor = ResourceMonitor(interval=1)
        current_stats = monitor.get_current_stats()
        print(f"✅ 资源监控器创建成功 (CPU: {current_stats.cpu_usage:.1f}%)")
        
        # 清理资源
        monitor.stop_monitoring()
        process_manager.cleanup_all_processes()
        
        return True
        
    except Exception as e:
        print(f"❌ 核心组件测试失败: {e}")
        return False

def test_visualization_engine():
    """测试可视化引擎"""
    print("\n🎨 测试可视化引擎...")
    
    try:
        from hexstrike_ai.visualization import ModernVisualEngine
        
        # 创建可视化引擎
        visual = ModernVisualEngine()
        print("✅ 可视化引擎创建成功")
        
        # 测试各种显示功能
        visual.print_header("测试标题", 1)
        visual.print_success("这是一个成功消息")
        visual.print_warning("这是一个警告消息")
        visual.print_info("这是一个信息消息")
        visual.print_tool_status("测试工具", "running", "正在扫描目标...")
        visual.print_vulnerability("SQL注入", "high", "example.com", "发现注入点")
        
        # 测试进度条
        progress = visual.create_progress_bar(100, "测试进度")
        for i in range(0, 101, 20):
            progress.set_progress(i, f"处理项目 {i}")
        progress.finish("测试完成")
        
        print("✅ 可视化功能测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 可视化引擎测试失败: {e}")
        return False

def test_tools_manager():
    """测试工具管理器"""
    print("\n🛠️  测试工具管理器...")
    
    try:
        from hexstrike_ai.tools import SecurityToolsManager
        
        # 创建工具管理器
        tools_manager = SecurityToolsManager()
        print("✅ 工具管理器创建成功")
        
        # 初始化工具
        available_count = tools_manager.initialize_tools()
        print(f"✅ 工具初始化完成 (可用工具: {available_count})")
        
        # 获取工具状态
        status = tools_manager.get_all_tools_status()
        print(f"📊 工具统计: 总计 {status['total_tools']} 个，可用 {status['available_tools']} 个")
        
        # 显示各类别工具数量
        for category, info in status['categories'].items():
            if info['available'] > 0:
                print(f"   📂 {category}: {info['available']}/{info['total']} 可用")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具管理器测试失败: {e}")
        return False

def test_api_server():
    """测试API服务器创建"""
    print("\n🌐 测试API服务器...")
    
    try:
        from hexstrike_ai.api import create_flask_app
        from hexstrike_ai.config import get_config
        from hexstrike_ai.core import ProcessManager
        from hexstrike_ai.tools import SecurityToolsManager
        from hexstrike_ai.intelligence import IntelligentDecisionEngine
        
        # 创建必要组件
        config = get_config()
        process_manager = ProcessManager(max_concurrent_processes=2)
        tools_manager = SecurityToolsManager()
        decision_engine = IntelligentDecisionEngine()
        
        # 创建Flask应用
        app = create_flask_app(
            config=config,
            process_manager=process_manager,
            tools_manager=tools_manager,
            decision_engine=decision_engine
        )
        
        print("✅ Flask应用创建成功")
        
        # 测试应用配置
        if hasattr(app, 'hexstrike_api'):
            print("✅ HexStrike API管理器附加成功")
        
        # 清理资源
        process_manager.cleanup_all_processes()
        
        return True
        
    except Exception as e:
        print(f"❌ API服务器测试失败: {e}")
        return False

def test_banner_display():
    """测试横幅显示"""
    print("\n🎯 测试横幅显示...")
    
    try:
        from hexstrike_ai import display_banner, get_version_info
        
        # 显示横幅
        banner = display_banner()
        print("✅ 横幅生成成功")
        
        # 显示版本信息
        version_info = get_version_info()
        print(f"✅ 版本信息获取成功: {version_info['version']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 横幅显示测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("HexStrike AI 重构系统功能测试")
    print("=" * 60)
    
    test_results = []
    
    # 执行各项测试
    tests = [
        ("基础模块导入", test_basic_imports),
        ("配置系统", test_configuration_system),
        ("日志系统", test_logging_system),
        ("核心组件", test_core_components),
        ("可视化引擎", test_visualization_engine),
        ("工具管理器", test_tools_manager),
        ("API服务器", test_api_server),
        ("横幅显示", test_banner_display),
    ]
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            test_results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            test_results.append((test_name, False))
    
    # 显示测试结果摘要
    print("\n" + "=" * 60)
    print("📊 测试结果摘要:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, success in test_results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    total = len(test_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print("=" * 60)
    print(f"总计测试: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {failed}")
    print(f"成功率: {success_rate:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有测试通过！重构系统工作正常。")
        print("🚀 您可以使用以下命令启动服务器:")
        print("   python3 hexstrike_server_new.py")
        exit_code = 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查错误信息。")
        exit_code = 1
    
    return exit_code

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试脚本异常: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        sys.exit(1)