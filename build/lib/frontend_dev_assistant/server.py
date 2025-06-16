#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 服务器
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from frontend_dev_assistant.prompt_manager import PromptManager
from frontend_dev_assistant.component_generator import ComponentGenerator
from frontend_dev_assistant.usage_tracker import UsageTracker

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend-dev-mcp")

class FrontendDevMCP:
    def __init__(self):
        self.server = Server("frontend-dev-assistant")
        self.prompt_manager = PromptManager()
        self.component_generator = ComponentGenerator()
        self.usage_tracker = UsageTracker()
        self.setup_tools()
    
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
                                "enum": ["git_commit", "code_review", "component_reuse", "custom"],
                                "description": "提示词类型：git_commit(代码提交), code_review(代码审查), component_reuse(组件复用), custom(自定义)"
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
                    name="generate_vue_component",
                    description="基于编码规范生成Vue组件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_type": {
                                "type": "string",
                                "enum": ["form", "table", "modal", "card", "list", "custom"],
                                "description": "组件类型"
                            },
                            "component_name": {
                                "type": "string",
                                "description": "组件名称（PascalCase）"
                            },
                            "vue_version": {
                                "type": "string", 
                                "enum": ["vue2", "vue3"],
                                "description": "Vue版本"
                            },
                            "props": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "required": {"type": "boolean"},
                                        "default": {"type": "string"}
                                    }
                                },
                                "description": "组件props定义"
                            },
                            "features": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "组件功能特性"
                            }
                        },
                        "required": ["component_type", "component_name", "vue_version"]
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
                    
                elif name == "generate_vue_component":
                    result = await self.component_generator.generate_component(
                        component_type=arguments.get("component_type"),
                        component_name=arguments.get("component_name"),
                        vue_version=arguments.get("vue_version"),
                        props=arguments.get("props", []),
                        features=arguments.get("features", [])
                    )
                    
                elif name == "find_reusable_components":
                    result = await self.component_generator.find_reusable_components(
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
                    

                    
                else:
                    result = f"未知工具: {name}"
                
                # 记录工具使用
                await self.usage_tracker.log_tool_call(name, arguments)
                
                return [types.TextContent(type="text", text=str(result))]
                
            except Exception as e:
                logger.error(f"工具调用错误 {name}: {str(e)}")
                return [types.TextContent(type="text", text=f"错误: {str(e)}")]

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