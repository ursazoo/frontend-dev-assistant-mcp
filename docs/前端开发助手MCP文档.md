# 前端开发助手MCP完整文档

## 1. 项目简介

前端开发助手MCP是一个专为前端开发团队设计的智能助手工具，基于Model Context Protocol (MCP)协议构建。它通过集成多种开发辅助功能，显著提升前端开发效率和代码质量。

### 核心价值

**提升开发效率**：通过智能组件查找和代码生成，减少重复劳动，加快开发速度。开发者可以快速定位项目中已有的可复用组件，避免重复造轮子，同时自动生成符合团队规范的标准组件代码。

**保证代码质量**：基于团队编码规范的自动化代码审查和标准化提示词管理，确保代码一致性。所有生成的代码都严格遵循预设的编码规范，包括命名约定、结构标准和质量要求。

**智能工作流程**：通过AI驱动的工作流程优化，将常见的开发任务标准化。从Git提交规范化到组件复用建议，每个环节都有智能助手参与，形成高效的开发闭环。

**团队协作增强**：统一的开发标准和工具使用，促进团队成员之间的协作效率。通过标准化的提示词模板和组件生成规范，确保不同开发者产出的代码风格一致。

### 技术架构

**MCP协议基础**：基于最新的Model Context Protocol构建，与Cursor、Claude等AI工具深度集成，提供原生的AI助手体验。支持异步操作和实时通信，确保流畅的用户交互体验。

**模块化设计**：采用清晰的模块化架构，包含提示词管理器、组件生成器、使用追踪器等独立模块，便于维护和扩展。每个模块都有明确的职责边界，支持独立部署和更新。

**智能算法引擎**：内置多维度智能匹配算法，支持组件智能查找、相似度计算、功能分析等高级特性。算法支持语义理解、模糊匹配和上下文分析，提供精准的推荐结果。

## 2. 快速开始

### 环境要求

- Python 3.8+
- Cursor编辑器或其他支持MCP的AI工具
- Git（用于代码管理功能）

### 安装步骤

**方式一：直接安装（推荐）**

```bash
# 从Git仓库安装最新版本
pip install git+https://github.com/your-username/frontend-dev-assistant-mcp.git

# 如果遇到权限问题，使用用户模式安装
pip install --user git+https://github.com/your-username/frontend-dev-assistant-mcp.git
```

**方式二：本地开发安装**

```bash
# 克隆仓库
git clone https://github.com/your-username/frontend-dev-assistant-mcp.git
cd frontend-dev-assistant-mcp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

### 配置设置

**在Cursor中配置MCP服务器**

在项目根目录或全局`~/.cursor`目录下创建`mcp.json`配置文件：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "frontend-dev-assistant",
      "args": [],
      "env": {}
    }
  }
}
```

**高级配置选项**

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "frontend-dev-assistant",
      "args": ["--project-path", "/path/to/your/project"],
      "env": {
        "LOG_LEVEL": "INFO",
        "TEMPLATE_PATH": "/custom/templates"
      }
    }
  }
}
```

### 验证安装

重启Cursor后，在聊天界面测试基本功能：

```
"获取git_commit提示词模板"
"帮我生成一个Vue3的用户列表组件"
"在项目中查找button相关的组件"
```

如果安装成功，你会看到相应的功能响应和结果输出。

### 常见问题解决

**命令找不到**：确认pip安装路径在系统PATH中，或使用`python -m frontend_dev_assistant`替代命令。

**权限问题**：使用`--user`参数进行用户级安装，或在虚拟环境中安装。

**依赖冲突**：建议在独立的虚拟环境中安装，避免与其他项目的依赖冲突。

## 3. 功能说明

### 3.1 智能提示词管理

提示词管理系统提供标准化的开发提示词模板，帮助开发者快速获取符合团队规范的AI提示词。

**Git代码提交助手**

```bash
# 使用示例
mcp_frontend-dev-assistant_get_prompt_template git_commit "修改了用户模块的登录功能"
```

功能特点：

- 自动分析git status，智能分组未提交的文件
- 生成符合Conventional Commits规范的提交信息
- 支持中文描述，便于团队理解
- 按功能模块合理分组，避免混合不相关改动

**代码审查助手**

基于团队编码规范进行自动化代码质量检查，包括魔法值检测、命名规范验证、注释完整性检查等。审查范围覆盖变量命名、方法结构、错误处理、性能优化等多个维度。

**组件复用助手**

智能分析项目中的现有组件，提供复用建议和使用指导。系统会自动扫描组件目录，分析组件接口，生成完整的使用示例代码。

### 3.2 Vue组件智能生成

组件生成器基于团队编码规范，自动生成标准化的Vue组件代码。

**支持的组件类型**

- **表单组件**：包含验证逻辑、错误处理、多种输入控件
- **表格组件**：支持排序、分页、自定义列渲染
- **弹窗组件**：多种尺寸、自定义内容、动画效果
- **卡片组件**：灵活布局、响应式设计
- **列表组件**：虚拟滚动、自定义项模板
- **自定义组件**：根据具体需求生成基础结构

**生成示例**

```javascript
// 生成Vue3表格组件
mcp_frontend-dev-assistant_generate_vue_component({
  component_type: "table",
  component_name: "UserTable", 
  vue_version: "vue3",
  props: [
    {name: "data", type: "Array", required: true},
    {name: "loading", type: "Boolean", default: false}
  ],
  features: ["排序", "分页", "筛选"]
})
```

生成的组件自动包含：

- 完整的TypeScript类型定义
- 响应式数据绑定
- 错误边界处理
- 无障碍访问支持
- 完整的JSDoc注释
- Scoped样式定义

### 3.3 智能组件查找系统

组件查找系统采用多维度智能匹配算法，在项目中快速定位可复用组件。

**查找算法原理**

算法使用四个维度进行评分：

- **类型相似度(40%)**：组件类型语义匹配，支持同义词识别
- **关键词匹配(30%)**：名称、路径、属性的文本匹配  
- **功能相似度(20%)**：基于props和events的功能分析
- **名称相似度(10%)**：字符串模糊匹配和编辑距离计算

**使用示例**

```javascript
// 查找列表相关组件
mcp_frontend-dev-assistant_find_reusable_components({
  project_path: "/path/to/project",
  component_type: "list",
  search_keywords: ["列表", "table", "表格"]
})
```

查找结果包含：

- 组件路径和名称
- 智能生成的功能描述
- Props和Events接口分析
- 使用场景推荐
- 代码使用示例

**智能命名算法**

系统自动处理常见的组件命名模式：

- 通用前缀识别：`base`, `common`, `fs`, `fb`等
- Index文件处理：使用父目录名生成语义化名称
- 重名解决：基于路径上下文生成唯一标识

### 3.4 使用统计与分析

使用追踪系统记录工具使用情况，提供团队效率分析和优化建议。

**统计维度**

- 工具使用频率和成功率
- 团队成员活跃度分析
- 功能模块受欢迎程度
- 用户满意度评价

**数据展示**

```javascript
// 获取使用统计
mcp_frontend-dev-assistant_get_usage_stats("week")
```

输出包含：

- 各功能模块使用次数
- 用户反馈评分分布
- 效率提升指标
- 使用趋势分析

## 4. 后续迭代计划

**算法优化升级**

提升组件查找算法的准确率和召回率，增强语义理解能力。计划引入更先进的自然语言处理技术，提高对组件功能的理解精度。优化多语言支持，增强对中英文混合项目的处理能力。

**框架支持扩展**

扩展对React、Angular等主流前端框架的支持，提供跨框架的组件分析能力。开发框架特定的代码生成模板，确保生成的代码符合各框架的最佳实践。
