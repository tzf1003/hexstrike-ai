# HexStrike AI MCP客户端 - 重构版本

## 🚀 概述

HexStrike AI MCP客户端是一个完全重构的模块化架构，为AI代理提供了与HexStrike AI安全平台的无缝通信接口。该版本采用了现代化的设计模式，支持150+安全工具，并提供了完整的中文化界面。

## 🏗️ 架构设计

### 模块化结构
```
hexstrike_ai/
├── mcp/                           # MCP模块根目录
│   ├── __init__.py               # 模块初始化和配置
│   ├── server.py                 # MCP服务器管理
│   ├── client/                   # 客户端通信模块
│   │   ├── hexstrike_client.py   # HexStrike API客户端
│   │   └── connection_manager.py # 连接管理和健康监控
│   └── tools/                    # 工具函数管理
│       ├── manager.py            # 工具管理器
│       ├── network_tools.py      # 网络安全工具
│       ├── web_tools.py          # Web应用安全工具
│       └── system_tools.py       # 系统工具
```

### 核心特性

#### 🛠️ 工具函数管理系统
- **统一注册**: 所有工具函数通过统一的管理器注册和分类
- **执行监控**: 实时监控工具执行状态、性能指标和成功率
- **智能恢复**: 自动故障恢复机制，确保工具执行的可靠性
- **分类管理**: 按功能分类管理工具（网络、Web、系统、分析等）

#### 🌐 客户端通信优化
- **连接池管理**: 高效的HTTP连接池和会话管理
- **健康监控**: 实时监控与HexStrike服务器的连接状态
- **自动重连**: 智能重连机制，支持指数退避策略
- **请求优化**: 支持缓存、超时控制和重试机制

#### 📊 监控和统计
- **执行指标**: 详细的工具执行统计和性能分析
- **成功率追踪**: 实时追踪工具执行成功率和失败原因
- **资源监控**: 监控系统资源使用情况
- **中文日志**: 完整的中文化日志输出，便于调试和监控

## 🚀 快速开始

### 1. 安装依赖
```bash
# 进入项目目录
cd hexstrike-ai

# 安装Python依赖
python3 -m pip install -r requirements.txt
```

### 2. 启动HexStrike服务器
```bash
# 启动主服务器
python3 hexstrike_server.py

# 或者指定端口启动
python3 hexstrike_server.py --port 8888
```

### 3. 启动MCP客户端
```bash
# 使用默认配置启动
python3 hexstrike_mcp_new.py

# 自定义配置启动
python3 hexstrike_mcp_new.py --server-url http://localhost:8888 --debug
```

### 4. Claude Desktop集成
1. 更新 `hexstrike-ai-mcp.json` 配置文件中的路径
2. 将配置文件添加到Claude Desktop的MCP设置中
3. 重启Claude Desktop

## 🛠️ 工具分类

### 网络侦察工具
- **Nmap**: 网络扫描和服务识别
- **Masscan**: 高速端口扫描
- **RustScan**: 快速端口发现
- **Amass**: 子域名发现
- **Subfinder**: 被动子域名收集

### Web应用安全工具
- **Gobuster**: 目录和子域名暴力破解
- **Nuclei**: 漏洞扫描模板引擎
- **SQLMap**: SQL注入检测和利用
- **FFUF**: Web模糊测试
- **Nikto**: Web服务器扫描
- **Katana**: Web爬虫
- **HTTPx**: HTTP探测

### 系统工具
- **命令执行**: 安全的系统命令执行
- **健康检查**: 服务器状态监控
- **系统信息**: 系统配置收集
- **网络信息**: 网络配置分析
- **进程管理**: 进程列表和监控
- **文件操作**: 文件存在性检查和信息获取

### 智能分析工具
- **AI目标分析**: 智能目标分析和建议
- **漏洞关联**: 多阶段攻击链发现
- **技术检测**: 自动技术栈识别

## 📖 使用示例

### 基本工具调用
```python
# 执行Nmap扫描
result = nmap_scan(
    target="192.168.1.1",
    scan_type="-sV",
    ports="80,443,22"
)

# 执行目录扫描
result = gobuster_scan(
    url="http://example.com",
    mode="dir",
    wordlist="/usr/share/wordlists/dirb/common.txt"
)

# 执行漏洞扫描
result = nuclei_scan(
    target="http://example.com",
    severity="high,critical"
)
```

### 系统管理
```python
# 检查服务器健康状态
status = check_health()

# 获取系统信息
info = get_system_info()

# 执行系统命令
result = execute_command("netstat -tuln")
```

### 智能分析
```python
# AI目标分析
analysis = analyze_target(
    target="example.com",
    analysis_type="comprehensive"
)
```

## 🔧 配置选项

### 命令行参数
```bash
python3 hexstrike_mcp_new.py [选项]

选项:
  --server-url URL     HexStrike服务器地址 (默认: http://127.0.0.1:8888)
  --name NAME          MCP服务器名称 (默认: hexstrike-ai-mcp)
  --timeout SECONDS    请求超时时间 (默认: 300)
  --max-retries COUNT  最大重试次数 (默认: 3)
  --debug              启用调试模式
  --log-level LEVEL    日志级别 (DEBUG, INFO, WARNING, ERROR)
  --version            显示版本信息
  --help               显示帮助信息
```

### 环境变量
```bash
# 设置HexStrike服务器地址
export HEXSTRIKE_SERVER_URL="http://192.168.1.100:8888"

# 设置日志级别
export HEXSTRIKE_LOG_LEVEL="DEBUG"

# 设置超时时间
export HEXSTRIKE_TIMEOUT="600"
```

## 📊 监控和调试

### 日志系统
重构版本提供了完整的中文化日志系统：

```
🚀 MCP服务器管理器初始化完成: hexstrike-ai-mcp
📋 开始向MCP服务器注册工具函数...
🔧 注册工具: nmap_scan (执行Nmap网络扫描)
✅ 工具注册完成: 25/25 个工具成功注册
🎯 等待AI代理连接...
```

### 工具执行监控
```
🚀 开始执行工具: 执行Nmap网络扫描 (nmap_scan)
🔍 启动Nmap扫描: 192.168.1.1
✅ 工具执行成功: 执行Nmap网络扫描, 耗时: 15.32秒
🎯 发现开放端口: 5 个
```

### 性能指标
系统提供详细的性能监控：
- 工具执行次数和成功率
- 平均执行时间
- 失败原因分析
- 资源使用统计

## 🛡️ 安全考虑

### 命令执行安全
- **危险命令过滤**: 自动阻止危险的系统命令
- **参数验证**: 严格的输入参数验证
- **超时控制**: 防止长时间运行的命令

### 网络安全
- **连接加密**: 支持HTTPS通信
- **认证机制**: 可配置的API认证
- **访问控制**: 细粒度的权限控制

## 🔄 故障恢复

### 自动恢复机制
- **工具执行失败**: 自动尝试替代工具
- **网络连接中断**: 智能重连和状态恢复
- **服务器异常**: 优雅降级和错误处理

### 错误处理
```python
# 示例：自动故障恢复
result = nmap_scan("192.168.1.1")
if result.get("recovery_info", {}).get("recovery_applied"):
    print("🔄 应用了故障恢复机制")
```

## 📈 扩展开发

### 添加新工具
```python
# 在适当的工具模块中添加新函数
def my_custom_tool(target: str, options: str = "") -> Dict[str, Any]:
    """自定义安全工具"""
    # 工具实现
    pass

# 在管理器中注册
self.register_tool(
    name="my_custom_tool",
    category="custom",
    description="My custom security tool",
    chinese_description="我的自定义安全工具",
    function=my_custom_tool
)
```

### 自定义工具分类
```python
# 在管理器中添加新分类
self.categories["custom"] = "自定义工具"
```

## 🐛 故障排除

### 常见问题

#### 1. MCP服务器无法启动
```bash
# 检查依赖
python3 -c "import mcp; print('MCP库已安装')"

# 检查HexStrike服务器连接
curl http://localhost:8888/health
```

#### 2. 工具执行失败
```bash
# 启用调试模式
python3 hexstrike_mcp_new.py --debug

# 检查工具可用性
which nmap nuclei gobuster
```

#### 3. Claude Desktop集成问题
- 检查配置文件路径是否正确
- 确认Python环境和依赖是否完整
- 查看Claude Desktop的MCP日志

### 日志分析
```bash
# 查看详细日志
python3 hexstrike_mcp_new.py --log-level DEBUG

# 过滤特定组件日志
python3 hexstrike_mcp_new.py --debug 2>&1 | grep "MCP-ToolsManager"
```

## 📞 支持和反馈

- **项目主页**: [HexStrike AI GitHub](https://github.com/hexstrike/hexstrike-ai)
- **问题报告**: 通过GitHub Issues提交问题
- **功能建议**: 欢迎提交Pull Request

## 📄 许可证

本项目采用开源许可证，详见LICENSE文件。

---

*HexStrike AI Team - 专业的网络安全自动化平台*