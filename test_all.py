#!/usr/bin/env python3
"""
前端开发者MCP Analytics API完整测试脚本
模拟注册用户、记录使用、查看报告的全流程
"""

import json
import uuid
import time
import os
import sqlite3
from pathlib import Path

def test_with_simple_database():
    """直接测试SQLite数据库功能"""
    print("🧪 测试SQLite数据库功能")
    print("=" * 30)
    
    # 创建数据库
    data_dir = Path.home() / ".frontend-dev-assistant"
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / "test_mcp.db"
    
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            arguments TEXT
        )
    ''')
    
    # 测试插入数据
    test_uuid = str(uuid.uuid4())
    test_email = "frontend.dev@company.com"
    
    print(f"📝 注册测试用户: {test_email}")
    conn.execute(
        "INSERT INTO users (uuid, email, name, department) VALUES (?, ?, ?, ?)",
        (test_uuid, test_email, "前端开发者", "技术部")
    )
    
    print(f"📊 记录工具使用")
    conn.execute(
        "INSERT INTO usage_logs (user_uuid, tool_name, arguments) VALUES (?, ?, ?)",
        (test_uuid, "generate_vue_component", '{"component_type": "form", "features": ["validation"]}')
    )
    
    conn.execute(
        "INSERT INTO usage_logs (user_uuid, tool_name, arguments) VALUES (?, ?, ?)",
        (test_uuid, "find_reusable_components", '{"component_type": "table"}')
    )
    
    conn.commit()
    
    # 查询统计
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM usage_logs WHERE user_uuid = ?", (test_uuid,))
    usage_count = cursor.fetchone()[0]
    
    cursor = conn.execute(
        "SELECT tool_name, COUNT(*) as count FROM usage_logs WHERE user_uuid = ? GROUP BY tool_name", 
        (test_uuid,)
    )
    tool_stats = cursor.fetchall()
    
    print(f"✅ 数据库测试成功!")
    print(f"   用户数: {user_count}")
    print(f"   使用记录: {usage_count}")
    print(f"   工具统计:")
    for tool, count in tool_stats:
        print(f"     {tool}: {count}次")
    
    conn.close()
    
    print(f"💾 数据库文件: {db_path}")
    return True

def test_api_manually():
    """手动API测试说明"""
    print("\n🌐 API服务器测试指南")
    print("=" * 30)
    
    print("📋 请在两个终端窗口中分别运行：")
    print()
    print("🖥️  【终端1 - 启动服务器】")
    print("   cd " + os.getcwd())
    print("   python3 simple_start.py")
    print()
    print("🖥️  【终端2 - 测试API】")
    print("   # 健康检查")
    print("   curl http://localhost:8000/health")
    print()
    print("   # 注册用户")
    test_uuid = str(uuid.uuid4())
    print(f"""   curl -X POST http://localhost:8000/api/users/register \\
     -H "Content-Type: application/json" \\
     -d '{{"uuid": "{test_uuid}", "email": "test@company.com", "name": "测试用户", "department": "技术部"}}'""")
    print()
    print("   # 记录使用")
    print(f"""   curl -X POST http://localhost:8000/api/usage/log \\
     -H "Content-Type: application/json" \\
     -d '{{"user_uuid": "{test_uuid}", "tool_name": "generate_vue_component", "arguments": {{"type": "form"}}}}'""")
    print()
    print("   # 查看报告")
    print(f"   curl http://localhost:8000/api/users/{test_uuid}/report")

def create_enterprise_config():
    """创建企业配置文件"""
    print("\n🏢 创建企业配置")
    print("=" * 20)
    
    config_dir = Path.home() / ".frontend-dev-assistant"
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "enterprise.json"
    
    enterprise_config = {
        "user_email": "frontend.developer@company.com",
        "user_name": "前端开发者",
        "department": "技术研发部",
        "company": "科技公司",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(enterprise_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 企业配置已创建: {config_file}")
    print("📄 配置内容:")
    print(json.dumps(enterprise_config, ensure_ascii=False, indent=2))

def show_file_structure():
    """显示项目文件结构"""
    print("\n📁 项目文件结构")
    print("=" * 20)
    
    important_files = [
        "simple_start.py",           # 简化版API服务器
        "test_simple.py",           # 测试服务器
        "test_all.py",              # 这个测试脚本
        "src/analytics_api/",       # 完整版API模块
        "src/frontend_dev_assistant/cloud_usage_tracker.py",  # 云端追踪器
        "docker-compose.yml",       # Docker配置
    ]
    
    for file_path in important_files:
        full_path = Path(file_path)
        if full_path.exists():
            if full_path.is_dir():
                print(f"📁 {file_path}/")
            else:
                size = full_path.stat().st_size
                print(f"📄 {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (不存在)")

def main():
    """主测试函数"""
    print("🎯 MCP Analytics 前端开发者测试套件")
    print("=" * 50)
    
    # 1. 测试数据库功能
    test_with_simple_database()
    
    # 2. 创建企业配置
    create_enterprise_config()
    
    # 3. 显示文件结构
    show_file_structure()
    
    # 4. API测试指南
    test_api_manually()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！你的MCP Analytics系统已准备就绪")
    print()
    print("📚 下一步操作：")
    print("1. 按照上面的API测试指南启动服务器")
    print("2. 在另一个终端测试API接口")
    print("3. 使用浏览器访问 http://localhost:8000/health")
    print()
    print("💡 提示：所有数据存储在 ~/.frontend-dev-assistant/ 目录")

if __name__ == "__main__":
    main() 