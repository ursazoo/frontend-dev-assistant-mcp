#!/usr/bin/env python3
"""
启动 MCP Analytics API 服务器
"""

import sys
import os
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """启动API服务器"""
    try:
        from analytics_api.server import start_server
        
        print("🚀 启动 MCP Analytics API 服务器...")
        print("=" * 50)
        
        # 检查环境变量
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            print(f"📊 数据库连接: {database_url}")
        else:
            print("📊 数据库连接: 使用默认本地PostgreSQL配置")
        
        # 启动服务器
        start_server(
            host="0.0.0.0",
            port=8000,
            reload=True  # 开发模式，代码变更自动重启
        )
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装必要的依赖：pip install fastapi uvicorn asyncpg")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 