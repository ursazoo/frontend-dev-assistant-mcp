#!/usr/bin/env python3
"""
数据查看器 - 如果Navicat不显示数据，用这个脚本查看
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def view_database_data():
    """查看数据库数据"""
    db_path = Path.home() / ".frontend-dev-assistant" / "mcp_analytics.db"
    
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return
    
    print(f"📄 数据库文件: {db_path}")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # 查看用户数据
    print("👥 用户表 (users):")
    print("-" * 30)
    cursor = conn.execute("SELECT * FROM users ORDER BY created_at")
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"📧 {user['email']}")
            print(f"   姓名: {user['name']}")
            print(f"   部门: {user['department']}")
            print(f"   UUID: {user['uuid'][:8]}...")
            print(f"   注册时间: {user['created_at']}")
            print(f"   最后活跃: {user['last_active']}")
            print()
    else:
        print("   (无数据)")
    
    # 查看使用记录统计
    print("\n📊 使用记录统计:")
    print("-" * 30)
    cursor = conn.execute("""
        SELECT 
            tool_name, 
            COUNT(*) as count,
            MAX(timestamp) as last_used
        FROM usage_logs 
        GROUP BY tool_name 
        ORDER BY count DESC
    """)
    
    tool_stats = cursor.fetchall()
    for tool in tool_stats:
        print(f"🔧 {tool['tool_name']}: {tool['count']}次 (最后使用: {tool['last_used'][:10]})")
    
    # 查看最近使用记录
    print("\n📝 最近10条使用记录:")
    print("-" * 30)
    cursor = conn.execute("""
        SELECT 
            u.name,
            u.email,
            ul.tool_name,
            ul.timestamp,
            ul.arguments
        FROM usage_logs ul
        JOIN users u ON ul.user_uuid = u.uuid
        ORDER BY ul.timestamp DESC
        LIMIT 10
    """)
    
    recent_logs = cursor.fetchall()
    for i, log in enumerate(recent_logs, 1):
        print(f"{i:2d}. {log['name']} 使用了 {log['tool_name']}")
        print(f"     时间: {log['timestamp']}")
        if log['arguments']:
            args = json.loads(log['arguments'])
            print(f"     参数: {args}")
        print()
    
    # 每日使用趋势
    print("\n📈 每日使用趋势 (最近7天):")
    print("-" * 30)
    cursor = conn.execute("""
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as daily_count
        FROM usage_logs 
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    """)
    
    daily_stats = cursor.fetchall()
    for day in daily_stats:
        print(f"📅 {day['date']}: {day['daily_count']}次使用")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("💡 提示: 这些数据同样存在于Navicat中，请尝试:")
    print("   1. 展开左侧的 'Tables' 文件夹")
    print("   2. 双击 'users' 或 'usage_logs' 表")
    print("   3. 或者使用 '新建查询' 执行SQL")

if __name__ == "__main__":
    view_database_data() 