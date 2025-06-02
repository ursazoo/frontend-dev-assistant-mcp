@echo off
chcp 65001 >nul
REM 前端开发提示词智能助手 MCP - Windows快速配置脚本

echo 🚀 前端开发提示词智能助手 MCP 快速配置
echo ========================================

REM 获取脚本所在目录
set DIR=%~dp0
cd /d "%DIR%"

REM 步骤1：检查Python版本
echo.
echo 📌 步骤1: 检查Python版本...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ 发现Python版本: %PYTHON_VERSION%

REM 步骤2：创建虚拟环境
echo.
echo 📌 步骤2: 创建虚拟环境...
if exist venv (
    echo ⚠️  虚拟环境已存在，跳过创建
) else (
    python -m venv venv
    echo ✓ 虚拟环境创建成功
)

REM 步骤3：安装依赖
echo.
echo 📌 步骤3: 安装依赖包...
REM 检查 requirements.txt 是否存在
if not exist requirements.txt (
    echo ❌ 缺少 requirements.txt，请确认目录完整
    pause
    exit /b 1
)
REM 检查 start_mcp.py 是否存在
if not exist start_mcp.py (
    echo ❌ 缺少 start_mcp.py，无法启动主服务
    pause
    exit /b 1
)
venv\Scripts\pip install -r requirements.txt >install.log 2>&1
if %errorlevel% equ 0 (
    echo ✓ 依赖安装成功
) else (
    echo ❌ 依赖安装失败，详情见 install.log
    pause
    exit /b 1
)

REM 步骤4：验证MCP模块
echo.
echo 📌 步骤4: 验证MCP模块...
venv\Scripts\python -c "import mcp" 2>nul
if %errorlevel% equ 0 (
    echo ✓ MCP模块验证成功
) else (
    echo ❌ MCP模块验证失败
    pause
    exit /b 1
)

REM 步骤5：运行功能测试
echo.
echo 📌 步骤5: 运行功能测试...
venv\Scripts\python test_server.py >test_output.log 2>&1
if %errorlevel% equ 0 (
    echo ✓ 功能测试通过
    echo.
    echo 测试结果摘要：
    findstr "✅" test_output.log
) else (
    echo ❌ 功能测试失败，查看test_output.log了解详情
    pause
    exit /b 1
)

REM 步骤6：生成Cursor配置
echo.
echo 📌 步骤6: 生成Cursor配置...
echo.
echo 请将以下配置复制到Cursor的settings.json中：
echo.
echo ----------------------------------------
echo {
echo   "mcpServers": {
echo     "frontend-dev-assistant": {
echo       "command": "%DIR%venv\Scripts\python.exe",
echo       "args": ["%DIR%start_mcp.py"],
echo       "env": {}
echo     }
echo   }
echo }
echo ----------------------------------------

echo.
echo 🎉 配置完成！
echo.
echo 📋 后续步骤：
echo 1. 复制上面的配置到Cursor settings.json
echo 2. 重启Cursor
echo 3. 在Cursor聊天中测试：'请帮我获取git_commit提示词模板'
echo.
echo 💡 提示：
echo - 使用 venv\Scripts\python 运行Python脚本
echo - 查看 MCP使用手册.md 了解详细使用方法
echo - 遇到问题运行: venv\Scripts\python test_server.py

REM 清理临时文件
if exist test_output.log del test_output.log

REM 结束时增加一键启动主服务提示
echo.
echo 🚦 一键启动 MCP 主服务：
echo venv\Scripts\python start_mcp.py

pause 