#!/usr/bin/env python3
"""
前端开发助手 MCP 服务器
提供代码生成、组件查找、Git管理等功能
"""

import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from .call_tracker import call_tracker

__version__ = "0.1.0"
__author__ = "Frontend Dev Team"
__description__ = "前端开发提示词智能助手 MCP服务器 - 专为前端团队设计的AI开发助手"

from .main import main

__all__ = ["main"]

async def test_context_access(
    tool_name: str = "context_test",
    usage_context: str = "测试MCP上下文获取能力",
    test_data: str = "",
    **kwargs
) -> List[TextContent]:
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
"""

    return [TextContent(type="text", text=result_text)]

# 注册新的测试工具
@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        # ... existing tools ...
        Tool(
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
        # ... rest of existing tools ...
    ]
