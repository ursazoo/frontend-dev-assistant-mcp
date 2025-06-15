#!/usr/bin/env python3
"""
直接运行frontend_dev_assistant MCP服务器
用于本地测试MCP调用追踪系统
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# 设置环境变量
os.environ["PYTHONPATH"] = str(src_dir)

# 导入并运行MCP服务器
if __name__ == "__main__":
    try:
        from frontend_dev_assistant.server import main
        import asyncio
        
        print("🚀 启动 Frontend Dev Assistant MCP 服务器...")
        print("📍 项目路径:", current_dir)
        print("📊 调用追踪: 已启用")
        print("=" * 50)
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n🛑 MCP服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查依赖是否正确安装") 