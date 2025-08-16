#!/usr/bin/env python3
"""
HexStrike AI - 简单测试脚本
Simple Test Script
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试基础导入"""
    print("测试模块导入...")
    
    try:
        # 测试主包导入
        import hexstrike_ai
        print(f"导入hexstrike_ai成功 - 版本: {hexstrike_ai.__version__}")
        
        # 测试配置导入
        from hexstrike_ai.config import settings
        print("导入配置模块成功")
        
        # 测试颜色配置
        from hexstrike_ai.config.colors import HexStrikeColors
        print("导入颜色配置成功")
        
        # 测试日志配置
        from hexstrike_ai.config.logger_config import get_logger
        print("导入日志系统成功")
        
        return True
        
    except Exception as e:
        print(f"导入失败: {e}")
        return False

def test_configuration():
    """测试配置系统"""
    print("\n测试配置系统...")
    
    try:
        from hexstrike_ai.config import get_config
        
        config = get_config()
        print("获取配置成功")
        
        print(f"服务器地址: {config.server.host}:{config.server.port}")
        print(f"缓存状态: {config.cache.enabled}")
        print(f"AI引擎: {config.ai.decision_engine_enabled}")
        
        return True
        
    except Exception as e:
        print(f"配置测试失败: {e}")
        return False

def test_logging():
    """测试日志系统"""
    print("\n测试日志系统...")
    
    try:
        from hexstrike_ai.config.logger_config import get_logger
        
        logger = get_logger('测试')
        print("创建日志器成功")
        
        logger.info("测试信息日志")
        logger.warning("测试警告日志")
        
        return True
        
    except Exception as e:
        print(f"日志测试失败: {e}")
        return False

def main():
    """主函数"""
    print("HexStrike AI 重构系统基础测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("配置系统", test_configuration),
        ("日志系统", test_logging),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"{name}测试异常: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("测试结果:")
    
    passed = 0
    for name, success in results:
        status = "通过" if success else "失败"
        print(f"{name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {len(results)}, 通过: {passed}, 失败: {len(results) - passed}")
    
    if passed == len(results):
        print("\n所有基础测试通过！系统重构成功。")
        return 0
    else:
        print("\n部分测试失败，请检查错误。")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"测试脚本异常: {e}")
        sys.exit(1)