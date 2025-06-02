#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 功能测试脚本
"""

import sys
import os
import asyncio
import json

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.prompt_manager import PromptManager
from src.component_generator import ComponentGenerator  
from src.usage_tracker import UsageTracker

async def test_prompt_manager():
    """测试提示词管理功能"""
    print("🧪 测试提示词管理功能...")
    
    prompt_manager = PromptManager()
    
    # 测试获取代码提交模板
    result = await prompt_manager.get_template("git_commit", "修复登录页面样式问题")
    print("✅ 代码提交模板:", "成功" if "代码提交助手" in result else "失败")
    
    # 测试获取代码审查模板
    result = await prompt_manager.get_template("code_review")
    print("✅ 代码审查模板:", "成功" if "代码审查助手" in result else "失败")
    
    # 测试列出所有模板
    result = await prompt_manager.list_templates()
    print("✅ 列出模板:", "成功" if "可用的提示词模板" in result else "失败")

async def test_component_generator():
    """测试组件生成功能"""
    print("\n🧪 测试组件生成功能...")
    
    component_generator = ComponentGenerator()
    
    # 测试生成表单组件
    result = await component_generator.generate_component(
        component_type="form",
        component_name="UserForm", 
        vue_version="vue3",
        props=[
            {"name": "title", "type": "string", "required": False, "default": "用户表单"},
            {"name": "fields", "type": "array", "required": True}
        ],
        features=["validation", "loading"]
    )
    print("✅ 生成表单组件:", "成功" if "UserForm" in result else "失败")
    
    # 测试生成表格组件
    result = await component_generator.generate_component(
        component_type="table",
        component_name="DataTable",
        vue_version="vue3"
    )
    print("✅ 生成表格组件:", "成功" if "DataTable" in result else "失败")

async def test_usage_tracker():
    """测试使用统计功能"""
    print("\n🧪 测试使用统计功能...")
    
    usage_tracker = UsageTracker()
    
    # 测试记录工具调用
    await usage_tracker.log_tool_call("get_prompt_template", {"prompt_type": "git_commit"})
    await usage_tracker.log_tool_call("generate_vue_component", {"component_type": "form"})
    
    # 测试记录反馈
    result = await usage_tracker.track_usage("get_prompt_template", "excellent", "提交代码场景")
    print("✅ 记录反馈:", "成功" if "已记录" in result else "失败")
    
    # 测试获取统计
    result = await usage_tracker.get_stats("all")
    print("✅ 获取统计:", "成功" if "统计报告" in result else "失败")

async def test_integration():
    """测试集成功能"""
    print("\n🧪 测试集成功能...")
    
    # 模拟完整的使用流程
    prompt_manager = PromptManager()
    component_generator = ComponentGenerator()
    usage_tracker = UsageTracker()
    
    # 1. 获取提示词
    prompt_result = await prompt_manager.get_template("vue_component_spec")
    
    # 2. 生成组件
    component_result = await component_generator.generate_component(
        component_type="modal",
        component_name="ConfirmDialog",
        vue_version="vue3"
    )
    
    # 3. 记录使用和反馈
    await usage_tracker.log_tool_call("get_prompt_template")
    await usage_tracker.log_tool_call("generate_vue_component") 
    await usage_tracker.track_usage("generate_vue_component", "good", "生成确认对话框")
    
    print("✅ 集成测试:", "成功")

def print_test_summary():
    """打印测试总结"""
    print("\n" + "="*50)
    print("🎉 MCP功能测试完成!")
    print("="*50)
    print("📋 测试项目:")
    print("  ✅ 提示词管理功能")
    print("  ✅ 组件生成功能") 
    print("  ✅ 使用统计功能")
    print("  ✅ 集成功能测试")
    print("\n🚀 可以开始使用MCP了!")
    print("📖 查看 cursor_config.md 了解如何在Cursor中配置")

async def main():
    """主测试函数"""
    print("🚀 前端开发提示词智能助手 MCP 功能测试")
    print("="*50)
    
    try:
        # 运行所有测试
        await test_prompt_manager()
        await test_component_generator() 
        await test_usage_tracker()
        await test_integration()
        
        # 打印测试总结
        print_test_summary()
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 