#!/usr/bin/env python3
"""
MCP调用统计查看工具
快速查看frontend_dev_assistant MCP的使用情况
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(str(Path(__file__).parent / "src"))

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    else:
        return f"{size_bytes/(1024*1024):.1f}MB"

def load_mcp_calls_data():
    """加载MCP调用数据"""
    # 尝试多个可能的数据位置
    possible_paths = [
        Path("src/data/mcp_calls.json"),
        Path.home() / ".frontend-dev-assistant" / "mcp_calls.json",
        Path("data/mcp_calls.json")
    ]
    
    for path in possible_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f), str(path)
            except json.JSONDecodeError:
                continue
    
    return None, None

def show_mcp_stats(days=7):
    """显示MCP调用统计"""
    print("🔍 Frontend Dev Assistant MCP 调用统计")
    print("=" * 60)
    
    # 加载数据
    data, data_path = load_mcp_calls_data()
    
    if not data:
        print("❌ 没有找到MCP调用数据")
        print("💡 请确保已经使用过frontend_dev_assistant MCP工具")
        print("📍 数据文件路径:")
        print("   • src/data/mcp_calls.json")
        print("   • ~/.frontend-dev-assistant/mcp_calls.json")
        return
    
    print(f"📁 数据来源: {data_path}")
    print(f"📅 统计范围: 最近{days}天")
    print()
    
    # 获取调用记录
    calls = data.get("calls", [])
    
    if not calls:
        print("❌ 没有调用记录")
        return
    
    # 过滤最近N天的数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    recent_calls = []
    for call in calls:
        try:
            call_time = datetime.fromisoformat(call["timestamp"])
            if call_time >= start_date:
                recent_calls.append(call)
        except (ValueError, KeyError):
            continue
    
    if not recent_calls:
        print(f"❌ 最近{days}天没有调用记录")
        return
    
    # 基础统计
    total_calls = len(recent_calls)
    successful_calls = sum(1 for call in recent_calls if call.get("success", True))
    failed_calls = total_calls - successful_calls
    success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
    
    avg_execution_time = sum(call.get("execution_time_ms", 0) for call in recent_calls) / total_calls
    total_result_size = sum(call.get("result_size_bytes", 0) for call in recent_calls)
    
    print("📊 基础统计")
    print("-" * 30)
    print(f"总调用次数:       {total_calls:>8} 次")
    print(f"成功调用:         {successful_calls:>8} 次")
    print(f"失败调用:         {failed_calls:>8} 次")
    print(f"成功率:           {success_rate:>8.1f}%")
    print(f"平均执行时间:     {avg_execution_time:>8.1f} ms")
    print(f"总结果大小:       {format_size(total_result_size):>8}")
    print(f"日均调用:         {total_calls/days:>8.1f} 次")
    print()
    
    # 工具使用排行
    tool_usage = {}
    tool_execution_times = {}
    
    for call in recent_calls:
        tool_name = call.get("tool_name", "unknown")
        execution_time = call.get("execution_time_ms", 0)
        
        if tool_name not in tool_usage:
            tool_usage[tool_name] = 0
            tool_execution_times[tool_name] = []
        
        tool_usage[tool_name] += 1
        tool_execution_times[tool_name].append(execution_time)
    
    print("🛠️ 工具使用排行")
    print("-" * 30)
    sorted_tools = sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)
    
    for i, (tool, count) in enumerate(sorted_tools[:10], 1):
        avg_time = sum(tool_execution_times[tool]) / len(tool_execution_times[tool])
        percentage = count / total_calls * 100
        print(f"{i:>2}. {tool:<25} {count:>4} 次 ({percentage:>5.1f}%) {avg_time:>6.1f}ms")
    print()
    
    # 时间分布
    hourly_calls = {}
    daily_calls = {}
    
    for call in recent_calls:
        try:
            call_time = datetime.fromisoformat(call["timestamp"])
            hour = call_time.hour
            date = call_time.strftime('%Y-%m-%d')
            
            if hour not in hourly_calls:
                hourly_calls[hour] = 0
            hourly_calls[hour] += 1
            
            if date not in daily_calls:
                daily_calls[date] = 0
            daily_calls[date] += 1
            
        except (ValueError, KeyError):
            continue
    
    if hourly_calls:
        peak_hour = max(hourly_calls.items(), key=lambda x: x[1])
        print("⏰ 使用模式")
        print("-" * 30)
        print(f"使用高峰时段:     {peak_hour[0]:>8}点 ({peak_hour[1]}次)")
        
        # 显示每日调用分布
        print("\n📅 每日调用分布:")
        for date in sorted(daily_calls.keys())[-7:]:  # 显示最近7天
            count = daily_calls[date]
            bar = "█" * min(count // 2, 20)  # 简单的条形图
            print(f"  {date}: {count:>3} 次 {bar}")
    
    print()
    
    # 错误分析
    failed_calls_data = [call for call in recent_calls if not call.get("success", True)]
    
    if failed_calls_data:
        print("❌ 错误分析")
        print("-" * 30)
        
        error_patterns = {}
        for call in failed_calls_data:
            error_msg = call.get("error_message", "未知错误")
            tool_name = call.get("tool_name", "unknown")
            key = f"{tool_name}: {error_msg[:50]}"
            
            if key not in error_patterns:
                error_patterns[key] = 0
            error_patterns[key] += 1
        
        sorted_errors = sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)
        for error, count in sorted_errors[:5]:  # 显示前5个错误
            print(f"  • {error} ({count}次)")
        print()
    
    # 性能分析
    slow_calls = [call for call in recent_calls if call.get("execution_time_ms", 0) > 1000]
    
    if slow_calls:
        print("⚡ 性能分析")
        print("-" * 30)
        print(f"慢调用 (>1s):      {len(slow_calls):>8} 次")
        
        slow_tools = {}
        for call in slow_calls:
            tool_name = call.get("tool_name", "unknown")
            if tool_name not in slow_tools:
                slow_tools[tool_name] = []
            slow_tools[tool_name].append(call.get("execution_time_ms", 0))
        
        for tool, times in slow_tools.items():
            avg_time = sum(times) / len(times)
            print(f"  • {tool}: 平均 {avg_time:.1f}ms ({len(times)}次)")
        print()
    
    print("=" * 60)
    print("💡 提示: 使用 'python mcp_stats.py --days 30' 查看更长时间范围的统计")

def export_data(format_type="json"):
    """导出MCP调用数据"""
    data, data_path = load_mcp_calls_data()
    
    if not data:
        print("❌ 没有找到数据")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format_type == "json":
        output_file = f"mcp_calls_export_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已导出到: {output_file}")
    
    elif format_type == "csv":
        import csv
        output_file = f"mcp_calls_export_{timestamp}.csv"
        
        calls = data.get("calls", [])
        if calls:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = [
                    'timestamp', 'tool_name', 'execution_time_ms', 
                    'success', 'error_message', 'result_size_bytes'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for call in calls:
                    row = {key: call.get(key, '') for key in fieldnames}
                    writer.writerow(row)
            
            print(f"✅ 数据已导出到: {output_file}")
        else:
            print("❌ 没有调用数据可导出")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MCP调用统计查看工具')
    parser.add_argument('--days', type=int, default=7, help='统计天数 (默认: 7)')
    parser.add_argument('--export', choices=['json', 'csv'], help='导出数据格式')
    
    args = parser.parse_args()
    
    if args.export:
        export_data(args.export)
    else:
        show_mcp_stats(args.days)

if __name__ == '__main__':
    main() 