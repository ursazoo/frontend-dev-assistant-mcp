#!/usr/bin/env python3
"""
前端开发提示词智能助手 MCP 启动脚本
"""

import sys
import os
import asyncio

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.server import main

if __name__ == "__main__":
    print("🚀 启动前端开发提示词智能助手 MCP...")
    print("⚡ 正在初始化服务器...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 MCP服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        sys.exit(1) 