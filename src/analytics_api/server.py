"""
MCP Analytics API服务器
提供用户注册、使用日志记录和报告查询功能
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from datetime import datetime

from .models import UserRegister, UsageLog, ApiResponse
from .database import db_manager

# 创建FastAPI应用
app = FastAPI(
    title="MCP Analytics API",
    description="前端开发AI助手使用数据收集和分析API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    try:
        await db_manager.init_database()
        print("🚀 MCP Analytics API 启动成功!")
        print("📊 数据库连接正常")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        raise

@app.get("/")
async def root():
    """根路径 - API状态检查"""
    return {
        "message": "MCP Analytics API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 测试数据库连接
        conn = await db_manager.get_connection()
        await conn.fetchval("SELECT 1")
        await conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"数据库连接失败: {str(e)}")

@app.post("/api/users/register")
async def register_user(user: UserRegister):
    """
    用户注册/更新接口
    
    将UUID与企业邮箱绑定，支持更新用户信息
    """
    try:
        result = await db_manager.register_user(
            uuid=user.uuid,
            email=user.email,
            name=user.name,
            department=user.department
        )
        
        return {
            "status": "success",
            "message": f"用户{result['status']}成功",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/usage/log")
async def log_usage(usage: UsageLog):
    """
    记录使用日志接口
    
    记录用户对MCP工具的使用情况
    """
    try:
        result = await db_manager.log_usage(
            user_uuid=usage.user_uuid,
            tool_name=usage.tool_name,
            arguments=usage.arguments
        )
        
        return {
            "status": "success",
            "message": "使用记录已保存",
            "data": result
        }
        
    except Exception as e:
        if "用户不存在" in str(e):
            raise HTTPException(status_code=404, detail="用户不存在，请先注册")
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_uuid}/report")
async def get_user_report(user_uuid: str, days: int = 30):
    """
    获取用户使用报告接口
    
    返回指定时间范围内的用户使用统计数据
    """
    try:
        if days <= 0 or days > 365:
            raise HTTPException(status_code=400, detail="天数范围应在1-365之间")
        
        report = await db_manager.get_user_report(user_uuid, days)
        
        return {
            "status": "success",
            "message": "报告生成成功",
            "data": report
        }
        
    except Exception as e:
        if "用户不存在" in str(e):
            raise HTTPException(status_code=404, detail="用户不存在")
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/summary")
async def get_summary_stats():
    """
    获取整体统计摘要（未来扩展用）
    """
    return {
        "status": "success",
        "message": "功能开发中",
        "data": {
            "total_users": 0,
            "total_usage": 0,
            "active_tools": 0
        }
    }

# 错误处理器
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return {
        "status": "error",
        "message": f"服务器内部错误: {str(exc)}",
        "timestamp": datetime.now().isoformat()
    }

def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """启动服务器"""
    print(f"🚀 启动 MCP Analytics API 服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📚 API文档: http://{host}:{port}/docs")
    
    uvicorn.run(
        "analytics_api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    start_server(reload=True)