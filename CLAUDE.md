# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在处理此代码库时提供中文化指导说明。

## 核心命令

### 启动服务器
```bash
# 启动 HexStrike AI 重构版服务器 (推荐)
python3 hexstrike_server_new.py

# 使用自定义端口启动
python3 hexstrike_server_new.py --port 9999

# 启用调试模式
python3 hexstrike_server_new.py --debug

# 检查工具可用性
python3 hexstrike_server_new.py --check-tools

# 显示版本信息
python3 hexstrike_server_new.py --version

# 启动原版服务器 (兼容性)
python3 hexstrike_server.py
```

### 开发环境设置
```bash
# 创建并激活虚拟环境
python3 -m venv hexstrike_env
source hexstrike_env/bin/activate  # Linux/Mac
# hexstrike_env\Scripts\activate   # Windows

# 安装依赖包
python3 -m pip install -r requirements.txt

# 验证安装
python3 hexstrike_server_new.py --version
```

### 健康检查和状态检测
```bash
# 检查服务器健康状态
curl http://localhost:8888/health

# 测试工具可用性
curl http://localhost:8888/api/tools/status

# 测试AI代理能力
curl -X POST http://localhost:8888/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'

# 查看系统统计信息
curl http://localhost:8888/stats

# 查看进程状态
curl http://localhost:8888/api/processes/status
```

### MCP配置
项目包含 `hexstrike-ai-mcp.json` 用于 Claude Desktop 集成。请更新配置文件中的路径以匹配您的安装目录。

## 系统架构概述

### 双脚本系统设计
项目采用创新的双脚本架构：

1. **hexstrike_server_new.py** - 重构版Flask API服务器，通过REST端点提供150+安全工具 (推荐使用)
2. **hexstrike_server.py** - 原版服务器 (向后兼容)
3. **hexstrike_mcp.py** - MCP (模型上下文协议) 客户端，在AI代理和HexStrike服务器之间进行转换

### 核心组件

#### AI代理和智能系统
- **智能决策引擎 (IntelligentDecisionEngine)** - AI驱动的工具选择和参数优化
- **漏洞赏金工作流管理器 (BugBountyWorkflowManager)** - 专门用于漏洞赏金狩猎的工作流
- **CTF工作流管理器 (CTFWorkflowManager)** - 自动化CTF挑战解决，支持类别检测
- **CVE情报管理器 (CVEIntelligenceManager)** - 实时漏洞情报和漏洞利用分析
- **AI漏洞利用生成器 (AIExploitGenerator)** - 从CVE数据自动开发漏洞利用
- **漏洞关联器 (VulnerabilityCorrelator)** - 多阶段攻击链发现
- **技术检测器 (TechnologyDetector)** - 高级技术栈识别
- **浏览器代理 (BrowserAgent)** - 无头Chrome自动化Web安全测试

#### 进程管理系统
- **进程管理器 (ProcessManager)** - 实时进程控制和监控
- **高级缓存 (AdvancedCache)** - LRU缓存系统，智能TTL管理
- **资源监控器 (ResourceMonitor)** - CPU、内存和性能监控
- **故障恢复系统 (FailureRecoverySystem)** - 自动错误处理和替代工具选择

#### 现代可视化引擎
- **现代可视化引擎 (ModernVisualEngine)** - 美观的红色黑客主题终端输出
- 带ETA计算的实时进度条
- 颜色编码的漏洞严重性指示器
- 实时进程仪表盘

### 安全工具分类

系统集成了150+外部安全工具，涵盖以下领域：

- **网络侦察** (25+ 工具): nmap, masscan, rustscan, amass, subfinder
- **Web应用安全** (40+ 工具): nuclei, sqlmap, gobuster, ffuf, katana, httpx
- **二进制分析** (25+ 工具): ghidra, radare2, gdb, pwntools, angr, volatility3
- **云安全** (20+ 工具): prowler, scout-suite, trivy, kube-hunter, kube-bench
- **身份认证** (12+ 工具): hydra, hashcat, john, medusa, patator
- **CTF和取证** (20+ 工具): volatility3, foremost, steghide, exiftool
- **OSINT情报** (20+ 工具): sherlock, theharvester, shodan, censys

### 核心特性

#### 智能自动化
- 基于目标分析的AI驱动工具选择
- 上下文感知的参数优化
- 多阶段攻击链编排
- 带替代策略的自动故障恢复

#### 高级功能
- 无头浏览器自动化 (Burp Suite替代方案)
- 实时漏洞情报监控
- 从CVE描述自动生成漏洞利用
- 跨多个类别的CTF挑战自动解决
- 漏洞赏金工作流自动化

#### 性能优化
- 智能缓存，支持LRU淘汰和动态TTL
- 并发工具执行和资源管理
- 实时进程终止，无需重启服务器
- 内存和CPU优化

## 代码库使用指南

### 重构后的文件结构
- `hexstrike_server_new.py` - 重构版主服务器，包含所有AI代理和工具集成 (推荐)
- `hexstrike_server.py` - 原版服务器 (向后兼容)  
- `hexstrike_mcp.py` - 用于AI代理通信的MCP客户端
- `hexstrike_ai/` - 模块化核心框架
  - `core/` - 核心系统组件 (进程管理、缓存、资源监控等)
  - `intelligence/` - AI智能分析模块
  - `tools/` - 安全工具集成管理
  - `visualization/` - 现代化可视化引擎
  - `api/` - Web API服务器
  - `config/` - 配置和日志系统
- `requirements.txt` - Python依赖 (仅核心框架)
- `hexstrike-ai-mcp.json` - Claude Desktop MCP配置模板
- `README_CN.md` - 中文版综合文档和设置说明

### 需要理解的关键类
- `IntelligentDecisionEngine` - 中央AI决策系统
- `BugBountyWorkflowManager` - 漏洞赏金自动化工作流
- `CTFWorkflowManager` - CTF挑战解决自动化
- `BrowserAgent` - 使用Chrome自动化的Web应用安全测试
- `ModernVisualEngine` - 终端输出样式和进度可视化
- `ProcessManager` - 进程控制和监控
- `AdvancedCache` - 智能缓存系统
- `SecurityToolsManager` - 安全工具统一管理
- `HexStrikeAPI` - API服务器管理

### 外部工具集成
系统期望外部安全工具单独安装。通过`which`命令检测工具并标记为可用。缺失的工具会被优雅处理 - 系统可以与任何已安装工具的子集一起工作。

### API端点结构
- `/health` - 服务器健康状态和工具可用性状态
- `/version` - 版本信息
- `/stats` - 系统统计信息
- `/api/command` - 执行任意命令，支持缓存
- `/api/tools/*` - 单个工具端点 (nmap, nuclei等)
- `/api/intelligence/*` - AI驱动的分析和决策
- `/api/processes/*` - 实时进程管理
- `/api/ai/*` - 载荷生成和测试功能

### MCP工具函数
MCP客户端为AI代理公开了100+工具函数，包括每个安全工具类别的专门函数和用于自主操作的智能工作流管理器。

### 安全注意事项
这是一个专为授权安全测试设计的渗透测试框架。系统为AI代理提供强大功能，应在隔离环境中运行并进行适当监督。