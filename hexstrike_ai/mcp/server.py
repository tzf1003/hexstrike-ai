#!/usr/bin/env python3
"""
HexStrike AI - MCP服务器管理
MCP Server Management

这个模块提供了MCP服务器的创建和管理功能，包括：
- FastMCP服务器配置
- 工具函数注册和暴露
- AI代理通信协议
- 中文化的状态报告和错误处理
"""

import os
import argparse
from typing import Dict, Any, Optional
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from ..config.logger_config import get_logger
from ..config.colors import HexStrikeColors
from .client import HexStrikeMCPClient
from .tools import MCPToolsManager

class MCPServerManager:
    """MCP服务器管理器 - 管理FastMCP服务器实例"""
    
    def __init__(self, 
                 server_name: str = "hexstrike-ai-mcp",
                 hexstrike_server_url: str = "http://127.0.0.1:8888"):
        """初始化MCP服务器管理器
        
        Args:
            server_name: MCP服务器名称
            hexstrike_server_url: HexStrike AI服务器URL
        """
        self.server_name = server_name
        self.hexstrike_server_url = hexstrike_server_url
        self.logger = get_logger('MCP-ServerManager')
        
        # 创建FastMCP实例
        self.mcp = FastMCP(server_name)
        
        # 创建HexStrike客户端
        self.hexstrike_client = HexStrikeMCPClient(hexstrike_server_url)
        
        # 创建工具管理器
        self.tools_manager = MCPToolsManager(self.hexstrike_client)
        
        # 服务器统计信息
        self.stats = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0
        }
        
        self.logger.info(f"🚀 MCP服务器管理器初始化完成: {server_name}")
        
        # 注册所有工具函数
        self._register_all_tools()
    
    def _register_all_tools(self):
        """注册所有工具函数到MCP服务器"""
        self.logger.info("📋 开始向MCP服务器注册工具函数...")
        
        registered_count = 0
        
        # 获取所有工具
        all_tools = self.tools_manager.get_all_tools()
        
        for tool_name, tool_info in all_tools.items():
            try:
                # 创建监控包装函数
                monitored_function = self.tools_manager.create_monitored_tool(tool_info)
                
                # 注册到MCP服务器
                self.mcp.tool()(monitored_function)
                
                registered_count += 1
                self.logger.debug(f"✅ 注册工具: {tool_name} - {tool_info.chinese_description}")
                
            except Exception as e:
                self.logger.error(f"❌ 注册工具失败 {tool_name}: {e}")
        
        self.logger.success(f"🎯 工具注册完成: {registered_count}/{len(all_tools)} 个工具成功注册")
        
        # 注册额外的MCP功能
        self._register_mcp_utilities()
    
    def _register_mcp_utilities(self):
        """注册MCP实用工具"""
        
        @self.mcp.tool()
        def get_tools_list() -> Dict[str, Any]:
            """获取所有可用工具列表
            
            Returns:
                包含所有工具信息的字典
            """
            self.logger.info("📋 获取工具列表请求")
            
            tools_summary = self.tools_manager.get_tools_summary()
            all_tools = self.tools_manager.get_all_tools()
            
            tools_list = {}
            for tool_name, tool_info in all_tools.items():
                tools_list[tool_name] = {
                    'name': tool_name,
                    'category': tool_info.category,
                    'description': tool_info.description,
                    'chinese_description': tool_info.chinese_description,
                    'parameters': tool_info.parameters,
                    'examples': tool_info.examples,
                    'tags': tool_info.tags
                }
            
            return {
                'success': True,
                'data': {
                    'summary': tools_summary,
                    'tools': tools_list
                },
                'message': '工具列表获取成功'
            }
        
        @self.mcp.tool()
        def get_server_status() -> Dict[str, Any]:
            """获取MCP服务器状态信息
            
            Returns:
                服务器状态信息
            """
            self.logger.info("📊 获取服务器状态请求")
            
            # 获取运行时间
            uptime = (datetime.now() - self.stats['start_time']).total_seconds()
            
            # 获取客户端统计
            client_stats = self.hexstrike_client.get_client_stats()
            
            # 获取工具统计
            tools_summary = self.tools_manager.get_tools_summary()
            
            status = {
                'server_name': self.server_name,
                'status': 'running',
                'uptime_seconds': uptime,
                'hexstrike_connected': client_stats['connected'],
                'hexstrike_server_url': self.hexstrike_server_url,
                'stats': self.stats.copy(),
                'tools_summary': tools_summary,
                'client_stats': client_stats
            }
            
            return {
                'success': True,
                'data': status,
                'message': 'MCP服务器状态获取成功'
            }
        
        @self.mcp.tool()
        def get_tool_metrics(tool_name: str = "") -> Dict[str, Any]:
            """获取工具执行指标
            
            Args:
                tool_name: 工具名称，为空则返回所有工具指标
                
            Returns:
                工具执行指标信息
            """
            self.logger.info(f"📈 获取工具指标请求: {tool_name if tool_name else '所有工具'}")
            
            if tool_name:
                # 获取单个工具指标
                metrics = self.tools_manager.get_tool_metrics(tool_name)
                if metrics:
                    return {
                        'success': True,
                        'data': {
                            'tool_name': tool_name,
                            'metrics': {
                                'total_calls': metrics.total_calls,
                                'successful_calls': metrics.successful_calls,
                                'failed_calls': metrics.failed_calls,
                                'success_rate': (metrics.successful_calls / max(1, metrics.total_calls)) * 100,
                                'average_duration': metrics.average_duration,
                                'total_duration': metrics.total_duration,
                                'last_called': metrics.last_called.isoformat() if metrics.last_called else None,
                                'last_error': metrics.last_error
                            }
                        },
                        'message': f'工具 {tool_name} 指标获取成功'
                    }
                else:
                    return {
                        'success': False,
                        'error': f'工具 {tool_name} 不存在',
                        'message': '工具不存在'
                    }
            else:
                # 获取所有工具指标
                all_metrics = {}
                for name, metrics in self.tools_manager.tool_metrics.items():
                    all_metrics[name] = {
                        'total_calls': metrics.total_calls,
                        'successful_calls': metrics.successful_calls,
                        'failed_calls': metrics.failed_calls,
                        'success_rate': (metrics.successful_calls / max(1, metrics.total_calls)) * 100,
                        'average_duration': metrics.average_duration,
                        'last_called': metrics.last_called.isoformat() if metrics.last_called else None
                    }
                
                return {
                    'success': True,
                    'data': {
                        'all_tools_metrics': all_metrics,
                        'summary': self.tools_manager.get_tools_summary()
                    },
                    'message': '所有工具指标获取成功'
                }
        
        self.logger.success("🔧 MCP实用工具注册完成")
    
    def run(self):
        """运行MCP服务器"""
        try:
            self.logger.info(f"🚀 启动MCP服务器: {self.server_name}")
            self.logger.info(f"🔗 连接到HexStrike服务器: {self.hexstrike_server_url}")
            
            # 显示服务器信息
            tools_count = len(self.tools_manager.get_all_tools())
            categories_count = len(self.tools_manager.tool_categories)
            
            self.logger.success(f"✅ MCP服务器准备就绪")
            self.logger.info(f"🛠️  可用工具: {tools_count} 个")
            self.logger.info(f"📂 工具分类: {categories_count} 个")
            self.logger.info("🎯 等待AI代理连接...")
            
            # 运行MCP服务器
            self.mcp.run()
            
        except KeyboardInterrupt:
            self.logger.warning("⚠️  收到中断信号，正在关闭MCP服务器...")
        except Exception as e:
            self.logger.error(f"❌ MCP服务器运行异常: {e}")
            raise
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        self.logger.info("🧹 清理MCP服务器资源...")
        
        try:
            # 断开HexStrike客户端连接
            if hasattr(self.hexstrike_client, 'session'):
                self.hexstrike_client.session.close()
                
        except Exception as e:
            self.logger.warning(f"⚠️  清理资源时出现异常: {e}")
        
        self.logger.info("✅ MCP服务器已关闭")

def create_mcp_server(server_name: str = "hexstrike-ai-mcp",
                     hexstrike_server_url: str = "http://127.0.0.1:8888") -> MCPServerManager:
    """创建MCP服务器实例
    
    Args:
        server_name: MCP服务器名称
        hexstrike_server_url: HexStrike AI服务器URL
        
    Returns:
        MCP服务器管理器实例
    """
    return MCPServerManager(server_name, hexstrike_server_url)

def parse_command_line_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='HexStrike AI MCP服务器 - AI代理通信接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python hexstrike_mcp_new.py                           # 使用默认设置启动
  python hexstrike_mcp_new.py --server-url http://192.168.1.100:8888  # 指定服务器地址
  python hexstrike_mcp_new.py --name my-mcp-server      # 自定义服务器名称
        """
    )
    
    parser.add_argument(
        '--server-url',
        default='http://127.0.0.1:8888',
        help='HexStrike AI服务器URL (默认: http://127.0.0.1:8888)'
    )
    
    parser.add_argument(
        '--name',
        default='hexstrike-ai-mcp',
        help='MCP服务器名称 (默认: hexstrike-ai-mcp)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='请求超时时间(秒) (默认: 300)'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='最大重试次数 (默认: 3)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式'
    )
    
    return parser.parse_args()

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_command_line_args()
    
    # 设置日志级别
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 显示启动信息
    from ..config.colors import HexStrikeColors
    
    print(f"{HexStrikeColors.BANNER_TITLE}=== HexStrike AI MCP服务器 v6.0 ==={HexStrikeColors.RESET}")
    print(f"{HexStrikeColors.NEON_BLUE}AI代理通信接口{HexStrikeColors.RESET}")
    print(f"{HexStrikeColors.SEPARATOR}{'─' * 50}{HexStrikeColors.RESET}")
    
    try:
        # 创建并运行MCP服务器
        server_manager = create_mcp_server(
            server_name=args.name,
            hexstrike_server_url=args.server_url
        )
        
        server_manager.run()
        
    except Exception as e:
        logger = get_logger('MCP-Main')
        logger.error(f"❌ MCP服务器启动失败: {e}")
        exit(1)

if __name__ == '__main__':
    main()