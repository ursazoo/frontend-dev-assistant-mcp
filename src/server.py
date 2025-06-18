#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 服务器
"""

import asyncio
import json
import logging
import os
import sys
import inspect
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from frontend_dev_assistant.prompt_manager import PromptManager
from frontend_dev_assistant.component_finder import ComponentFinder
from frontend_dev_assistant.usage_tracker import UsageTracker
from frontend_dev_assistant.call_tracker import call_tracker

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend-dev-mcp")

class FrontendDevMCP:
    def __init__(self):
        self.server = Server("frontend-dev-assistant")
        self.prompt_manager = PromptManager()
        self.component_finder = ComponentFinder()
        self.usage_tracker = UsageTracker()
        self.setup_tools()
    
    async def test_context_access(self, tool_name: str, usage_context: str, test_data: str, **kwargs) -> str:
        """
        测试MCP工具能获取到的上下文信息
        """
        
        # 收集调用参数
        params = {
            "tool_name": tool_name,
            "usage_context": usage_context, 
            "test_data": test_data,
        }
        params.update(kwargs)
        
        # 调用详细的上下文测试
        context_data = call_tracker.detailed_context_test("test_context_access", params, **kwargs)
        
        # 分析结果
        analysis = {
            "summary": "MCP上下文获取能力测试完成",
            "findings": {
                "can_access_params": bool(params),
                "has_environment_info": bool(context_data.get("environment")),
                "call_stack_depth": context_data.get("call_stack_info", {}).get("stack_depth", 0),
                "env_vars_found": len(context_data.get("hidden_context", {}).get("env_vars", {})),
                "conversation_context": "无法直接获取" if not any("conversation" in str(v).lower() for v in params.values()) else "可能包含对话信息"
            },
            "raw_data_saved": str(call_tracker.data_dir / "context_test_log.jsonl"),
            "next_steps": [
                "1. 检查保存的测试数据文件",
                "2. 分析调用栈信息",
                "3. 验证是否有隐藏的上下文传递"
            ]
        }
        
        result_text = f"""
# MCP上下文获取能力测试结果

## 测试概况
- 工具名称: {tool_name}
- 测试场景: {usage_context}
- 测试时间: {context_data.get('timestamp')}

## 发现结果
- 能否获取参数: {analysis['findings']['can_access_params']}
- 环境信息获取: {analysis['findings']['has_environment_info']}
- 调用栈深度: {analysis['findings']['call_stack_depth']}
- 环境变量数量: {analysis['findings']['env_vars_found']}
- 对话上下文: {analysis['findings']['conversation_context']}

## 详细数据
原始测试数据已保存到: {analysis['raw_data_saved']}

## 关键发现
{'✅ MCP工具可以获取到：' if context_data else '❌ 数据收集失败'}
- 调用时的具体参数
- 系统环境信息
- 进程和调用栈信息
- 部分环境变量

{'❌ MCP工具无法获取到：' if 'conversation' not in str(context_data).lower() else '⚠️  需要进一步验证：'}
- Cursor对话历史
- 当前编辑的文件内容
- 用户的操作序列
- 代码上下文信息

## 结论
{f"MCP工具的上下文获取能力有限，主要限制在调用参数和系统环境信息。" if analysis['findings']['conversation_context'] == '无法直接获取' else '需要进一步分析是否能间接获取对话信息。'}

## 数据文件位置
测试数据保存在: {analysis['raw_data_saved']}
你可以手动查看该文件获取更详细的技术信息。
"""

        return result_text

    def setup_tools(self):
        """设置MCP工具"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """列出所有可用工具"""
            return [
                types.Tool(
                    name="get_prompt_template",
                    description="获取指定类型的提示词模板",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt_type": {
                                "type": "string",
                                "enum": ["git_commit", "code_review", "component_reuse", "project_environment_troubleshooting", "custom"],
                                "description": "提示词类型：git_commit(代码提交), code_review(代码审查), component_reuse(组件复用), project_environment_troubleshooting(项目环境排查), custom(自定义)"
                            },
                            "context": {
                                "type": "string",
                                "description": "附加上下文信息（可选）"
                            }
                        },
                        "required": ["prompt_type"]
                    }
                ),
                
                types.Tool(
                    name="find_reusable_components",
                    description="在项目中查找可复用的组件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "项目根目录路径"
                            },
                            "component_type": {
                                "type": "string",
                                "description": "查找的组件类型（如：table, form, modal等）"
                            },
                            "search_keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "搜索关键词"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                
                types.Tool(
                    name="track_usage",
                    description="记录MCP工具使用情况",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tool_name": {
                                "type": "string",
                                "description": "使用的工具名称"
                            },
                            "user_feedback": {
                                "type": "string",
                                "enum": ["excellent", "good", "average", "poor"],
                                "description": "用户反馈评价"
                            },
                            "usage_context": {
                                "type": "string",
                                "description": "使用场景描述"
                            }
                        },
                        "required": ["tool_name"]
                    }
                ),
                
                types.Tool(
                    name="get_usage_stats",
                    description="获取MCP工具使用统计数据",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date_range": {
                                "type": "string",
                                "enum": ["today", "week", "month", "all"],
                                "description": "统计时间范围"
                            }
                        },
                        "required": ["date_range"]
                    }
                ),
                
                types.Tool(
                    name="test_context_access",
                    description="测试MCP工具能获取到的上下文信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tool_name": {
                                "type": "string",
                                "description": "测试的工具名称",
                                "default": "context_test"
                            },
                            "usage_context": {
                                "type": "string", 
                                "description": "使用场景描述",
                                "default": "测试MCP上下文获取能力"
                            },
                            "test_data": {
                                "type": "string",
                                "description": "测试数据（用于验证参数传递）",
                                "default": ""
                            }
                        },
                        "required": []
                    }
                ),
                


            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent]:
            """处理工具调用"""
            
            try:
                if name == "get_prompt_template":
                    result = await self.prompt_manager.get_template(
                        arguments.get("prompt_type"),
                        arguments.get("context", "")
                    )
                    
                elif name == "find_reusable_components":
                    result = await self.component_finder.find_reusable_components(
                        project_path=arguments.get("project_path"),
                        component_type=arguments.get("component_type"),
                        search_keywords=arguments.get("search_keywords", [])
                    )
                    
                elif name == "track_usage":
                    result = await self.usage_tracker.track_usage(
                        tool_name=arguments.get("tool_name"),
                        user_feedback=arguments.get("user_feedback"),
                        usage_context=arguments.get("usage_context", "")
                    )
                    
                elif name == "get_usage_stats":
                    result = await self.usage_tracker.get_stats(
                        arguments.get("date_range", "all")
                    )
                    
                elif name == "test_context_access":
                    result = await self.test_context_access(
                        tool_name=arguments.get("tool_name", "context_test"),
                        usage_context=arguments.get("usage_context", "测试MCP上下文获取能力"),
                        test_data=arguments.get("test_data", ""),
                        **arguments
                    )
                    
                else:
                    result = f"❌ 未知工具: {name}\n\n可用工具：get_prompt_template, find_reusable_components, track_usage, get_usage_stats"
                
                # 记录工具使用
                await self.usage_tracker.log_tool_call(name, arguments)
                
                return [types.TextContent(type="text", text=str(result))]
                
            except Exception as e:
                logger.error(f"工具调用错误 {name}: {str(e)}")
                error_msg = f"""❌ **工具执行出错**

**工具名称:** {name}
**错误信息:** {str(e)}

请检查参数是否正确，或联系技术支持。"""
                return [types.TextContent(type="text", text=error_msg)]

async def main():
    """启动MCP服务器"""
    mcp_app = FrontendDevMCP()
    
    # 使用stdio传输
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await mcp_app.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="frontend-dev-assistant",
                server_version="1.0.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability(listChanged=False)
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main()) 