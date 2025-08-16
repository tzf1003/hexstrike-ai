#!/usr/bin/env python3
"""
HexStrike AI - 进程管理器
Process Manager

这个模块提供了高级的进程管理功能，包括：
- 实时进程控制和监控
- 并发执行管理
- 进程资源监控
- 超时处理和故障恢复
- 进程生命周期管理
"""

import subprocess
import threading
import time
import signal
import os
import psutil
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, Future
import queue
from dataclasses import dataclass, field

from .base_classes import ProcessStatus
from ..config.logger_config import get_logger
from ..config.colors import HexStrikeColors

@dataclass
class ProcessInfo:
    """进程信息类"""
    pid: int                                    # 进程ID
    command: str                               # 执行命令
    status: ProcessStatus                      # 进程状态
    start_time: datetime                       # 开始时间
    end_time: Optional[datetime] = None        # 结束时间
    duration: float = 0.0                     # 运行时长
    cpu_usage: float = 0.0                    # CPU使用率
    memory_usage: float = 0.0                 # 内存使用量(MB)
    return_code: Optional[int] = None         # 返回代码
    stdout: str = ""                          # 标准输出
    stderr: str = ""                          # 错误输出
    timeout: int = 300                        # 超时时间
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    def update_stats(self):
        """更新进程统计信息"""
        try:
            if self.pid and psutil.pid_exists(self.pid):
                process = psutil.Process(self.pid)
                self.cpu_usage = process.cpu_percent()
                self.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
                
                if self.end_time:
                    self.duration = (self.end_time - self.start_time).total_seconds()
                else:
                    self.duration = (datetime.now() - self.start_time).total_seconds()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

class ProcessManager:
    """高级进程管理器"""
    
    def __init__(self, max_concurrent_processes: int = 10):
        """初始化进程管理器
        
        Args:
            max_concurrent_processes: 最大并发进程数
        """
        self.max_concurrent = max_concurrent_processes
        self.processes: Dict[int, ProcessInfo] = {}
        self.active_processes: Dict[int, subprocess.Popen] = {}
        self.process_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_processes)
        self.monitoring_active = False
        self.monitor_thread = None
        self.logger = get_logger('ProcessManager')
        
        # 启动监控线程
        self.start_monitoring()
        
        # 注册信号处理器
        self._register_signal_handlers()
    
    def _register_signal_handlers(self):
        """注册信号处理器"""
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except ValueError:
            # 在某些环境中可能无法注册信号处理器
            pass
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        self.logger.warning(f"⚠️  收到信号 {signum}，正在清理进程...")
        self.cleanup_all_processes()
    
    def start_monitoring(self):
        """启动进程监控"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_processes,
                daemon=True
            )
            self.monitor_thread.start()
            self.logger.info("📊 进程监控已启动")
    
    def stop_monitoring(self):
        """停止进程监控"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("📊 进程监控已停止")
    
    def _monitor_processes(self):
        """监控进程状态"""
        while self.monitoring_active:
            try:
                current_time = datetime.now()
                pids_to_remove = []
                
                for pid, process_info in self.processes.items():
                    # 更新进程统计信息
                    process_info.update_stats()
                    
                    # 检查超时
                    if (process_info.status == ProcessStatus.RUNNING and 
                        current_time - process_info.start_time > timedelta(seconds=process_info.timeout)):
                        self.logger.warning(f"⏰ 进程 {pid} 执行超时，正在终止...")
                        self.kill_process(pid)
                    
                    # 检查已完成的进程
                    if (process_info.status in [ProcessStatus.FINISHED, ProcessStatus.KILLED, ProcessStatus.ERROR] and
                        current_time - (process_info.end_time or process_info.start_time) > timedelta(minutes=10)):
                        pids_to_remove.append(pid)
                
                # 清理已完成的旧进程
                for pid in pids_to_remove:
                    self.processes.pop(pid, None)
                
                time.sleep(1)  # 每秒检查一次
                
            except Exception as e:
                self.logger.error(f"❌ 进程监控错误: {e}")
                time.sleep(5)
    
    def execute_command(self, 
                       command: str, 
                       timeout: int = 300,
                       cwd: str = None,
                       env: Dict[str, str] = None,
                       capture_output: bool = True,
                       shell: bool = True) -> Dict[str, Any]:
        """执行命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间(秒)
            cwd: 工作目录
            env: 环境变量
            capture_output: 是否捕获输出
            shell: 是否使用shell
            
        Returns:
            执行结果字典
        """
        self.logger.info(f"🚀 执行命令: {command}")
        
        start_time = datetime.now()
        
        try:
            # 创建进程
            if shell:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE if capture_output else None,
                    stderr=subprocess.PIPE if capture_output else None,
                    cwd=cwd,
                    env=env,
                    universal_newlines=True,
                    bufsize=1
                )
            else:
                process = subprocess.Popen(
                    command.split(),
                    stdout=subprocess.PIPE if capture_output else None,
                    stderr=subprocess.PIPE if capture_output else None,
                    cwd=cwd,
                    env=env,
                    universal_newlines=True,
                    bufsize=1
                )
            
            pid = process.pid
            
            # 创建进程信息
            process_info = ProcessInfo(
                pid=pid,
                command=command,
                status=ProcessStatus.RUNNING,
                start_time=start_time,
                timeout=timeout
            )
            
            # 注册进程
            self.processes[pid] = process_info
            self.active_processes[pid] = process
            
            self.logger.info(f"📝 进程已启动: PID={pid}")
            
            # 等待进程完成或超时
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return_code = process.returncode
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # 更新进程信息
                process_info.end_time = end_time
                process_info.duration = duration
                process_info.return_code = return_code
                process_info.stdout = stdout or ""
                process_info.stderr = stderr or ""
                process_info.status = ProcessStatus.FINISHED
                
                # 清理活跃进程记录
                self.active_processes.pop(pid, None)
                
                self.logger.success(f"✅ 进程完成: PID={pid}, 返回码={return_code}, 耗时={duration:.2f}秒")
                
                return {
                    'pid': pid,
                    'return_code': return_code,
                    'stdout': stdout or "",
                    'stderr': stderr or "",
                    'duration': duration,
                    'command': command
                }
                
            except subprocess.TimeoutExpired:
                self.logger.warning(f"⏰ 进程超时: PID={pid}")
                
                # 终止进程
                self.kill_process(pid)
                
                return {
                    'pid': pid,
                    'return_code': -1,
                    'stdout': "",
                    'stderr': f"进程执行超时 ({timeout}秒)",
                    'duration': timeout,
                    'command': command,
                    'timeout': True
                }
        
        except Exception as e:
            self.logger.error(f"❌ 执行命令失败: {e}")
            return {
                'pid': -1,
                'return_code': -1,
                'stdout': "",
                'stderr': f"执行失败: {e}",
                'duration': 0,
                'command': command,
                'error': str(e)
            }
    
    def execute_command_async(self, 
                             command: str, 
                             timeout: int = 300,
                             callback: Callable = None,
                             **kwargs) -> Future:
        """异步执行命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间
            callback: 完成时的回调函数
            **kwargs: 其他参数
            
        Returns:
            Future对象
        """
        def _execute_with_callback():
            result = self.execute_command(command, timeout, **kwargs)
            if callback:
                try:
                    callback(result)
                except Exception as e:
                    self.logger.error(f"❌ 回调函数执行失败: {e}")
            return result
        
        future = self.executor.submit(_execute_with_callback)
        self.logger.info(f"🔄 异步执行命令: {command}")
        return future
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """终止进程
        
        Args:
            pid: 进程ID
            force: 是否强制终止
            
        Returns:
            是否成功终止
        """
        try:
            if pid in self.active_processes:
                process = self.active_processes[pid]
                
                if force:
                    # 强制终止
                    process.kill()
                    self.logger.warning(f"💀 强制终止进程: PID={pid}")
                else:
                    # 优雅终止
                    process.terminate()
                    self.logger.info(f"🛑 终止进程: PID={pid}")
                
                # 等待进程结束
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # 如果优雅终止失败，则强制终止
                    if not force:
                        process.kill()
                        process.wait()
                        self.logger.warning(f"💀 优雅终止失败，强制终止进程: PID={pid}")
                
                # 更新进程状态
                if pid in self.processes:
                    self.processes[pid].status = ProcessStatus.KILLED
                    self.processes[pid].end_time = datetime.now()
                
                # 清理记录
                self.active_processes.pop(pid, None)
                
                return True
            
            else:
                # 尝试使用系统方法终止进程
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    if force:
                        process.kill()
                    else:
                        process.terminate()
                    
                    self.logger.info(f"🛑 系统级终止进程: PID={pid}")
                    return True
                
                self.logger.warning(f"⚠️  进程不存在: PID={pid}")
                return False
        
        except Exception as e:
            self.logger.error(f"❌ 终止进程失败: PID={pid}, 错误={e}")
            return False
    
    def kill_process_by_name(self, name: str) -> int:
        """根据名称终止进程
        
        Args:
            name: 进程名称
            
        Returns:
            终止的进程数量
        """
        killed_count = 0
        
        try:
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (name.lower() in process.info['name'].lower() or
                        any(name.lower() in cmd.lower() for cmd in process.info['cmdline'] or [])):
                        
                        pid = process.info['pid']
                        self.kill_process(pid, force=True)
                        killed_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        except Exception as e:
            self.logger.error(f"❌ 根据名称终止进程失败: {e}")
        
        if killed_count > 0:
            self.logger.success(f"✅ 成功终止 {killed_count} 个 '{name}' 进程")
        else:
            self.logger.info(f"ℹ️  未找到名为 '{name}' 的进程")
        
        return killed_count
    
    def cleanup_all_processes(self) -> int:
        """清理所有活跃进程
        
        Returns:
            清理的进程数量
        """
        self.logger.info("🧹 开始清理所有活跃进程...")
        
        cleanup_count = 0
        pids_to_cleanup = list(self.active_processes.keys())
        
        for pid in pids_to_cleanup:
            if self.kill_process(pid):
                cleanup_count += 1
        
        self.logger.success(f"✅ 清理完成，共清理 {cleanup_count} 个进程")
        return cleanup_count
    
    def get_process_info(self, pid: int) -> Optional[ProcessInfo]:
        """获取进程信息
        
        Args:
            pid: 进程ID
            
        Returns:
            进程信息或None
        """
        return self.processes.get(pid)
    
    def get_all_processes(self) -> List[ProcessInfo]:
        """获取所有进程信息"""
        return list(self.processes.values())
    
    def get_active_processes(self) -> List[ProcessInfo]:
        """获取活跃进程信息"""
        return [p for p in self.processes.values() if p.status == ProcessStatus.RUNNING]
    
    def get_process_count(self) -> Dict[str, int]:
        """获取进程数量统计"""
        stats = {
            'total': len(self.processes),
            'running': 0,
            'finished': 0,
            'killed': 0,
            'error': 0
        }
        
        for process_info in self.processes.values():
            if process_info.status == ProcessStatus.RUNNING:
                stats['running'] += 1
            elif process_info.status == ProcessStatus.FINISHED:
                stats['finished'] += 1
            elif process_info.status == ProcessStatus.KILLED:
                stats['killed'] += 1
            elif process_info.status == ProcessStatus.ERROR:
                stats['error'] += 1
        
        return stats
    
    def get_system_processes(self) -> List[Dict[str, Any]]:
        """获取系统进程信息"""
        processes = []
        
        try:
            for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append({
                        'pid': process.info['pid'],
                        'name': process.info['name'],
                        'cpu_percent': process.info['cpu_percent'],
                        'memory_percent': process.info['memory_percent'],
                        'status': process.info['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        except Exception as e:
            self.logger.error(f"❌ 获取系统进程信息失败: {e}")
        
        return processes
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """获取资源使用情况"""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'memory_available': memory.available / 1024 / 1024 / 1024,  # GB
                'disk_usage': disk.percent,
                'disk_free': disk.free / 1024 / 1024 / 1024,  # GB
                'active_processes': len(self.active_processes),
                'total_processes': len(self.processes)
            }
        
        except Exception as e:
            self.logger.error(f"❌ 获取资源使用情况失败: {e}")
            return {}
    
    def __del__(self):
        """析构函数"""
        try:
            self.stop_monitoring()
            self.cleanup_all_processes()
            self.executor.shutdown(wait=False)
        except:
            pass