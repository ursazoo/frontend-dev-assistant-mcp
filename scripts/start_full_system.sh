#!/bin/bash
# MCP Analytics 完整系统启动脚本

echo "🚀 启动 MCP Analytics 完整系统"
echo "================================"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 切换到项目根目录
cd "$(dirname "$0")/.."

echo "📦 检查依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt 不存在"
    exit 1
fi

echo "🐳 启动 Docker 服务..."
docker-compose up -d postgres

echo "⏳ 等待数据库启动..."
sleep 10

# 检查数据库是否就绪
echo "🔍 检查数据库连接..."
docker-compose exec postgres pg_isready -U mcp_user -d mcp_analytics

if [ $? -eq 0 ]; then
    echo "✅ 数据库已就绪"
else
    echo "❌ 数据库启动失败"
    docker-compose logs postgres
    exit 1
fi

echo "🌐 启动 API 服务..."
echo "📍 API 地址: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"

# 启动API服务
python3 scripts/start_api_server.py &
API_PID=$!

echo "⏳ 等待 API 服务启动..."
sleep 5

# 检查API服务
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API 服务已启动"
else
    echo "❌ API 服务启动失败"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 系统启动完成！"
echo "================================"
echo "📊 PostgreSQL: localhost:5432"
echo "🌐 API 服务: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo ""
echo "🧪 运行测试: python3 scripts/test_cloud_api.py"
echo "🛑 停止服务: docker-compose down"
echo ""

# 保持脚本运行
echo "按 Ctrl+C 停止所有服务..."
trap 'echo ""; echo "🛑 正在停止服务..."; kill $API_PID 2>/dev/null; docker-compose down; exit 0' INT

wait $API_PID 