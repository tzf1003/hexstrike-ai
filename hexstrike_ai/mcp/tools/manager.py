#!/usr/bin/env python3
"""
HexStrike AI - MCP工具管理器
MCP Tools Manager

这个模块提供了MCP工具函数的统一管理，包括：
- 工具函数注册和分类
- 工具执行统计和监控
- 中文化的工具描述和日志
- 错误处理和恢复
"""

from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from dataclasses import dataclass, field
from functools import wraps

from ...config.logger_config import get_logger
from ...config.colors import HexStrikeColors

@dataclass
class ToolMetrics:
    """工具执行指标"""
    name: str
    category: str
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_duration: float = 0.0
    last_called: Optional[datetime] = None
    last_error: Optional[str] = None
    average_duration: float = 0.0

@dataclass
class ToolInfo:
    """工具信息"""
    name: str
    category: str
    description: str
    chinese_description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

class MCPToolsManager:
    """MCP工具管理器 - 统一管理所有MCP工具函数"""
    
    def __init__(self, hexstrike_client):
        """初始化工具管理器
        
        Args:
            hexstrike_client: HexStrike MCP客户端实例
        """
        self.client = hexstrike_client
        self.logger = get_logger('MCP-ToolsManager')
        
        # 工具注册表
        self.tools: Dict[str, ToolInfo] = {}
        self.tool_categories: Dict[str, List[str]] = {}
        self.tool_metrics: Dict[str, ToolMetrics] = {}
        
        # 工具分类定义
        self.categories = {
            'network': '网络侦察',
            'web': 'Web应用安全',
            'system': '系统工具',
            'analysis': '分析工具',
            'intelligence': '情报收集',
            'reporting': '报告生成'
        }
        
        self.logger.info("🛠️  MCP工具管理器初始化完成")
        
        # 注册所有工具
        self._register_all_tools()
    
    def register_tool(self, 
                     name: str,
                     category: str,
                     description: str,
                     chinese_description: str,
                     function: Callable,
                     parameters: Optional[Dict[str, Any]] = None,
                     examples: Optional[List[str]] = None,
                     tags: Optional[List[str]] = None):
        """注册工具函数
        
        Args:
            name: 工具名称
            category: 工具分类
            description: 英文描述
            chinese_description: 中文描述
            function: 工具函数
            parameters: 参数定义
            examples: 使用示例
            tags: 标签列表
        """
        if parameters is None:
            parameters = {}
        if examples is None:
            examples = []
        if tags is None:
            tags = []
        
        # 创建工具信息
        tool_info = ToolInfo(
            name=name,
            category=category,
            description=description,
            chinese_description=chinese_description,
            function=function,
            parameters=parameters,
            examples=examples,
            tags=tags
        )
        
        # 注册工具
        self.tools[name] = tool_info
        
        # 更新分类索引
        if category not in self.tool_categories:
            self.tool_categories[category] = []
        self.tool_categories[category].append(name)
        
        # 初始化指标
        self.tool_metrics[name] = ToolMetrics(
            name=name,
            category=category
        )
        
        self.logger.debug(f"🔧 注册工具: {name} ({chinese_description})")
    
    def create_monitored_tool(self, tool_info: ToolInfo):
        """创建带监控的工具函数包装器"""
        
        @wraps(tool_info.function)
        def monitored_function(*args, **kwargs):
            """监控工具函数执行"""
            start_time = datetime.now()
            tool_name = tool_info.name
            
            self.logger.info(f"🚀 开始执行工具: {tool_info.chinese_description} ({tool_name})")
            
            # 更新调用统计
            metrics = self.tool_metrics[tool_name]
            metrics.total_calls += 1
            metrics.last_called = start_time
            
            try:
                # 执行工具函数
                result = tool_info.function(*args, **kwargs)
                
                # 计算执行时间
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # 更新成功统计
                metrics.successful_calls += 1
                metrics.total_duration += duration
                metrics.average_duration = metrics.total_duration / metrics.total_calls
                
                self.logger.success(f"✅ 工具执行成功: {tool_info.chinese_description}, 耗时: {duration:.2f}秒")
                
                # 检查结果中的漏洞信息
                if isinstance(result, dict) and result.get('success'):
                    data = result.get('data', {})
                    if 'vulnerabilities_found' in data:
                        vuln_count = data['vulnerabilities_found']
                        if vuln_count > 0:
                            self.logger.warning(f"🎯 发现 {vuln_count} 个安全问题")
                
                return result
                
            except Exception as e:
                # 计算执行时间
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # 更新失败统计
                metrics.failed_calls += 1
                metrics.total_duration += duration
                metrics.last_error = str(e)
                metrics.average_duration = metrics.total_duration / metrics.total_calls
                
                error_msg = f"工具执行异常: {str(e)}"
                self.logger.error(f"❌ {tool_info.chinese_description} 执行失败: {error_msg}")
                
                return {
                    "success": False,
                    "error": error_msg,
                    "tool_name": tool_name,
                    "duration": duration
                }
        
        return monitored_function
    
    def _register_all_tools(self):
        """注册所有工具函数"""
        self.logger.info("📋 开始注册所有MCP工具函数...")
        
        # 注册网络扫描工具
        self._register_network_tools()
        
        # 注册Web应用工具
        self._register_web_tools()
        
        # 注册系统工具
        self._register_system_tools()
        
        # 注册分析工具
        self._register_analysis_tools()
        
        total_tools = len(self.tools)
        categories_count = len(self.tool_categories)
        
        self.logger.success(f"✅ 工具注册完成: {total_tools} 个工具，{categories_count} 个分类")
        
        # 显示分类统计
        for category, tools in self.tool_categories.items():
            category_name = self.categories.get(category, category)
            self.logger.info(f"  📂 {category_name}: {len(tools)} 个工具")
    
    def _register_network_tools(self):
        """注册网络扫描工具"""
        
        def nmap_scan(target: str, 
                     scan_type: str = "-sV", 
                     ports: str = "", 
                     additional_args: str = ""):
            """执行Nmap网络扫描"""
            self.logger.info(f"🔍 启动Nmap扫描: {target}")
            
            data = {
                "target": target,
                "scan_type": scan_type,
                "ports": ports,
                "additional_args": additional_args,
                "use_recovery": True
            }
            
            result = self.client.safe_post("api/tools/nmap", data)
            
            if result.get("success"):
                # 检查恢复信息
                if result.get("recovery_info", {}).get("recovery_applied"):
                    recovery_info = result["recovery_info"]
                    attempts = recovery_info.get("attempts_made", 1)
                    self.logger.info(f"🔄 应用了故障恢复: {attempts} 次尝试")
            
            return result
        
        def masscan_scan(target: str, 
                        ports: str = "1-65535", 
                        rate: str = "1000"):
            """执行Masscan高速端口扫描"""
            self.logger.info(f"⚡ 启动Masscan高速扫描: {target}")
            
            data = {
                "target": target,
                "ports": ports,
                "rate": rate
            }
            
            return self.client.safe_post("api/tools/masscan", data)
        
        # 注册网络工具
        self.register_tool(
            name="nmap_scan",
            category="network",
            description="Execute Nmap network scan",
            chinese_description="执行Nmap网络扫描",
            function=nmap_scan,
            parameters={
                "target": {"type": "str", "required": True, "description": "扫描目标IP或域名"},
                "scan_type": {"type": "str", "default": "-sV", "description": "扫描类型"},
                "ports": {"type": "str", "default": "", "description": "端口范围"},
                "additional_args": {"type": "str", "default": "", "description": "额外参数"}
            },
            examples=[
                "nmap_scan('192.168.1.1')",
                "nmap_scan('example.com', scan_type='-sS', ports='80,443')"
            ],
            tags=["network", "scanning", "ports"]
        )
        
        self.register_tool(
            name="masscan_scan", 
            category="network",
            description="Execute Masscan high-speed port scan",
            chinese_description="执行Masscan高速端口扫描",
            function=masscan_scan,
            parameters={
                "target": {"type": "str", "required": True, "description": "扫描目标"},
                "ports": {"type": "str", "default": "1-65535", "description": "端口范围"},
                "rate": {"type": "str", "default": "1000", "description": "扫描速率"}
            },
            examples=[
                "masscan_scan('192.168.1.0/24')",
                "masscan_scan('example.com', ports='80,443,8080', rate='500')"
            ],
            tags=["network", "scanning", "fast"]
        )
    
    def _register_web_tools(self):
        """注册Web应用安全工具"""
        
        def gobuster_scan(url: str,
                         mode: str = "dir",
                         wordlist: str = "/usr/share/wordlists/dirb/common.txt",
                         additional_args: str = ""):
            """执行Gobuster目录/子域名扫描"""
            self.logger.info(f"📁 启动Gobuster {mode} 扫描: {url}")
            
            data = {
                "url": url,
                "mode": mode,
                "wordlist": wordlist,
                "additional_args": additional_args,
                "use_recovery": True
            }
            
            return self.client.safe_post("api/tools/gobuster", data)
        
        def nuclei_scan(target: str,
                       templates: str = "",
                       severity: str = "",
                       additional_args: str = ""):
            """执行Nuclei漏洞扫描"""
            self.logger.info(f"🎯 启动Nuclei漏洞扫描: {target}")
            
            data = {
                "target": target,
                "templates": templates,
                "severity": severity,
                "additional_args": additional_args
            }
            
            return self.client.safe_post("api/tools/nuclei", data)
        
        # 注册Web工具
        self.register_tool(
            name="gobuster_scan",
            category="web",
            description="Execute Gobuster directory/subdomain scan",
            chinese_description="执行Gobuster目录/子域名扫描",
            function=gobuster_scan,
            parameters={
                "url": {"type": "str", "required": True, "description": "目标URL"},
                "mode": {"type": "str", "default": "dir", "description": "扫描模式"},
                "wordlist": {"type": "str", "default": "/usr/share/wordlists/dirb/common.txt", "description": "字典文件"},
                "additional_args": {"type": "str", "default": "", "description": "额外参数"}
            },
            examples=[
                "gobuster_scan('http://example.com')",
                "gobuster_scan('http://example.com', mode='dns', wordlist='/path/to/subdomains.txt')"
            ],
            tags=["web", "directory", "fuzzing"]
        )
        
        self.register_tool(
            name="nuclei_scan",
            category="web", 
            description="Execute Nuclei vulnerability scan",
            chinese_description="执行Nuclei漏洞扫描",
            function=nuclei_scan,
            parameters={
                "target": {"type": "str", "required": True, "description": "扫描目标"},
                "templates": {"type": "str", "default": "", "description": "模板过滤"},
                "severity": {"type": "str", "default": "", "description": "严重性过滤"},
                "additional_args": {"type": "str", "default": "", "description": "额外参数"}
            },
            examples=[
                "nuclei_scan('http://example.com')",
                "nuclei_scan('http://example.com', severity='high,critical')"
            ],
            tags=["web", "vulnerability", "scanning"]
        )
    
    def _register_system_tools(self):
        """注册系统工具"""
        
        def execute_command(command: str, 
                           use_cache: bool = True,
                           timeout: int = 300):
            """执行系统命令"""
            self.logger.info(f"💻 执行系统命令: {command}")
            
            return self.client.execute_command(command, use_cache, timeout)
        
        def check_health():
            """检查服务器健康状态"""
            self.logger.info("💓 检查服务器健康状态")
            return self.client.check_health()
        
        # 注册系统工具
        self.register_tool(
            name="execute_command",
            category="system",
            description="Execute system command",
            chinese_description="执行系统命令",
            function=execute_command,
            parameters={
                "command": {"type": "str", "required": True, "description": "要执行的命令"},
                "use_cache": {"type": "bool", "default": True, "description": "是否使用缓存"},
                "timeout": {"type": "int", "default": 300, "description": "超时时间(秒)"}
            },
            examples=[
                "execute_command('ls -la')",
                "execute_command('ping -c 4 google.com', use_cache=False)"
            ],
            tags=["system", "command", "shell"]
        )
        
        self.register_tool(
            name="check_health",
            category="system",
            description="Check server health status",
            chinese_description="检查服务器健康状态",
            function=check_health,
            parameters={},
            examples=["check_health()"],
            tags=["system", "health", "monitoring"]
        )
    
    def _register_analysis_tools(self):
        """注册分析工具"""
        
        def analyze_target(target: str, analysis_type: str = "comprehensive"):
            """AI智能目标分析"""
            self.logger.info(f"🧠 启动AI目标分析: {target}")
            
            data = {
                "target": target,
                "analysis_type": analysis_type
            }
            
            return self.client.safe_post("api/intelligence/analyze-target", data)
        
        # 注册分析工具
        self.register_tool(
            name="analyze_target",
            category="intelligence",
            description="AI-powered target analysis",
            chinese_description="AI智能目标分析",
            function=analyze_target,
            parameters={
                "target": {"type": "str", "required": True, "description": "分析目标"},
                "analysis_type": {"type": "str", "default": "comprehensive", "description": "分析类型"}
            },
            examples=[
                "analyze_target('example.com')",
                "analyze_target('192.168.1.1', analysis_type='basic')"
            ],
            tags=["intelligence", "ai", "analysis"]
        )
    
    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """获取工具信息"""
        return self.tools.get(name)
    
    def get_tools_by_category(self, category: str) -> List[ToolInfo]:
        """按分类获取工具"""
        tool_names = self.tool_categories.get(category, [])
        return [self.tools[name] for name in tool_names]
    
    def get_all_tools(self) -> Dict[str, ToolInfo]:
        """获取所有工具"""
        return self.tools.copy()
    
    def get_tool_metrics(self, name: str) -> Optional[ToolMetrics]:
        """获取工具执行指标"""
        return self.tool_metrics.get(name)
    
    def get_tools_summary(self) -> Dict[str, Any]:
        """获取工具摘要信息"""
        total_tools = len(self.tools)
        total_calls = sum(m.total_calls for m in self.tool_metrics.values())
        successful_calls = sum(m.successful_calls for m in self.tool_metrics.values())
        
        categories_summary = {}
        for category, tool_names in self.tool_categories.items():
            category_metrics = [self.tool_metrics[name] for name in tool_names]
            categories_summary[category] = {
                'chinese_name': self.categories.get(category, category),
                'tool_count': len(tool_names),
                'total_calls': sum(m.total_calls for m in category_metrics),
                'successful_calls': sum(m.successful_calls for m in category_metrics)
            }
        
        return {
            'total_tools': total_tools,
            'total_categories': len(self.tool_categories),
            'total_calls': total_calls,
            'successful_calls': successful_calls,
            'success_rate': (successful_calls / max(1, total_calls)) * 100,
            'categories': categories_summary
        }