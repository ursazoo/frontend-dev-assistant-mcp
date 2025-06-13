"""
Pydantic数据模型定义
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, Any, List

class UserRegister(BaseModel):
    """用户注册模型"""
    uuid: str
    email: EmailStr
    name: Optional[str] = None
    department: Optional[str] = None

class UsageLog(BaseModel):
    """使用日志模型"""
    user_uuid: str
    tool_name: str
    arguments: Optional[Dict[str, Any]] = None

class UserResponse(BaseModel):
    """用户信息响应模型"""
    uuid: str
    email: str
    name: Optional[str]
    department: Optional[str]
    created_at: datetime
    last_active: datetime

class UsageStatsResponse(BaseModel):
    """使用统计响应模型"""
    user: Dict[str, Any]
    period: str
    summary: Dict[str, Any]
    tool_stats: List[Dict[str, Any]]
    daily_usage: List[Dict[str, Any]]

class ApiResponse(BaseModel):
    """通用API响应模型"""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None