#!/usr/bin/env python3
"""
HexStrike AI - MCP系统工具
MCP System Tools

这个模块提供了系统相关的MCP工具函数，包括：
- 命令执行工具
- 系统信息收集
- 文件操作工具
- 中文化的日志和错误处理
"""

from typing import Dict, Any
from ...config.logger_config import get_logger

class SystemTools:
    """系统工具集合"""
    
    def __init__(self, hexstrike_client):
        """初始化系统工具
        
        Args:
            hexstrike_client: HexStrike MCP客户端实例
        """
        self.client = hexstrike_client
        self.logger = get_logger('SystemTools')
    
    def execute_command(self,
                       command: str,
                       use_cache: bool = True,
                       timeout: int = 300,
                       working_directory: str = "") -> Dict[str, Any]:
        """执行系统命令
        
        Args:
            command: 要执行的命令
            use_cache: 是否使用缓存
            timeout: 超时时间(秒)
            working_directory: 工作目录
            
        Returns:
            命令执行结果
        """
        self.logger.info(f"💻 执行系统命令: {command}")
        
        # 安全检查 - 阻止危险命令
        dangerous_commands = [
            'rm -rf /', 'del /f /s /q', 'format', 'fdisk',
            'mkfs', 'dd if=', 'shutdown', 'reboot', 'halt'
        ]
        
        command_lower = command.lower()
        for dangerous in dangerous_commands:
            if dangerous in command_lower:
                self.logger.error(f"🚫 拒绝执行危险命令: {command}")
                return {
                    "success": False,
                    "error": f"出于安全考虑，拒绝执行危险命令: {dangerous}",
                    "command": command
                }
        
        request_data = {
            "command": command,
            "use_cache": use_cache,
            "timeout": timeout
        }
        
        if working_directory:
            request_data["working_directory"] = working_directory
        
        result = self.client.safe_post("api/command", request_data)
        
        if result.get("success"):
            duration = result.get("duration", 0)
            self.logger.success(f"✅ 命令执行成功，耗时: {duration:.2f}秒")
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 命令执行失败: {error}")
        
        return result
    
    def check_health(self) -> Dict[str, Any]:
        """检查服务器健康状态
        
        Returns:
            服务器健康状态信息
        """
        self.logger.info("💓 检查服务器健康状态")
        
        result = self.client.check_health()
        
        if result.get("success"):
            data = result.get("data", {})
            status = data.get("status", "unknown")
            self.logger.success(f"✅ 服务器健康状态: {status}")
            
            # 显示详细信息
            if "uptime" in data:
                uptime = data["uptime"]
                self.logger.info(f"⏱️  服务器运行时间: {uptime}")
            
            if "tools" in data:
                tools_info = data["tools"]
                available = tools_info.get("available_tools", 0)
                total = tools_info.get("total_tools", 0)
                self.logger.info(f"🛠️  工具状态: {available}/{total} 可用")
                
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 健康检查失败: {error}")
        
        return result
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息
        
        Returns:
            系统信息字典
        """
        self.logger.info("📊 获取系统信息")
        
        # 根据操作系统执行不同的命令
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            commands = [
                ("hostname", "主机名"),
                ("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"", "操作系统"),
                ("wmic cpu get name", "CPU信息"),
                ("wmic computersystem get TotalPhysicalMemory", "内存信息")
            ]
        else:
            commands = [
                ("hostname", "主机名"),
                ("uname -a", "系统内核"),
                ("cat /proc/cpuinfo | grep 'model name' | head -1", "CPU信息"),
                ("free -h", "内存信息"),
                ("df -h", "磁盘信息")
            ]
        
        system_info = {}
        
        for cmd, description in commands:
            self.logger.debug(f"🔍 获取{description}...")
            result = self.execute_command(cmd, use_cache=True)
            
            if result.get("success"):
                output = result.get("stdout", "").strip()
                system_info[description] = output
            else:
                system_info[description] = "获取失败"
        
        self.logger.success("✅ 系统信息收集完成")
        
        return {
            "success": True,
            "data": {
                "system_info": system_info,
                "platform": platform.platform(),
                "python_version": platform.python_version()
            },
            "message": "系统信息获取成功"
        }
    
    def get_network_info(self) -> Dict[str, Any]:
        """获取网络信息
        
        Returns:
            网络信息字典
        """
        self.logger.info("🌐 获取网络信息")
        
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            commands = [
                ("ipconfig", "网络配置"),
                ("netstat -an | findstr LISTEN", "监听端口"),
                ("arp -a", "ARP表")
            ]
        else:
            commands = [
                ("ip addr show", "网络接口"),
                ("netstat -tuln", "监听端口"),
                ("route -n", "路由表")
            ]
        
        network_info = {}
        
        for cmd, description in commands:
            self.logger.debug(f"🔍 获取{description}...")
            result = self.execute_command(cmd, use_cache=True)
            
            if result.get("success"):
                output = result.get("stdout", "").strip()
                network_info[description] = output
            else:
                network_info[description] = "获取失败"
        
        self.logger.success("✅ 网络信息收集完成")
        
        return {
            "success": True,
            "data": {"network_info": network_info},
            "message": "网络信息获取成功"
        }
    
    def get_process_list(self, filter_name: str = "") -> Dict[str, Any]:
        """获取进程列表
        
        Args:
            filter_name: 过滤进程名称
            
        Returns:
            进程列表
        """
        self.logger.info(f"📋 获取进程列表{f' (过滤: {filter_name})' if filter_name else ''}")
        
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = "tasklist"
            if filter_name:
                cmd += f" | findstr /i {filter_name}"
        else:
            cmd = "ps aux"
            if filter_name:
                cmd += f" | grep {filter_name}"
        
        result = self.execute_command(cmd, use_cache=False)
        
        if result.get("success"):
            output = result.get("stdout", "")
            lines = output.strip().split('\n')
            process_count = max(0, len(lines) - 1)  # 减去标题行
            
            self.logger.success(f"✅ 进程列表获取成功: {process_count} 个进程")
            
            return {
                "success": True,
                "data": {
                    "process_list": output,
                    "process_count": process_count,
                    "filter": filter_name
                },
                "message": "进程列表获取成功"
            }
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 进程列表获取失败: {error}")
            return result
    
    def check_file_exists(self, file_path: str) -> Dict[str, Any]:
        """检查文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件存在性检查结果
        """
        self.logger.info(f"📁 检查文件是否存在: {file_path}")
        
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = f'if exist "{file_path}" echo EXISTS else echo NOT_EXISTS'
        else:
            cmd = f'if [ -f "{file_path}" ]; then echo EXISTS; else echo NOT_EXISTS; fi'
        
        result = self.execute_command(cmd, use_cache=True)
        
        if result.get("success"):
            output = result.get("stdout", "").strip()
            exists = "EXISTS" in output
            
            self.logger.info(f"📁 文件存在性: {file_path} - {'存在' if exists else '不存在'}")
            
            return {
                "success": True,
                "data": {
                    "file_path": file_path,
                    "exists": exists,
                    "check_output": output
                },
                "message": f"文件{'存在' if exists else '不存在'}"
            }
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 文件存在性检查失败: {error}")
            return result
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息
        """
        self.logger.info(f"📄 获取文件信息: {file_path}")
        
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = f'dir "{file_path}"'
        else:
            cmd = f'ls -la "{file_path}"'
        
        result = self.execute_command(cmd, use_cache=True)
        
        if result.get("success"):
            output = result.get("stdout", "").strip()
            self.logger.success(f"✅ 文件信息获取成功: {file_path}")
            
            return {
                "success": True,
                "data": {
                    "file_path": file_path,
                    "file_info": output
                },
                "message": "文件信息获取成功"
            }
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ 文件信息获取失败: {error}")
            return result
    
    def ping_host(self, 
                  host: str, 
                  count: int = 4, 
                  timeout: int = 5) -> Dict[str, Any]:
        """Ping主机连通性测试
        
        Args:
            host: 目标主机
            count: 发送包数量
            timeout: 超时时间
            
        Returns:
            Ping测试结果
        """
        self.logger.info(f"📡 Ping连通性测试: {host}")
        
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = f"ping -n {count} {host}"
        else:
            cmd = f"ping -c {count} -W {timeout} {host}"
        
        result = self.execute_command(cmd, use_cache=False)
        
        if result.get("success"):
            output = result.get("stdout", "")
            
            # 简单解析ping结果
            if "时间=" in output or "time=" in output:
                self.logger.success(f"✅ Ping成功: {host} 可达")
                reachable = True
            else:
                self.logger.warning(f"⚠️  Ping失败: {host} 不可达")
                reachable = False
            
            return {
                "success": True,
                "data": {
                    "host": host,
                    "reachable": reachable,
                    "ping_output": output,
                    "count": count
                },
                "message": f"主机{'可达' if reachable else '不可达'}"
            }
        else:
            error = result.get("error", "未知错误")
            self.logger.error(f"❌ Ping测试失败: {error}")
            return result