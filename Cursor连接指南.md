# Cursor MCP 连接指南

## 🎯 目标
将本地的`frontend_dev_assistant` MCP服务器连接到Cursor，启用**自动调用追踪**功能。

## ✅ 前置条件检查
- [x] MCP包已安装 (`pip3 install --user mcp`)
- [x] 服务器初始化测试通过
- [x] 调用追踪系统已集成

## 📋 配置步骤

### 1. 找到Cursor的MCP配置文件

**方法1: 通过Cursor设置**
1. 打开Cursor
2. 按 `Cmd+Shift+P` (macOS) 打开命令面板
3. 输入 "mcp" 搜索MCP相关设置
4. 选择 "Open MCP Settings" 或类似选项

**方法2: 手动编辑配置文件**
Cursor的MCP配置文件通常位于：
```
~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.cursor-small-mcp/mcp_settings.json
```
或者
```
~/.cursor/mcp_settings.json
```
或者
```
~/.config/cursor/mcp_settings.json
```

### 2. 添加MCP服务器配置

将以下配置添加到Cursor的MCP配置中：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "python3",
      "args": ["/Users/rabbitsbear/project/mine/python-mcp/run_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/rabbitsbear/project/mine/python-mcp/src"
      }
    }
  }
}
```

**重要提示：**
- 确保路径 `/Users/rabbitsbear/project/mine/python-mcp/run_mcp_server.py` 正确
- 如果你的用户名不是 `rabbitsbear`，请修改为正确的路径

### 3. 重启Cursor

配置保存后，完全退出并重新启动Cursor。

### 4. 验证连接

1. 在Cursor中打开任意前端项目
2. 尝试使用MCP功能（通常通过@符号或特定快捷键）
3. 查看是否出现 `frontend-dev-assistant` 选项

## 🧪 测试MCP功能

### 测试工具1: 获取提示词模板
```
@frontend-dev-assistant get_prompt_template
```
参数示例：
```json
{
  "prompt_type": "git_commit",
  "context": "修复登录bug"
}
```

### 测试工具2: 生成Vue组件
```
@frontend-dev-assistant generate_vue_component
```
参数示例：
```json
{
  "component_type": "form",
  "component_name": "UserLoginForm",
  "vue_version": "vue3"
}
```

### 测试工具3: 查找可复用组件
```
@frontend-dev-assistant find_reusable_components
```
参数示例：
```json
{
  "project_path": "/path/to/your/frontend/project",
  "component_type": "table"
}
```

## 📊 查看调用统计

每次使用MCP工具后，都会自动记录调用数据。在项目目录运行：

```bash
# 进入MCP项目目录
cd /Users/rabbitsbear/project/mine/python-mcp

# 查看最近7天的统计
python mcp_stats.py

# 查看今天的统计
python mcp_stats.py --days 1

# 导出数据给领导汇报
python mcp_stats.py --export csv
```

## 🔧 故障排除

### 问题1: Cursor中看不到MCP服务器
**解决方案：**
1. 检查配置文件路径是否正确
2. 确保JSON格式正确（没有语法错误）
3. 重启Cursor
4. 查看Cursor的开发者工具控制台是否有错误信息

### 问题2: MCP工具调用失败
**解决方案：**
1. 检查 `run_mcp_server.py` 路径是否正确
2. 确保有执行权限：`chmod +x run_mcp_server.py`
3. 手动测试服务器：`python3 test_mcp_server.py`

### 问题3: 依赖包缺失
**解决方案：**
```bash
pip3 install --user mcp pydantic typing-extensions aiofiles
```

### 问题4: 权限问题
**解决方案：**
```bash
# 确保脚本有执行权限
chmod +x /Users/rabbitsbear/project/mine/python-mcp/run_mcp_server.py

# 确保数据目录可写
mkdir -p /Users/rabbitsbear/project/mine/python-mcp/src/data
```

## 📈 使用统计示例

成功连接后，使用几次MCP工具，然后查看统计：

```bash
python mcp_stats.py
```

你会看到类似这样的输出：
```
🔍 Frontend Dev Assistant MCP 调用统计
============================================================
📁 数据来源: src/data/mcp_calls.json
📅 统计范围: 最近7天

📊 基础统计
------------------------------
总调用次数:              5 次
成功调用:                5 次
失败调用:                0 次
成功率:              100.0%
平均执行时间:        245.2 ms
总结果大小:         12.3KB
日均调用:              0.7 次

🛠️ 工具使用排行
------------------------------
 1. get_prompt_template          3 次 ( 60.0%)  120.0ms
 2. generate_vue_component       2 次 ( 40.0%)  410.5ms

⏰ 使用模式
------------------------------
使用高峰时段:           14点 (3次)
```

## 🚀 下一步

连接成功后，你可以：

1. **日常开发中使用MCP工具**
   - 获取标准化的Git提交信息模板
   - 生成符合规范的Vue组件代码
   - 查找项目中可复用的组件

2. **定期查看使用统计**
   - 每周运行 `python mcp_stats.py` 了解使用情况
   - 识别最常用的工具，优化开发流程
   - 导出数据用于团队效率分析

3. **扩展功能**
   - 根据使用情况添加新的MCP工具
   - 优化慢调用的性能
   - 基于错误统计改进工具稳定性

---

**📞 如果遇到问题：**
1. 先运行 `python3 test_mcp_server.py` 确认服务器正常
2. 检查Cursor的开发者工具控制台错误信息
3. 确认配置文件路径和格式正确

祝使用愉快！🎉 