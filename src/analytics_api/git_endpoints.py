#!/usr/bin/env python3
"""
Git集成API端点
企业级AI编程效果评估的Git分析功能
支持私有GitLab和阿里云云效仓库
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid
import os

from .database import Database
from .models import GitSession, CodeChange, CommitAnalysis, GitAnalyticsReport, ApiResponse
from .local_git_analyzer import LocalGitAnalyzer, AICodeSessionTracker

router = APIRouter(prefix="/api/git", tags=["Git分析"])

# 请求模型
class StartSessionRequest(BaseModel):
    user_uuid: str
    repository_path: str
    tool_name: str = "cursor"

class TrackChangeRequest(BaseModel):
    session_id: str
    file_path: str

class EndSessionRequest(BaseModel):
    session_id: str

class AnalyzeRepositoryRequest(BaseModel):
    user_uuid: str
    repository_path: str
    days: int = 7

# Git分析器实例（在实际应用中可能需要依赖注入）
def get_git_analyzer(repo_path: str) -> LocalGitAnalyzer:
    """获取Git分析器实例"""
    try:
        return LocalGitAnalyzer(repo_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 存储活跃的会话追踪器
session_trackers: Dict[str, AICodeSessionTracker] = {}

@router.post("/sessions/start")
async def start_git_session(request: StartSessionRequest) -> ApiResponse:
    """开始Git编程会话"""
    try:
        # 验证仓库路径
        if not os.path.exists(request.repository_path):
            raise HTTPException(status_code=400, detail="仓库路径不存在")
        
        # 初始化Git分析器
        git_analyzer = get_git_analyzer(request.repository_path)
        
        # 获取仓库信息
        repo_info = git_analyzer.get_repo_info()
        
        # 生成会话ID
        session_id = str(uuid.uuid4())
        
        # 创建会话追踪器
        tracker = AICodeSessionTracker(git_analyzer)
        session_trackers[session_id] = tracker
        
        # 启动会话
        session_data = tracker.start_ai_session(
            session_id=session_id,
            user_email=f"user_{request.user_uuid}@company.com",  # 临时邮箱
            tool_name=request.tool_name
        )
        
        # 保存会话到数据库
        db = Database()
        db.execute("""
            INSERT INTO git_sessions 
            (session_id, user_uuid, repository_url, repository_type, branch_name, start_time, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            request.user_uuid,
            repo_info.get('remote_url', 'local'),
            repo_info.get('repo_type', 'unknown'),
            repo_info.get('current_branch', 'main'),
            datetime.now().isoformat(),
            True
        ))
        
        return ApiResponse(
            status="success",
            message="Git会话已启动",
            data={
                "session_id": session_id,
                "repository_info": repo_info,
                "initial_status": session_data.get('initial_status', {})
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动会话失败: {str(e)}")

@router.post("/sessions/track-change")
async def track_file_change(request: TrackChangeRequest) -> ApiResponse:
    """追踪文件变更"""
    try:
        if request.session_id not in session_trackers:
            raise HTTPException(status_code=404, detail="会话未找到")
        
        tracker = session_trackers[request.session_id]
        
        # 分析文件变更
        change_analysis = tracker.track_file_change(request.session_id, request.file_path)
        
        if 'error' in change_analysis:
            raise HTTPException(status_code=400, detail=change_analysis['error'])
        
        # 保存变更到数据库
        db = Database()
        summary = change_analysis.get('change_summary', {})
        db.execute("""
            INSERT INTO code_changes 
            (session_id, file_path, lines_added, lines_deleted, complexity_change, 
             functions_added, has_type_annotations, has_error_handling, change_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.session_id,
            request.file_path,
            change_analysis.get('lines_added', 0),
            change_analysis.get('lines_deleted', 0),
            change_analysis.get('complexity_change', 0),
            summary.get('functions_added', 0),
            summary.get('has_type_changes', False),
            summary.get('has_error_handling', False),
            datetime.now().isoformat()
        ))
        
        return ApiResponse(
            status="success",
            message="文件变更已记录",
            data=change_analysis
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"追踪变更失败: {str(e)}")

@router.post("/sessions/end")
async def end_git_session(request: EndSessionRequest) -> ApiResponse:
    """结束Git编程会话"""
    try:
        if request.session_id not in session_trackers:
            raise HTTPException(status_code=404, detail="会话未找到")
        
        tracker = session_trackers[request.session_id]
        
        # 生成会话报告
        session_report = tracker.end_ai_session(request.session_id)
        
        # 更新数据库中的会话状态
        db = Database()
        db.execute("""
            UPDATE git_sessions 
            SET end_time = ?, is_active = FALSE 
            WHERE session_id = ?
        """, (datetime.now().isoformat(), request.session_id))
        
        # 清理会话追踪器
        del session_trackers[request.session_id]
        
        return ApiResponse(
            status="success",
            message="会话已结束",
            data=session_report
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"结束会话失败: {str(e)}")

@router.post("/analyze")
async def analyze_repository(request: AnalyzeRepositoryRequest) -> ApiResponse:
    """分析仓库的AI编程效果"""
    try:
        # 初始化Git分析器
        git_analyzer = get_git_analyzer(request.repository_path)
        
        # 获取提交历史
        commits = git_analyzer.get_commit_history(since_days=request.days)
        
        # 分析提交模式
        commit_patterns = git_analyzer.analyze_commit_patterns(commits)
        
        # 获取仓库信息
        repo_info = git_analyzer.get_repo_info()
        
        # 计算生产力指标
        productivity_metrics = {
            "total_commits": len(commits),
            "ai_assisted_commits": commit_patterns.get('ai_assisted_commits', 0),
            "ai_assistance_rate": commit_patterns.get('ai_assistance_rate', 0),
            "authors_analysis": commit_patterns.get('authors', {}),
            "average_commits_per_day": len(commits) / request.days if request.days > 0 else 0
        }
        
        # 生成建议
        recommendations = []
        if productivity_metrics["ai_assistance_rate"] < 0.3:
            recommendations.append("AI辅助使用率较低，建议团队增加AI工具的使用频率")
        if productivity_metrics["total_commits"] < request.days:
            recommendations.append("提交频率较低，建议采用更频繁的提交策略")
        
        analysis_result = {
            "repository_info": repo_info,
            "analysis_period": f"{request.days} 天",
            "productivity_metrics": productivity_metrics,
            "commit_analysis": commit_patterns,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat()
        }
        
        return ApiResponse(
            status="success",
            message="仓库分析完成",
            data=analysis_result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"仓库分析失败: {str(e)}")

@router.get("/sessions/{session_id}/status")
async def get_session_status(session_id: str) -> ApiResponse:
    """获取会话状态"""
    try:
        db = Database()
        result = db.fetch_one("""
            SELECT * FROM git_sessions WHERE session_id = ?
        """, (session_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="会话未找到")
        
        # 获取会话的代码变更
        changes = db.fetch_all("""
            SELECT * FROM code_changes WHERE session_id = ? ORDER BY change_timestamp DESC
        """, (session_id,))
        
        session_data = dict(result)
        session_data['code_changes'] = [dict(change) for change in changes]
        
        return ApiResponse(
            status="success",
            data=session_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话状态失败: {str(e)}")

@router.get("/users/{user_uuid}/report")
async def get_user_git_report(user_uuid: str, days: int = 30) -> ApiResponse:
    """获取用户的Git分析报告"""
    try:
        db = Database()
        
        # 获取用户的Git会话
        sessions = db.fetch_all("""
            SELECT * FROM git_sessions 
            WHERE user_uuid = ? AND start_time >= date('now', '-{} days')
            ORDER BY start_time DESC
        """.format(days), (user_uuid,))
        
        if not sessions:
            return ApiResponse(
                status="success", 
                message="无数据",
                data={"sessions": [], "summary": {}}
            )
        
        # 计算汇总数据
        total_sessions = len(sessions)
        active_sessions = sum(1 for s in sessions if s['is_active'])
        
        # 获取代码变更统计
        total_changes = 0
        total_lines_added = 0
        total_lines_deleted = 0
        
        for session in sessions:
            changes = db.fetch_all("""
                SELECT * FROM code_changes WHERE session_id = ?
            """, (session['session_id'],))
            
            total_changes += len(changes)
            for change in changes:
                total_lines_added += change['lines_added']
                total_lines_deleted += change['lines_deleted']
        
        summary = {
            "analysis_period_days": days,
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_code_changes": total_changes,
            "total_lines_added": total_lines_added,
            "total_lines_deleted": total_lines_deleted,
            "net_lines_change": total_lines_added - total_lines_deleted,
            "average_session_productivity": total_changes / total_sessions if total_sessions > 0 else 0
        }
        
        return ApiResponse(
            status="success",
            data={
                "user_uuid": user_uuid,
                "sessions": [dict(s) for s in sessions],
                "summary": summary
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}") 