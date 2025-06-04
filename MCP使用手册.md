# 前端开发提示词智能助手 MCP 使用手册

## 📋 目录
1. [环境准备](#环境准备)
2. [安装步骤](#安装步骤)
3. [功能验证](#功能验证)
4. [Cursor配置](#cursor配置)
5. [使用说明](#使用说明)
6. [常见问题解决](#常见问题解决)
7. [功能演示](#功能演示)
8. [团队部署建议](#团队部署建议)

---

## 🔧 环境准备

### 系统要求
- macOS / Linux / Windows
- Python 3.8 或更高版本
- Cursor 编辑器

### 检查Python版本
```bash
python3 --version
# 应该显示 Python 3.8 或更高版本
```

### ⚠️ 重要提示：Python别名问题
如果你的系统配置了Python别名（常见于macOS用户），可能会导致虚拟环境失效。

检查是否有别名：
```bash
alias | grep python
```

如果看到类似 `python='...'` 的输出，你需要：
1. 使用完整路径运行Python
2. 或临时取消别名：`unalias python`

---

## 📦 安装步骤

### 1. 克隆或下载项目
```bash
cd /your/project/directory
# 如果是新项目，确保所有文件都已复制到项目目录
```

### 2. 创建虚拟环境
```bash
# 使用python3明确指定版本
python3 -m venv venv
```

### 3. 安装依赖
```bash
# macOS/Linux - 使用完整路径避免别名问题
./venv/bin/pip install -r requirements.txt

# Windows
.\venv\Scripts\pip install -r requirements.txt
```

### 4. 验证安装
```bash
# 验证MCP模块是否安装成功
./venv/bin/python -c "import mcp; print('✅ MCP模块安装成功')"
```

---

## ✅ 功能验证

### 运行测试脚本
```bash
# macOS/Linux
./venv/bin/python test_server.py

# Windows
.\venv\Scripts\python test_server.py
```

预期输出：
```
🚀 测试前端开发提示词智能助手 MCP 服务器
============================================================
🧪 测试MCP服务器初始化...
✅ MCP服务器初始化成功!
🔧 测试提示词管理器...
✅ 提示词管理器工作正常
🎨 测试组件生成器...
✅ 组件生成器工作正常
📊 测试使用统计器...
✅ 使用统计器工作正常

🎉 服务器测试通过!
```

如果测试失败，请查看[常见问题解决](#常见问题解决)部分。

---

## 🎯 Cursor配置

### 1. 获取项目路径
```bash
# 在项目目录下运行
pwd
# 记下输出的路径，例如：/Users/username/project/python-mcp
```

### 2. 打开Cursor配置
- macOS: `Cmd+Shift+P` → 输入 "Preferences: Open Settings (JSON)"
- Windows/Linux: `Ctrl+Shift+P` → 输入 "Preferences: Open Settings (JSON)"

### 3. 添加MCP配置

#### 方式A：使用Python路径（推荐）
```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "/你的项目路径/venv/bin/python",
      "args": ["/你的项目路径/start_mcp.py"],
      "env": {}
    }
  }
}
```

#### 方式B：使用启动脚本
```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "/你的项目路径/run_mcp.sh",
      "args": [],
      "env": {}
    }
  }
}
```

#### Windows配置示例
```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "C:\\你的项目路径\\venv\\Scripts\\python.exe",
      "args": ["C:\\你的项目路径\\start_mcp.py"],
      "env": {}
    }
  }
}
```

### 4. 重启Cursor
保存配置后，完全退出并重新启动Cursor。

### 5. 验证连接
在Cursor聊天窗口中输入：
```
测试MCP连接
```

如果配置成功，你应该能够使用MCP功能。

---

## 💡 使用说明

### 基础功能

#### 1. 获取提示词模板
```
请帮我获取git_commit类型的提示词模板
```

支持的提示词类型：
- `git_commit` - 代码提交助手
- `code_review` - 代码审查
- `component_reuse` - 组件复用
- `vue_component_spec` - Vue组件规范

#### 2. 生成Vue组件
```
请生成一个Vue3表单组件，名称为UserForm，包含以下props：
- title: string (可选)
- fields: array (必填)
- loading: boolean (可选)

功能特性：表单验证、错误提示
```

#### 3. 查找可复用组件
```
在项目/Users/username/my-vue-project中查找表格类型的组件
```

#### 4. 记录使用反馈
```
记录工具使用情况：
- 工具名称：generate_vue_component
- 反馈：excellent
- 使用场景：生成用户管理表格
```

#### 5. 查看使用统计

```markdown
显示本周的MCP使用统计报告
```

---

## 🔧 常见问题解决

### 问题1：ModuleNotFoundError: No module named 'mcp'

**原因**：使用了错误的Python解释器

**解决方案**：
```bash
# 1. 确认使用虚拟环境的Python
which python  # 如果显示系统路径，说明有别名问题

# 2. 使用完整路径
./venv/bin/python test_server.py

# 3. 或取消别名
unalias python
source venv/bin/activate
python test_server.py
```

### 问题2：Cursor无法连接MCP

**检查步骤**：
1. 确认路径正确
   ```bash
   ls -la /你配置的路径/venv/bin/python
   ls -la /你配置的路径/start_mcp.py
   ```

2. 测试启动脚本
   ```bash
   /你配置的路径/venv/bin/python /你配置的路径/start_mcp.py
   # 应该看到程序启动但等待输入（按Ctrl+C退出）
   ```

3. 检查Cursor日志
   - 打开Cursor开发者工具：`Help` → `Toggle Developer Tools`
   - 查看Console标签中的错误信息

### 问题3：unhandled errors in a TaskGroup

**原因**：MCP服务器需要通过stdio与客户端通信

**解决方案**：这是正常的，MCP服务器不能直接运行，必须通过Cursor连接。使用`test_server.py`来验证功能。

### 问题4：Permission denied

**解决方案**：
```bash
# 给脚本添加执行权限
chmod +x run_mcp.sh
chmod +x start_mcp.py
```

---

## 🎬 功能演示

### 示例1：智能代码提交
```
用户：请使用git_commit提示词，我修改了登录页面的样式和验证逻辑

MCP返回：
[Git提交计划]
批次1 - 样式修改：
- src/views/Login.vue (样式部分)
- src/styles/login.scss
建议commit: feat: 优化登录页面UI样式

批次2 - 验证逻辑：
- src/views/Login.vue (逻辑部分)
- src/utils/validators.js
建议commit: feat: 增强登录表单验证逻辑
```

### 示例2：组件生成
```
用户：生成一个Vue3的数据表格组件DataTable，支持分页和排序

MCP返回：
[完整的Vue组件代码，包含：]
- TypeScript类型定义
- 组件模板
- 响应式数据处理
- 分页逻辑
- 排序功能
- 使用示例
```

### 示例3：团队使用统计
```
用户：显示本月的使用统计

MCP返回：
📊 MCP工具使用统计报告 (近30天)

总调用次数：156
使用的工具数：5
活跃用户数：7

工具使用排行：
1. get_prompt_template: 68次 (43.6%)
2. generate_vue_component: 42次 (26.9%)
3. find_reusable_components: 28次 (17.9%)

满意度：92.3% (好评+优秀)
```

---

## 👥 团队部署建议

### 1. 统一环境配置
创建团队配置文档：
```bash
# team-setup.sh
#!/bin/bash
echo "🚀 设置团队MCP环境..."
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python test_server.py
echo "✅ 环境配置完成！"
```

### 2. 共享配置模板
提供标准的Cursor配置模板，团队成员只需要修改路径。

### 3. 定期查看统计
技术负责人可以定期运行：
```
显示all时间范围的使用统计
```

### 4. 收集反馈优化
鼓励团队成员使用反馈功能，持续改进提示词模板。

---

## 📞 技术支持

遇到问题时的排查顺序：

1. **运行测试脚本**：`./venv/bin/python test_server.py`
2. **检查Python路径**：`which python` 和 `./venv/bin/python --version`
3. **验证依赖安装**：`./venv/bin/pip list | grep mcp`
4. **查看错误日志**：检查具体的错误信息
5. **参考本文档**：大部分问题都有解决方案

## 🚀 下一步

1. 完成配置后，开始使用MCP提升开发效率
2. 定期查看使用统计，了解团队使用情况
3. 根据实际需求，扩展和优化提示词模板
4. 考虑添加更多自定义功能，如API文档生成、测试用例生成等

---

**版本**: 1.0.0  
**更新日期**: 2024-01  
**维护团队**: 前端开发团队 