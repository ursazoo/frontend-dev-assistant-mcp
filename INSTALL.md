# 前端开发助手 MCP 安装指南

## 🚀 一键安装（推荐）

```bash
# 直接从Git安装最新版本
pip install git+https://github.com/your-username/frontend-dev-assistant-mcp.git
```

## 🔧 Cursor配置

安装完成后，在Cursor中添加配置：

### 方法1：全局配置
编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "frontend-dev-assistant"
    }
  }
}
```

### 方法2：项目配置
在项目根目录创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "frontend-dev-assistant"
    }
  }
}
```

## 📦 更新到最新版本

```bash
# 获取最新更新
pip install --upgrade git+https://github.com/your-username/frontend-dev-assistant-mcp.git
```

## ✅ 验证安装

安装完成后，在终端运行：

```bash
frontend-dev-assistant --help
```

或者直接启动服务：

```bash
frontend-dev-assistant
```

## 🎯 开始使用

重启Cursor后，你可以在聊天中使用以下功能：

1. **获取提示词模板**
   - "请帮我获取git_commit提示词模板"
   - "给我一个代码审查的提示词"

2. **生成Vue组件**
   - "帮我生成一个Vue3的表格组件"
   - "创建一个模态框组件"

3. **查找可复用组件**
   - "在当前项目中查找表格相关的组件"

4. **使用统计**
   - "显示MCP工具的使用统计"

## 🔧 故障排除

### 问题1：命令找不到
```bash
# 确保pip安装路径在系统PATH中
python -m pip show frontend-dev-assistant-mcp

# 或使用完整Python模块路径
python -m frontend_dev_assistant
```

### 问题2：权限问题
```bash
# 使用用户安装模式
pip install --user git+https://github.com/your-username/frontend-dev-assistant-mcp.git
```

### 问题3：网络问题
如果无法访问GitHub，可以：
1. 联系管理员获取内网Git地址
2. 或下载ZIP包手动安装

## 📞 技术支持

- 📧 邮箱：dev@example.com
- 💬 团队群：前端开发助手交流群
- �� 文档：查看项目README.md 