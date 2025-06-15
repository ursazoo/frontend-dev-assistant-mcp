#!/usr/bin/env python3
"""
GitMCP客户端模块
与https://gitmcp.io服务器通信，获取GitHub仓库的代码和文档数据
用于企业级AI编程效果评估
"""

import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitMCPClient:
    """GitMCP HTTP客户端"""
    
    def __init__(self, repo_owner: str = None, repo_name: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://gitmcp.io"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def set_repository(self, owner: str, name: str):
        """设置目标仓库"""
        self.repo_owner = owner
        self.repo_name = name
    
    def _get_repo_url(self) -> str:
        """获取仓库专用的GitMCP URL"""
        if not self.repo_owner or not self.repo_name:
            return f"{self.base_url}/docs"  # 通用端点
        return f"{self.base_url}/{self.repo_owner}/{self.repo_name}"
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """调用GitMCP工具"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        url = self._get_repo_url()
        
        # 构造MCP工具调用请求
        payload = {
            "jsonrpc": "2.0",
            "id": f"call_{datetime.now().timestamp()}",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            async with self.session.post(
                f"{url}/mcp", 
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("result", {})
                else:
                    logger.error(f"GitMCP API error: {response.status}")
                    return {"error": f"HTTP {response.status}"}
                    
        except Exception as e:
            logger.error(f"GitMCP request failed: {e}")
            return {"error": str(e)}
    
    async def search_code(self, query: str, language: str = None) -> List[Dict[str, Any]]:
        """搜索代码"""
        tool_name = f"search_{self.repo_name}_code" if self.repo_name else "search_generic_code"
        
        arguments = {"query": query}
        if language:
            arguments["language"] = language
        if not self.repo_name:
            arguments["repository"] = f"{self.repo_owner}/{self.repo_name}"
            
        result = await self._call_mcp_tool(tool_name, arguments)
        return result.get("content", []) if "error" not in result else []
    
    async def search_documentation(self, query: str) -> List[Dict[str, Any]]:
        """搜索文档"""
        tool_name = f"search_{self.repo_name}_documentation" if self.repo_name else "search_generic_documentation"
        
        arguments = {"query": query}
        if not self.repo_name:
            arguments["repository"] = f"{self.repo_owner}/{self.repo_name}"
            
        result = await self._call_mcp_tool(tool_name, arguments)
        return result.get("content", []) if "error" not in result else []
    
    async def fetch_documentation(self) -> Dict[str, Any]:
        """获取项目文档"""
        tool_name = f"fetch_{self.repo_name}_documentation" if self.repo_name else "fetch_generic_documentation"
        
        arguments = {}
        if not self.repo_name:
            arguments["repository"] = f"{self.repo_owner}/{self.repo_name}"
            
        result = await self._call_mcp_tool(tool_name, arguments)
        return result if "error" not in result else {}

class AICodeAnalyzer:
    """AI代码效果分析器"""
    
    def __init__(self, git_client: GitMCPClient):
        self.git_client = git_client
    
    async def analyze_code_acceptance(self, generated_code: str, session_id: str) -> Dict[str, Any]:
        """分析AI生成代码的采纳率"""
        
        # 1. 搜索相关的代码提交
        search_results = await self.git_client.search_code(
            generated_code[:100],  # 使用代码片段作为搜索关键词
            language="typescript"  # 根据实际情况调整
        )
        
        # 2. 分析代码相似度和保留情况
        acceptance_data = {
            "session_id": session_id,
            "generated_lines": len(generated_code.split('\n')),
            "found_matches": len(search_results),
            "similarity_scores": [],
            "acceptance_rate": 0.0,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        if search_results:
            # 计算代码相似度（简化版本）
            for match in search_results[:5]:  # 只分析前5个匹配
                similarity = self._calculate_similarity(generated_code, match.get("content", ""))
                acceptance_data["similarity_scores"].append(similarity)
            
            # 计算平均采纳率
            if acceptance_data["similarity_scores"]:
                acceptance_data["acceptance_rate"] = sum(acceptance_data["similarity_scores"]) / len(acceptance_data["similarity_scores"])
        
        return acceptance_data
    
    def _calculate_similarity(self, original: str, committed: str) -> float:
        """计算代码相似度（简化版本）"""
        original_lines = set(line.strip() for line in original.split('\n') if line.strip())
        committed_lines = set(line.strip() for line in committed.split('\n') if line.strip())
        
        if not original_lines:
            return 0.0
            
        intersection = original_lines.intersection(committed_lines)
        return len(intersection) / len(original_lines)
    
    async def detect_rollbacks(self, session_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """检测代码回滚"""
        
        # 搜索包含revert关键词的文档和代码
        revert_docs = await self.git_client.search_documentation("revert commit rollback")
        revert_code = await self.git_client.search_code("revert")
        
        rollbacks = []
        
        # 分析回滚相关的内容
        for item in revert_docs + revert_code:
            rollback_info = {
                "type": "documentation" if item in revert_docs else "code",
                "content": item.get("content", "")[:200],  # 截取前200字符
                "url": item.get("url", ""),
                "detected_at": datetime.now().isoformat()
            }
            rollbacks.append(rollback_info)
        
        return rollbacks
    
    async def generate_quality_report(self, session_id: str, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """生成代码质量报告"""
        
        self.git_client.set_repository(repo_owner, repo_name)
        
        # 获取项目文档概览
        documentation = await self.git_client.fetch_documentation()
        
        # 搜索测试相关内容
        test_info = await self.git_client.search_code("test spec describe it expect")
        
        # 搜索错误和bug相关内容
        error_info = await self.git_client.search_documentation("bug error issue fix")
        
        quality_report = {
            "session_id": session_id,
            "repository": f"{repo_owner}/{repo_name}",
            "documentation_available": bool(documentation),
            "test_coverage_indicators": len(test_info),
            "known_issues_count": len(error_info),
            "project_description": documentation.get("content", "")[:300] if documentation else "",
            "generated_at": datetime.now().isoformat(),
            "quality_score": self._calculate_quality_score(documentation, test_info, error_info)
        }
        
        return quality_report
    
    def _calculate_quality_score(self, docs: Dict, tests: List, issues: List) -> float:
        """计算项目质量分数（0-100）"""
        score = 50  # 基础分数
        
        # 有文档 +20分
        if docs:
            score += 20
            
        # 有测试 +20分
        if tests:
            score += 20
            
        # 问题较少 +10分
        if len(issues) < 5:
            score += 10
            
        return min(score, 100)

# 使用示例和测试函数
async def test_git_mcp_integration():
    """测试GitMCP集成功能"""
    
    # 测试微软的TypeScript项目
    async with GitMCPClient("microsoft", "typescript") as client:
        
        # 测试代码搜索
        print("🔍 测试代码搜索...")
        code_results = await client.search_code("interface Promise")
        print(f"找到 {len(code_results)} 个代码匹配")
        
        # 测试文档搜索
        print("📚 测试文档搜索...")
        doc_results = await client.search_documentation("getting started")
        print(f"找到 {len(doc_results)} 个文档匹配")
        
        # 测试AI代码分析
        print("🤖 测试AI代码分析...")
        analyzer = AICodeAnalyzer(client)
        
        # 模拟AI生成的代码
        sample_code = """
        interface UserData {
            id: string;
            name: string;
            email: string;
        }
        """
        
        acceptance_analysis = await analyzer.analyze_code_acceptance(sample_code, "test_session_123")
        print(f"代码采纳率分析: {acceptance_analysis}")
        
        # 测试质量报告
        quality_report = await analyzer.generate_quality_report("test_session_123", "microsoft", "typescript")
        print(f"质量报告生成: {quality_report}")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_git_mcp_integration()) 