#!/usr/bin/env python3
"""
HexStrike AI - MCP网络工具
MCP Network Tools

这个模块提供了网络安全相关的MCP工具函数，包括：
- 网络扫描工具
- 端口发现工具
- 服务识别工具
- 中文化的日志和错误处理
"""

from typing import Dict, Any
from ...config.logger_config import get_logger

class NetworkTools:
    """网络安全工具集合"""
    
    def __init__(self, hexstrike_client):
        """初始化网络工具
        
        Args:
            hexstrike_client: HexStrike MCP客户端实例
        """
        self.client = hexstrike_client
        self.logger = get_logger('NetworkTools')
    
    def nmap_scan(self, 
                  target: str, 
                  scan_type: str = "-sV", 
                  ports: str = "", 
                  additional_args: str = "") -> Dict[str, Any]:
        """执行Nmap网络扫描
        
        Args:
            target: 扫描目标IP地址或主机名
            scan_type: 扫描类型 (例如: -sV 版本检测, -sC 脚本扫描)
            ports: 端口列表或端口范围 (逗号分隔)
            additional_args: 额外的Nmap参数
            
        Returns:
            扫描结果字典，包含详细的扫描信息
        """
        self.logger.info(f"🔍 启动Nmap扫描: {target}")
        
        # 构建请求数据
        data = {
            "target": target,
            "scan_type": scan_type,
            "ports": ports,
            "additional_args": additional_args,
            "use_recovery": True  # 启用故障恢复
        }
        
        # 执行扫描
        result = self.client.safe_post("api/tools/nmap", data)
        
        # 处理结果
        if result.get("success"):
            self.logger.success(f"✅ Nmap扫描完成: {target}")
            
            # 检查恢复信息
            if result.get("recovery_info", {}).get("recovery_applied"):
                recovery_info = result["recovery_info"]
                attempts = recovery_info.get("attempts_made", 1)
                self.logger.info(f"🔄 应用了故障恢复: {attempts} 次尝试")
            
            # 检查发现的服务
            data = result.get("data", {})
            if "open_ports" in data:
                open_ports = data["open_ports"]
                self.logger.info(f"🎯 发现开放端口: {len(open_ports)} 个")
                
            if "services" in data:
                services = data["services"]
                self.logger.info(f"🛠️  识别的服务: {len(services)} 个")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Nmap扫描失败: {error}")
            
            # 检查是否需要人工干预
            if result.get("human_escalation"):
                self.logger.critical("🚨 需要人工干预")
        
        return result
    
    def masscan_scan(self, 
                     target: str, 
                     ports: str = "1-65535", 
                     rate: str = "1000",
                     additional_args: str = "") -> Dict[str, Any]:
        """执行Masscan高速端口扫描
        
        Args:
            target: 扫描目标
            ports: 端口范围 (例如: "1-1000", "80,443,8080")
            rate: 扫描速率 (每秒包数)
            additional_args: 额外参数
            
        Returns:
            扫描结果字典
        """
        self.logger.info(f"⚡ 启动Masscan高速扫描: {target}")
        
        data = {
            "target": target,
            "ports": ports,
            "rate": rate,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/masscan", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Masscan扫描完成: {target}")
            
            # 统计发现的端口
            data = result.get("data", {})
            if "open_ports" in data:
                port_count = len(data["open_ports"])
                self.logger.info(f"🎯 发现开放端口: {port_count} 个")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Masscan扫描失败: {error}")
        
        return result
    
    def rustscan_scan(self,
                      target: str,
                      ports: str = "1-65535",
                      timeout: str = "1500",
                      additional_args: str = "") -> Dict[str, Any]:
        """执行RustScan快速端口扫描
        
        Args:
            target: 扫描目标
            ports: 端口范围
            timeout: 超时时间(毫秒)
            additional_args: 额外参数
            
        Returns:
            扫描结果字典
        """
        self.logger.info(f"🦀 启动RustScan扫描: {target}")
        
        data = {
            "target": target,
            "ports": ports,
            "timeout": timeout,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/rustscan", data)
        
        if result.get("success"):
            self.logger.success(f"✅ RustScan扫描完成: {target}")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ RustScan扫描失败: {error}")
        
        return result
    
    def amass_scan(self,
                   domain: str,
                   mode: str = "enum",
                   passive: bool = True,
                   additional_args: str = "") -> Dict[str, Any]:
        """执行Amass子域名发现
        
        Args:
            domain: 目标域名
            mode: 扫描模式 (enum, intel, viz, track, db)
            passive: 是否仅使用被动方法
            additional_args: 额外参数
            
        Returns:
            子域名发现结果
        """
        self.logger.info(f"🌐 启动Amass子域名发现: {domain}")
        
        data = {
            "domain": domain,
            "mode": mode,
            "passive": passive,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/amass", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Amass扫描完成: {domain}")
            
            # 统计发现的子域名
            data = result.get("data", {})
            if "subdomains" in data:
                subdomain_count = len(data["subdomains"])
                self.logger.info(f"🎯 发现子域名: {subdomain_count} 个")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Amass扫描失败: {error}")
        
        return result
    
    def subfinder_scan(self,
                       domain: str,
                       silent: bool = False,
                       sources: str = "",
                       additional_args: str = "") -> Dict[str, Any]:
        """执行Subfinder子域名发现
        
        Args:
            domain: 目标域名
            silent: 静默模式
            sources: 指定数据源
            additional_args: 额外参数
            
        Returns:
            子域名发现结果
        """
        self.logger.info(f"🔍 启动Subfinder子域名发现: {domain}")
        
        data = {
            "domain": domain,
            "silent": silent,
            "sources": sources,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/subfinder", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Subfinder扫描完成: {domain}")
            
            # 统计结果
            data = result.get("data", {})
            if "subdomains" in data:
                subdomain_count = len(data["subdomains"])
                self.logger.info(f"🎯 发现子域名: {subdomain_count} 个")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Subfinder扫描失败: {error}")
        
        return result
    
    def ping_scan(self,
                  target: str,
                  count: int = 4,
                  timeout: int = 5) -> Dict[str, Any]:
        """执行Ping连通性测试
        
        Args:
            target: 目标地址
            count: 发送包数量
            timeout: 超时时间
            
        Returns:
            Ping测试结果
        """
        self.logger.info(f"📡 执行Ping测试: {target}")
        
        # 构建ping命令
        import platform
        if platform.system().lower() == "windows":
            command = f"ping -n {count} {target}"
        else:
            command = f"ping -c {count} -W {timeout} {target}"
        
        result = self.client.execute_command(command, use_cache=False)
        
        if result.get("success"):
            self.logger.success(f"✅ Ping测试完成: {target}")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Ping测试失败: {error}")
        
        return result