# 前端开发提示词库

## 📋 快速使用指南

直接复制以下提示词到Cursor中使用，无需安装任何依赖。

---

## 🔧 1. Git代码提交助手

```
帮我分批次提交代码。请先检查 git status，然后分析所有未暂存的修改，并一次性提供一个完整的、按模块或功能分组的提交计划。

计划应包含：
1. 每个批次要提交的文件列表
2. 为每个批次建议的 commit message (格式为 feat/fix: 中文描述)

请等待我确认或修改计划后再执行任何 git 命令。

注意事项：
- 遵循 Conventional Commits 规范
- commit message 使用中文描述
- 按功能模块合理分组
- 避免混合不相关的改动

附加上下文：[在这里填写你的具体改动描述]
```

---

## 🔍 2. 代码审查助手

```
根据前端代码规范对以下代码进行 code review，主要关注：

规范检查：
1. **魔法值处理**：是否存在硬编码的数字、字符串等魔法值
2. **常量定义**：常量是否正确定义和使用
3. **方法注释**：方法是否有完整的JSDoc注释
4. **命名规范**：变量、方法、组件命名是否符合规范
5. **代码结构**：是否遵循团队约定的代码组织结构

业务逻辑检查：
1. **错误处理**：是否有适当的错误边界和异常处理
2. **性能优化**：是否存在明显的性能问题
3. **可维护性**：代码是否易于理解和维护
4. **测试覆盖**：是否遗漏重要的测试场景

请提供具体的改进建议和示例代码。

参考编码规范：
- 使用 PascalCase 命名组件
- 使用 camelCase 命名变量和方法
- 常量使用 UPPER_SNAKE_CASE
- 方法必须有 JSDoc 注释
- 避免使用魔法值，定义为常量

代码内容：
[在这里粘贴要审查的代码]
```

---

## 🎨 3. Vue组件生成助手

### Vue3 表单组件

```
请基于团队编码规范生成一个Vue3表单组件。

组件要求：
- 组件名称：[ComponentName]
- Vue版本：vue3
- 组件类型：form

编码规范要求：
1. **命名规范**：
   - 组件使用 PascalCase
   - props 使用 camelCase
   - 事件使用 kebab-case
   - 插槽使用 kebab-case

2. **结构规范**：
   - 使用 <script setup> 语法
   - props 必须定义类型和默认值
   - 导出的方法需要 JSDoc 注释
   - 样式使用 scoped

3. **代码质量**：
   - 添加适当的类型检查
   - 包含错误边界处理
   - 支持响应式设计
   - 遵循无障碍规范

4. **注释要求**：
   - 组件顶部添加功能说明
   - 复杂逻辑添加行内注释
   - props 添加描述注释

Props需求：
- title: string (可选，默认为空)
- fields: array (必填，表单字段配置)
- loading: boolean (可选，默认false)

功能特性：
- 表单验证
- 数据绑定
- 错误提示
- 加载状态

请生成完整的组件代码，包括：
- 完整的 Vue 单文件组件
- TypeScript 类型定义
- 使用示例和文档
```

### Vue3 表格组件

```
请基于团队编码规范生成一个Vue3表格组件。

组件要求：
- 组件名称：[ComponentName]
- Vue版本：vue3
- 组件类型：table

Props需求：
- data: array (必填，表格数据)
- columns: array (必填，列配置)
- loading: boolean (可选，默认false)
- pagination: object (可选，分页配置)

功能特性：
- 数据展示
- 排序功能
- 分页功能
- 行选择
- 加载状态

请按照上述Vue组件编码规范生成完整代码。
```

### Vue3 弹窗组件

```
请基于团队编码规范生成一个Vue3弹窗组件。

组件要求：
- 组件名称：[ComponentName]
- Vue版本：vue3
- 组件类型：modal

Props需求：
- visible: boolean (必填，控制显示)
- title: string (可选，弹窗标题)
- width: string (可选，弹窗宽度)
- closable: boolean (可选，是否可关闭)

功能特性：
- 遮罩层
- 居中显示
- 可拖拽
- 键盘事件
- 插槽支持

请按照上述Vue组件编码规范生成完整代码。
```

---

## 🔍 4. 组件复用查找助手

```
帮我复用项目中的组件。

请执行以下步骤：

1. **查找现有组件**：
   - 在项目的 components 目录下查找相关组件
   - 分析组件的 props 接口和使用方式
   - 确定组件的适用场景

2. **生成使用代码**：
   - 提供完整的引入语句
   - 展示基本使用示例
   - 说明主要 props 的作用和类型

3. **定制建议**：
   - 如果现有组件不完全匹配需求，提供修改建议
   - 建议如何扩展组件功能
   - 提醒注意事项和最佳实践

搜索范围：
- 项目路径：[填写项目路径]
- 组件类型：[如：table, form, modal等]
- 搜索关键词：[填写关键词]

期望功能：
[描述你需要的具体功能]

请在指定位置生成对应的代码，并确保：
- 正确引入组件依赖
- 使用符合团队规范的代码风格
- 添加必要的注释说明
```

---

## 📦 5. API接口封装助手

```
请帮我创建一个标准的API接口封装。

业务需求：
- 接口名称：[接口名]
- 请求方法：[GET/POST/PUT/DELETE]
- 接口路径：[API路径]
- 请求参数：[参数说明]
- 响应格式：[响应数据结构]

编码要求：
1. **使用axios实例**
2. **统一错误处理**
3. **请求/响应拦截器**
4. **TypeScript类型定义**
5. **JSDoc注释**

技术栈：
- Vue3 + TypeScript
- Axios
- 团队统一的接口规范

请生成：
1. API函数封装
2. TypeScript类型定义
3. 使用示例
4. 错误处理方案
```

---

## 🧪 6. 单元测试生成助手

```
请为以下Vue组件/函数生成单元测试。

测试目标：
[粘贴要测试的代码]

测试要求：
1. **使用Vitest + Vue Test Utils**
2. **覆盖主要功能点**
3. **包含边界情况测试**
4. **Props测试**
5. **事件测试**
6. **异步操作测试**

测试场景：
- 组件正常渲染
- Props传递和验证
- 用户交互行为
- 异步数据加载
- 错误状态处理

请生成：
1. 完整的测试文件
2. Mock数据和方法
3. 测试覆盖率报告
4. 运行命令说明
```

---

## 💡 使用技巧

### 快速选择提示词

1. **代码提交场景** → 使用"Git代码提交助手"
2. **代码审查场景** → 使用"代码审查助手"  
3. **新建组件场景** → 使用"Vue组件生成助手"
4. **复用组件场景** → 使用"组件复用查找助手"
5. **API开发场景** → 使用"API接口封装助手"
6. **测试编写场景** → 使用"单元测试生成助手"

### 自定义修改

- 将`[ComponentName]`替换为实际组件名
- 将`[接口名]`等占位符替换为具体内容
- 根据项目技术栈调整代码规范

### 保存到Cursor

建议将常用提示词保存到Cursor的代码片段中，方便快速调用。

---

## 🔄 与完整MCP的对比

| 功能 | 静态提示词 | 完整MCP |
|------|------------|---------|
| 使用便捷性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 功能丰富性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 统计追踪 | ❌ | ✅ |
| 自动化程度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 部署复杂度 | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**建议**：

- 快速开始 → 使用静态提示词
- 团队深度使用 → 部署完整MCP
