<div align="center">

<img src="assets/hexstrike-logo.png" alt="HexStrike AI Logo" width="220" style="margin-bottom: 20px;"/>

# HexStrike AI 渗透测试框架 v6.0
### 🔥 **重大更新** - 增强型AI驱动网络安全平台

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-渗透测试-red.svg)](https://github.com/0x4m4/hexstrike-ai)
[![MCP](https://img.shields.io/badge/MCP-兼容-purple.svg)](https://github.com/0x4m4/hexstrike-ai)
[![Version](https://img.shields.io/badge/Version-6.0.0-orange.svg)](https://github.com/0x4m4/hexstrike-ai/releases)
[![Tools](https://img.shields.io/badge/安全工具-150%2B-brightgreen.svg)](https://github.com/0x4m4/hexstrike-ai)
[![Intelligence](https://img.shields.io/badge/AI智能-高级-blue.svg)](https://github.com/0x4m4/hexstrike-ai)
[![Agents](https://img.shields.io/badge/AI代理-12%2B-purple.svg)](https://github.com/0x4m4/hexstrike-ai)

**🚀 全球最先进的AI驱动渗透测试框架，具备自主代理、智能决策引擎和150+安全工具集成**

[🔥 新增功能](#-v60版本新功能) • [🏗️ 系统架构](#️-系统架构概述) • [🚀 安装指南](#快速安装) • [🛠️ 功能特性](#全面功能集) • [🤖 AI代理](#ai代理--智能自动化) • [📡 API参考](#api参考) • [⭐ 给我们点星](https://github.com/0x4m4/hexstrike-ai)

</div>

---

## 🔥 **v6.0版本新功能**

### **🎯 重大改进和新功能**

<div align="center">

| 🤖 **12+ AI代理** | 🛠️ **150+ 安全工具** | 🧠 **智能决策引擎** |
|:---:|:---:|:---:|
| 自主渗透测试代理 | 完整安全测试工具集 | AI驱动的工具选择和优化 |

| 🎨 **现代可视化引擎** | ⚡ **高级进程管理** | 🔍 **漏洞情报分析** |
|:---:|:---:|:---:|
| 美观的实时输出和仪表盘 | 智能缓存和资源优化 | CVE分析和漏洞利用生成 |

</div>

### **✨ 革命性新功能：**

#### **🤖 自主AI代理 (全新!)**
- **智能决策引擎** - AI驱动的工具选择和参数优化
- **漏洞赏金工作流管理器** - 专门用于漏洞赏金狩猎的工作流
- **CTF工作流管理器** - 自动化CTF挑战解决，支持分类特定方法
- **CVE情报管理器** - 实时漏洞情报和漏洞利用分析
- **AI漏洞利用生成器** - 从CVE数据自动开发漏洞利用
- **漏洞关联器** - 多阶段攻击链发现和优化
- **技术检测器** - 高级技术栈识别和分析
- **浏览器代理** - 无头Chrome自动化，替代Burp Suite

#### **🎨 现代可视化引擎 (全新!)**
- **红色黑客主题** - 一致的cyberpunk风格终端界面
- **实时进度条** - 带ETA计算的美观进度显示
- **状态仪表盘** - 实时系统和工具状态监控
- **彩色日志系统** - 中文化的彩色日志输出
- **漏洞严重性指示器** - 颜色编码的漏洞级别显示

#### **⚡ 高级系统管理 (增强!)**
- **智能进程管理** - 实时进程控制，无需重启服务器
- **LRU缓存系统** - 动态TTL管理和内存优化
- **资源监控** - CPU、内存和性能实时监控
- **故障恢复系统** - 自动错误处理和替代工具选择
- **并发执行** - 多线程工具执行和资源管理

#### **🧠 AI智能功能 (革命性!)**
- **上下文感知决策** - 基于目标特征的智能工具推荐
- **动态参数优化** - 实时调整工具参数以获得最佳结果
- **攻击链编排** - 自动化多阶段渗透测试工作流
- **学习算法** - 从之前的扫描中学习和改进
- **置信度评分** - 所有AI决策的可靠性指标

---

## 🏗️ **系统架构概述**

### **双脚本系统设计**

HexStrike AI采用创新的双脚本架构，实现AI代理和安全工具的无缝集成：

```
📁 HexStrike AI v6.0 架构
├── 🖥️  hexstrike_server_new.py    # 主API服务器 (Flask + 150+工具)
├── 🤖 hexstrike_mcp.py           # MCP客户端 (AI代理通信)
├── 📦 hexstrike_ai/              # 模块化核心框架
│   ├── 🧠 intelligence/          # AI决策引擎和智能分析
│   ├── 🛠️  tools/                # 150+安全工具集成
│   ├── 🎨 visualization/         # 现代化可视化引擎
│   ├── ⚙️  core/                 # 核心系统组件
│   ├── 🌐 api/                   # REST API接口
│   └── 📋 config/                # 配置和日志系统
└── 📊 实时仪表盘和监控系统
```

### **核心组件详解**

#### **🧠 AI代理和智能系统**
- **智能决策引擎** - AI驱动的工具选择和参数优化
- **漏洞赏金工作流管理器** - 专业漏洞赏金狩猎工作流
- **CTF工作流管理器** - 自动化CTF挑战解决，支持类别检测
- **CVE情报管理器** - 实时漏洞情报和漏洞利用分析
- **AI漏洞利用生成器** - 从CVE数据自动开发漏洞利用
- **漏洞关联器** - 多阶段攻击链发现
- **技术检测器** - 高级技术栈识别
- **浏览器代理** - 无头Chrome自动化Web安全测试

#### **⚙️ 进程管理和性能**
- **进程管理器** - 实时进程控制和监控
- **高级缓存** - LRU缓存系统，智能TTL管理
- **资源监控器** - CPU、内存和性能监控
- **故障恢复系统** - 自动错误处理和替代工具选择

#### **🎨 现代可视化引擎**
- **红色黑客主题终端输出**
- **带ETA计算的实时进度条**
- **彩色漏洞严重性指示器**
- **实时进程仪表盘**

---

## 🚀 **快速安装**

### **系统要求**
- **Python**: 3.8+ (推荐 3.11+)
- **操作系统**: Linux (Kali/Ubuntu推荐), macOS, Windows
- **内存**: 最少4GB RAM (推荐8GB+)
- **存储**: 10GB可用空间
- **网络**: 稳定的互联网连接

### **1. 克隆仓库**
```bash
git clone https://github.com/0x4m4/hexstrike-ai.git
cd hexstrike-ai
```

### **2. 创建虚拟环境**
```bash
# 创建虚拟环境
python3 -m venv hexstrike_env

# 激活虚拟环境
source hexstrike_env/bin/activate  # Linux/macOS
# 或在Windows上:
# hexstrike_env\Scripts\activate
```

### **3. 安装Python依赖**
```bash
# 安装核心框架依赖
pip install -r requirements.txt

# 验证安装
python3 hexstrike_server_new.py --version
```

### **4. 检查工具可用性**
```bash
# 检查已安装的安全工具
python3 hexstrike_server_new.py --check-tools
```

### **5. 启动服务器**
```bash
# 使用默认设置启动
python3 hexstrike_server_new.py

# 自定义配置启动
python3 hexstrike_server_new.py --host 0.0.0.0 --port 9999 --debug
```

### **6. 配置Claude Desktop (可选)**
```bash
# 复制MCP配置模板
cp hexstrike-ai-mcp.json ~/.config/claude-desktop/hexstrike-ai-mcp.json

# 编辑配置文件中的路径
nano ~/.config/claude-desktop/hexstrike-ai-mcp.json
```

---

## 🛠️ **全面功能集**

### **🔍 网络侦察工具 (25+工具)**
| 工具 | 描述 | AI增强功能 |
|------|------|-----------|
| `nmap` | 网络发现和安全审计 | 智能端口选择，自动服务指纹识别 |
| `masscan` | 高速互联网端口扫描器 | 动态速率调整，智能目标分割 |
| `rustscan` | 超快端口扫描器 | AI驱动的端口优先级 |
| `amass` | 深度攻击面映射 | 智能子域名关联 |
| `subfinder` | 被动子域名发现 | AI驱动的源选择 |

### **🌐 Web应用安全工具 (40+工具)**
| 工具 | 描述 | AI增强功能 |
|------|------|-----------|
| `nuclei` | 快速漏洞扫描器 | 智能模板选择，动态载荷生成 |
| `gobuster` | URI/DNS和VHost暴力破解 | AI驱动的字典选择 |
| `sqlmap` | 自动SQL注入工具 | 智能载荷定制，上下文感知测试 |
| `ffuf` | 快速web模糊测试器 | 动态模糊测试策略 |
| `katana` | 下一代爬虫框架 | AI驱动的爬取策略 |

### **🔐 身份验证和密码工具 (12+工具)**
| 工具 | 描述 | AI增强功能 |
|------|------|-----------|
| `hydra` | 并行网络登录破解器 | 智能用户名/密码组合 |
| `hashcat` | 高级密码恢复 | AI优化的攻击模式 |
| `john` | John the Ripper破解器 | 智能规则生成 |

### **🔬 二进制分析和逆向工程 (25+工具)**
| 工具 | 描述 | AI增强功能 |
|------|------|-----------|
| `ghidra` | 软件逆向工程套件 | AI辅助代码分析 |
| `radare2` | 逆向工程框架 | 智能符号识别 |
| `angr` | 二进制分析平台 | AI驱动的路径探索 |

---

## 🤖 **AI代理 & 智能自动化**

### **🧠 智能决策引擎**
```python
# AI驱动的目标分析示例
POST /api/intelligence/analyze-target
{
    "target": "example.com",
    "analysis_type": "comprehensive",
    "context": {
        "previous_scans": [],
        "known_technologies": ["nginx", "php"],
        "time_constraints": "30_minutes"
    }
}

# AI响应示例
{
    "recommended_tools": ["nmap", "nuclei", "gobuster"],
    "scan_strategy": "layered_approach",
    "estimated_time": "25-30分钟",
    "confidence": 0.92,
    "reasoning": "基于检测到的技术栈，建议分层扫描方法..."
}
```

### **🎯 专业工作流管理器**

#### **漏洞赏金工作流**
- 自动化侦察阶段
- 智能漏洞验证
- 影响评估和报告生成
- 时间线跟踪和管理

#### **CTF挑战解决器**
- 自动类别检测 (Web, Crypto, Forensics, 等)
- 动态工具选择
- 逐步解决策略
- 自动flag提取

#### **红队作战模拟**
- 多阶段攻击规划
- 横向移动策略
- 持久化技术建议
- 规避技术推荐

---

## 📡 **API参考**

### **🔧 核心端点**

#### **健康检查**
```bash
curl http://localhost:8888/health
```

#### **工具状态查询**
```bash
curl http://localhost:8888/api/tools/status
```

#### **智能目标分析**
```bash
curl -X POST http://localhost:8888/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "analysis_type": "comprehensive"
  }'
```

#### **执行安全扫描**
```bash
curl -X POST http://localhost:8888/api/command \
  -H "Content-Type: application/json" \
  -H "X-HexStrike-API-Key: your-api-key" \
  -d '{
    "command": "nmap -sS -T4 example.com",
    "timeout": 300
  }'
```

### **🛠️ 工具特定端点**

每个集成的安全工具都有专门的API端点：

- `/api/tools/nmap` - Nmap网络扫描
- `/api/tools/nuclei` - Nuclei漏洞扫描
- `/api/tools/gobuster` - 目录暴力破解
- `/api/tools/sqlmap` - SQL注入测试
- `/api/tools/masscan` - 高速端口扫描

---

## 🔧 **高级配置**

### **环境变量配置**
```bash
# 服务器配置
export HEXSTRIKE_HOST="0.0.0.0"
export HEXSTRIKE_PORT="8888"
export HEXSTRIKE_DEBUG="true"

# 性能配置
export HEXSTRIKE_MAX_WORKERS="20"
export HEXSTRIKE_CACHE_SIZE="2000"

# AI配置
export HEXSTRIKE_AI_THREADS="8"

# 工具配置
export HEXSTRIKE_TOOLS_PATH="/opt/security-tools/bin"
```

### **配置文件示例**
```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8888,
    "debug": false,
    "max_workers": 10
  },
  "cache": {
    "enabled": true,
    "max_size": 1000,
    "default_ttl": 3600
  },
  "ai": {
    "decision_engine_enabled": true,
    "confidence_threshold": 0.7,
    "max_analysis_threads": 4
  },
  "security": {
    "require_authorization": true,
    "allowed_targets": ["*.example.com"],
    "blocked_targets": ["localhost", "127.0.0.1"]
  }
}
```

---

## 📚 **使用示例**

### **基础渗透测试工作流**
```bash
# 1. 启动HexStrike AI服务器
python3 hexstrike_server_new.py --debug

# 2. 基础目标分析
curl -X POST http://localhost:8888/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "analysis_type": "basic"}'

# 3. 执行推荐的扫描
curl -X POST http://localhost:8888/api/command \
  -d '{"command": "nmap -sS -sV -T4 example.com"}'

# 4. 查看进程状态
curl http://localhost:8888/api/processes/status
```

### **漏洞赏金自动化工作流**
```python
import requests

# 启动漏洞赏金工作流
response = requests.post('http://localhost:8888/api/workflows/bugbounty', 
    json={
        "target": "bugcrowd-target.com",
        "scope": ["*.bugcrowd-target.com"],
        "budget_hours": 6,
        "focus_areas": ["web_apps", "subdomains", "api_endpoints"]
    })

print(f"工作流ID: {response.json()['workflow_id']}")
```

---

## 🛡️ **安全说明**

### **⚠️ 重要免责声明**
- ✅ **仅用于授权测试**: HexStrike AI仅设计用于授权的渗透测试和安全研究
- ✅ **合法合规使用**: 用户必须确保在合法授权的环境中使用本工具
- ✅ **责任自负**: 开发团队不对恶意使用或非法活动承担任何责任
- ✅ **教育目的**: 本工具主要用于安全教育和防御能力提升

### **🔒 安全最佳实践**
1. **隔离环境**: 在隔离的测试环境中运行
2. **访问控制**: 配置强API密钥和访问限制
3. **审计日志**: 启用详细的操作日志记录
4. **网络隔离**: 限制网络访问范围
5. **定期更新**: 保持工具和依赖的最新版本

---

## 🤝 **社区和支持**

### **📞 获取帮助**
- 📚 **文档**: [完整文档](https://docs.hexstrike.ai)
- 💬 **Discord社区**: [加入我们的Discord](https://discord.gg/hexstrike)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/0x4m4/hexstrike-ai/issues)
- 📧 **邮件支持**: support@hexstrike.ai

### **🎯 路线图**
- [ ] **GPT-4集成** - 增强AI决策能力
- [ ] **云端部署** - Docker和Kubernetes支持
- [ ] **移动应用** - iOS/Android客户端
- [ ] **团队协作** - 多用户和项目管理
- [ ] **商业版本** - 企业级功能和支持

### **🏆 贡献指南**
我们欢迎社区贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解如何：
- 报告bug和功能请求
- 提交代码改进
- 添加新的安全工具集成
- 改进文档和教程

---

## 📄 **许可证**

本项目基于MIT许可证开源 - 查看[LICENSE](LICENSE)文件了解详情。

---

## 🌟 **致谢**

感谢所有为HexStrike AI项目做出贡献的安全研究人员、开发者和社区成员。特别感谢：

- 开源安全工具开发者社区
- AI和机器学习研究社区  
- 网络安全教育工作者
- 所有测试人员和反馈提供者

---

<div align="center">

**🚀 准备好体验下一代AI驱动的渗透测试了吗？**

[⬇️ 立即下载](https://github.com/0x4m4/hexstrike-ai/releases) • [📖 阅读文档](https://docs.hexstrike.ai) • [⭐ 给我们点星](https://github.com/0x4m4/hexstrike-ai)

**用AI的力量，重新定义网络安全测试**

</div>