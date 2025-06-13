#!/usr/bin/env python3
"""
MCP Analytics 实时测试脚本
模拟真实的用户使用场景并验证数据流
"""

import json
import uuid
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode

class MCPAnalyticsTest:
    def __init__(self):
        self.api_base = "http://localhost:7220"
        self.db_path = Path.home() / ".frontend-dev-assistant" / "mcp_analytics.db"
        self.test_user_uuid = str(uuid.uuid4())
        self.test_email = f"tester_{int(time.time())}@company.com"
    
    def send_request(self, method, endpoint, data=None):
        """发送HTTP请求"""
        url = f"{self.api_base}{endpoint}"
        
        if method == "GET":
            try:
                with urlopen(url) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                return {"error": str(e)}
        
        elif method == "POST":
            try:
                headers = {'Content-Type': 'application/json'}
                json_data = json.dumps(data).encode('utf-8')
                req = Request(url, data=json_data, headers=headers, method='POST')
                with urlopen(req) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                return {"error": str(e)}
    
    def check_api_health(self):
        """检查API健康状态"""
        print("🩺 检查API服务器状态...")
        result = self.send_request("GET", "/health")
        
        if "error" not in result:
            print(f"✅ API服务器正常运行")
            print(f"   版本: {result.get('version')}")
            print(f"   数据库: {result.get('database')}")
            return True
        else:
            print(f"❌ API服务器连接失败: {result['error']}")
            return False
    
    def register_test_user(self):
        """注册测试用户"""
        print(f"\n👤 注册新用户...")
        print(f"   UUID: {self.test_user_uuid[:8]}...")
        print(f"   邮箱: {self.test_email}")
        
        user_data = {
            "uuid": self.test_user_uuid,
            "email": self.test_email,
            "name": "实时测试用户",
            "department": "测试部门"
        }
        
        result = self.send_request("POST", "/api/users/register", user_data)
        
        if "error" not in result and result.get("status") == "success":
            print(f"✅ 用户注册成功")
            print(f"   状态: {result['data']['status']}")
            return True
        else:
            print(f"❌ 用户注册失败: {result}")
            return False
    
    def simulate_tool_usage(self):
        """模拟MCP工具使用"""
        print(f"\n🔧 模拟MCP工具使用...")
        
        test_scenarios = [
            {
                "tool": "generate_vue_component",
                "args": {
                    "component_type": "form",
                    "features": ["validation", "submit"],
                    "vue_version": "vue3"
                }
            },
            {
                "tool": "find_reusable_components",
                "args": {
                    "component_type": "table",
                    "search_keywords": ["pagination", "sort"]
                }
            },
            {
                "tool": "get_prompt_template",
                "args": {
                    "prompt_type": "code_review"
                }
            }
        ]
        
        success_count = 0
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"   {i}. 使用工具: {scenario['tool']}")
            
            usage_data = {
                "user_uuid": self.test_user_uuid,
                "tool_name": scenario["tool"],
                "arguments": scenario["args"]
            }
            
            result = self.send_request("POST", "/api/usage/log", usage_data)
            
            if "error" not in result and result.get("status") == "success":
                print(f"      ✅ 记录成功")
                success_count += 1
            else:
                print(f"      ❌ 记录失败: {result}")
            
            time.sleep(0.5)  # 短暂延迟模拟真实使用
        
        print(f"   📊 成功记录 {success_count}/{len(test_scenarios)} 条使用记录")
        return success_count > 0
    
    def get_user_report(self):
        """获取用户报告"""
        print(f"\n📈 获取用户使用报告...")
        
        result = self.send_request("GET", f"/api/users/{self.test_user_uuid}/report?days=7")
        
        if "error" not in result and result.get("status") == "success":
            report = result["data"]
            print(f"✅ 报告生成成功")
            print(f"   时间范围: {report['period']}")
            print(f"   总使用次数: {report['summary']['total_usage']}")
            print(f"   使用工具数: {report['summary']['tools_count']}")
            print(f"   日均使用: {report['summary']['avg_daily']}")
            
            print(f"   🔧 工具使用详情:")
            for tool in report["tool_stats"]:
                print(f"      - {tool['tool']}: {tool['count']}次")
            
            return True
        else:
            print(f"❌ 获取报告失败: {result}")
            return False
    
    def verify_in_database(self):
        """验证数据库中的数据"""
        print(f"\n🗄️ 验证数据库中的记录...")
        
        if not self.db_path.exists():
            print("❌ 数据库文件不存在")
            return False
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # 检查用户记录
            cursor = conn.execute(
                "SELECT * FROM users WHERE uuid = ?", 
                (self.test_user_uuid,)
            )
            user = cursor.fetchone()
            
            if user:
                print(f"✅ 用户记录已保存")
                print(f"   姓名: {user['name']}")
                print(f"   邮箱: {user['email']}")
                print(f"   部门: {user['department']}")
            else:
                print("❌ 用户记录未找到")
                return False
            
            # 检查使用记录
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM usage_logs WHERE user_uuid = ?",
                (self.test_user_uuid,)
            )
            usage_count = cursor.fetchone()["count"]
            
            print(f"✅ 使用记录已保存: {usage_count}条")
            
            # 显示具体记录
            cursor = conn.execute(
                """SELECT tool_name, timestamp, arguments 
                   FROM usage_logs 
                   WHERE user_uuid = ? 
                   ORDER BY timestamp DESC""",
                (self.test_user_uuid,)
            )
            
            logs = cursor.fetchall()
            print(f"   📝 记录详情:")
            for log in logs:
                print(f"      - {log['tool_name']} ({log['timestamp'][:19]})")
            
            return True
            
        except Exception as e:
            print(f"❌ 数据库验证失败: {e}")
            return False
        finally:
            conn.close()
    
    def run_full_test(self):
        """运行完整测试"""
        print("🎯 MCP Analytics 实时测试开始")
        print("=" * 50)
        
        # 测试步骤
        steps = [
            ("API健康检查", self.check_api_health),
            ("注册测试用户", self.register_test_user),
            ("模拟工具使用", self.simulate_tool_usage),
            ("获取使用报告", self.get_user_report),
            ("验证数据库记录", self.verify_in_database)
        ]
        
        success_count = 0
        
        for step_name, step_func in steps:
            print(f"\n🔄 执行: {step_name}")
            if step_func():
                success_count += 1
            else:
                print(f"⚠️  {step_name} 失败，但继续测试...")
        
        print("\n" + "=" * 50)
        print(f"🎉 测试完成! {success_count}/{len(steps)} 步骤成功")
        
        if success_count == len(steps):
            print("✅ 所有功能正常，MCP Analytics系统运行完美！")
        else:
            print("⚠️  部分功能存在问题，请检查错误信息")
        
        # 提示下一步操作
        print(f"\n📱 下一步操作:")
        print(f"1. 在Navicat中刷新数据，查看新增的测试用户")
        print(f"2. 用户邮箱: {self.test_email}")
        print(f"3. 用户UUID: {self.test_user_uuid}")
        print(f"4. 检查 usage_logs 表中的新记录")

if __name__ == "__main__":
    tester = MCPAnalyticsTest()
    tester.run_full_test()