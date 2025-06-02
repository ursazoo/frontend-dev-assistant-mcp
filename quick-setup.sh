#!/bin/bash
# 前端开发提示词智能助手 MCP - 快速配置脚本

set -e

echo "🚀 前端开发提示词智能助手 MCP 快速配置"
echo "========================================"

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 步骤1：检查Python版本
echo ""
echo "📌 步骤1: 检查Python版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} 发现Python版本: $PYTHON_VERSION"
    
    # 检查版本是否>=3.8
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo -e "${GREEN}✓${NC} Python版本满足要求 (>=3.8)"
    else
        echo -e "${RED}✗${NC} Python版本过低，需要3.8或更高版本"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 步骤2：创建虚拟环境
echo ""
echo "📌 步骤2: 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 虚拟环境创建成功"
fi

# 步骤3：安装依赖
echo ""
echo "📌 步骤3: 安装依赖包..."
# 检查 requirements.txt 是否存在
if [ ! -f "requirements.txt" ]; then
  echo -e "${RED}✗${NC} 缺少 requirements.txt，请确认目录完整"
  exit 1
fi
# 检查 start_mcp.py 是否存在
if [ ! -f "start_mcp.py" ]; then
  echo -e "${RED}✗${NC} 缺少 start_mcp.py，无法启动主服务"
  exit 1
fi
./venv/bin/pip install -r requirements.txt > install.log 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 依赖安装成功"
else
    echo -e "${RED}✗${NC} 依赖安装失败，详情见 install.log"
    exit 1
fi

# 步骤4：验证MCP模块
echo ""
echo "📌 步骤4: 验证MCP模块..."
./venv/bin/python -c "import mcp" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} MCP模块验证成功"
else
    echo -e "${RED}✗${NC} MCP模块验证失败"
    exit 1
fi

# 步骤5：运行功能测试
echo ""
echo "📌 步骤5: 运行功能测试..."
./venv/bin/python test_server.py > test_output.log 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 功能测试通过"
    echo ""
    echo "测试结果摘要："
    grep "✅" test_output.log
else
    echo -e "${RED}✗${NC} 功能测试失败，查看test_output.log了解详情"
    exit 1
fi

# 步骤6：生成Cursor配置
echo ""
echo "📌 步骤6: 生成Cursor配置..."
echo ""
echo "请将以下配置复制到Cursor的settings.json中："
echo ""
echo "----------------------------------------"
cat << EOF
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "$DIR/venv/bin/python",
      "args": ["$DIR/start_mcp.py"],
      "env": {}
    }
  }
}
EOF
echo "----------------------------------------"

# 给启动脚本添加执行权限
chmod +x run_mcp.sh
chmod +x start_mcp.py

echo ""
echo "🎉 配置完成！"
echo ""
echo "📋 后续步骤："
echo "1. 复制上面的配置到Cursor settings.json"
echo "2. 重启Cursor"
echo "3. 在Cursor聊天中测试：'请帮我获取git_commit提示词模板'"
echo ""
echo "💡 提示："
echo "- 使用 ./venv/bin/python 运行Python脚本"
echo "- 查看 MCP使用手册.md 了解详细使用方法"
echo "- 遇到问题运行: ./venv/bin/python test_server.py"

# 清理临时文件
rm -f test_output.log 

# 结束时增加一键启动主服务提示
echo ""
echo "🚦 一键启动 MCP 主服务："
echo "./venv/bin/python start_mcp.py" 