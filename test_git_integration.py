#!/usr/bin/env python3
"""
Git集成完整测试脚本
演示企业级AI编程效果评估的完整workflow
支持私有GitLab和阿里云云效仓库
"""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
import sys

# 添加项目路径
sys.path.append(str(Path(__file__).parent / "src"))

from analytics_api.local_git_analyzer import LocalGitAnalyzer, AICodeSessionTracker

class GitIntegrationDemo:
    """Git集成演示"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or "."
        self.analyzer = None
        self.tracker = None
        
    async def initialize(self):
        """初始化系统"""
        print("🚀 初始化Git集成系统...")
        
        try:
            self.analyzer = LocalGitAnalyzer(self.repo_path)
            self.tracker = AICodeSessionTracker(self.analyzer)
            print("✅ Git分析器初始化成功")
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return False
        
        return True
    
    async def demo_repository_analysis(self):
        """演示仓库分析功能"""
        print("\n📊 === 仓库分析演示 ===")
        
        # 1. 获取仓库基本信息
        print("\n🔍 仓库基本信息:")
        repo_info = self.analyzer.get_repo_info()
        for key, value in repo_info.items():
            print(f"  📋 {key}: {value}")
        
        # 2. 检查工作目录状态
        print("\n📁 当前工作目录状态:")
        status = self.analyzer.get_working_directory_status()
        print(f"  📝 修改文件: {len(status.get('modified_files', []))}")
        print(f"  ➕ 新增文件: {len(status.get('added_files', []))}")
        print(f"  ❓ 未跟踪文件: {len(status.get('untracked_files', []))}")
        print(f"  🔢 总变更数: {status.get('total_changes', 0)}")
        
        # 显示具体的变更文件
        if status.get('modified_files'):
            print("  📝 修改的文件:")
            for file in status['modified_files'][:5]:  # 只显示前5个
                print(f"    - {file}")
        
        if status.get('untracked_files'):
            print("  ❓ 未跟踪的文件:")
            for file in status['untracked_files'][:5]:  # 只显示前5个
                print(f"    - {file}")
        
        # 3. 分析最近的提交历史
        print("\n📝 最近7天的提交历史:")
        commits = self.analyzer.get_commit_history(since_days=7)
        
        if commits:
            for i, commit in enumerate(commits[:5]):  # 显示前5个
                ai_flag = "🤖" if commit['is_ai_assisted'] else "👤"
                print(f"  {ai_flag} {commit['hash'][:8]} - {commit['author_name']}")
                print(f"     📅 {commit['date']}")
                print(f"     💬 {commit['message'][:80]}...")
                print()
        else:
            print("  📭 没有找到最近的提交记录")
        
        # 4. 分析提交模式
        print("\n📈 提交模式分析:")
        patterns = self.analyzer.analyze_commit_patterns(commits)
        print(f"  📊 总提交数: {patterns.get('total_commits', 0)}")
        print(f"  🤖 AI辅助提交: {patterns.get('ai_assisted_commits', 0)}")
        print(f"  📈 AI辅助率: {patterns.get('ai_assistance_rate', 0):.1%}")
        
        # 显示作者统计
        authors = patterns.get('authors', {})
        if authors:
            print("  👥 作者统计:")
            for author, stats in authors.items():
                ai_rate = stats['ai_assisted'] / stats['total'] if stats['total'] > 0 else 0
                print(f"    - {author}: {stats['total']} 次提交 (AI: {ai_rate:.1%})")
    
    async def demo_ai_session_tracking(self):
        """演示AI编程会话追踪"""
        print("\n🤖 === AI编程会话追踪演示 ===")
        
        # 1. 开始AI编程会话
        session_id = f"demo_session_{uuid.uuid4().hex[:8]}"
        user_email = "developer@company.com"
        tool_name = "cursor"
        
        print(f"\n🚀 启动AI编程会话:")
        print(f"  🆔 会话ID: {session_id}")
        print(f"  👤 用户: {user_email}")
        print(f"  🛠️ 工具: {tool_name}")
        
        session_data = self.tracker.start_ai_session(session_id, user_email, tool_name)
        print(f"  ✅ 会话启动成功")
        
        # 2. 模拟文件变更追踪
        print(f"\n📝 文件变更追踪演示:")
        
        # 检查是否有可以分析的文件
        status = self.analyzer.get_working_directory_status()
        sample_files = (status.get('modified_files', []) + 
                       status.get('added_files', []) + 
                       ['src/analytics_api/local_git_analyzer.py'])  # 添加一个默认文件
        
        analyzed_files = 0
        for file_path in sample_files[:3]:  # 最多分析3个文件
            if Path(file_path).exists():
                print(f"\n  🔍 分析文件: {file_path}")
                try:
                    change_analysis = self.tracker.track_file_change(session_id, file_path)
                    
                    if 'error' not in change_analysis:
                        print(f"    ➕ 新增行数: {change_analysis.get('lines_added', 0)}")
                        print(f"    ➖ 删除行数: {change_analysis.get('lines_deleted', 0)}")
                        print(f"    🔄 净变更: {change_analysis.get('net_lines_change', 0)}")
                        print(f"    🧠 复杂度变化: {change_analysis.get('complexity_change', 0)}")
                        
                        summary = change_analysis.get('change_summary', {})
                        print(f"    🔧 新增函数: {summary.get('functions_added', 0)}")
                        print(f"    📦 导入变更: {summary.get('imports_changed', 0)}")
                        print(f"    💬 新增注释: {summary.get('comments_added', 0)}")
                        print(f"    🏷️ 类型注解: {'✅' if summary.get('has_type_changes') else '❌'}")
                        print(f"    🛡️ 错误处理: {'✅' if summary.get('has_error_handling') else '❌'}")
                        
                        analyzed_files += 1
                    else:
                        print(f"    ❌ 分析失败: {change_analysis['error']}")
                        
                except Exception as e:
                    print(f"    ❌ 分析异常: {e}")
        
        if analyzed_files == 0:
            print("  📭 没有找到可分析的文件变更")
        
        # 3. 结束会话并生成报告
        print(f"\n📊 生成会话报告:")
        try:
            session_report = self.tracker.end_ai_session(session_id)
            
            summary = session_report.get('session_summary', {})
            metrics = session_report.get('productivity_metrics', {})
            recommendations = session_report.get('recommendations', [])
            
            print(f"  ⏱️ 会话时长: {summary.get('duration_minutes', 0):.1f} 分钟")
            print(f"  📁 修改文件: {summary.get('files_modified', 0)} 个")
            print(f"  📝 提交次数: {summary.get('commits_made', 0)} 次")
            print(f"  ➕ 新增代码行: {metrics.get('lines_added', 0)}")
            print(f"  ➖ 删除代码行: {metrics.get('lines_deleted', 0)}")
            print(f"  🔧 新增函数: {metrics.get('functions_added', 0)}")
            print(f"  🏆 代码质量分: {metrics.get('code_quality_score', 0)}")
            
            if recommendations:
                print(f"  💡 改进建议:")
                for rec in recommendations:
                    print(f"    - {rec}")
            
        except Exception as e:
            print(f"  ❌ 生成报告失败: {e}")
    
    async def demo_enterprise_metrics(self):
        """演示企业级指标分析"""
        print("\n🏢 === 企业级指标分析演示 ===")
        
        # 获取提交数据
        commits = self.analyzer.get_commit_history(since_days=30)
        patterns = self.analyzer.analyze_commit_patterns(commits)
        
        print("\n📊 30天内团队效果分析:")
        
        # 1. 采纳度指标 (Adoption)
        total_commits = patterns.get('total_commits', 0)
        ai_commits = patterns.get('ai_assisted_commits', 0)
        ai_rate = patterns.get('ai_assistance_rate', 0)
        
        print(f"\n🎯 采纳度 (Adoption):")
        print(f"  📈 AI辅助率: {ai_rate:.1%}")
        print(f"  📊 AI辅助提交: {ai_commits}/{total_commits}")
        
        adoption_score = "优秀" if ai_rate > 0.5 else "良好" if ai_rate > 0.3 else "需改进"
        print(f"  🏆 采纳评级: {adoption_score}")
        
        # 2. 产出量指标 (Output)
        avg_commits_per_day = total_commits / 30 if total_commits > 0 else 0
        
        print(f"\n🚀 产出量 (Output):")
        print(f"  📝 总提交数: {total_commits}")
        print(f"  📅 日均提交: {avg_commits_per_day:.1f}")
        
        # 3. 团队分析
        authors = patterns.get('authors', {})
        print(f"\n👥 团队分析:")
        print(f"  🧑‍💻 活跃开发者: {len(authors)}")
        
        for author, stats in list(authors.items())[:5]:  # 显示前5个最活跃的开发者
            author_ai_rate = stats['ai_assisted'] / stats['total'] if stats['total'] > 0 else 0
            print(f"  - {author}: {stats['total']} 次提交, AI辅助率 {author_ai_rate:.1%}")
        
        # 4. 质量指标 (简化版)
        print(f"\n🎯 质量指标:")
        
        # 检查最近的提交消息质量
        quality_commits = 0
        for commit in commits[:10]:  # 检查最近10个提交
            msg = commit['message'].lower()
            if any(keyword in msg for keyword in ['fix', 'feat', 'docs', 'refactor', 'test']):
                quality_commits += 1
        
        quality_rate = quality_commits / min(len(commits), 10) if commits else 0
        print(f"  📋 规范提交率: {quality_rate:.1%}")
        
        # 5. 生成企业级建议
        print(f"\n💡 企业级改进建议:")
        
        if ai_rate < 0.3:
            print("  🎯 建议加强AI工具培训，提高团队AI辅助开发的采纳率")
        
        if avg_commits_per_day < 1:
            print("  📈 建议采用更频繁的提交策略，提高开发迭代速度")
        
        if len(authors) < 3:
            print("  👥 建议扩大开发团队规模或增加代码贡献者")
        
        if quality_rate < 0.7:
            print("  📋 建议建立代码提交规范，使用Conventional Commits格式")
        
        print("  🔧 建议定期使用此分析系统追踪团队AI编程效果")

async def main():
    """主函数"""
    print("🎯 Git集成企业级AI编程效果评估系统")
    print("=" * 50)
    
    # 检查是否在git仓库中
    if not Path(".git").exists():
        print("❌ 当前目录不是git仓库，请在git仓库中运行此脚本")
        return
    
    demo = GitIntegrationDemo()
    
    # 初始化系统
    if not await demo.initialize():
        return
    
    print("\n🎭 开始完整演示...")
    
    try:
        # 1. 仓库分析
        await demo.demo_repository_analysis()
        
        # 2. AI会话追踪
        await demo.demo_ai_session_tracking()
        
        # 3. 企业级指标
        await demo.demo_enterprise_metrics()
        
        print("\n🎉 === 演示完成 ===")
        print("\n📋 系统功能总结:")
        print("✅ 本地Git仓库分析 (支持GitLab/云效)")
        print("✅ 实时AI编程会话追踪")
        print("✅ 代码变更效果评估")
        print("✅ 企业级团队分析")
        print("✅ 提交模式智能检测")
        print("✅ 代码质量自动评分")
        print("✅ 改进建议生成")
        
        print("\n🎯 下一步:")
        print("1. 集成到现有MCP Analytics API")
        print("2. 添加实时数据收集")
        print("3. 创建管理界面看板")
        print("4. 对接企业级数据库")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 