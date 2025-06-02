#!/bin/bash
"""
前端开发提示词智能助手 MCP 启动脚本
解决Python别名问题
"""

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🚀 启动前端开发提示词智能助手 MCP..."
echo "📁 项目目录: $DIR"

# 检查虚拟环境是否存在
if [ ! -f "$DIR/venv/bin/python" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# 使用虚拟环境中的Python启动MCP
echo "⚡ 使用虚拟环境Python: $DIR/venv/bin/python"
exec "$DIR/venv/bin/python" "$DIR/start_mcp.py" 