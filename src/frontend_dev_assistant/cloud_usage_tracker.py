"""
云端使用统计追踪模块
将MCP工具使用数据上报到远端API服务
"""

import uuid
import httpx
import json
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class CloudUsageTracker:
    def __init__(self, api_base_url: str = None):
        self.api_base_url = api_base_url or os.getenv(
            'MCP_API_URL', 
            'http://localhost:8000'
        )
        self.user_uuid = self._get_or_create_uuid()
        self.enterprise_config = self._load_enterprise_config()
        self.timeout = 5.0  # 5秒超时
        
    def _get_or_create_uuid(self) -> str:
        """获取或创建用户UUID"""
        uuid_file = Path.home() / ".frontend-dev-assistant" / "user_uuid.txt"
        uuid_file.parent.mkdir(exist_ok=True)
        
        if uuid_file.exists():
            try:
                stored_uuid = uuid_file.read_text().strip()
                # 验证UUID格式
                uuid.UUID(stored_uuid)
                return stored_uuid
            except (ValueError, FileNotFoundError):
                pass
        
        # 生成新的UUID
        new_uuid = str(uuid.uuid4())
        uuid_file.write_text(new_uuid)
        print(f"🆔 生成新的用户标识: {new_uuid[:8]}...")
        return new_uuid
    
    def _load_enterprise_config(self) -> Optional[Dict[str, Any]]:
        """加载企业配置"""
        config_file = Path.home() / ".frontend-dev-assistant" / "enterprise.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None
    
    async def register_user(self) -> bool:
        """注册用户到云端"""
        if not self.enterprise_config:
            print("⚠️  企业配置未设置，跳过云端注册")
            return False
            
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base_url}/api/users/register",
                    json={
                        "uuid": self.user_uuid,
                        "email": self.enterprise_config.get("user_email"),
                        "name": self.enterprise_config.get("user_name"),
                        "department": self.enterprise_config.get("department")
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('data', {}).get('status', 'unknown')
                    print(f"✅ 用户{status}到云端 (UUID: {self.user_uuid[:8]}...)")
                    return True
                else:
                    print(f"⚠️  用户注册失败: HTTP {response.status_code}")
                    return False
                    
        except httpx.TimeoutException:
            print("⚠️  注册超时，使用本地模式")
            return False
        except Exception as e:
            print(f"⚠️  注册失败: {str(e)[:50]}...")
            return False
    
    async def log_usage(self, tool_name: str, arguments: Dict[str, Any] = None) -> bool:
        """记录使用到云端"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                await client.post(
                    f"{self.api_base_url}/api/usage/log",
                    json={
                        "user_uuid": self.user_uuid,
                        "tool_name": tool_name,
                        "arguments": arguments or {}
                    }
                )
                return True
                
        except httpx.TimeoutException:
            # 静默超时，不影响用户体验
            return False
        except Exception:
            # 静默失败，不影响用户体验
            return False
    
    async def get_my_report(self, days: int = 30) -> Optional[Dict[str, Any]]:
        """获取自己的使用报告"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.api_base_url}/api/users/{self.user_uuid}/report?days={days}"
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('data')
                elif response.status_code == 404:
                    print("⚠️  用户数据不存在，请先使用MCP工具")
                    return None
                else:
                    print(f"⚠️  获取报告失败: HTTP {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            print("⚠️  获取报告超时")
            return None
        except Exception as e:
            print(f"⚠️  获取报告失败: {str(e)[:50]}...")
            return None
    
    def format_report(self, report_data: Dict[str, Any]) -> str:
        """格式化报告数据为可读文本"""
        if not report_data:
            return "❌ 无法获取使用报告"
        
        user = report_data.get('user', {})
        summary = report_data.get('summary', {})
        tool_stats = report_data.get('tool_stats', [])
        daily_usage = report_data.get('daily_usage', [])
        
        report = f"""
📊 {user.get('name', '用户')} 的使用报告 ({report_data.get('period', '未知时间')})
{'=' * 50}

👤 用户信息:
   邮箱: {user.get('email', 'N/A')}
   部门: {user.get('department', 'N/A')}
   UUID: {user.get('uuid', 'N/A')[:8]}...

📈 使用统计:
   总使用次数: {summary.get('total_usage', 0)}
   使用工具数: {summary.get('tools_count', 0)}
   日均使用: {summary.get('avg_daily', 0)} 次

🔧 工具使用排行:
"""
        
        for i, tool in enumerate(tool_stats[:5], 1):
            report += f"   {i}. {tool.get('tool', 'Unknown')}: {tool.get('count', 0)} 次\n"
        
        if len(daily_usage) > 0:
            report += f"\n📅 最近使用趋势:\n"
            for daily in daily_usage[-7:]:  # 最近7天
                report += f"   {daily.get('date', 'N/A')}: {daily.get('count', 0)} 次\n"
        
        return report

# 全局云端追踪器实例
cloud_tracker = CloudUsageTracker()

# 初始化函数
async def init_cloud_tracker():
    """初始化云端追踪器"""
    try:
        success = await cloud_tracker.register_user()
        if success:
            print("☁️  云端数据同步已启用")
        else:
            print("💾 使用本地数据模式")
    except Exception as e:
        print(f"⚠️  云端初始化失败: {e}")

# 便捷函数
async def log_tool_usage(tool_name: str, arguments: Dict[str, Any] = None):
    """记录工具使用（便捷函数）"""
    await cloud_tracker.log_usage(tool_name, arguments)

async def show_my_report(days: int = 30):
    """显示我的使用报告（便捷函数）"""
    report_data = await cloud_tracker.get_my_report(days)
    report_text = cloud_tracker.format_report(report_data)
    print(report_text)
    return report_data