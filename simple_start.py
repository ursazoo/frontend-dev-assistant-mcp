#!/usr/bin/env python3
"""
前端开发者友好的MCP Analytics启动脚本
无需Docker、PostgreSQL等复杂配置，一键启动测试环境
"""

import json
import uuid
import sqlite3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

class SimpleMCPDatabase:
    """简化的SQLite数据库管理"""
    
    def __init__(self):
        # 在用户主目录创建数据库
        data_dir = Path.home() / ".frontend-dev-assistant"
        data_dir.mkdir(exist_ok=True)
        self.db_path = data_dir / "mcp_analytics.db"
        self.init_database()
        print(f"📄 SQLite数据库: {self.db_path}")
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uuid TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_uuid TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                arguments TEXT,
                FOREIGN KEY (user_uuid) REFERENCES users(uuid)
            )
        ''')
        
        # 创建索引
        conn.execute('CREATE INDEX IF NOT EXISTS idx_usage_logs_user_uuid ON usage_logs(user_uuid)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_usage_logs_timestamp ON usage_logs(timestamp)')
        
        conn.commit()
        conn.close()
        print("✅ 数据库表结构已创建")
    
    def register_user(self, uuid_str: str, email: str, name: str = None, department: str = None):
        """注册用户"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # 检查是否存在
            cursor = conn.execute("SELECT uuid FROM users WHERE uuid = ?", (uuid_str,))
            existing = cursor.fetchone()
            
            if existing:
                conn.execute(
                    "UPDATE users SET email = ?, name = ?, department = ?, last_active = ? WHERE uuid = ?",
                    (email, name, department, datetime.now().isoformat(), uuid_str)
                )
                status = "updated"
            else:
                conn.execute(
                    "INSERT INTO users (uuid, email, name, department) VALUES (?, ?, ?, ?)",
                    (uuid_str, email, name, department)
                )
                status = "created"
            
            conn.commit()
            return {"status": status, "uuid": uuid_str}
        finally:
            conn.close()
    
    def log_usage(self, user_uuid: str, tool_name: str, arguments: Dict = None):
        """记录使用"""
        conn = sqlite3.connect(self.db_path)
        try:
            # 检查用户是否存在
            cursor = conn.execute("SELECT uuid FROM users WHERE uuid = ?", (user_uuid,))
            if not cursor.fetchone():
                raise Exception("用户不存在")
            
            conn.execute(
                "INSERT INTO usage_logs (user_uuid, tool_name, arguments) VALUES (?, ?, ?)",
                (user_uuid, tool_name, json.dumps(arguments) if arguments else None)
            )
            
            # 更新最后活跃时间
            conn.execute(
                "UPDATE users SET last_active = ? WHERE uuid = ?",
                (datetime.now().isoformat(), user_uuid)
            )
            
            conn.commit()
            return {"status": "logged"}
        finally:
            conn.close()
    
    def get_user_report(self, user_uuid: str, days: int = 30):
        """获取用户报告"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # 获取用户信息
            cursor = conn.execute("SELECT * FROM users WHERE uuid = ?", (user_uuid,))
            user = cursor.fetchone()
            if not user:
                raise Exception("用户不存在")
            
            # 计算时间范围
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # 统计数据
            cursor = conn.execute(
                "SELECT COUNT(*) FROM usage_logs WHERE user_uuid = ? AND timestamp >= ?",
                (user_uuid, start_date)
            )
            total_usage = cursor.fetchone()[0]
            
            # 工具统计
            cursor = conn.execute(
                "SELECT tool_name, COUNT(*) as count FROM usage_logs WHERE user_uuid = ? AND timestamp >= ? GROUP BY tool_name ORDER BY count DESC",
                (user_uuid, start_date)
            )
            tool_stats = [{"tool": row["tool_name"], "count": row["count"]} for row in cursor.fetchall()]
            
            return {
                "user": {
                    "uuid": user["uuid"],
                    "email": user["email"],
                    "name": user["name"],
                    "department": user["department"]
                },
                "period": f"{days} days",
                "summary": {
                    "total_usage": total_usage,
                    "tools_count": len(tool_stats),
                    "avg_daily": round(total_usage / days, 1) if days > 0 else 0
                },
                "tool_stats": tool_stats
            }
        finally:
            conn.close()

class MCPAPIHandler(BaseHTTPRequestHandler):
    """简化的API处理器"""
    
    def __init__(self, *args, db_manager=None, **kwargs):
        self.db = db_manager
        super().__init__(*args, **kwargs)
    
    def _send_json(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _get_json_body(self):
        """获取JSON请求体"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body.decode('utf-8'))
            return {}
        except:
            return {}
    
    def do_OPTIONS(self):
        self._send_json(200, {"message": "OK"})
    
    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        
        try:
            if path == '/' or path == '/health':
                self._send_json(200, {
                    "message": "MCP Analytics API (前端友好版)",
                    "version": "1.0.0-simple",
                    "status": "running",
                    "database": "SQLite",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif path.startswith('/api/users/') and path.endswith('/report'):
                user_uuid = path.split('/')[-2]
                days = int(query.get('days', ['30'])[0])
                
                try:
                    report = self.db.get_user_report(user_uuid, days)
                    self._send_json(200, {
                        "status": "success",
                        "data": report
                    })
                except Exception as e:
                    if "用户不存在" in str(e):
                        self._send_json(404, {"status": "error", "message": "用户不存在"})
                    else:
                        self._send_json(500, {"status": "error", "message": str(e)})
            
            else:
                self._send_json(404, {"status": "error", "message": "接口不存在"})
                
        except Exception as e:
            self._send_json(500, {"status": "error", "message": str(e)})
    
    def do_POST(self):
        path = urlparse(self.path).path
        data = self._get_json_body()
        
        try:
            if path == '/api/users/register':
                if 'uuid' not in data or 'email' not in data:
                    self._send_json(400, {"status": "error", "message": "缺少uuid或email字段"})
                    return
                
                result = self.db.register_user(
                    data['uuid'], data['email'], 
                    data.get('name'), data.get('department')
                )
                self._send_json(200, {"status": "success", "data": result})
            
            elif path == '/api/usage/log':
                if 'user_uuid' not in data or 'tool_name' not in data:
                    self._send_json(400, {"status": "error", "message": "缺少user_uuid或tool_name字段"})
                    return
                
                result = self.db.log_usage(
                    data['user_uuid'], data['tool_name'], 
                    data.get('arguments', {})
                )
                self._send_json(200, {"status": "success", "data": result})
            
            else:
                self._send_json(404, {"status": "error", "message": "接口不存在"})
                
        except Exception as e:
            if "用户不存在" in str(e):
                self._send_json(404, {"status": "error", "message": "用户不存在，请先注册"})
            else:
                self._send_json(500, {"status": "error", "message": str(e)})
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

def main():
    """主函数"""
    print("🎯 MCP Analytics - 前端开发者友好版")
    print("=" * 40)
    
    # 初始化数据库
    db = SimpleMCPDatabase()
    
    # 创建服务器
    def handler_factory(*args, **kwargs):
        return MCPAPIHandler(*args, db_manager=db, **kwargs)
    
    host, port = 'localhost', 7220
    server = HTTPServer((host, port), handler_factory)
    
    print(f"🚀 服务器启动成功!")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📊 数据库: SQLite")
    print(f"🧪 测试接口:")
    print(f"   GET  http://{host}:{port}/health")
    print(f"   POST http://{host}:{port}/api/users/register")
    print(f"   POST http://{host}:{port}/api/usage/log")
    print(f"   GET  http://{host}:{port}/api/users/{{uuid}}/report")
    print("=" * 40)
    print("📝 示例测试命令:")
    print("curl http://localhost:7220/health")
    print("🛑 按 Ctrl+C 停止服务器")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        server.shutdown()

if __name__ == "__main__":
    main()