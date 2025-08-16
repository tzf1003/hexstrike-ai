#!/usr/bin/env python3
"""
HexStrike AI - 安全工具管理器
Security Tools Manager

这个模块提供了安全工具的统一管理功能，包括：
- 工具发现和注册
- 工具状态监控
- 工具执行调度
- 结果收集和处理
"""

import shutil
from typing import Dict, List, Any, Tuple, Optional
from ..config.logger_config import get_logger
from ..core.base_classes import SecurityTool

class SecurityToolsManager:
    """安全工具管理器"""
    
    def __init__(self):
        """初始化工具管理器"""
        self.logger = get_logger('ToolsManager')
        self.tools: Dict[str, SecurityTool] = {}
        self.tool_categories = {
            '网络侦察': [],
            'Web应用安全': [],
            '密码破解': [],
            '二进制分析': [],
            '云安全': [],
            'CTF工具': [],
            'OSINT情报': [],
            '漏洞扫描': [],
            '渗透测试': [],
            '取证分析': []
        }
        
        self.logger.info("🛠️  安全工具管理器初始化完成")
    
    def initialize_tools(self) -> int:
        """初始化所有工具
        
        Returns:
            可用工具数量
        """
        self.logger.info("🔍 开始检测安全工具...")
        
        # 定义常用安全工具
        common_tools = [
            # 网络侦察工具
            ('nmap', '网络侦察', 'Nmap网络扫描器'),
            ('masscan', '网络侦察', '高速端口扫描器'),
            ('rustscan', '网络侦察', 'Rust编写的快速端口扫描器'),
            ('amass', '网络侦察', '子域名发现工具'),
            ('subfinder', '网络侦察', '子域名枚举工具'),
            
            # Web应用安全工具
            ('nuclei', 'Web应用安全', '漏洞扫描器'),
            ('gobuster', 'Web应用安全', '目录/文件爆破工具'),
            ('ffuf', 'Web应用安全', 'Web模糊测试工具'),
            ('sqlmap', 'Web应用安全', 'SQL注入检测工具'),
            ('nikto', 'Web应用安全', 'Web服务器扫描器'),
            
            # 密码破解工具
            ('hydra', '密码破解', '在线密码爆破工具'),
            ('john', '密码破解', 'John the Ripper密码破解器'),
            ('hashcat', '密码破解', 'GPU加速密码破解器'),
            
            # 二进制分析工具
            ('ghidra', '二进制分析', 'NSA开源逆向工程工具'),
            ('radare2', '二进制分析', '逆向工程框架'),
            ('gdb', '二进制分析', 'GNU调试器'),
            ('binwalk', '二进制分析', '固件分析工具'),
            
            # 系统工具
            ('curl', '系统工具', 'HTTP客户端'),
            ('wget', '系统工具', '文件下载工具'),
            ('nc', '系统工具', 'Netcat网络工具'),
            ('ncat', '系统工具', 'Nmap版本的Netcat'),
        ]
        
        available_count = 0
        
        for tool_name, category, description in common_tools:
            if self._check_tool_availability(tool_name):
                tool = SecurityTool(tool_name, tool_name, description)
                tool.category = category
                tool.available = True
                
                self.tools[tool_name] = tool
                self.tool_categories[category].append(tool)
                available_count += 1
                
                self.logger.success(f"✅ 发现工具: {tool_name} ({category})")
            else:
                self.logger.debug(f"⚪ 工具不可用: {tool_name}")
        
        self.logger.success(f"🎯 工具检测完成: {available_count}/{len(common_tools)} 可用")
        return available_count
    
    def _check_tool_availability(self, tool_name: str) -> bool:
        """检查工具是否可用"""
        return shutil.which(tool_name) is not None
    
    def get_tool(self, tool_name: str) -> Optional[SecurityTool]:
        """获取指定工具"""
        return self.tools.get(tool_name)
    
    def get_available_tools(self) -> List[SecurityTool]:
        """获取所有可用工具"""
        return [tool for tool in self.tools.values() if tool.available]
    
    def get_tools_by_category(self, category: str) -> List[SecurityTool]:
        """按类别获取工具"""
        return self.tool_categories.get(category, [])
    
    def get_all_tools_status(self) -> Dict[str, Any]:
        """获取所有工具状态"""
        status = {
            'total_tools': len(self.tools),
            'available_tools': len(self.get_available_tools()),
            'categories': {}
        }
        
        for category, tools in self.tool_categories.items():
            available_tools = [tool for tool in tools if tool.available]
            status['categories'][category] = {
                'total': len(tools),
                'available': len(available_tools),
                'tools': [tool.name for tool in available_tools]
            }
        
        return status
    
    def get_tools_summary(self) -> Dict[str, Any]:
        """获取工具摘要信息"""
        total = len(self.tools)
        available = len(self.get_available_tools())
        
        return {
            'total_tools': total,
            'available_tools': available,
            'availability_rate': (available / total * 100) if total > 0 else 0,
            'categories_count': len(self.tool_categories)
        }
    
    def check_all_tools(self) -> Tuple[Dict[str, List[Dict]], Dict[str, List[Dict]]]:
        """检查所有工具可用性
        
        Returns:
            (可用工具字典, 不可用工具字典)
        """
        available_tools = {}
        unavailable_tools = {}
        
        for category in self.tool_categories:
            available_tools[category] = []
            unavailable_tools[category] = []
        
        for tool in self.tools.values():
            tool_info = {
                'name': tool.name,
                'description': tool.description,
                'version': tool.get_version()
            }
            
            if tool.available:
                category = tool.category
                if category in available_tools:
                    available_tools[category].append(tool_info)
            else:
                category = tool.category
                tool_info['reason'] = '未找到可执行文件'
                if category in unavailable_tools:
                    unavailable_tools[category].append(tool_info)
        
        return available_tools, unavailable_tools