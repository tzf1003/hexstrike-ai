#!/usr/bin/env python3
"""
HexStrike AI - 全局设置配置
Global Settings Configuration

这个模块定义了HexStrike AI框架的全局配置参数，包括：
- API服务器配置
- 安全工具路径配置
- 缓存和性能配置
- 日志配置
- 超时和重试配置
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ServerConfig:
    """服务器配置类"""
    host: str = '127.0.0.1'
    port: int = 8888
    debug: bool = False
    max_workers: int = 10
    request_timeout: int = 300  # 5分钟
    max_request_size: int = 16 * 1024 * 1024  # 16MB
    
    def __post_init__(self):
        """初始化后处理，从环境变量读取配置"""
        self.host = os.environ.get('HEXSTRIKE_HOST', self.host)
        self.port = int(os.environ.get('HEXSTRIKE_PORT', self.port))
        self.debug = os.environ.get('HEXSTRIKE_DEBUG', '').lower() == 'true'

@dataclass
class CacheConfig:
    """缓存配置类"""
    enabled: bool = True
    max_size: int = 1000  # 最大缓存条目数
    default_ttl: int = 3600  # 默认TTL: 1小时
    cleanup_interval: int = 300  # 清理间隔: 5分钟
    memory_limit_mb: int = 512  # 内存限制: 512MB
    
@dataclass
class SecurityConfig:
    """安全配置类"""
    max_concurrent_scans: int = 5
    max_scan_duration: int = 7200  # 2小时
    allowed_targets: list = field(default_factory=list)
    blocked_targets: list = field(default_factory=list)
    require_authorization: bool = True
    api_key_header: str = 'X-HexStrike-API-Key'
    
@dataclass
class ToolsConfig:
    """工具配置类"""
    tools_directory: str = '/usr/bin'
    custom_tools_path: str = ''
    tool_timeout: int = 600  # 10分钟
    max_retries: int = 3
    retry_delay: int = 5  # 5秒
    health_check_interval: int = 60  # 1分钟
    
    def __post_init__(self):
        """检查工具路径配置"""
        if self.custom_tools_path:
            if not os.path.exists(self.custom_tools_path):
                print(f"⚠️  警告: 自定义工具路径不存在: {self.custom_tools_path}")

@dataclass
class AIConfig:
    """AI配置类"""
    decision_engine_enabled: bool = True
    max_decision_time: int = 30  # 30秒
    confidence_threshold: float = 0.7
    learning_enabled: bool = True
    model_cache_size: int = 100
    parallel_analysis: bool = True
    max_analysis_threads: int = 4

@dataclass
class LoggingConfig:
    """日志配置类"""
    level: str = 'INFO'
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_enabled: bool = True
    file_path: str = 'hexstrike.log'
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_enabled: bool = True
    colored_output: bool = True

class Settings:
    """HexStrike AI 全局设置管理器"""
    
    def __init__(self):
        """初始化设置"""
        self.server = ServerConfig()
        self.cache = CacheConfig()
        self.security = SecurityConfig()
        self.tools = ToolsConfig()
        self.ai = AIConfig()
        self.logging = LoggingConfig()
        
        # 从环境变量或配置文件加载设置
        self._load_from_environment()
        self._load_from_config_file()
    
    def _load_from_environment(self):
        """从环境变量加载配置"""
        # 服务器配置
        if 'HEXSTRIKE_MAX_WORKERS' in os.environ:
            self.server.max_workers = int(os.environ['HEXSTRIKE_MAX_WORKERS'])
        
        # 缓存配置
        if 'HEXSTRIKE_CACHE_SIZE' in os.environ:
            self.cache.max_size = int(os.environ['HEXSTRIKE_CACHE_SIZE'])
        
        # 工具配置
        if 'HEXSTRIKE_TOOLS_PATH' in os.environ:
            self.tools.custom_tools_path = os.environ['HEXSTRIKE_TOOLS_PATH']
        
        # AI配置
        if 'HEXSTRIKE_AI_THREADS' in os.environ:
            self.ai.max_analysis_threads = int(os.environ['HEXSTRIKE_AI_THREADS'])
        
        # 日志配置
        if 'HEXSTRIKE_LOG_LEVEL' in os.environ:
            self.logging.level = os.environ['HEXSTRIKE_LOG_LEVEL'].upper()
    
    def _load_from_config_file(self):
        """从配置文件加载设置"""
        config_file = Path('hexstrike_config.json')
        if config_file.exists():
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 更新配置
                if 'server' in config:
                    for key, value in config['server'].items():
                        if hasattr(self.server, key):
                            setattr(self.server, key, value)
                
                if 'cache' in config:
                    for key, value in config['cache'].items():
                        if hasattr(self.cache, key):
                            setattr(self.cache, key, value)
                
                print(f"✅ 成功加载配置文件: {config_file}")
                            
            except Exception as e:
                print(f"⚠️  警告: 无法加载配置文件 {config_file}: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """将设置转换为字典格式"""
        return {
            'server': {
                'host': self.server.host,
                'port': self.server.port,
                'debug': self.server.debug,
                'max_workers': self.server.max_workers
            },
            'cache': {
                'enabled': self.cache.enabled,
                'max_size': self.cache.max_size,
                'default_ttl': self.cache.default_ttl
            },
            'security': {
                'max_concurrent_scans': self.security.max_concurrent_scans,
                'require_authorization': self.security.require_authorization
            },
            'tools': {
                'tools_directory': self.tools.tools_directory,
                'tool_timeout': self.tools.tool_timeout,
                'max_retries': self.tools.max_retries
            },
            'ai': {
                'decision_engine_enabled': self.ai.decision_engine_enabled,
                'confidence_threshold': self.ai.confidence_threshold,
                'max_analysis_threads': self.ai.max_analysis_threads
            }
        }
    
    def save_to_file(self, filepath: str = 'hexstrike_config.json'):
        """保存设置到配置文件"""
        try:
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已保存到: {filepath}")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def validate(self) -> bool:
        """验证配置的有效性"""
        try:
            # 验证端口范围
            if not 1024 <= self.server.port <= 65535:
                print(f"❌ 无效的端口号: {self.server.port}")
                return False
            
            # 验证工具目录
            if not os.path.exists(self.tools.tools_directory):
                print(f"⚠️  工具目录不存在: {self.tools.tools_directory}")
            
            # 验证缓存配置
            if self.cache.max_size <= 0:
                print(f"❌ 无效的缓存大小: {self.cache.max_size}")
                return False
            
            # 验证AI配置
            if not 0.0 <= self.ai.confidence_threshold <= 1.0:
                print(f"❌ 无效的置信度阈值: {self.ai.confidence_threshold}")
                return False
            
            print("✅ 配置验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置验证失败: {e}")
            return False

# 全局设置实例
settings = Settings()

def get_config() -> Settings:
    """获取全局配置实例"""
    return settings

def reload_config():
    """重新加载配置"""
    global settings
    settings = Settings()
    print("🔄 配置已重新加载")
    return settings