#!/usr/bin/env python3
"""
数据库初始化脚本
设置MCP Analytics数据库和表结构
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def setup_database():
    """初始化数据库"""
    try:
        from src.analytics_api.mcp_data_service import MCPDataService
        
        print("🗄️  初始化 MCP Analytics 数据库...")
        print("-" * 50)
        
        # 创建数据服务实例
        data_service = MCPDataService()
        
        # 初始化数据库
        await data_service.init_service()
        
        print("✅ 数据库初始化完成!")
        print("\n📊 数据表结构:")
        print("• users - 用户信息表")
        print("• usage_logs - MCP工具使用日志表")
        print("• git_sessions - Git编程会话表")
        print("• code_changes - 代码变更记录表")
        print("• commit_analysis - 提交分析表")
        
        print("\n🔧 下一步:")
        print("1. 启动API服务器: python scripts/start_api_server.py")
        print("2. 查看API文档: http://localhost:8000/docs")
        
        await data_service.close()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print("\n💡 常见解决方案:")
        print("1. 确保PostgreSQL服务正在运行")
        print("2. 检查数据库连接配置")
        print("3. 确保数据库用户有创建表的权限")
        return False
    
    return True

def print_database_config():
    """打印数据库配置信息"""
    print("🔧 数据库配置:")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"   环境变量: {database_url}")
    else:
        print("   默认配置: postgresql://mcp_user:mcp_password@localhost:5432/mcp_analytics")
        print("   💡 可通过设置 DATABASE_URL 环境变量来覆盖")
    
    print()

if __name__ == "__main__":
    print_database_config()
    
    if asyncio.run(setup_database()):
        sys.exit(0)
    else:
        sys.exit(1) 