#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 主入口
"""

import asyncio
import sys
import os
from pathlib import Path

def main():
    """主入口函数"""
    print("🚀 启动前端开发提示词智能助手 MCP...")
    print("⚡ 正在初始化服务器...")
    
    try:
        # 导入服务器主函数
        from .server import main as server_main
        
        print("✅ MCP服务器启动成功！等待客户端连接...")
        print("💡 提示：服务器已就绪，可以在Cursor中使用MCP工具")
        asyncio.run(server_main())
    except KeyboardInterrupt:
        print("\n👋 MCP服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 