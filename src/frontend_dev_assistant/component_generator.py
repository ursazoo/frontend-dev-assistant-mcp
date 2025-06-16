"""
Vue组件生成器模块
负责生成符合团队规范的Vue组件代码，并支持查找项目中的可复用组件
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class ComponentGenerator:
    def __init__(self):
        self.vue_coding_standards = self.load_coding_standards()
        
    def load_coding_standards(self) -> Dict[str, Any]:
        """加载Vue编码规范"""
        return {
            "naming": {
                "component": "PascalCase",
                "props": "camelCase", 
                "events": "kebab-case",
                "slots": "kebab-case",
                "constants": "UPPER_SNAKE_CASE"
            },
            "structure": {
                "vue3_script_setup": True,
                "props_with_types": True,
                "jsdoc_comments": True,
                "scoped_styles": True
            },
            "quality": {
                "type_checking": True,
                "error_handling": True,
                "responsive_design": True,
                "accessibility": True
            }
        }
    
    async def generate_component(
        self, 
        component_type: str, 
        component_name: str, 
        vue_version: str,
        props: List[Dict] = None,
        features: List[str] = None
    ) -> str:
        """生成Vue组件代码"""
        
        try:
            props = props or []
            features = features or []
            
            if vue_version == "vue3":
                return await self._generate_vue3_component(
                    component_type, component_name, props, features
                )
            else:
                return await self._generate_vue2_component(
                    component_type, component_name, props, features
                )
                
        except Exception as e:
            return f"生成组件时出错：{str(e)}"
    
    async def _generate_vue3_component(
        self, 
        component_type: str, 
        component_name: str, 
        props: List[Dict],
        features: List[str]
    ) -> str:
        """生成Vue3组件"""
        
        # 组件模板映射
        component_templates = {
            "form": self._get_form_template(),
            "table": self._get_table_template(),
            "modal": self._get_modal_template(),
            "card": self._get_card_template(),
            "list": self._get_list_template()
        }
        
        base_template = component_templates.get(component_type, self._get_custom_template())
        
        # 生成props定义
        props_code = self._generate_props_code(props, "vue3")
        
        # 生成imports
        imports = self._generate_imports(component_type, features, "vue3")
        
        # 组装完整组件
        component_code = f"""<template>
{base_template}
</template>

<script setup lang="ts">
/**
 * {component_name} - {self._get_component_description(component_type)}
 * @author 前端开发团队
 * @created {datetime.now().strftime('%Y-%m-%d')}
 */

{imports}

{props_code}

{self._generate_component_logic(component_type, features)}
</script>

<style lang="scss" scoped>
{self._generate_component_styles(component_type)}
</style>"""

        return f"""
## 🎨 生成的Vue3组件代码

### 组件文件：`{component_name}.vue`

```vue
{component_code}
```

### 使用示例：

```vue
<template>
  <{self._to_kebab_case(component_name)} 
    {self._generate_usage_example(props)}
  />
</template>

<script setup>
import {component_name} from '@/components/{component_name}.vue'
</script>
```

### 组件特性：
{self._format_features_list(features)}

### 注意事项：
- ✅ 遵循团队编码规范
- ✅ 支持TypeScript类型检查
- ✅ 包含响应式设计
- ✅ 添加无障碍支持
- ✅ 完整的JSDoc注释

---
💡 **提示**：请根据实际业务需求调整组件props和样式
"""

    def _get_form_template(self) -> str:
        """获取表单组件模板"""
        return '''  <div class="custom-form">
    <form @submit.prevent="handleSubmit" class="form-container">
      <div class="form-header" v-if="title">
        <h3 class="form-title">{{ title }}</h3>
      </div>
      
      <div class="form-body">
        <div 
          v-for="field in fields" 
          :key="field.name"
          class="form-item"
          :class="{ 'form-item--error': getFieldError(field.name) }"
        >
          <label :for="field.name" class="form-label">
            {{ field.label }}
            <span v-if="field.required" class="required">*</span>
          </label>
          
          <!-- 输入框 -->
          <input
            v-if="field.type === 'input'"
            :id="field.name"
            v-model="formData[field.name]"
            :type="field.inputType || 'text'"
            :placeholder="field.placeholder"
            :disabled="field.disabled || loading"
            class="form-input"
            @blur="validateField(field.name)"
          />
          
          <!-- 选择框 -->
          <select
            v-else-if="field.type === 'select'"
            :id="field.name"
            v-model="formData[field.name]"
            :disabled="field.disabled || loading"
            class="form-select"
            @change="validateField(field.name)"
          >
            <option value="" disabled>{{ field.placeholder || '请选择' }}</option>
            <option 
              v-for="option in field.options" 
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
          
          <!-- 文本域 -->
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.name"
            v-model="formData[field.name]"
            :placeholder="field.placeholder"
            :disabled="field.disabled || loading"
            class="form-textarea"
            :rows="field.rows || 3"
            @blur="validateField(field.name)"
          />
          
          <div v-if="getFieldError(field.name)" class="field-error">
            {{ getFieldError(field.name) }}
          </div>
        </div>
      </div>
      
      <div class="form-footer">
        <button 
          type="button" 
          @click="handleCancel"
          class="btn btn--secondary"
          :disabled="loading"
        >
          {{ cancelText || '取消' }}
        </button>
        <button 
          type="submit" 
          class="btn btn--primary"
          :disabled="loading || !isFormValid"
        >
          <span v-if="loading" class="loading-spinner"></span>
          {{ submitText || '提交' }}
        </button>
      </div>
    </form>
  </div>'''

    def _get_table_template(self) -> str:
        """获取表格组件模板"""
        return '''  <div class="custom-table">
    <div class="table-header" v-if="showHeader">
      <div class="table-title">
        <h3 v-if="title">{{ title }}</h3>
        <div class="table-tools">
          <slot name="tools">
            <button 
              v-if="showRefresh"
              @click="handleRefresh"
              class="btn btn--secondary btn--sm"
              :disabled="loading"
            >
              刷新
            </button>
          </slot>
        </div>
      </div>
      
      <div class="table-filters" v-if="showFilters">
        <slot name="filters"></slot>
      </div>
    </div>
    
    <div class="table-container">
      <table class="table" :class="tableClass">
        <thead>
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="column.className"
              :style="{ width: column.width }"
            >
              <div class="th-content">
                {{ column.title }}
                <span 
                  v-if="column.sortable"
                  class="sort-icon"
                  :class="getSortClass(column.key)"
                  @click="handleSort(column.key)"
                >
                  ↕
                </span>
              </div>
            </th>
          </tr>
        </thead>
        
        <tbody>
          <tr v-if="loading" class="loading-row">
            <td :colspan="columns.length">
              <div class="loading-content">
                <span class="loading-spinner"></span>
                正在加载...
              </div>
            </td>
          </tr>
          
          <tr v-else-if="!data.length" class="empty-row">
            <td :colspan="columns.length">
              <div class="empty-content">
                <slot name="empty">
                  暂无数据
                </slot>
              </div>
            </td>
          </tr>
          
          <tr 
            v-else
            v-for="(row, index) in paginatedData" 
            :key="getRowKey(row, index)"
            class="table-row"
            :class="{ 'row--selected': isRowSelected(row) }"
            @click="handleRowClick(row, index)"
          >
            <td 
              v-for="column in columns" 
              :key="column.key"
              :class="column.className"
            >
              <slot 
                :name="column.key" 
                :row="row" 
                :index="index"
                :value="getColumnValue(row, column.key)"
              >
                {{ getColumnValue(row, column.key) }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="table-footer" v-if="showPagination && pagination.total > 0">
      <div class="pagination">
        <button 
          @click="goToPage(pagination.current - 1)"
          :disabled="pagination.current <= 1"
          class="btn btn--secondary btn--sm"
        >
          上一页
        </button>
        
        <span class="pagination-info">
          第 {{ pagination.current }} 页，共 {{ totalPages }} 页，
          总计 {{ pagination.total }} 条
        </span>
        
        <button 
          @click="goToPage(pagination.current + 1)"
          :disabled="pagination.current >= totalPages"
          class="btn btn--secondary btn--sm"
        >
          下一页
        </button>
      </div>
    </div>
  </div>'''

    def _get_modal_template(self) -> str:
        """获取弹窗组件模板"""
        return '''  <teleport to="body">
    <div 
      v-if="visible" 
      class="modal-overlay"
      :class="{ 'modal-overlay--center': centered }"
      @click="handleOverlayClick"
    >
      <div 
        class="modal"
        :class="[modalClass, sizeClass]"
        @click.stop
      >
        <div class="modal-header" v-if="showHeader">
          <div class="modal-title">
            <slot name="title">
              {{ title }}
            </slot>
          </div>
          <button 
            v-if="closable"
            @click="handleClose"
            class="modal-close"
            aria-label="关闭弹窗"
          >
            ✕
          </button>
        </div>
        
        <div class="modal-body" :class="bodyClass">
          <slot></slot>
        </div>
        
        <div class="modal-footer" v-if="showFooter">
          <slot name="footer">
            <button 
              @click="handleCancel"
              class="btn btn--secondary"
              :disabled="loading"
            >
              {{ cancelText || '取消' }}
            </button>
            <button 
              @click="handleConfirm"
              class="btn btn--primary"
              :disabled="loading"
            >
              <span v-if="loading" class="loading-spinner"></span>
              {{ confirmText || '确定' }}
            </button>
          </slot>
        </div>
      </div>
    </div>
  </teleport>'''

    def _get_card_template(self) -> str:
        """获取卡片组件模板"""
        return '''  <div class="custom-card" :class="cardClass">
    <div class="card-header" v-if="showHeader">
      <div class="card-title">
        <slot name="title">
          {{ title }}
        </slot>
      </div>
      <div class="card-extra" v-if="$slots.extra">
        <slot name="extra"></slot>
      </div>
    </div>
    
    <div class="card-body" :class="bodyClass">
      <slot></slot>
    </div>
    
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>'''

    def _get_list_template(self) -> str:
        """获取列表组件模板"""
        return '''  <div class="custom-list">
    <div class="list-header" v-if="showHeader">
      <div class="list-title">
        <slot name="title">
          {{ title }}
        </slot>
      </div>
      <div class="list-tools">
        <slot name="tools"></slot>
      </div>
    </div>
    
    <div class="list-container">
      <div v-if="loading" class="list-loading">
        <span class="loading-spinner"></span>
        正在加载...
      </div>
      
      <div v-else-if="!data.length" class="list-empty">
        <slot name="empty">
          暂无数据
        </slot>
      </div>
      
      <div v-else class="list-content">
        <div 
          v-for="(item, index) in data" 
          :key="getItemKey(item, index)"
          class="list-item"
          :class="getItemClass(item, index)"
          @click="handleItemClick(item, index)"
        >
          <slot :item="item" :index="index">
            {{ item }}
          </slot>
        </div>
      </div>
    </div>
    
    <div class="list-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>'''

    def _get_custom_template(self) -> str:
        """获取自定义组件模板"""
        return '''  <div class="custom-component">
    <div class="component-header" v-if="title">
      <h3>{{ title }}</h3>
    </div>
    
    <div class="component-content">
      <slot></slot>
    </div>
  </div>'''

    def _generate_props_code(self, props: List[Dict], vue_version: str) -> str:
        """生成props代码"""
        if not props:
            return """// Props 定义
interface Props {
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: ''
})"""
        
        # TypeScript接口定义
        interface_props = []
        default_props = []
        
        for prop in props:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'string')
            is_required = prop.get('required', False)
            default_value = prop.get('default', '')
            
            # 接口定义
            optional_mark = '' if is_required else '?'
            interface_props.append(f"  {prop_name}{optional_mark}: {prop_type}")
            
            # 默认值
            if not is_required and default_value:
                if prop_type in ['string']:
                    default_props.append(f"  {prop_name}: '{default_value}'")
                else:
                    default_props.append(f"  {prop_name}: {default_value}")
        
        interface_code = "interface Props {\n" + "\n".join(interface_props) + "\n}"
        
        if default_props:
            defaults_code = f"const props = withDefaults(defineProps<Props>(), {{\n" + ",\n".join(default_props) + "\n})"
        else:
            defaults_code = "const props = defineProps<Props>()"
        
        return f"""// Props 定义
{interface_code}

{defaults_code}"""

    def _generate_imports(self, component_type: str, features: List[str], vue_version: str) -> str:
        """生成import语句"""
        imports = ["import { ref, computed, onMounted } from 'vue'"]
        
        if component_type == "form":
            imports.append("import { reactive, watch } from 'vue'")
        elif component_type == "table":
            imports.append("import { reactive, computed } from 'vue'")
        elif component_type == "modal":
            imports.append("import { nextTick, watch } from 'vue'")
        
        if "validation" in features:
            imports.append("// import { useValidation } from '@/composables/useValidation'")
        
        return "\n".join(imports)

    def _generate_component_logic(self, component_type: str, features: List[str]) -> str:
        """生成组件逻辑代码"""
        
        if component_type == "form":
            return '''// 组件状态
const formData = reactive({})
const errors = ref({})
const loading = ref(false)

// 计算属性
const isFormValid = computed(() => {
  return Object.keys(errors.value).length === 0
})

// 方法
const validateField = (fieldName: string) => {
  // 字段验证逻辑
}

const handleSubmit = () => {
  // 表单提交逻辑
  emit('submit', formData)
}

const handleCancel = () => {
  emit('cancel')
}

const getFieldError = (fieldName: string) => {
  return errors.value[fieldName]
}

// 事件定义
const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()'''

        elif component_type == "table":
            return '''// 组件状态
const loading = ref(false)
const sortConfig = ref({ key: '', direction: 'asc' })

// 计算属性
const paginatedData = computed(() => {
  // 分页逻辑
  const start = (pagination.current - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return data.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(pagination.total / pagination.pageSize)
})

// 方法
const handleRefresh = () => {
  emit('refresh')
}

const handleSort = (key: string) => {
  // 排序逻辑
  emit('sort', { key, direction: sortConfig.value.direction })
}

const handleRowClick = (row: any, index: number) => {
  emit('row-click', { row, index })
}

const getRowKey = (row: any, index: number) => {
  return row.id || index
}

const getColumnValue = (row: any, key: string) => {
  return row[key]
}

const getSortClass = (key: string) => {
  // 排序样式类
  return ''
}

const isRowSelected = (row: any) => {
  return false
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    emit('page-change', page)
  }
}

// 事件定义
const emit = defineEmits<{
  refresh: []
  sort: [config: { key: string; direction: string }]
  'row-click': [data: { row: any; index: number }]
  'page-change': [page: number]
}>()'''

        elif component_type == "modal":
            return '''// 组件状态
const loading = ref(false)

// 计算属性
const sizeClass = computed(() => {
  return `modal--${size}`
})

// 方法
const handleClose = () => {
  emit('update:visible', false)
  emit('close')
}

const handleCancel = () => {
  emit('cancel')
  handleClose()
}

const handleConfirm = () => {
  emit('confirm')
}

const handleOverlayClick = () => {
  if (maskClosable) {
    handleClose()
  }
}

// 监听visible变化
watch(() => props.visible, (newVal) => {
  if (newVal) {
    nextTick(() => {
      // 获取焦点等操作
    })
  }
})

// 事件定义
const emit = defineEmits<{
  'update:visible': [visible: boolean]
  close: []
  cancel: []
  confirm: []
}>()'''

        else:
            return '''// 组件状态
const loading = ref(false)

// 生命周期
onMounted(() => {
  // 组件挂载后的操作
})

// 事件定义
const emit = defineEmits<{
  // 根据需要定义事件
}>()'''

    def _generate_component_styles(self, component_type: str) -> str:
        """生成组件样式"""
        base_styles = '''// 组件基础样式
.custom-component {
  // 基础样式
}'''

        if component_type == "form":
            return '''.custom-form {
  .form-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .form-item {
    display: flex;
    flex-direction: column;
    gap: 8px;

    &--error {
      .form-input,
      .form-select,
      .form-textarea {
        border-color: #ff4d4f;
      }
    }
  }

  .form-label {
    font-weight: 500;
    color: #333;

    .required {
      color: #ff4d4f;
      margin-left: 4px;
    }
  }

  .form-input,
  .form-select,
  .form-textarea {
    padding: 8px 12px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    transition: border-color 0.3s;

    &:focus {
      border-color: #1890ff;
      outline: none;
    }

    &:disabled {
      background-color: #f5f5f5;
      cursor: not-allowed;
    }
  }

  .field-error {
    color: #ff4d4f;
    font-size: 12px;
  }

  .form-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
  }
}'''

        elif component_type == "table":
            return '''.custom-table {
  .table-container {
    overflow-x: auto;
  }

  .table {
    width: 100%;
    border-collapse: collapse;
    
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #f0f0f0;
    }

    th {
      background-color: #fafafa;
      font-weight: 500;
      
      .th-content {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .sort-icon {
        cursor: pointer;
        opacity: 0.5;
        
        &:hover {
          opacity: 1;
        }
      }
    }

    .table-row {
      &:hover {
        background-color: #f5f5f5;
      }

      &.row--selected {
        background-color: #e6f7ff;
      }
    }
  }

  .loading-content,
  .empty-content {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    color: #999;
  }

  .pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-top: 16px;
  }
}'''

        elif component_type == "modal":
            return '''.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 100px 16px 16px;
  z-index: 1000;

  &.modal-overlay--center {
    align-items: center;
    padding: 16px;
  }
}

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  &.modal--small {
    width: 400px;
  }

  &.modal--medium {
    width: 600px;
  }

  &.modal--large {
    width: 800px;
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 1px solid #f0f0f0;

    .modal-title {
      font-size: 16px;
      font-weight: 500;
    }

    .modal-close {
      border: none;
      background: none;
      font-size: 18px;
      cursor: pointer;
      padding: 4px;
      color: #999;

      &:hover {
        color: #333;
      }
    }
  }

  .modal-body {
    padding: 24px;
    flex: 1;
    overflow-y: auto;
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid #f0f0f0;
  }
}'''

        else:
            return base_styles

    async def find_reusable_components(
        self, 
        project_path: str, 
        component_type: Optional[str] = None,
        search_keywords: List[str] = None
    ) -> str:
        """在项目中查找可复用的组件 - 使用智能语义匹配"""
        
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return f"项目路径不存在：{project_path}"
            
            # 搜索组件文件
            component_files = self._find_component_files(project_dir)
            
            if not component_files:
                return "项目中未找到Vue组件文件"
            
            # 分析组件
            components_info = []
            for file_path in component_files:
                component_info = self._analyze_component_file(file_path)
                if component_info:
                    components_info.append(component_info)
            
            # 使用智能匹配算法
            filtered_components = self._intelligent_component_filter(
                components_info, component_type, search_keywords
            )
            
            if not filtered_components:
                # 提供搜索建议
                suggestions = self._generate_search_suggestions(components_info, search_keywords)
                return f"未找到匹配的组件。{suggestions}"
            
            # 生成结果报告
            return self._generate_component_report(filtered_components)
            
        except Exception as e:
            return f"查找组件时出错：{str(e)}"
    
    def _find_component_files(self, project_dir: Path) -> List[Path]:
        """查找项目中的Vue组件文件"""
        component_files = []
        
        # 扩展的组件目录搜索
        search_dirs = [
            "src/components",
            "src/views", 
            "src/pages",
            "components",
            "views",
            "pages",
            "src",  # 直接搜索src目录
            "."     # 搜索整个项目根目录
        ]
        
        # 支持更多文件类型
        file_patterns = ["*.vue", "*.jsx", "*.tsx", "*.js", "*.ts"]
        
        for search_dir in search_dirs:
            component_dir = project_dir / search_dir
            if component_dir.exists():
                # 递归查找多种组件文件
                for pattern in file_patterns:
                    files = list(component_dir.rglob(pattern))
                    component_files.extend(files)
        
        # 去重
        component_files = list(set(component_files))
        
        # 输出调试信息
        print(f"🔍 在 {project_dir} 中找到 {len(component_files)} 个组件文件")
        for file in component_files[:5]:  # 只显示前5个作为示例
            print(f"  - {file}")
        
        return component_files
    
    def _analyze_component_file(self, file_path: Path) -> Optional[Dict]:
        """分析组件文件，提取组件信息"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 优化组件名称提取 - 使用目录名而不是文件名
            component_name = self._extract_component_name(file_path)
            
            # 提取组件信息
            props = self._extract_props(content)
            events = self._extract_events(content)
            slots = self._extract_slots(content)
            description = self._extract_description(content)
            
            # 分析组件功能特性
            functional_type = self._analyze_component_functionality(content, props, events, component_name, file_path)
            
            component_info = {
                "name": component_name,
                "path": str(file_path),
                "props": props,
                "events": events,
                "slots": slots,
                "description": description,
                "type": functional_type,
                "is_wrapper": self._is_wrapper_component(content, file_path),
                "dependency_type": self._get_dependency_type(file_path),
                "features": self._extract_component_features(content, props, events)
            }
            
            return component_info
            
        except Exception as e:
            print(f"分析组件文件失败 {file_path}: {e}")
            return None
    
    def _extract_component_name(self, file_path: Path) -> str:
        """提取组件名称 - 优先使用目录名"""
        # 如果文件名是 index.vue，使用父目录名
        if file_path.name == 'index.vue' or file_path.name == 'index.js' or file_path.name == 'index.tsx':
            parent_dir = file_path.parent.name
            # 转换为 PascalCase
            return ''.join(word.capitalize() for word in parent_dir.replace('-', '_').split('_'))
        else:
            # 使用文件名（去掉扩展名）
            name = file_path.stem
            # 处理常见的组件命名模式
            if name.lower().endswith('component'):
                name = name[:-9]  # 移除 'component' 后缀
            return name

    def _is_wrapper_component(self, content: str, file_path: Path) -> bool:
        """判断是否为二次封装组件"""
        content_lower = content.lower()
        
        # 检查是否引入了第三方UI库组件
        ui_library_patterns = [
            'el-', 'a-', 'van-', 'n-',  # Element, Ant Design, Vant, Naive UI
            'from \'element', 'from \'antd', 'from \'vant',
            'import.*element', 'import.*antd', 'import.*vant'
        ]
        
        has_ui_import = any(pattern in content_lower for pattern in ui_library_patterns)
        
        # 检查目录结构是否表明是二次封装
        path_str = str(file_path).lower()
        wrapper_indicators = ['fb', 'fs', 'custom', 'base', 'my']
        has_wrapper_prefix = any(indicator in path_str for indicator in wrapper_indicators)
        
        return has_ui_import or has_wrapper_prefix

    def _get_dependency_type(self, file_path: Path) -> str:
        """获取依赖类型"""
        path_str = str(file_path)
        if 'node_modules' in path_str:
            return 'third_party'
        elif any(prefix in path_str.lower() for prefix in ['src/components', 'components']):
            return 'project'
        else:
            return 'view'
    
    def _extract_props(self, content: str) -> List[Dict]:
        """提取组件Props"""
        props = []
        
        # 匹配defineProps的内容
        props_pattern = r'defineProps<([^>]+)>'
        match = re.search(props_pattern, content)
        
        if match:
            props_interface = match.group(1)
            # 简单解析props（实际应该用更复杂的AST解析）
            prop_lines = props_interface.split('\n')
            for line in prop_lines:
                line = line.strip()
                if ':' in line and not line.startswith('//'):
                    prop_match = re.match(r'(\w+)\??\s*:\s*(.+)', line)
                    if prop_match:
                        props.append({
                            "name": prop_match.group(1),
                            "type": prop_match.group(2).rstrip(','),
                            "required": '?' not in line
                        })
        
        return props
    
    def _extract_events(self, content: str) -> List[str]:
        """提取组件事件"""
        events = []
        
        # 匹配defineEmits的内容
        events_pattern = r'defineEmits<\{([^}]+)\}>'
        match = re.search(events_pattern, content)
        
        if match:
            events_content = match.group(1)
            event_lines = events_content.split('\n')
            for line in event_lines:
                line = line.strip()
                if ':' in line and not line.startswith('//'):
                    event_match = re.match(r'(\w+|\'\w+\'|"\w+")', line)
                    if event_match:
                        event_name = event_match.group(1).strip('\'"')
                        events.append(event_name)
        
        return events
    
    def _extract_slots(self, content: str) -> List[str]:
        """提取组件插槽"""
        slots = []
        
        # 匹配slot标签
        slot_pattern = r'<slot\s+name=["\']([^"\']+)["\']'
        matches = re.findall(slot_pattern, content)
        slots.extend(matches)
        
        # 检查默认插槽
        if '<slot' in content and 'name=' not in content:
            slots.append('default')
        
        return list(set(slots))
    
    def _extract_description(self, content: str) -> str:
        """提取组件描述"""
        # 从注释中提取描述
        comment_pattern = r'/\*\*\s*\n\s*\*\s*([^\n]+)'
        match = re.search(comment_pattern, content)
        
        if match:
            return match.group(1).strip()
        
        return ""
    
    def _analyze_component_functionality(self, content: str, props: List[Dict], events: List[str], name: str, file_path: Path) -> str:
        """通过内容、props和events分析组件功能类型"""
        content_lower = content.lower()
        name_lower = name.lower()
        path_lower = str(file_path).lower()
        
        # 分析props来判断组件功能
        prop_names = [prop.get('name', '').lower() for prop in props]
        prop_text = ' '.join(prop_names)
        
        # 分析events来判断组件功能
        event_text = ' '.join(events).lower()
        
        # 合并所有分析文本
        all_analysis_text = f"{content_lower} {name_lower} {path_lower} {prop_text} {event_text}"
        
        # 增强的组件特征检测
        button_indicators = [
            'click', 'onclick', 'button', 'btn', 'common', 'base', 'action',
            'submit', 'confirm', 'cancel', 'type', 'size', 'loading', 'disabled'
        ]
        
        checkbox_indicators = [
            'checked', 'ischecked', 'value', 'modelvalue', 'selected', 'isradio',
            'change', 'input', 'update:modelvalue', 'checkbox', 'radio'
        ]
        
        form_indicators = [
            'form', 'validate', 'rules', 'label', 'required', 'placeholder'
        ]
        
        table_indicators = [
            'columns', 'data', 'rows', 'pagination', 'sort', 'filter'
        ]
        
        modal_indicators = [
            'visible', 'open', 'show', 'close', 'cancel', 'confirm'
        ]
        
        # 检查各类组件特征
        button_score = sum(1 for indicator in button_indicators if indicator in all_analysis_text)
        checkbox_score = sum(1 for indicator in checkbox_indicators if indicator in all_analysis_text)
        form_score = sum(1 for indicator in form_indicators if indicator in all_analysis_text)
        table_score = sum(1 for indicator in table_indicators if indicator in all_analysis_text)
        modal_score = sum(1 for indicator in modal_indicators if indicator in all_analysis_text)
        
        # 特殊检查：如果组件名包含特定词汇，加权
        if any(word in name_lower for word in ['button', 'btn', 'common']):
            button_score += 3
        if any(word in name_lower for word in ['radio', 'check', 'select', 'option', 'choose']):
            checkbox_score += 2
        
        # 特殊检查：如果组件支持特定模式
        if any(prop.get('name', '').lower() in ['isradio', 'multiple', 'mode'] for prop in props):
            checkbox_score += 1
        if any(prop.get('name', '').lower() in ['type', 'size', 'loading'] for prop in props):
            button_score += 1
        
        # 根据得分判断组件类型
        scores = {
            'button': button_score,
            'checkbox': checkbox_score,
            'form': form_score,
            'table': table_score,
            'modal': modal_score
        }
        
        # 选择得分最高的类型
        max_score = max(scores.values())
        if max_score >= 2:  # 至少要有2个特征匹配
            for comp_type, score in scores.items():
                if score == max_score:
                    return comp_type
        
        # 回退到原始的猜测逻辑
        return self._guess_component_type(name, content, file_path)
    
    def _extract_component_features(self, content: str, props: List[Dict], events: List[str]) -> List[str]:
        """提取组件功能特性"""
        features = []
        content_lower = content.lower()
        
        # 检查常见功能特性
        if any(prop.get('name', '').lower() in ['disabled', 'readonly'] for prop in props):
            features.append('禁用状态')
        
        if any(prop.get('name', '').lower() in ['size', 'large', 'small'] for prop in props):
            features.append('多尺寸')
            
        if any(prop.get('name', '').lower() in ['loading', 'pending'] for prop in props):
            features.append('加载状态')
            
        if any(event in ['change', 'input', 'update:modelValue'] for event in events):
            features.append('双向绑定')
            
        if 'v-model' in content_lower:
            features.append('响应式数据')
            
        if any(prop.get('name', '').lower() in ['options', 'items', 'data'] for prop in props):
            features.append('数据驱动')
        
        return features
    
    def _guess_component_type(self, name: str, content: str, file_path: Path) -> str:
        """根据组件名称、内容和路径猜测组件类型"""
        name_lower = name.lower()
        content_lower = content.lower()
        path_lower = str(file_path).lower()
        
        # 扩展的组件类型识别，包含路径信息
        modal_keywords = ['modal', 'dialog', 'popup', 'drawer', '弹窗', '对话框', 'fb', 'overlay']
        table_keywords = ['table', 'grid', 'list', 'datagrid', '表格', '列表']
        form_keywords = ['form', 'input', 'edit', 'create', '表单', '编辑', '新增']
        card_keywords = ['card', 'panel', 'box', '卡片', '面板']
        tag_keywords = ['tag', 'badge', 'label', 'chip', '标签', '徽章']
        # 新增选择类组件关键词
        checkbox_keywords = ['checkbox', 'radio', 'check', 'select', 'option', 'choose', 'toggle', 'switch', '选择', '勾选', '单选', '多选', '复选']
        
        # 检查名称、内容和路径
        all_text = f"{name_lower} {content_lower} {path_lower}"
        
        # 优先检查选择类组件
        if any(keyword in all_text for keyword in checkbox_keywords):
            # 进一步判断具体类型
            if any(word in all_text for word in ['radio', '单选']):
                return 'radio'
            elif any(word in all_text for word in ['checkbox', 'check', '复选', '多选']):
                return 'checkbox'
            else:
                return 'select'  # 通用选择组件
        elif any(keyword in all_text for keyword in tag_keywords):
            return 'tag'
        elif any(keyword in all_text for keyword in modal_keywords):
            return 'modal'
        elif any(keyword in all_text for keyword in table_keywords):
            return 'table'
        elif any(keyword in all_text for keyword in form_keywords):
            return 'form'
        elif any(keyword in all_text for keyword in card_keywords):
            return 'card'
        elif any(keyword in content_lower for keyword in ['<el-dialog', '<a-modal', 'v-model:visible', 'v-model:open']):
            return 'modal'
        elif any(keyword in content_lower for keyword in ['<el-table', '<a-table', 'pagination']):
            return 'table'
        elif any(keyword in content_lower for keyword in ['<el-form', '<a-form', 'form-item']):
            return 'form'
        # 检查选择类UI组件
        elif any(keyword in content_lower for keyword in ['<el-checkbox', '<a-checkbox', '<el-radio', '<a-radio', 'v-model:checked']):
            return 'checkbox'
        else:
            return 'custom'
    
    def _intelligent_component_filter(
        self, 
        components: List[Dict], 
        component_type: Optional[str],
        keywords: Optional[List[str]]
    ) -> List[Dict]:
        """智能组件过滤 - 使用语义匹配和功能分析"""
        
        if not keywords and not component_type:
            return components
        
        scored_components = []
        
        for component in components:
            score = self._calculate_component_similarity(component, component_type, keywords)
            if score > 0:
                scored_components.append((component, score))
        
        # 按相似度排序
        scored_components.sort(key=lambda x: x[1], reverse=True)
        
        # 降低相似度阈值，特别是对button类组件
        threshold = 0.15  # 从0.3降低到0.15
        if keywords and any('button' in kw.lower() or 'btn' in kw.lower() for kw in keywords):
            threshold = 0.1  # button组件更低阈值
        
        filtered = [comp for comp, score in scored_components if score >= threshold]
        
        # 如果没找到任何组件，进一步降低阈值重试
        if not filtered and scored_components:
            emergency_threshold = 0.05
            filtered = [comp for comp, score in scored_components if score >= emergency_threshold]
        
        return filtered
    
    def _calculate_component_similarity(
        self, 
        component: Dict, 
        target_type: Optional[str], 
        keywords: Optional[List[str]]
    ) -> float:
        """计算组件与搜索条件的相似度"""
        
        total_score = 0.0
        max_possible_score = 0.0
        
        # 构建组件的全文本描述
        component_text = self._build_component_full_text(component)
        
        # 1. 组件类型匹配 (权重: 0.4)
        if target_type:
            type_score = self._calculate_type_similarity(component, target_type)
            total_score += type_score * 0.4
            max_possible_score += 0.4
        
        # 2. 关键词匹配 (权重: 0.3)
        if keywords:
            keyword_score = self._calculate_keyword_similarity(component_text, keywords)
            total_score += keyword_score * 0.3
            max_possible_score += 0.3
        
        # 3. 功能相似度 (权重: 0.2)
        if keywords:
            function_score = self._calculate_function_similarity(component, keywords)
            total_score += function_score * 0.2
            max_possible_score += 0.2
        
        # 4. 名称相似度 (权重: 0.1)
        if keywords:
            name_score = self._calculate_name_similarity(component['name'], keywords)
            total_score += name_score * 0.1
            max_possible_score += 0.1
        
        return total_score / max_possible_score if max_possible_score > 0 else 0.0
    
    def _build_component_full_text(self, component: Dict) -> str:
        """构建组件的完整文本描述"""
        texts = [
            component.get('name', ''),
            component.get('description', ''),
            component.get('path', ''),
            ' '.join([prop.get('name', '') for prop in component.get('props', [])]),
            ' '.join(component.get('events', [])),
            ' '.join(component.get('slots', [])),
            ' '.join(component.get('features', []))
        ]
        return ' '.join(texts).lower()
    
    def _calculate_type_similarity(self, component: Dict, target_type: str) -> float:
        """计算类型相似度"""
        comp_type = component.get('type', '')
        
        # 直接匹配
        if comp_type == target_type:
            return 1.0
        
        # 语义相似度映射
        similarity_map = {
            'checkbox': ['radio', 'select', 'toggle', 'switch'],
            'radio': ['checkbox', 'select', 'option'],
            'select': ['checkbox', 'radio', 'dropdown', 'picker'],
            'form': ['input', 'field', 'control'],
            'table': ['grid', 'list', 'dataview'],
            'modal': ['dialog', 'popup', 'overlay'],
            'button': ['btn', 'link', 'action', 'common', 'base'],
            'input': ['field', 'control', 'form']
        }
        
        # 检查相似类型
        related_types = similarity_map.get(target_type, [])
        if comp_type in related_types:
            return 0.7
        
        # 检查反向映射
        for main_type, related in similarity_map.items():
            if main_type == comp_type and target_type in related:
                return 0.7
        
        # 特殊处理：检查组件名称中是否包含目标类型的同义词
        comp_name = component.get('name', '').lower()
        comp_path = component.get('path', '').lower()
        
        if target_type == 'button':
            button_indicators = ['button', 'btn', 'common', 'base', 'action', 'click']
            if any(indicator in comp_name or indicator in comp_path for indicator in button_indicators):
                return 0.6
        
        return 0.0
    
    def _calculate_keyword_similarity(self, component_text: str, keywords: List[str]) -> float:
        """计算关键词相似度"""
        if not keywords:
            return 0.0
        
        total_matches = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # 精确匹配
            if keyword_lower in component_text:
                total_matches += 1.0
                continue
            
            # 模糊匹配 (编辑距离)
            fuzzy_score = self._fuzzy_match(keyword_lower, component_text)
            total_matches += fuzzy_score
        
        return min(total_matches / len(keywords), 1.0)
    
    def _calculate_function_similarity(self, component: Dict, keywords: List[str]) -> float:
        """基于功能分析计算相似度"""
        if not keywords:
            return 0.0
        
        # 功能意图映射
        intent_map = {
            'checkbox': ['选择', '勾选', '多选', '选中', '确认'],
            'radio': ['单选', '选择', '切换'],
            'select': ['选择', '下拉', '筛选', '挑选'],
            'input': ['输入', '填写', '录入'],
            'upload': ['上传', '选择文件', '导入'],
            'date': ['日期', '时间', '选择日期'],
            'search': ['搜索', '查找', '筛选']
        }
        
        score = 0.0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for intent, descriptions in intent_map.items():
                if any(desc in keyword_lower for desc in descriptions):
                    # 检查组件是否支持这种功能
                    if self._component_supports_intent(component, intent):
                        score += 0.8
                        break
        
        return min(score / len(keywords), 1.0) if keywords else 0.0
    
    def _component_supports_intent(self, component: Dict, intent: str) -> bool:
        """检查组件是否支持特定功能意图"""
        component_text = self._build_component_full_text(component)
        
        intent_indicators = {
            'checkbox': ['checked', 'value', 'modelvalue', 'selected', 'change'],
            'radio': ['checked', 'value', 'modelvalue', 'isradio'],
            'select': ['options', 'value', 'modelvalue', 'change'],
            'input': ['value', 'modelvalue', 'placeholder', 'input'],
            'upload': ['file', 'upload', 'accept', 'multiple'],
            'date': ['date', 'time', 'picker', 'calendar'],
            'search': ['search', 'filter', 'query']
        }
        
        indicators = intent_indicators.get(intent, [])
        return any(indicator in component_text for indicator in indicators)
    
    def _calculate_name_similarity(self, component_name: str, keywords: List[str]) -> float:
        """计算名称相似度"""
        if not keywords:
            return 0.0
        
        name_lower = component_name.lower()
        max_similarity = 0.0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # 完全匹配
            if keyword_lower == name_lower:
                max_similarity = max(max_similarity, 1.0)
                continue
            
            # 包含匹配
            if keyword_lower in name_lower or name_lower in keyword_lower:
                max_similarity = max(max_similarity, 0.8)
                continue
            
            # 编辑距离相似度
            similarity = self._string_similarity(keyword_lower, name_lower)
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _fuzzy_match(self, keyword: str, text: str) -> float:
        """模糊匹配算法"""
        # 简单的模糊匹配实现
        words = text.split()
        best_match = 0.0
        
        for word in words:
            similarity = self._string_similarity(keyword, word)
            best_match = max(best_match, similarity)
        
        return best_match
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """计算字符串相似度 (基于编辑距离)"""
        if not s1 or not s2:
            return 0.0
        
        # 简化的相似度算法
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        
        # 计算公共子序列长度
        common = 0
        for i, char in enumerate(s1):
            if i < len(s2) and char == s2[i]:
                common += 1
        
        return common / max_len
    
    def _generate_search_suggestions(self, all_components: List[Dict], keywords: Optional[List[str]]) -> str:
        """生成搜索建议"""
        if not all_components:
            return ""
        
        # 统计可用的组件类型
        available_types = {}
        for comp in all_components:
            comp_type = comp.get('type', 'unknown')
            available_types[comp_type] = available_types.get(comp_type, 0) + 1
        
        # 生成建议
        suggestions = []
        
        if keywords:
            # 基于关键词提供相似组件建议
            similar_comps = []
            for comp in all_components[:5]:  # 只看前5个
                name = comp.get('name', '')
                if any(self._string_similarity(kw.lower(), name.lower()) > 0.3 for kw in keywords):
                    similar_comps.append(name)
            
            if similar_comps:
                suggestions.append(f"可能相关的组件：{', '.join(similar_comps)}")
        
        # 提供类型建议
        popular_types = sorted(available_types.items(), key=lambda x: x[1], reverse=True)[:3]
        if popular_types:
            type_list = [f"{t[0]}({t[1]}个)" for t in popular_types]
            suggestions.append(f"项目中主要组件类型：{', '.join(type_list)}")
        
        return " ".join(suggestions) if suggestions else "建议检查搜索关键词或组件类型。"
    
    def _generate_component_report(self, components: List[Dict]) -> str:
        """生成组件查找报告"""
        if not components:
            return "未找到匹配的组件"
        
        report = f"## 🔍 找到 {len(components)} 个可复用组件\n\n"
        
        for i, component in enumerate(components, 1):
            name = component['name']
            type_str = component['type']
            is_wrapper = component.get('is_wrapper', False)
            dep_type = component.get('dependency_type', 'unknown')
            features = component.get('features', [])
            
            # 添加组件类型标识
            type_badge = f"**类型**: {type_str}"
            if is_wrapper:
                type_badge += " (二次封装)"
            if dep_type == 'third_party':
                type_badge += " (第三方)"
            
            report += f"### {i}. {name}\n\n"
            report += f"{type_badge}\n"
            report += f"**路径**: `{component['path']}`\n"
            
            if component['description']:
                report += f"**描述**: {component['description']}\n"
            
            # 显示功能特性
            if features:
                report += f"**功能特性**: {', '.join(features)}\n"
            
            if component['props']:
                report += f"**Props**: \n"
                for prop in component['props']:
                    required = "必填" if prop['required'] else "可选"
                    report += f"- `{prop['name']}`: {prop['type']} ({required})\n"
            
            if component['events']:
                report += f"**事件**: {', '.join(component['events'])}\n"
            
            if component['slots']:
                report += f"**插槽**: {', '.join(component['slots'])}\n"
            
            # 生成使用示例
            report += f"\n**使用示例**:\n```vue\n"
            report += f"<template>\n  <{self._to_kebab_case(name)}"
            
            if component['props']:
                report += f"\n    {self._generate_props_example(component['props'])}"
            
            report += f"\n  />\n</template>\n\n"
            report += f"<script setup>\n"
            report += f"import {name} from '{component['path']}'\n"
            report += f"</script>\n```\n\n"
            
            report += "---\n\n"
        
        return report
    
    def _generate_props_example(self, props: List[Dict]) -> str:
        """生成props使用示例"""
        examples = []
        for prop in props[:3]:  # 只显示前3个props作为示例
            if prop['type'] == 'string':
                examples.append(f'{prop["name"]}="示例值"')
            elif prop['type'] == 'boolean':
                examples.append(f':{prop["name"]}="true"')
            elif prop['type'] == 'number':
                examples.append(f':{prop["name"]}="100"')
            else:
                examples.append(f':{prop["name"]}="data"')
        
        return '\n    '.join(examples)
    
    def _to_kebab_case(self, text: str) -> str:
        """将PascalCase转换为kebab-case"""
        return re.sub(r'([A-Z])', r'-\1', text).lower().lstrip('-')
    
    def _format_features_list(self, features: List[str]) -> str:
        """格式化功能特性列表"""
        if not features:
            return "- 基础功能"
        
        return "\n".join([f"- {feature}" for feature in features])
    
    def _generate_usage_example(self, props: List[Dict]) -> str:
        """生成使用示例的props"""
        if not props:
            return 'title="示例标题"'
        
        examples = []
        for prop in props[:2]:  # 只显示前2个作为示例
            name = prop.get('name', 'prop')
            prop_type = prop.get('type', 'string')
            
            if prop_type == 'string':
                examples.append(f'{name}="示例值"')
            elif prop_type == 'boolean':
                examples.append(f':{name}="true"')
            else:
                examples.append(f':{name}="data"')
        
        return '\n    '.join(examples)
    
    def _get_component_description(self, component_type: str) -> str:
        """获取组件类型描述"""
        descriptions = {
            "form": "表单组件，支持多种表单控件和验证",
            "table": "表格组件，支持排序、分页和自定义列",
            "modal": "弹窗组件，支持多种尺寸和自定义内容",
            "card": "卡片组件，用于内容展示",
            "list": "列表组件，支持自定义列表项",
            "custom": "自定义组件"
        }
        
        return descriptions.get(component_type, "通用组件")
    
    def generate_concise_commit_message(self, files: List[str], description: str) -> str:
        """生成简洁的commit信息"""
        # 分析文件类型来确定commit类型
        commit_type = self._determine_commit_type(files)
        
        # 简化描述，确保不超过50字符
        concise_desc = self._simplify_description(description)
        
        return f"{commit_type}: {concise_desc}"
    
    def _determine_commit_type(self, files: List[str]) -> str:
        """根据文件变化确定commit类型"""
        file_str = " ".join(files)
        
        if any(pattern in file_str for pattern in ['.md', 'README', 'docs/']):
            return 'docs'
        elif any(pattern in file_str for pattern in ['.gitignore', 'config', 'requirements.txt']):
            return 'config'
        elif any(pattern in file_str for pattern in ['test_', 'tests/', '_test.py']):
            return 'test'
        elif any(pattern in file_str for pattern in ['fix', 'bug', 'error']):
            return 'fix'
        elif any(pattern in file_str for pattern in ['refactor', 'optimize', 'improve']):
            return 'refactor'
        else:
            return 'feat'
    
    def _simplify_description(self, description: str) -> str:
        """简化描述，确保简洁明了"""
        # 移除详细信息，保留核心描述
        if '- ' in description:
            # 如果包含列表，只取第一部分
            main_desc = description.split('- ')[0].strip()
        else:
            main_desc = description
        
        # 限制长度
        if len(main_desc) > 30:
            main_desc = main_desc[:27] + "..."
        
        return main_desc 