#!/usr/bin/env python3
"""
MCP Analytics API 服务器启动脚本
简化版数据收集服务
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("🚀 启动 MCP Analytics API 数据收集服务...")
    print("📊 专注于MCP工具使用数据收集和git分析")
    print("🔗 API文档: http://localhost:8000/docs")
    print("📍 健康检查: http://localhost:8000/health")
    print("-" * 50)
    
    try:
        from src.analytics_api.server import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1) 