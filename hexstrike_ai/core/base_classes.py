#!/usr/bin/env python3
"""
HexStrike AI - 基础类定义
Base Classes Definition

这个模块定义了HexStrike AI框架的基础类和数据结构，包括：
- 安全工具基类
- 工具执行结果类
- 状态枚举
- 通用接口定义
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

class ToolStatus(Enum):
    """工具执行状态枚举"""
    PENDING = "等待中"           # 等待执行
    RUNNING = "运行中"           # 正在执行
    COMPLETED = "已完成"         # 执行完成
    FAILED = "执行失败"          # 执行失败
    TIMEOUT = "执行超时"         # 执行超时
    CANCELLED = "已取消"         # 被取消
    RECOVERING = "恢复中"        # 故障恢复中

class VulnerabilitySeverity(Enum):
    """漏洞严重性级别"""
    CRITICAL = "严重"
    HIGH = "高危" 
    MEDIUM = "中危"
    LOW = "低危"
    INFO = "信息"

class ProcessStatus(Enum):
    """进程状态枚举"""
    CREATED = "已创建"
    RUNNING = "运行中"
    FINISHED = "已完成"
    KILLED = "已终止"
    ERROR = "出错"

@dataclass
class ToolResult:
    """工具执行结果类"""
    tool_name: str                              # 工具名称
    status: ToolStatus                          # 执行状态
    start_time: datetime                        # 开始时间
    end_time: Optional[datetime] = None         # 结束时间
    duration: float = 0.0                      # 执行时长(秒)
    exit_code: int = 0                         # 退出代码
    stdout: str = ""                           # 标准输出
    stderr: str = ""                           # 错误输出
    command: str = ""                          # 执行的命令
    target: str = ""                           # 目标
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)  # 发现的漏洞
    artifacts: List[str] = field(default_factory=list)                   # 生成的文件
    metadata: Dict[str, Any] = field(default_factory=dict)               # 元数据
    error_message: str = ""                    # 错误信息
    recovery_attempted: bool = False           # 是否尝试过恢复
    ai_analysis: Dict[str, Any] = field(default_factory=dict)           # AI分析结果
    
    def __post_init__(self):
        """初始化后处理"""
        if self.end_time and self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    @property
    def is_successful(self) -> bool:
        """判断是否执行成功"""
        return self.status == ToolStatus.COMPLETED and self.exit_code == 0
    
    @property
    def has_vulnerabilities(self) -> bool:
        """判断是否发现漏洞"""
        return len(self.vulnerabilities) > 0
    
    @property
    def vulnerability_count(self) -> int:
        """获取漏洞数量"""
        return len(self.vulnerabilities)
    
    @property
    def critical_vulnerabilities(self) -> List[Dict[str, Any]]:
        """获取严重漏洞列表"""
        return [v for v in self.vulnerabilities 
                if v.get('severity', '').lower() == 'critical']
    
    def add_vulnerability(self, 
                         vuln_type: str, 
                         severity: str, 
                         description: str,
                         location: str = "",
                         cve_id: str = "",
                         evidence: str = "",
                         remediation: str = "") -> None:
        """添加漏洞信息"""
        vulnerability = {
            'type': vuln_type,
            'severity': severity,
            'description': description,
            'location': location,
            'cve_id': cve_id,
            'evidence': evidence,
            'remediation': remediation,
            'discovered_at': datetime.now().isoformat(),
            'tool': self.tool_name
        }
        self.vulnerabilities.append(vulnerability)
    
    def add_artifact(self, file_path: str, description: str = "") -> None:
        """添加生成的文件"""
        artifact = {
            'path': file_path,
            'description': description,
            'created_at': datetime.now().isoformat()
        }
        self.artifacts.append(artifact)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'tool_name': self.tool_name,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'exit_code': self.exit_code,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'command': self.command,
            'target': self.target,
            'vulnerabilities': self.vulnerabilities,
            'artifacts': self.artifacts,
            'metadata': self.metadata,
            'error_message': self.error_message,
            'recovery_attempted': self.recovery_attempted,
            'ai_analysis': self.ai_analysis
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON格式"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

class SecurityTool:
    """安全工具基类"""
    
    def __init__(self, name: str, binary_path: str = "", description: str = ""):
        """初始化安全工具
        
        Args:
            name: 工具名称
            binary_path: 二进制文件路径
            description: 工具描述
        """
        self.name = name
        self.binary_path = binary_path
        self.description = description
        self.available = False
        self.version = ""
        self.category = ""
        self.tags = []
        self.default_timeout = 600  # 10分钟
        self.max_retries = 3
        self.last_used = None
        
        # 检查工具可用性
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查工具是否可用"""
        import shutil
        if self.binary_path:
            self.available = shutil.which(self.binary_path) is not None
        else:
            self.available = shutil.which(self.name) is not None
        return self.available
    
    def get_version(self) -> str:
        """获取工具版本"""
        # 子类应该重写此方法
        return self.version
    
    def validate_target(self, target: str) -> bool:
        """验证目标有效性"""
        # 子类可以重写此方法
        return bool(target and target.strip())
    
    def build_command(self, target: str, **kwargs) -> str:
        """构建执行命令"""
        # 子类必须重写此方法
        raise NotImplementedError("子类必须实现 build_command 方法")
    
    def parse_output(self, stdout: str, stderr: str) -> ToolResult:
        """解析工具输出"""
        # 子类应该重写此方法
        result = ToolResult(
            tool_name=self.name,
            status=ToolStatus.COMPLETED,
            start_time=datetime.now(),
            stdout=stdout,
            stderr=stderr
        )
        return result
    
    def execute(self, target: str, timeout: int = None, **kwargs) -> ToolResult:
        """执行工具"""
        from ..core.process_manager import ProcessManager
        from ..config.logger_config import get_logger
        
        logger = get_logger()
        
        # 验证工具可用性
        if not self.available:
            logger.error(f"工具不可用: {self.name}")
            result = ToolResult(
                tool_name=self.name,
                status=ToolStatus.FAILED,
                start_time=datetime.now(),
                error_message=f"工具不可用: {self.name}"
            )
            return result
        
        # 验证目标
        if not self.validate_target(target):
            logger.error(f"无效的目标: {target}")
            result = ToolResult(
                tool_name=self.name,
                status=ToolStatus.FAILED,
                start_time=datetime.now(),
                error_message=f"无效的目标: {target}"
            )
            return result
        
        # 构建命令
        try:
            command = self.build_command(target, **kwargs)
        except Exception as e:
            logger.error(f"构建命令失败: {e}")
            result = ToolResult(
                tool_name=self.name,
                status=ToolStatus.FAILED,
                start_time=datetime.now(),
                error_message=f"构建命令失败: {e}"
            )
            return result
        
        # 执行命令
        timeout = timeout or self.default_timeout
        logger.tool_start(self.name, target)
        
        start_time = datetime.now()
        
        try:
            process_manager = ProcessManager()
            process_result = process_manager.execute_command(
                command, timeout=timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 解析输出
            result = self.parse_output(
                process_result.get('stdout', ''),
                process_result.get('stderr', '')
            )
            
            # 更新结果信息
            result.start_time = start_time
            result.end_time = end_time
            result.duration = duration
            result.exit_code = process_result.get('return_code', 0)
            result.command = command
            result.target = target
            
            if result.exit_code == 0:
                result.status = ToolStatus.COMPLETED
                logger.tool_success(self.name, duration)
            else:
                result.status = ToolStatus.FAILED
                result.error_message = process_result.get('stderr', '')
                logger.tool_failed(self.name, result.error_message)
            
            self.last_used = datetime.now()
            return result
            
        except Exception as e:
            logger.error(f"执行工具失败: {e}")
            result = ToolResult(
                tool_name=self.name,
                status=ToolStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error_message=str(e),
                target=target,
                command=command
            )
            return result
    
    def get_info(self) -> Dict[str, Any]:
        """获取工具信息"""
        return {
            'name': self.name,
            'binary_path': self.binary_path,
            'description': self.description,
            'available': self.available,
            'version': self.version,
            'category': self.category,
            'tags': self.tags,
            'default_timeout': self.default_timeout,
            'max_retries': self.max_retries,
            'last_used': self.last_used.isoformat() if self.last_used else None
        }

@dataclass
class SystemStats:
    """系统统计信息"""
    cpu_usage: float = 0.0          # CPU使用率
    memory_usage: float = 0.0       # 内存使用率
    disk_usage: float = 0.0         # 磁盘使用率
    network_io: Dict[str, int] = field(default_factory=dict)  # 网络IO
    active_processes: int = 0       # 活跃进程数
    timestamp: datetime = field(default_factory=datetime.now)  # 时间戳

@dataclass
class CacheStats:
    """缓存统计信息"""
    total_entries: int = 0          # 总条目数
    hit_count: int = 0              # 命中次数
    miss_count: int = 0             # 未命中次数
    hit_rate: float = 0.0           # 命中率
    memory_usage: int = 0           # 内存使用量(字节)
    oldest_entry: Optional[datetime] = None  # 最旧条目时间
    newest_entry: Optional[datetime] = None  # 最新条目时间

class RecoveryStrategy(Enum):
    """恢复策略枚举"""
    RETRY = "重试"                  # 简单重试
    ALTERNATIVE_TOOL = "替代工具"    # 使用替代工具
    PARAMETER_ADJUSTMENT = "参数调整"  # 调整参数
    TIMEOUT_EXTENSION = "延长超时"   # 延长超时时间
    MANUAL_INTERVENTION = "人工干预" # 需要人工干预