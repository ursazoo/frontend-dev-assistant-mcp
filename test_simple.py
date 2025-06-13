#!/usr/bin/env python3

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "message": "前端开发者友好版MCP Analytics服务器",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

if __name__ == "__main__":
    port = 8001  # 使用不同端口避免冲突
    server = HTTPServer(('localhost', port), TestHandler)
    print(f"🚀 测试服务器启动: http://localhost:{port}")
    print(f"📋 测试命令: curl http://localhost:{port}/health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.shutdown() 