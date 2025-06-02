# Cursor MCP 配置指南

## 📖 配置步骤

### 1. 安装依赖

```bash
# 创建Python虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或 Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 测试MCP服务器

```bash
# 确保在虚拟环境中
source venv/bin/activate

# 测试服务器功能
python test_server.py
```

### 3. 配置Cursor

在Cursor中按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)，输入 "Preferences: Open Settings (JSON)"

添加以下配置到你的Cursor settings.json文件中：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "/Users/rabbitsbear/project/mine/python-mcp/venv/bin/python",
      "args": ["/Users/rabbitsbear/project/mine/python-mcp/start_mcp.py"],
      "env": {}
    }
  }
}
```

**⚠️ 重要**:

- 将两个路径都替换为你的实际项目路径
- `command` 必须使用虚拟环境中的python路径：`你的项目路径/venv/bin/python`
- `args` 使用启动脚本的绝对路径：`你的项目路径/start_mcp.py`

#### 查找正确路径

在项目目录下运行以下命令获取正确路径：

```bash
# 获取Python路径
pwd && echo "/venv/bin/python"

# 获取启动脚本路径  
pwd && echo "/start_mcp.py"
```

### 4. 重启Cursor

配置完成后，重启Cursor以使配置生效。

## 🎯 使用方法

### 基础使用

在Cursor的聊天窗口中，你现在可以使用以下功能：

1. **获取提示词模板**

   ```
   请帮我获取代码提交的提示词模板
   ```

2. **生成Vue组件**

   ```
   请生成一个Vue3表单组件，名称为UserForm
   ```

3. **查找可复用组件**

   ```
   帮我在项目中查找表格组件
   ```

4. **查看使用统计**

   ```
   显示本周的MCP工具使用统计
   ```

### 具体示例

#### 示例1：使用代码提交助手

```
请使用"git_commit"类型的提示词模板，上下文是"修复了用户登录页面的样式问题"
```

#### 示例2：生成表格组件

```
请生成一个Vue3表格组件，名称为DataTable，包含以下props：
- data: array (必填)
- columns: array (必填)  
- loading: boolean (可选，默认false)

功能特性：
- 分页
- 排序
- 行选择
```

#### 示例3：查找项目组件

```
帮我在/path/to/your/project中查找表单相关的组件，关键词包含：form、input
```

## 🔧 故障排除

### 常见问题

1. **MCP服务器无法启动**
   - 检查Python版本 (需要3.8+): `python3 --version`
   - 确保使用虚拟环境: `source venv/bin/activate`
   - 确保所有依赖已安装: `pip install -r requirements.txt`
   - 测试服务器组件: `python test_server.py`

2. **Cursor无法连接到MCP**
   - 确认配置文件中的路径正确（使用绝对路径）
   - 确认使用虚拟环境中的Python路径
   - 重启Cursor
   - 检查MCP日志输出

3. **工具调用失败**
   - 查看终端输出的错误信息
   - 确认工具参数格式正确
   - 检查文件权限
   - 运行 `python test_server.py` 验证组件功能

### 调试方法

1. **验证虚拟环境**

   ```bash
   source venv/bin/activate
   which python  # 应该显示venv路径
   python -c "import mcp; print('MCP可用')"
   ```

2. **测试服务器组件**

   ```bash
   python test_server.py
   ```

3. **检查配置路径**

   ```bash
   # 在项目目录下运行
   echo "Python路径: $(pwd)/venv/bin/python"
   echo "启动脚本: $(pwd)/start_mcp.py"
   ```

## 🚀 快速替代方案

如果MCP配置遇到困难，可以使用**静态提示词**方案：

1. 打开 `static_prompts.md` 文件
2. 复制需要的提示词模板
3. 直接在Cursor中使用
4. 无需任何安装和配置

## 📊 使用统计说明

MCP会自动记录以下数据供CTO查看：

- **工具使用次数**: 每个功能的调用频率
- **用户活跃度**: 团队成员的使用情况
- **反馈评价**: 工具效果的主观评价
- **使用趋势**: 每日使用量变化

查看统计数据：

```
请显示本月的MCP使用统计报告
```

## 🎯 最佳实践

1. **提示词使用**
   - 先熟悉默认提示词模板
   - 根据团队需求添加自定义模板
   - 定期更新和完善提示词

2. **组件生成**
   - 明确指定组件类型和功能需求
   - 提供详细的props定义
   - 遵循团队编码规范

3. **反馈记录**
   - 及时提供使用反馈
   - 描述具体使用场景
   - 建议改进方向

## 🚀 扩展功能

未来可以添加的功能：

- [ ] 自动代码格式化
- [ ] API文档生成
- [ ] 单元测试生成
- [ ] 性能分析报告
- [ ] 多项目支持
- [ ] 团队模板共享

## 📞 技术支持

如有问题或建议，请按以下顺序尝试：

1. **依赖问题**: 确保使用Python 3.8+和虚拟环境
2. **功能问题**: 运行 `python test_server.py` 检查
3. **路径问题**: 使用绝对路径和虚拟环境Python
4. **快速替代**: 使用 `static_prompts.md` 静态版本
