"""
提示词管理模块
负责管理和提供各种开发场景的标准化提示词模板
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class PromptManager:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        self.load_default_templates()
    
    def load_default_templates(self):
        """加载默认提示词模板"""
        default_templates = {
            "git_commit": {
                "name": "Git 代码提交助手",
                "description": "帮助开发者分批次、规范化提交代码",
                "template": """帮我分批次提交代码。请先检查 git status，然后分析所有未暂存的修改，并一次性提供一个完整的、按模块或功能分组的提交计划。

计划应包含：
1. 每个批次要提交的文件列表
2. 为每个批次建议的 commit message (格式为 feat/fix: 中文描述)

请等待我确认或修改计划后再执行任何 git 命令。

注意事项：
- 遵循 Conventional Commits 规范
- commit message 使用中文描述
- 按功能模块合理分组
- 避免混合不相关的改动

{context}""",
                "usage_count": 0,
                "last_used": None,
                "tags": ["git", "提交", "代码管理"]
            },
            
            "code_review": {
                "name": "代码审查助手",
                "description": "基于团队规范进行代码质量审查",
                "template": """根据前端代码规范对以下代码进行 code review，主要关注：

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

{context}""",
                "usage_count": 0,
                "last_used": None,
                "tags": ["代码审查", "质量检查", "规范"]
            },
            
            "component_reuse": {
                "name": "组件复用助手",
                "description": "帮助快速定位和复用项目中的现有组件",
                "template": """帮我复用项目中的{component_type}组件。

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

搜索关键词：{keywords}

期望功能：{expected_features}

请在指定位置生成对应的代码，并确保：
- 正确引入组件依赖
- 使用符合团队规范的代码风格
- 添加必要的注释说明

{context}""",
                "usage_count": 0,
                "last_used": None,
                "tags": ["组件复用", "代码生成", "效率工具"]
            },
            
            "vue_component_spec": {
                "name": "Vue组件规范生成",
                "description": "基于团队编码规范生成标准Vue组件",
                "template": """请基于团队编码规范生成一个{vue_version} {component_type}组件。

组件要求：
- 组件名称：{component_name}
- Vue版本：{vue_version}
- 组件类型：{component_type}

编码规范要求：
1. **命名规范**：
   - 组件使用 PascalCase
   - props 使用 camelCase
   - 事件使用 kebab-case
   - 插槽使用 kebab-case

2. **结构规范**：
   - 使用 <script setup> 语法（Vue3）
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

组件功能特性：{features}

请生成完整的组件代码，包括：
- 完整的 Vue 单文件组件
- TypeScript 类型定义（如适用）
- 使用示例和文档

{context}""",
                "usage_count": 0,
                "last_used": None,
                "tags": ["Vue组件", "代码生成", "编码规范"]
            }
        }
        
        # 保存默认模板到文件
        templates_file = self.templates_dir / "default_templates.json"
        if not templates_file.exists():
            with open(templates_file, 'w', encoding='utf-8') as f:
                json.dump(default_templates, f, ensure_ascii=False, indent=2)
    
    async def get_template(self, prompt_type: str, context: str = "") -> str:
        """获取指定类型的提示词模板"""
        try:
            templates_file = self.templates_dir / "default_templates.json"
            with open(templates_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            
            if prompt_type not in templates:
                return f"未找到类型为 '{prompt_type}' 的提示词模板"
            
            template_data = templates[prompt_type]
            template = template_data["template"]
            
            # 更新使用记录
            template_data["usage_count"] += 1
            template_data["last_used"] = datetime.now().isoformat()
            
            # 保存更新后的数据
            with open(templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
            
            # 替换上下文变量
            if context:
                template = template.replace("{context}", f"\n附加上下文：\n{context}")
            else:
                template = template.replace("{context}", "")
            
            # 构建返回信息
            result = f"""
📋 **{template_data['name']}**

{template_data['description']}

---

{template}

---
💡 使用次数：{template_data['usage_count']} | 标签：{', '.join(template_data['tags'])}
"""
            return result
            
        except Exception as e:
            return f"获取提示词模板时出错：{str(e)}"
    
    async def add_custom_template(self, name: str, template: str, description: str = "", tags: List[str] = None) -> str:
        """添加自定义提示词模板"""
        try:
            custom_file = self.templates_dir / "custom_templates.json"
            
            # 加载现有自定义模板
            if custom_file.exists():
                with open(custom_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
            else:
                custom_templates = {}
            
            # 添加新模板
            custom_templates[name] = {
                "name": name,
                "description": description,
                "template": template,
                "tags": tags or [],
                "usage_count": 0,
                "last_used": None,
                "created_at": datetime.now().isoformat()
            }
            
            # 保存
            with open(custom_file, 'w', encoding='utf-8') as f:
                json.dump(custom_templates, f, ensure_ascii=False, indent=2)
            
            return f"✅ 自定义提示词模板 '{name}' 已添加成功"
            
        except Exception as e:
            return f"添加自定义模板时出错：{str(e)}"
    
    async def list_templates(self) -> str:
        """列出所有可用的提示词模板"""
        try:
            result = "📚 **可用的提示词模板**\n\n"
            
            # 加载默认模板
            templates_file = self.templates_dir / "default_templates.json"
            if templates_file.exists():
                with open(templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                
                result += "## 默认模板\n"
                for key, template in templates.items():
                    result += f"- **{key}**: {template['name']}\n"
                    result += f"  {template['description']}\n"
                    result += f"  使用次数: {template['usage_count']} | 标签: {', '.join(template['tags'])}\n\n"
            
            # 加载自定义模板
            custom_file = self.templates_dir / "custom_templates.json"
            if custom_file.exists():
                with open(custom_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                
                if custom_templates:
                    result += "## 自定义模板\n"
                    for key, template in custom_templates.items():
                        result += f"- **{key}**: {template['name']}\n"
                        result += f"  {template['description']}\n"
                        result += f"  使用次数: {template['usage_count']} | 标签: {', '.join(template['tags'])}\n\n"
            
            return result
            
        except Exception as e:
            return f"列出模板时出错：{str(e)}" 