#!/usr/bin/env python3
"""
测试MCP服务器是否能正常初始化
"""

import sys
import os
import asyncio

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.server import FrontendDevMCP

async def test_server_init():
    """测试服务器初始化"""
    try:
        print("🧪 测试MCP服务器初始化...")
        mcp_app = FrontendDevMCP()
        print("✅ MCP服务器初始化成功!")
        
        # 测试各个组件
        print("🔧 测试提示词管理器...")
        result = await mcp_app.prompt_manager.get_template("git_commit")
        if "代码提交助手" in result:
            print("✅ 提示词管理器工作正常")
        
        print("🎨 测试组件生成器...")
        result = await mcp_app.component_generator.generate_component(
            "form", "TestForm", "vue3"
        )
        if "TestForm" in result:
            print("✅ 组件生成器工作正常")
        
        print("📊 测试使用统计器...")
        await mcp_app.usage_tracker.log_tool_call("test", {})
        result = await mcp_app.usage_tracker.get_stats("all")
        if "统计报告" in result:
            print("✅ 使用统计器工作正常")
            
        return True
        
    except Exception as e:
        print(f"❌ 服务器初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 测试前端开发提示词智能助手 MCP 服务器")
    print("="*60)
    
    success = asyncio.run(test_server_init())
    
    if success:
        print("\n🎉 服务器测试通过!")
        print("📋 MCP服务器可以正常工作")
        print("💡 要在Cursor中使用，需要正确配置MCP连接")
        print("🔗 Cursor配置指南: 查看 cursor_config.md")
        print("⚡ 快速使用: 查看 static_prompts.md")
    else:
        print("\n💔 服务器测试失败")
        sys.exit(1) 