#!/usr/bin/env python3
"""
MCP 使用数据导出脚本
用于导出 MCP 工具的使用记录和统计数据
"""

import sys
import json
import csv
from pathlib import Path
from datetime import datetime

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from frontend_dev_assistant.usage_tracker import UsageTracker

async def export_data():
    """导出使用数据"""
    tracker = UsageTracker()
    
    print("🚀 MCP 使用数据导出工具")
    print("=" * 50)
    
    # 显示可用的导出选项
    print("\n请选择导出格式:")
    print("1. JSON 格式 (完整数据)")
    print("2. CSV 格式 (调用记录)")
    print("3. 统计报告 (文本格式)")
    print("4. 全部导出")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_dir = project_root / "exports"
    export_dir.mkdir(exist_ok=True)
    
    if choice == "1" or choice == "4":
        # 导出 JSON 格式
        print("\n📄 导出 JSON 格式数据...")
        result = await tracker.export_usage_data("json")
        print(result)
    
    if choice == "2" or choice == "4":
        # 导出 CSV 格式
        print("\n📊 导出 CSV 格式数据...")
        await export_csv(tracker, export_dir, timestamp)
    
    if choice == "3" or choice == "4":
        # 导出统计报告
        print("\n📈 导出统计报告...")
        await export_report(tracker, export_dir, timestamp)
    
    print(f"\n✅ 导出完成！文件保存在: {export_dir}")

async def export_csv(tracker, export_dir, timestamp):
    """导出 CSV 格式的调用记录"""
    try:
        data = tracker._load_usage_data()
        usage_logs = data.get("usage_logs", [])
        
        csv_file = export_dir / f"mcp_usage_logs_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入标题行
            writer.writerow([
                'ID', '工具名称', '时间戳', '日期', '用户ID', '参数'
            ])
            
            # 写入数据行
            for log in usage_logs:
                writer.writerow([
                    log.get('id', ''),
                    log.get('tool_name', ''),
                    log.get('timestamp', ''),
                    log.get('date', ''),
                    log.get('user_id', ''),
                    json.dumps(log.get('arguments', {}), ensure_ascii=False)
                ])
        
        print(f"✅ CSV 数据已导出到: {csv_file}")
        
    except Exception as e:
        print(f"❌ CSV 导出失败: {str(e)}")

async def export_report(tracker, export_dir, timestamp):
    """导出统计报告"""
    try:
        # 获取不同时间范围的统计报告
        time_ranges = ["today", "week", "month", "all"]
        
        for time_range in time_ranges:
            report = await tracker.get_stats(time_range)
            
            report_file = export_dir / f"mcp_report_{time_range}_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ {time_range} 报告已导出到: {report_file}")
        
    except Exception as e:
        print(f"❌ 报告导出失败: {str(e)}")

async def show_current_stats():
    """显示当前统计信息"""
    tracker = UsageTracker()
    
    print("📊 当前 MCP 使用统计:")
    print("=" * 50)
    
    # 显示全部统计
    stats = await tracker.get_stats("all")
    print(stats)

if __name__ == "__main__":
    import asyncio
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        asyncio.run(show_current_stats())
    else:
        asyncio.run(export_data()) 