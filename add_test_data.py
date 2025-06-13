#!/usr/bin/env python3
"""
为MCP Analytics数据库添加测试数据
让你在Navicat中能看到丰富的示例数据
"""

import json
import uuid
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

def add_test_data_directly():
    """直接向SQLite数据库添加测试数据"""
    db_path = Path.home() / ".frontend-dev-assistant" / "mcp_analytics.db"
    
    if not db_path.exists():
        print("❌ 数据库文件不存在，请先运行 python3 simple_start.py 创建数据库")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    print(f"📄 连接数据库: {db_path}")
    
    # 添加测试用户
    test_users = [
        {
            "uuid": str(uuid.uuid4()),
            "email": "alice@company.com",
            "name": "Alice 前端工程师",
            "department": "前端开发部"
        },
        {
            "uuid": str(uuid.uuid4()),
            "email": "bob@company.com", 
            "name": "Bob UI设计师",
            "department": "设计部"
        },
        {
            "uuid": str(uuid.uuid4()),
            "email": "charlie@company.com",
            "name": "Charlie 全栈开发",
            "department": "技术部"
        }
    ]
    
    print("👥 添加测试用户...")
    for user in test_users:
        try:
            conn.execute(
                "INSERT OR REPLACE INTO users (uuid, email, name, department) VALUES (?, ?, ?, ?)",
                (user["uuid"], user["email"], user["name"], user["department"])
            )
            print(f"   ✅ {user['name']} ({user['email']})")
        except Exception as e:
            print(f"   ❌ {user['name']}: {e}")
    
    # 添加使用记录
    mcp_tools = [
        "generate_vue_component",
        "find_reusable_components", 
        "get_prompt_template",
        "track_usage",
        "smart_feedback_collector"
    ]
    
    print("\n📊 添加使用记录...")
    usage_count = 0
    
    for user in test_users:
        # 为每个用户添加不同数量的使用记录
        for day_offset in range(30):  # 过去30天的数据
            date = datetime.now() - timedelta(days=day_offset)
            
            # 每天随机使用1-5次工具
            import random
            daily_usage = random.randint(1, 5)
            
            for _ in range(daily_usage):
                tool = random.choice(mcp_tools)
                arguments = {
                    "component_type": random.choice(["form", "table", "modal", "card"]),
                    "features": random.choice([["validation"], ["pagination"], ["search"], []])
                }
                
                conn.execute(
                    "INSERT INTO usage_logs (user_uuid, tool_name, timestamp, arguments) VALUES (?, ?, ?, ?)",
                    (user["uuid"], tool, date.isoformat(), json.dumps(arguments))
                )
                usage_count += 1
    
    conn.commit()
    
    # 查询统计信息
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM usage_logs") 
    total_usage = cursor.fetchone()[0]
    
    cursor = conn.execute("""
        SELECT tool_name, COUNT(*) as count 
        FROM usage_logs 
        GROUP BY tool_name 
        ORDER BY count DESC
    """)
    tool_stats = cursor.fetchall()
    
    print(f"\n✅ 测试数据添加完成!")
    print(f"📊 统计信息:")
    print(f"   👥 用户数: {user_count}")
    print(f"   📝 使用记录: {total_usage}")
    print(f"   🔧 工具使用统计:")
    
    for tool in tool_stats:
        print(f"     {tool['tool_name']}: {tool['count']}次")
    
    conn.close()
    print(f"\n🎯 现在可以在Navicat中查看数据了!")
    print(f"📍 数据库文件路径: {db_path}")

def test_api_with_curl():
    """提供curl命令来测试API"""
    print("\n🌐 API测试命令:")
    print("=" * 40)
    
    # 生成一个测试UUID
    test_uuid = str(uuid.uuid4())
    
    print("1️⃣ 健康检查:")
    print("curl http://localhost:8000/health")
    print()
    
    print("2️⃣ 注册用户:")
    print(f'''curl -X POST http://localhost:8000/api/users/register \\
  -H "Content-Type: application/json" \\
  -d '{{"uuid": "{test_uuid}", "email": "test@company.com", "name": "测试用户", "department": "技术部"}}\'''')
    print()
    
    print("3️⃣ 记录使用:")
    print(f'''curl -X POST http://localhost:8000/api/usage/log \\
  -H "Content-Type: application/json" \\
  -d '{{"user_uuid": "{test_uuid}", "tool_name": "generate_vue_component", "arguments": {{"type": "form"}}}}\'''')
    print()
    
    print("4️⃣ 查看报告:")
    print(f"curl http://localhost:8000/api/users/{test_uuid}/report")

def main():
    """主函数"""
    print("🎯 MCP Analytics 测试数据生成器")
    print("=" * 50)
    
    # 添加测试数据
    add_test_data_directly()
    
    # 显示API测试命令
    test_api_with_curl()
    
    print("\n" + "=" * 50)
    print("📚 在Navicat中查看数据的步骤:")
    print("1. 打开Navicat")
    print("2. 点击 '连接' -> 'SQLite'")
    print("3. 选择数据库文件:")
    print("   ~/.frontend-dev-assistant/mcp_analytics.db")
    print("4. 连接后可以看到两个表:")
    print("   - users (用户表)")
    print("   - usage_logs (使用记录表)")
    print("5. 右键表名 -> '打开表' 查看数据")

if __name__ == "__main__":
    main() 