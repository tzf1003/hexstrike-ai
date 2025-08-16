#!/usr/bin/env python3
"""
HexStrike AI - MCP Web应用安全工具
MCP Web Application Security Tools

这个模块提供了Web应用安全相关的MCP工具函数，包括：
- 目录扫描工具
- 漏洞扫描工具
- Web爬虫工具
- 中文化的日志和错误处理
"""

from typing import Dict, Any
from ...config.logger_config import get_logger

class WebTools:
    """Web应用安全工具集合"""
    
    def __init__(self, hexstrike_client):
        """初始化Web应用安全工具
        
        Args:
            hexstrike_client: HexStrike MCP客户端实例
        """
        self.client = hexstrike_client
        self.logger = get_logger('WebTools')
    
    def gobuster_scan(self,
                      url: str,
                      mode: str = "dir",
                      wordlist: str = "/usr/share/wordlists/dirb/common.txt",
                      extensions: str = "",
                      additional_args: str = "") -> Dict[str, Any]:
        """执行Gobuster目录/子域名扫描
        
        Args:
            url: 目标URL
            mode: 扫描模式 (dir, dns, fuzz, vhost)
            wordlist: 字典文件路径
            extensions: 文件扩展名 (用于目录扫描)
            additional_args: 额外的Gobuster参数
            
        Returns:
            扫描结果字典，包含发现的目录或子域名
        """
        self.logger.info(f"📁 启动Gobuster {mode} 扫描: {url}")
        
        data = {
            "url": url,
            "mode": mode,
            "wordlist": wordlist,
            "extensions": extensions,
            "additional_args": additional_args,
            "use_recovery": True
        }
        
        result = self.client.safe_post("api/tools/gobuster", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Gobuster扫描完成: {url}")
            
            # 统计发现的内容
            data = result.get("data", {})
            if mode == "dir" and "directories" in data:
                dir_count = len(data["directories"])
                self.logger.info(f"🎯 发现目录: {dir_count} 个")
            elif mode == "dns" and "subdomains" in data:
                subdomain_count = len(data["subdomains"])
                self.logger.info(f"🎯 发现子域名: {subdomain_count} 个")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Gobuster扫描失败: {error}")
        
        return result
    
    def nuclei_scan(self,
                    target: str,
                    templates: str = "",
                    severity: str = "",
                    tags: str = "",
                    additional_args: str = "") -> Dict[str, Any]:
        """执行Nuclei漏洞扫描
        
        Args:
            target: 扫描目标URL或主机
            templates: 模板过滤 (例如: "cves/", "exposures/")
            severity: 严重性过滤 (critical, high, medium, low, info)
            tags: 标签过滤
            additional_args: 额外参数
            
        Returns:
            漏洞扫描结果字典
        """
        self.logger.info(f"🎯 启动Nuclei漏洞扫描: {target}")
        
        data = {
            "target": target,
            "templates": templates,
            "severity": severity,
            "tags": tags,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/nuclei", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Nuclei扫描完成: {target}")
            
            # 统计发现的漏洞
            data = result.get("data", {})
            if "vulnerabilities" in data:
                vuln_count = len(data["vulnerabilities"])
                if vuln_count > 0:
                    self.logger.warning(f"🚨 发现漏洞: {vuln_count} 个")
                    
                    # 按严重性分类统计
                    severity_stats = {}
                    for vuln in data["vulnerabilities"]:
                        severity = vuln.get("severity", "unknown")
                        severity_stats[severity] = severity_stats.get(severity, 0) + 1
                    
                    for severity, count in severity_stats.items():
                        self.logger.info(f"  {severity}: {count} 个")
                else:
                    self.logger.info("✅ 未发现已知漏洞")
                    
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Nuclei扫描失败: {error}")
        
        return result
    
    def sqlmap_scan(self,
                    url: str,
                    data: str = "",
                    cookie: str = "",
                    level: int = 1,
                    risk: int = 1,
                    additional_args: str = "") -> Dict[str, Any]:
        """执行SQLMap SQL注入测试
        
        Args:
            url: 目标URL
            data: POST数据
            cookie: Cookie值
            level: 测试级别 (1-5)
            risk: 风险级别 (1-3)
            additional_args: 额外参数
            
        Returns:
            SQL注入测试结果
        """
        self.logger.info(f"💉 启动SQLMap SQL注入测试: {url}")
        
        request_data = {
            "url": url,
            "data": data,
            "cookie": cookie,
            "level": level,
            "risk": risk,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/sqlmap", request_data)
        
        if result.get("success"):
            self.logger.success(f"✅ SQLMap测试完成: {url}")
            
            # 检查注入结果
            data = result.get("data", {})
            if "injectable_parameters" in data:
                injectable = data["injectable_parameters"]
                if injectable:
                    self.logger.critical(f"🚨 发现SQL注入漏洞: {len(injectable)} 个参数")
                else:
                    self.logger.info("✅ 未发现SQL注入漏洞")
                    
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ SQLMap测试失败: {error}")
        
        return result
    
    def ffuf_scan(self,
                  url: str,
                  wordlist: str,
                  mode: str = "dir",
                  extensions: str = "",
                  match_codes: str = "200,204,301,302,307,401,403",
                  additional_args: str = "") -> Dict[str, Any]:
        """执行FFUF Web模糊测试
        
        Args:
            url: 目标URL (包含FUZZ关键字)
            wordlist: 字典文件路径
            mode: 模糊测试模式
            extensions: 文件扩展名
            match_codes: 匹配的HTTP状态码
            additional_args: 额外参数
            
        Returns:
            模糊测试结果
        """
        self.logger.info(f"🔀 启动FFUF模糊测试: {url}")
        
        data = {
            "url": url,
            "wordlist": wordlist,
            "mode": mode,
            "extensions": extensions,
            "match_codes": match_codes,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/ffuf", data)
        
        if result.get("success"):
            self.logger.success(f"✅ FFUF测试完成: {url}")
            
            # 统计发现的内容
            data = result.get("data", {})
            if "results" in data:
                result_count = len(data["results"])
                self.logger.info(f"🎯 发现有效路径: {result_count} 个")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ FFUF测试失败: {error}")
        
        return result
    
    def nikto_scan(self,
                   host: str,
                   port: int = 80,
                   ssl: bool = False,
                   additional_args: str = "") -> Dict[str, Any]:
        """执行Nikto Web服务器扫描
        
        Args:
            host: 目标主机
            port: 目标端口
            ssl: 是否使用SSL
            additional_args: 额外参数
            
        Returns:
            Web服务器扫描结果
        """
        self.logger.info(f"🌐 启动Nikto Web服务器扫描: {host}:{port}")
        
        data = {
            "host": host,
            "port": port,
            "ssl": ssl,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/nikto", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Nikto扫描完成: {host}:{port}")
            
            # 统计发现的问题
            data = result.get("data", {})
            if "findings" in data:
                finding_count = len(data["findings"])
                if finding_count > 0:
                    self.logger.warning(f"⚠️  发现Web安全问题: {finding_count} 个")
                else:
                    self.logger.info("✅ 未发现明显的Web安全问题")
                    
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Nikto扫描失败: {error}")
        
        return result
    
    def katana_crawl(self,
                     url: str,
                     depth: int = 3,
                     concurrency: int = 10,
                     output_format: str = "json",
                     additional_args: str = "") -> Dict[str, Any]:
        """执行Katana Web爬虫
        
        Args:
            url: 起始URL
            depth: 爬取深度
            concurrency: 并发数
            output_format: 输出格式
            additional_args: 额外参数
            
        Returns:
            爬虫结果
        """
        self.logger.info(f"🕷️  启动Katana Web爬虫: {url}")
        
        data = {
            "url": url,
            "depth": depth,
            "concurrency": concurrency,
            "output_format": output_format,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/katana", data)
        
        if result.get("success"):
            self.logger.success(f"✅ Katana爬虫完成: {url}")
            
            # 统计爬取结果
            data = result.get("data", {})
            if "urls" in data:
                url_count = len(data["urls"])
                self.logger.info(f"🎯 发现URL: {url_count} 个")
                
            if "forms" in data:
                form_count = len(data["forms"])
                self.logger.info(f"📝 发现表单: {form_count} 个")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Katana爬虫失败: {error}")
        
        return result
    
    def httpx_probe(self,
                    target: str,
                    ports: str = "80,443,8080,8443",
                    threads: int = 50,
                    additional_args: str = "") -> Dict[str, Any]:
        """执行HTTPx HTTP探测
        
        Args:
            target: 目标地址或地址列表
            ports: 端口列表
            threads: 线程数
            additional_args: 额外参数
            
        Returns:
            HTTP探测结果
        """
        self.logger.info(f"🌐 启动HTTPx HTTP探测: {target}")
        
        data = {
            "target": target,
            "ports": ports,
            "threads": threads,
            "additional_args": additional_args
        }
        
        result = self.client.safe_post("api/tools/httpx", data)
        
        if result.get("success"):
            self.logger.success(f"✅ HTTPx探测完成: {target}")
            
            # 统计活跃的HTTP服务
            data = result.get("data", {})
            if "active_urls" in data:
                active_count = len(data["active_urls"])
                self.logger.info(f"🎯 发现活跃HTTP服务: {active_count} 个")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ HTTPx探测失败: {error}")
        
        return result