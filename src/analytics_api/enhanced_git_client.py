#!/usr/bin/env python3
"""
增强Git客户端 - 企业级AI编程效果评估
结合GitHub API和本地Git操作，实现代码采纳率、质量分析等功能
"""

import asyncio
import aiohttp
import subprocess
import json
import os
import difflib
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class EnhancedGitClient:
    """增强Git客户端 - 支持本地和远程Git分析"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.session = None
        
    async def __aenter__(self):
        headers = {"User-Agent": "MCP-Analytics/1.0"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_github_code(self, repo_owner: str, repo_name: str, query: str, 
                                language: str = None) -> List[Dict[str, Any]]:
        """使用GitHub API搜索代码"""
        if not self.session:
            await self.__aenter__()
        
        search_query = f"{query} repo:{repo_owner}/{repo_name}"
        if language:
            search_query += f" language:{language}"
        
        url = "https://api.github.com/search/code"
        params = {"q": search_query, "per_page": 10}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("items", [])
                elif response.status == 403:
                    logger.warning("GitHub API rate limit exceeded")
                    return []
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"GitHub search failed: {e}")
            return []
    
    async def get_repository_info(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """获取仓库基本信息"""
        if not self.session:
            await self.__aenter__()
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}
        except Exception as e:
            logger.error(f"Failed to get repo info: {e}")
            return {}
    
    async def get_recent_commits(self, repo_owner: str, repo_name: str, 
                               since_days: int = 7) -> List[Dict[str, Any]]:
        """获取最近的提交记录"""
        if not self.session:
            await self.__aenter__()
        
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        params = {"since": since_date, "per_page": 50}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []
        except Exception as e:
            logger.error(f"Failed to get commits: {e}")
            return []
    
    def run_git_command(self, command: List[str], repo_path: str = None) -> Tuple[bool, str]:
        """执行Git命令"""
        try:
            cwd = repo_path if repo_path else os.getcwd()
            result = subprocess.run(
                command, 
                cwd=cwd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error(f"Git command timeout: {' '.join(command)}")
            return False, "Command timeout"
        except Exception as e:
            logger.error(f"Git command failed: {e}")
            return False, str(e)
    
    def get_local_git_status(self, repo_path: str = None) -> Dict[str, Any]:
        """获取本地Git状态"""
        success, output = self.run_git_command(["git", "status", "--porcelain"], repo_path)
        
        if not success:
            return {"error": output}
        
        modified_files = []
        added_files = []
        deleted_files = []
        
        for line in output.split('\n'):
            if line.strip():
                status = line[:2]
                filename = line[3:]
                
                if 'M' in status:
                    modified_files.append(filename)
                elif 'A' in status:
                    added_files.append(filename)
                elif 'D' in status:
                    deleted_files.append(filename)
        
        return {
            "modified_files": modified_files,
            "added_files": added_files,
            "deleted_files": deleted_files,
            "total_changes": len(modified_files) + len(added_files) + len(deleted_files)
        }
    
    def get_file_diff(self, file_path: str, repo_path: str = None) -> Dict[str, Any]:
        """获取文件的diff信息"""
        success, output = self.run_git_command(
            ["git", "diff", "--", file_path], 
            repo_path
        )
        
        if not success:
            return {"error": output}
        
        # 分析diff统计
        lines = output.split('\n')
        added_lines = 0
        deleted_lines = 0
        
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                added_lines += 1
            elif line.startswith('-') and not line.startswith('---'):
                deleted_lines += 1
        
        return {
            "file": file_path,
            "added_lines": added_lines,
            "deleted_lines": deleted_lines,
            "diff_content": output
        }

class AICodeEffectivenessAnalyzer:
    """AI代码效果分析器 - 企业级评估"""
    
    def __init__(self, git_client: EnhancedGitClient):
        self.git_client = git_client
    
    async def analyze_code_adoption_rate(self, session_id: str, generated_code: str, 
                                       repo_owner: str, repo_name: str, 
                                       file_type: str = "typescript") -> Dict[str, Any]:
        """分析AI代码采纳率"""
        
        # 1. 使用GitHub API搜索相似代码
        search_results = await self.git_client.search_github_code(
            repo_owner, repo_name, 
            generated_code[:80],  # 使用前80字符作为搜索关键词
            file_type
        )
        
        adoption_analysis = {
            "session_id": session_id,
            "repository": f"{repo_owner}/{repo_name}",
            "generated_code_lines": len(generated_code.split('\n')),
            "search_matches": len(search_results),
            "similarity_scores": [],
            "adoption_rate": 0.0,
            "quality_indicators": {},
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # 2. 计算代码相似度
        for match in search_results[:5]:
            match_content = match.get("content", "")
            similarity = self._calculate_code_similarity(generated_code, match_content)
            adoption_analysis["similarity_scores"].append({
                "similarity": similarity,
                "file_name": match.get("name"),
                "file_url": match.get("html_url"),
                "match_score": match.get("score", 0)
            })
        
        # 3. 计算整体采纳率
        if adoption_analysis["similarity_scores"]:
            avg_similarity = sum(s["similarity"] for s in adoption_analysis["similarity_scores"]) / len(adoption_analysis["similarity_scores"])
            adoption_analysis["adoption_rate"] = min(avg_similarity * 100, 100)
        
        # 4. 质量指标分析
        adoption_analysis["quality_indicators"] = await self._analyze_code_quality(
            generated_code, repo_owner, repo_name
        )
        
        return adoption_analysis
    
    def _calculate_code_similarity(self, code1: str, code2: str) -> float:
        """计算代码相似度（改进版）"""
        # 预处理：移除空行和注释
        def preprocess_code(code):
            lines = []
            for line in code.split('\n'):
                line = line.strip()
                if line and not line.startswith('//') and not line.startswith('/*'):
                    lines.append(line)
            return lines
        
        lines1 = preprocess_code(code1)
        lines2 = preprocess_code(code2)
        
        if not lines1 or not lines2:
            return 0.0
        
        # 使用difflib计算相似度
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        return matcher.ratio()
    
    async def _analyze_code_quality(self, code: str, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """分析代码质量指标"""
        
        quality_indicators = {
            "complexity_score": self._calculate_complexity(code),
            "has_error_handling": self._has_error_handling(code),
            "has_type_annotations": self._has_type_annotations(code),
            "follows_naming_conventions": self._follows_naming_conventions(code),
            "test_coverage_likelihood": 0
        }
        
        # 搜索相关测试文件
        test_searches = await self.git_client.search_github_code(
            repo_owner, repo_name, 
            "test spec describe it", 
            "typescript"
        )
        quality_indicators["test_coverage_likelihood"] = min(len(test_searches) / 10, 1.0)
        
        return quality_indicators
    
    def _calculate_complexity(self, code: str) -> int:
        """计算代码复杂度（简化版）"""
        complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch']
        complexity = 1  # 基础复杂度
        
        for keyword in complexity_keywords:
            complexity += code.count(keyword)
        
        return min(complexity, 20)  # 限制在20以内
    
    def _has_error_handling(self, code: str) -> bool:
        """检查是否有错误处理"""
        error_patterns = ['try', 'catch', 'throw', 'Error', 'exception']
        return any(pattern in code for pattern in error_patterns)
    
    def _has_type_annotations(self, code: str) -> bool:
        """检查是否有类型注解（TypeScript）"""
        type_patterns = [': string', ': number', ': boolean', ': object', 'interface', 'type ']
        return any(pattern in code for pattern in type_patterns)
    
    def _follows_naming_conventions(self, code: str) -> bool:
        """检查是否遵循命名规范"""
        import re
        
        # 检查camelCase变量名
        camel_case_pattern = r'\b[a-z][a-zA-Z0-9]*\b'
        # 检查PascalCase类名/接口名
        pascal_case_pattern = r'\b[A-Z][a-zA-Z0-9]*\b'
        
        has_camel_case = bool(re.search(camel_case_pattern, code))
        has_pascal_case = bool(re.search(pascal_case_pattern, code))
        
        return has_camel_case or has_pascal_case
    
    async def detect_code_rollbacks(self, repo_owner: str, repo_name: str, 
                                  session_id: str = None, days: int = 7) -> List[Dict[str, Any]]:
        """检测代码回滚情况"""
        
        commits = await self.git_client.get_recent_commits(repo_owner, repo_name, days)
        rollbacks = []
        
        rollback_keywords = ['revert', 'rollback', 'undo', 'fix', 'hotfix']
        
        for commit in commits:
            message = commit.get("commit", {}).get("message", "").lower()
            
            if any(keyword in message for keyword in rollback_keywords):
                rollback_info = {
                    "commit_sha": commit.get("sha"),
                    "commit_message": commit.get("commit", {}).get("message"),
                    "author": commit.get("commit", {}).get("author", {}).get("name"),
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                    "html_url": commit.get("html_url"),
                    "rollback_likelihood": self._calculate_rollback_likelihood(message)
                }
                rollbacks.append(rollback_info)
        
        return rollbacks
    
    def _calculate_rollback_likelihood(self, commit_message: str) -> float:
        """计算回滚可能性"""
        high_confidence_keywords = ['revert', 'rollback']
        medium_confidence_keywords = ['undo', 'hotfix']
        low_confidence_keywords = ['fix']
        
        message_lower = commit_message.lower()
        
        if any(keyword in message_lower for keyword in high_confidence_keywords):
            return 0.9
        elif any(keyword in message_lower for keyword in medium_confidence_keywords):
            return 0.6
        elif any(keyword in message_lower for keyword in low_confidence_keywords):
            return 0.3
        else:
            return 0.1
    
    async def generate_effectiveness_report(self, session_id: str, repo_owner: str, 
                                          repo_name: str, generated_codes: List[str]) -> Dict[str, Any]:
        """生成AI编程效果报告"""
        
        repo_info = await self.git_client.get_repository_info(repo_owner, repo_name)
        
        report = {
            "session_id": session_id,
            "repository": {
                "name": f"{repo_owner}/{repo_name}",
                "description": repo_info.get("description", ""),
                "language": repo_info.get("language", ""),
                "stars": repo_info.get("stargazers_count", 0),
                "forks": repo_info.get("forks_count", 0)
            },
            "analysis_summary": {
                "total_code_generations": len(generated_codes),
                "average_adoption_rate": 0.0,
                "quality_score": 0.0,
                "rollback_risk": 0.0
            },
            "detailed_analysis": [],
            "recommendations": [],
            "generated_at": datetime.now().isoformat()
        }
        
        # 分析每个代码生成
        adoption_rates = []
        quality_scores = []
        
        for i, code in enumerate(generated_codes):
            analysis = await self.analyze_code_adoption_rate(
                f"{session_id}_{i}", code, repo_owner, repo_name
            )
            report["detailed_analysis"].append(analysis)
            adoption_rates.append(analysis["adoption_rate"])
            
            # 计算质量分数
            quality = analysis["quality_indicators"]
            quality_score = (
                (quality.get("complexity_score", 0) <= 10) * 25 +
                quality.get("has_error_handling", False) * 25 +
                quality.get("has_type_annotations", False) * 25 +
                quality.get("follows_naming_conventions", False) * 25
            )
            quality_scores.append(quality_score)
        
        # 计算汇总指标
        if adoption_rates:
            report["analysis_summary"]["average_adoption_rate"] = sum(adoption_rates) / len(adoption_rates)
        if quality_scores:
            report["analysis_summary"]["quality_score"] = sum(quality_scores) / len(quality_scores)
        
        # 检测回滚风险
        rollbacks = await self.detect_code_rollbacks(repo_owner, repo_name, session_id)
        if rollbacks:
            avg_rollback_risk = sum(r["rollback_likelihood"] for r in rollbacks) / len(rollbacks)
            report["analysis_summary"]["rollback_risk"] = avg_rollback_risk
        
        # 生成建议
        report["recommendations"] = self._generate_recommendations(report["analysis_summary"])
        
        return report
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        adoption_rate = summary.get("average_adoption_rate", 0)
        quality_score = summary.get("quality_score", 0)
        rollback_risk = summary.get("rollback_risk", 0)
        
        if adoption_rate < 30:
            recommendations.append("代码采纳率较低，建议改进AI提示词的具体性和上下文相关性")
        elif adoption_rate > 80:
            recommendations.append("代码采纳率很高，当前AI辅助策略效果良好")
        
        if quality_score < 50:
            recommendations.append("建议加强代码质量检查，包括错误处理、类型注解和命名规范")
        elif quality_score > 80:
            recommendations.append("代码质量优秀，保持当前的开发标准")
        
        if rollback_risk > 0.5:
            recommendations.append("检测到较高的回滚风险，建议加强代码审查和测试")
        
        return recommendations

# 测试函数
async def test_enhanced_git_integration():
    """测试增强Git集成功能"""
    
    print("🚀 测试增强Git集成...")
    
    # 可以添加GitHub token以提高API限制
    async with EnhancedGitClient() as git_client:
        analyzer = AICodeEffectivenessAnalyzer(git_client)
        
        # 测试代码采纳率分析
        sample_code = """
        interface UserProfile {
            id: string;
            email: string;
            name: string;
            avatar?: string;
        }
        
        function validateUser(profile: UserProfile): boolean {
            return profile.id && profile.email && profile.name;
        }
        """
        
        print("📊 分析代码采纳率...")
        adoption_analysis = await analyzer.analyze_code_adoption_rate(
            "test_session_enhanced", sample_code, "microsoft", "typescript"
        )
        print(f"采纳率: {adoption_analysis['adoption_rate']:.1f}%")
        print(f"搜索匹配: {adoption_analysis['search_matches']} 个")
        
        # 测试回滚检测
        print("\n🔍 检测代码回滚...")
        rollbacks = await analyzer.detect_code_rollbacks("microsoft", "typescript")
        print(f"发现 {len(rollbacks)} 个可能的回滚")
        
        # 生成效果报告
        print("\n📈 生成效果报告...")
        report = await analyzer.generate_effectiveness_report(
            "test_session_enhanced", "microsoft", "typescript", [sample_code]
        )
        print(f"仓库: {report['repository']['name']}")
        print(f"平均采纳率: {report['analysis_summary']['average_adoption_rate']:.1f}%")
        print(f"质量分数: {report['analysis_summary']['quality_score']:.1f}")
        print(f"建议数量: {len(report['recommendations'])}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_git_integration()) 