#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 服务器
"""

import logging
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from mcp_local.prompt_manager import PromptManager
from mcp_local.component_generator import ComponentGenerator
from mcp_local.usage_tracker import UsageTracker

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend-dev-mcp")

# 实例化 MCP 服务器
mcp = FastMCP("frontend-dev-assistant")

prompt_manager = PromptManager()
component_generator = ComponentGenerator()
usage_tracker = UsageTracker()

@mcp.tool()
def get_prompt_template(prompt_type: str, context: str = "") -> str:
    """获取指定类型的提示词模板"""
    return prompt_manager.get_template(prompt_type, context)

@mcp.tool()
def generate_vue_component(
    component_type: str,
    component_name: str,
    vue_version: str,
    props: list = None,
    features: list = None
) -> str:
    """基于编码规范生成Vue组件"""
    return component_generator.generate_component(
        component_type=component_type,
        component_name=component_name,
        vue_version=vue_version,
        props=props or [],
        features=features or []
    )

@mcp.tool()
def find_reusable_components(
    project_path: str,
    component_type: str = None,
    search_keywords: list = None
) -> str:
    """在项目中查找可复用的组件"""
    return component_generator.find_reusable_components(
        project_path=project_path,
        component_type=component_type,
        search_keywords=search_keywords or []
    )

@mcp.tool()
def track_usage(
    tool_name: str,
    user_feedback: str = None,
    usage_context: str = ""
) -> str:
    """记录MCP工具使用情况"""
    return usage_tracker.track_usage(
        tool_name=tool_name,
        user_feedback=user_feedback,
        usage_context=usage_context
    )

@mcp.tool()
async def get_usage_stats(date_range: str = "all") -> str:
    """获取MCP工具使用统计数据"""
    return await usage_tracker.get_stats(date_range)

if __name__ == "__main__":
    mcp.run() 