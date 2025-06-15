#!/usr/bin/env python3
"""
测试增强版的Usage Tracker
演示AI编程效果追踪功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent / "src"))

from frontend_dev_assistant.usage_tracker import UsageTracker

async def test_enhanced_usage_tracker():
    """测试增强版的usage tracker"""
    print("🧪 测试增强版 Usage Tracker")
    print("="*50)
    
    # 初始化tracker
    tracker = UsageTracker()
    
    # 模拟AI编程会话数据
    print("\n📊 模拟AI编程会话数据...")
    
    # 会话1: Cursor生成Vue组件
    session1_data = {
        'duration_minutes': 15,
        'files_modified': 2
    }
    
    coding1_metrics = {
        'lines_added': 85,
        'lines_deleted': 12,
        'complexity_score': 8,
        'ai_probability': 0.7
    }
    
    quality1_metrics = {
        'quality_score': 75,
        'has_comments': True,
        'has_error_handling': True,
        'has_type_annotations': False,
        'function_count': 4
    }
    
    result1 = await tracker.track_usage(
        tool_name="cursor_component_generation",
        user_feedback="good",
        usage_context="生成Vue3组件 - UserProfile.vue",
        ai_session_data=session1_data,
        coding_metrics=coding1_metrics,
        quality_metrics=quality1_metrics
    )
    print(f"✅ 会话1记录: {result1}")
    
    # 会话2: AI辅助重构
    session2_data = {
        'duration_minutes': 25,
        'files_modified': 3
    }
    
    coding2_metrics = {
        'lines_added': 45,
        'lines_deleted': 30,
        'complexity_score': 12,
        'ai_probability': 0.5
    }
    
    quality2_metrics = {
        'quality_score': 85,
        'has_comments': True,
        'has_error_handling': True,
        'has_type_annotations': True,
        'function_count': 6
    }
    
    result2 = await tracker.track_usage(
        tool_name="ai_code_refactor",
        user_feedback="excellent",
        usage_context="重构支付模块代码",
        ai_session_data=session2_data,
        coding_metrics=coding2_metrics,
        quality_metrics=quality2_metrics
    )
    print(f"✅ 会话2记录: {result2}")
    
    # 会话3: 小程序页面生成
    session3_data = {
        'duration_minutes': 18,
        'files_modified': 4
    }
    
    coding3_metrics = {
        'lines_added': 120,
        'lines_deleted': 5,
        'complexity_score': 15,
        'ai_probability': 0.9
    }
    
    quality3_metrics = {
        'quality_score': 65,
        'has_comments': False,
        'has_error_handling': False,
        'has_type_annotations': False,
        'function_count': 8
    }
    
    result3 = await tracker.track_usage(
        tool_name="miniprogram_page_gen",
        user_feedback="average",
        usage_context="生成微信小程序商品列表页",
        ai_session_data=session3_data,
        coding_metrics=coding3_metrics,
        quality_metrics=quality3_metrics
    )
    print(f"✅ 会话3记录: {result3}")
    
    # 会话4: TypeScript类型定义
    session4_data = {
        'duration_minutes': 8,
        'files_modified': 1
    }
    
    coding4_metrics = {
        'lines_added': 25,
        'lines_deleted': 2,
        'complexity_score': 3,
        'ai_probability': 0.4
    }
    
    quality4_metrics = {
        'quality_score': 90,
        'has_comments': True,
        'has_error_handling': False,
        'has_type_annotations': True,
        'function_count': 2
    }
    
    result4 = await tracker.track_usage(
        tool_name="typescript_types_gen",
        user_feedback="excellent",
        usage_context="生成API接口类型定义",
        ai_session_data=session4_data,
        coding_metrics=coding4_metrics,
        quality_metrics=quality4_metrics
    )
    print(f"✅ 会话4记录: {result4}")
    
    print("\n" + "="*50)
    print("📈 生成AI编程效果统计报告...")
    print("="*50)
    
    # 获取今天的统计
    today_stats = await tracker.get_stats("today")
    print(today_stats)
    
    print("\n" + "="*50)
    print("📋 获取所有时间统计...")
    print("="*50)
    
    # 获取所有时间的统计
    all_stats = await tracker.get_stats("all")
    print(all_stats)

async def test_smart_feedback():
    """测试智能反馈收集"""
    print("\n" + "="*50)
    print("💬 测试智能反馈收集功能")
    print("="*50)
    
    tracker = UsageTracker()
    
    # 生成反馈提示
    feedback_prompt = await tracker.collect_smart_feedback(
        task_summary="使用Cursor生成了一个完整的Vue3购物车组件",
        allow_skip=True
    )
    
    print("反馈提示:")
    print(feedback_prompt)
    
    # 模拟不同的反馈响应
    test_responses = [
        ("excellent", "优秀反馈"),
        ("跳过", "跳过反馈"),
        ("good", "良好反馈"),
        ("1", "数字跳过"),
        ("invalid_response", "无效反馈")
    ]
    
    for response, description in test_responses:
        result = await tracker.process_feedback_response(
            response=response,
            task_name="vue3_component_generation"
        )
        print(f"\n{description} - 响应: '{response}'")
        print(f"处理结果: {result}")

if __name__ == "__main__":
    print("🚀 开始测试增强版 Usage Tracker")
    
    # 运行基础功能测试
    asyncio.run(test_enhanced_usage_tracker())
    
    # 运行反馈收集测试
    asyncio.run(test_smart_feedback())
    
    print("\n✅ 所有测试完成！") 