#!/usr/bin/env python3
"""
本地Git分析器 - 企业级AI编程效果评估
专注于本地git命令操作，支持私有GitLab和阿里云云效仓库
追踪AI辅助开发的代码变更、提交记录和开发效率
"""

import subprocess
import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class LocalGitAnalyzer:
    """本地Git分析器 - 分析本地git仓库的AI编程效果"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.ensure_git_repo()
    
    def ensure_git_repo(self):
        """确保当前目录是git仓库"""
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            raise ValueError(f"目录 {self.repo_path} 不是git仓库")
    
    def run_git_command(self, command: List[str]) -> Tuple[bool, str]:
        """执行git命令"""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error(f"Git命令超时: git {' '.join(command)}")
            return False, "Command timeout"
        except Exception as e:
            logger.error(f"Git命令失败: {e}")
            return False, str(e)
    
    def get_repo_info(self) -> Dict[str, Any]:
        """获取仓库基本信息"""
        info = {}
        
        # 获取远程仓库URL
        success, remote_url = self.run_git_command(['config', '--get', 'remote.origin.url'])
        if success:
            info['remote_url'] = remote_url
            info['repo_type'] = self._detect_repo_type(remote_url)
        
        # 获取当前分支
        success, branch = self.run_git_command(['branch', '--show-current'])
        if success:
            info['current_branch'] = branch
        
        # 获取最近一次提交
        success, last_commit = self.run_git_command(['log', '-1', '--format=%H|%an|%ad|%s'])
        if success and last_commit:
            parts = last_commit.split('|', 3)
            if len(parts) >= 4:
                info['last_commit'] = {
                    'hash': parts[0],
                    'author': parts[1], 
                    'date': parts[2],
                    'message': parts[3]
                }
        
        return info
    
    def _detect_repo_type(self, remote_url: str) -> str:
        """检测仓库类型"""
        if 'gitlab' in remote_url.lower():
            return 'gitlab'
        elif 'codeup.aliyun.com' in remote_url or '云效' in remote_url:
            return 'aliyun_yunxiao'
        elif 'github.com' in remote_url:
            return 'github'
        else:
            return 'unknown'
    
    def get_working_directory_status(self) -> Dict[str, Any]:
        """获取工作目录状态"""
        success, status_output = self.run_git_command(['status', '--porcelain'])
        
        if not success:
            return {'error': status_output}
        
        status = {
            'modified_files': [],
            'added_files': [],
            'deleted_files': [],
            'untracked_files': [],
            'renamed_files': [],
            'total_changes': 0
        }
        
        for line in status_output.split('\n'):
            if line.strip():
                status_code = line[:2]
                filename = line[3:]
                
                if status_code[0] == 'M' or status_code[1] == 'M':
                    status['modified_files'].append(filename)
                elif status_code[0] == 'A' or status_code[1] == 'A':
                    status['added_files'].append(filename)
                elif status_code[0] == 'D' or status_code[1] == 'D':
                    status['deleted_files'].append(filename)
                elif status_code[0] == 'R':
                    status['renamed_files'].append(filename)
                elif status_code == '??':
                    status['untracked_files'].append(filename)
        
        status['total_changes'] = (
            len(status['modified_files']) + 
            len(status['added_files']) + 
            len(status['deleted_files']) +
            len(status['renamed_files'])
        )
        
        return status
    
    def analyze_file_changes(self, file_path: str) -> Dict[str, Any]:
        """分析单个文件的变更"""
        # 获取文件diff
        success, diff_output = self.run_git_command(['diff', 'HEAD', '--', file_path])
        
        if not success:
            return {'error': diff_output}
        
        analysis = {
            'file_path': file_path,
            'lines_added': 0,
            'lines_deleted': 0,
            'lines_modified': 0,
            'complexity_change': 0,
            'diff_content': diff_output,
            'change_summary': {}
        }
        
        # 分析diff统计
        for line in diff_output.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                analysis['lines_added'] += 1
            elif line.startswith('-') and not line.startswith('---'):
                analysis['lines_deleted'] += 1
        
        # 计算净变更
        analysis['net_lines_change'] = analysis['lines_added'] - analysis['lines_deleted']
        
        # 分析代码复杂度变化
        analysis['complexity_change'] = self._analyze_complexity_change(diff_output)
        
        # 生成变更摘要
        analysis['change_summary'] = self._generate_change_summary(diff_output)
        
        return analysis
    
    def _analyze_complexity_change(self, diff_content: str) -> int:
        """分析复杂度变化"""
        complexity_patterns = [
            r'\+.*\bif\b', r'\+.*\bfor\b', r'\+.*\bwhile\b', 
            r'\+.*\bswitch\b', r'\+.*\btry\b', r'\+.*\bcatch\b'
        ]
        
        complexity_increase = 0
        complexity_decrease = 0
        
        for line in diff_content.split('\n'):
            if line.startswith('+'):
                for pattern in complexity_patterns:
                    if re.search(pattern, line):
                        complexity_increase += 1
            elif line.startswith('-'):
                for pattern in complexity_patterns:
                    if re.search(pattern.replace(r'\+', r'\-'), line):
                        complexity_decrease += 1
        
        return complexity_increase - complexity_decrease
    
    def _generate_change_summary(self, diff_content: str) -> Dict[str, Any]:
        """生成变更摘要"""
        summary = {
            'functions_added': 0,
            'functions_modified': 0,
            'imports_changed': 0,
            'comments_added': 0,
            'has_type_changes': False,
            'has_error_handling': False
        }
        
        # 分析函数变更
        function_patterns = [r'\+.*function\s+\w+', r'\+.*\w+\s*\(.*\)\s*{', r'\+.*=>\s*{']
        for pattern in function_patterns:
            matches = re.findall(pattern, diff_content)
            summary['functions_added'] += len(matches)
        
        # 分析import变更
        import_patterns = [r'\+.*import\s+', r'\+.*from\s+.*import']
        for pattern in import_patterns:
            matches = re.findall(pattern, diff_content)
            summary['imports_changed'] += len(matches)
        
        # 分析注释添加
        comment_patterns = [r'\+.*//.*', r'\+.*\/\*.*', r'\+.*\*.*']
        for pattern in comment_patterns:
            matches = re.findall(pattern, diff_content)
            summary['comments_added'] += len(matches)
        
        # 检查类型变更
        type_patterns = [r'\+.*:\s*\w+', r'\+.*interface\s+', r'\+.*type\s+']
        summary['has_type_changes'] = any(re.search(pattern, diff_content) for pattern in type_patterns)
        
        # 检查错误处理
        error_patterns = [r'\+.*try\s*{', r'\+.*catch\s*\(', r'\+.*throw\s+']
        summary['has_error_handling'] = any(re.search(pattern, diff_content) for pattern in error_patterns)
        
        return summary
    
    def get_commit_history(self, since_days: int = 7, author: str = None) -> List[Dict[str, Any]]:
        """获取提交历史"""
        command = ['log', '--since', f'{since_days} days ago', '--format=%H|%an|%ae|%ad|%s']
        
        if author:
            command.extend(['--author', author])
        
        success, log_output = self.run_git_command(command)
        
        if not success:
            return []
        
        commits = []
        for line in log_output.split('\n'):
            if line.strip():
                parts = line.split('|', 4)
                if len(parts) >= 5:
                    commit = {
                        'hash': parts[0],
                        'author_name': parts[1],
                        'author_email': parts[2],
                        'date': parts[3],
                        'message': parts[4],
                        'is_ai_assisted': self._detect_ai_assisted_commit(parts[4])
                    }
                    commits.append(commit)
        
        return commits
    
    def _detect_ai_assisted_commit(self, commit_message: str) -> bool:
        """检测AI辅助的提交"""
        ai_keywords = [
            'ai', 'cursor', 'copilot', 'claude', 'gpt', 'assistant',
            '自动生成', '代码生成', 'auto-generated'
        ]
        
        message_lower = commit_message.lower()
        return any(keyword in message_lower for keyword in ai_keywords)
    
    def analyze_commit_patterns(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析提交模式"""
        if not commits:
            return {}
        
        analysis = {
            'total_commits': len(commits),
            'ai_assisted_commits': 0,
            'commit_frequency': {},
            'authors': {},
            'message_patterns': {},
            'ai_assistance_rate': 0.0
        }
        
        # 分析AI辅助提交
        for commit in commits:
            if commit.get('is_ai_assisted', False):
                analysis['ai_assisted_commits'] += 1
            
            # 统计作者
            author = commit['author_name']
            if author not in analysis['authors']:
                analysis['authors'][author] = {'total': 0, 'ai_assisted': 0}
            analysis['authors'][author]['total'] += 1
            if commit.get('is_ai_assisted', False):
                analysis['authors'][author]['ai_assisted'] += 1
        
        # 计算AI辅助率
        if analysis['total_commits'] > 0:
            analysis['ai_assistance_rate'] = analysis['ai_assisted_commits'] / analysis['total_commits']
        
        return analysis

class AICodeSessionTracker:
    """AI代码会话追踪器"""
    
    def __init__(self, git_analyzer: LocalGitAnalyzer):
        self.git_analyzer = git_analyzer
        self.session_data = {}
    
    def start_ai_session(self, session_id: str, user_email: str, tool_name: str) -> Dict[str, Any]:
        """开始AI编程会话"""
        # 记录会话开始时的仓库状态
        initial_status = self.git_analyzer.get_working_directory_status()
        
        session = {
            'session_id': session_id,
            'user_email': user_email,
            'tool_name': tool_name,
            'start_time': datetime.now().isoformat(),
            'initial_status': initial_status,
            'file_changes': {},
            'commits_made': [],
            'is_active': True
        }
        
        self.session_data[session_id] = session
        return session
    
    def track_file_change(self, session_id: str, file_path: str) -> Dict[str, Any]:
        """追踪文件变更"""
        if session_id not in self.session_data:
            return {'error': 'Session not found'}
        
        # 分析文件变更
        change_analysis = self.git_analyzer.analyze_file_changes(file_path)
        
        # 记录到会话数据
        self.session_data[session_id]['file_changes'][file_path] = {
            'analysis': change_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        return change_analysis
    
    def end_ai_session(self, session_id: str) -> Dict[str, Any]:
        """结束AI编程会话并生成报告"""
        if session_id not in self.session_data:
            return {'error': 'Session not found'}
        
        session = self.session_data[session_id]
        session['end_time'] = datetime.now().isoformat()
        session['is_active'] = False
        
        # 获取会话期间的提交
        session_commits = self._get_session_commits(session)
        session['commits_made'] = session_commits
        
        # 生成会话报告
        report = self._generate_session_report(session)
        
        return report
    
    def _get_session_commits(self, session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取会话期间的提交"""
        start_time = datetime.fromisoformat(session['start_time'])
        
        # 获取最近的提交（简化版本，实际可以更精确）
        recent_commits = self.git_analyzer.get_commit_history(since_days=1)
        
        session_commits = []
        for commit in recent_commits:
            # 这里可以添加更精确的时间过滤逻辑
            session_commits.append(commit)
        
        return session_commits
    
    def _generate_session_report(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """生成会话报告"""
        report = {
            'session_summary': {
                'session_id': session['session_id'],
                'user_email': session['user_email'],
                'tool_name': session['tool_name'],
                'duration_minutes': self._calculate_session_duration(session),
                'files_modified': len(session['file_changes']),
                'commits_made': len(session['commits_made'])
            },
            'productivity_metrics': {
                'lines_added': 0,
                'lines_deleted': 0,
                'functions_added': 0,
                'complexity_increase': 0,
                'code_quality_score': 0
            },
            'code_quality_analysis': {},
            'recommendations': []
        }
        
        # 计算生产力指标
        for file_path, change_data in session['file_changes'].items():
            analysis = change_data['analysis']
            report['productivity_metrics']['lines_added'] += analysis.get('lines_added', 0)
            report['productivity_metrics']['lines_deleted'] += analysis.get('lines_deleted', 0)
            report['productivity_metrics']['functions_added'] += analysis.get('change_summary', {}).get('functions_added', 0)
            report['productivity_metrics']['complexity_increase'] += analysis.get('complexity_change', 0)
        
        # 计算代码质量分数
        report['productivity_metrics']['code_quality_score'] = self._calculate_quality_score(session)
        
        # 生成建议
        report['recommendations'] = self._generate_session_recommendations(report)
        
        return report
    
    def _calculate_session_duration(self, session: Dict[str, Any]) -> float:
        """计算会话持续时间（分钟）"""
        start = datetime.fromisoformat(session['start_time'])
        end = datetime.fromisoformat(session.get('end_time', datetime.now().isoformat()))
        return (end - start).total_seconds() / 60
    
    def _calculate_quality_score(self, session: Dict[str, Any]) -> float:
        """计算代码质量分数"""
        score = 50  # 基础分数
        
        for file_path, change_data in session['file_changes'].items():
            summary = change_data['analysis'].get('change_summary', {})
            
            # 添加类型注解 +10分
            if summary.get('has_type_changes', False):
                score += 10
            
            # 添加错误处理 +15分  
            if summary.get('has_error_handling', False):
                score += 15
            
            # 添加注释 +10分
            if summary.get('comments_added', 0) > 0:
                score += 10
        
        return min(score, 100)
    
    def _generate_session_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """生成会话建议"""
        recommendations = []
        metrics = report['productivity_metrics']
        
        if metrics['code_quality_score'] < 60:
            recommendations.append("建议增加代码注释和类型注解以提高代码质量")
        
        if metrics['complexity_increase'] > 5:
            recommendations.append("代码复杂度增加较多，建议考虑重构以降低复杂度")
        
        if metrics['lines_added'] > metrics['lines_deleted'] * 3:
            recommendations.append("新增代码较多，建议适当重构以保持代码简洁")
        
        return recommendations

# 使用示例和测试
def test_local_git_analysis():
    """测试本地Git分析功能"""
    try:
        print("🔍 开始本地Git分析测试...")
        
        # 初始化分析器
        analyzer = LocalGitAnalyzer()
        
        # 获取仓库信息
        print("\n📊 仓库信息:")
        repo_info = analyzer.get_repo_info()
        for key, value in repo_info.items():
            print(f"  {key}: {value}")
        
        # 获取工作目录状态
        print("\n📁 工作目录状态:")
        status = analyzer.get_working_directory_status()
        print(f"  修改文件: {len(status.get('modified_files', []))}")
        print(f"  新增文件: {len(status.get('added_files', []))}")
        print(f"  未跟踪文件: {len(status.get('untracked_files', []))}")
        print(f"  总变更: {status.get('total_changes', 0)}")
        
        # 获取提交历史
        print("\n📝 最近提交:")
        commits = analyzer.get_commit_history(since_days=7)
        for commit in commits[:3]:  # 显示前3个
            print(f"  {commit['hash'][:8]} - {commit['author_name']}: {commit['message'][:50]}...")
        
        # 分析提交模式
        print("\n📈 提交模式分析:")
        patterns = analyzer.analyze_commit_patterns(commits)
        print(f"  总提交数: {patterns.get('total_commits', 0)}")
        print(f"  AI辅助提交: {patterns.get('ai_assisted_commits', 0)}")
        print(f"  AI辅助率: {patterns.get('ai_assistance_rate', 0):.1%}")
        
        # 测试会话追踪
        print("\n🤖 AI会话追踪测试:")
        tracker = AICodeSessionTracker(analyzer)
        session = tracker.start_ai_session("test_session", "test@company.com", "cursor")
        print(f"  会话已启动: {session['session_id']}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_local_git_analysis()