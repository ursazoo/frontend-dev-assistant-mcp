#!/bin/bash

# 前端开发提示词智能助手 MCP - 团队分发脚本
# 适用于 macOS 和 Linux

set -e

echo "🚀 前端开发提示词智能助手 MCP - 团队安装"
echo "========================================"

# 检查是否提供了仓库地址参数
if [ -z "$1" ]; then
    echo "❌ 请提供Git仓库地址"
    echo "用法: ./distribute-to-team.sh <git-repo-url>"
    echo "示例: ./distribute-to-team.sh https://github.com/your-team/python-mcp.git"
    exit 1
fi

REPO_URL="$1"
INSTALL_DIR="$HOME/mcp-tools/frontend-dev-assistant"

echo "📌 步骤1: 检查系统要求..."

# 检查Python版本
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ 发现Python版本: $PYTHON_VERSION"
    
    # 检查Python版本是否满足要求
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo "✓ Python版本满足要求 (>=3.8)"
    else
        echo "❌ Python版本需要 3.8 或更高版本"
        exit 1
    fi
else
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ 未找到Git，请先安装Git"
    exit 1
fi

echo "📌 步骤2: 克隆项目..."

# 创建安装目录
mkdir -p "$(dirname "$INSTALL_DIR")"

# 克隆或更新项目
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  目录已存在，更新项目..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📥 克隆项目到: $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "📌 步骤3: 创建虚拟环境..."

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
else
    echo "⚠️  虚拟环境已存在，跳过创建"
fi

echo "📌 步骤4: 安装依赖..."

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "📌 步骤5: 验证安装..."

# 运行测试
if python test_server.py; then
    echo "✅ 安装验证成功！"
else
    echo "❌ 安装验证失败，请检查错误信息"
    exit 1
fi

echo "📌 步骤6: 生成配置..."

# 生成Cursor配置
PYTHON_PATH="$INSTALL_DIR/venv/bin/python"
START_SCRIPT="$INSTALL_DIR/start_mcp.py"

echo ""
echo "🎉 安装完成！"
echo ""
echo "请将以下配置添加到Cursor的settings.json中："
echo ""
echo "----------------------------------------"
cat << EOF
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "$PYTHON_PATH",
      "args": ["$START_SCRIPT"],
      "env": {}
    }
  }
}
EOF
echo "----------------------------------------"
echo ""
echo "📋 后续步骤："
echo "1. 复制上面的配置到Cursor settings.json"
echo "2. 重启Cursor"
echo "3. 在聊天中测试：'请帮我获取git_commit提示词模板'"
echo ""
echo "💡 提示："
echo "- 项目安装在: $INSTALL_DIR"
echo "- 如需更新，重新运行此脚本即可"
echo "- 遇到问题可查看: $INSTALL_DIR/MCP使用手册.md" 