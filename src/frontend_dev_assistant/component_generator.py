"""
Vue组件生成器模块
负责生成符合团队规范的Vue组件代码，并支持查找项目中的可复用组件
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)

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

    async def _generate_vue2_component(
        self, 
        component_type: str, 
        component_name: str, 
        props: List[Dict],
        features: List[str]
    ) -> str:
        """生成Vue2组件"""
        
        # 组件模板映射
        component_templates = {
            "form": self._get_form_template(),
            "table": self._get_table_template(),
            "modal": self._get_modal_template(),
            "card": self._get_card_template(),
            "list": self._get_list_template()
        }
        
        # 为ThirdPartyAuth组件使用专门的模板
        if component_name == "ThirdPartyAuth":
            base_template = self._get_third_party_auth_template()
        else:
            base_template = component_templates.get(component_type, self._get_custom_template())
        
        # 生成Vue2的props定义
        props_code = self._generate_vue2_props_code(props)
        
        # 生成Vue2的组件逻辑
        component_logic = self._generate_vue2_component_logic(component_type, features)
        
        # 组装完整组件
        component_code = f"""<template>
{base_template}
</template>

<script>
/**
 * {component_name} - {self._get_component_description(component_type)}
 * @author 前端开发团队
 * @created {datetime.now().strftime('%Y-%m-%d')}
 */

export default {{
  name: '{component_name}',
  
{props_code}
  
{component_logic}
}}
</script>

<style lang="scss" scoped>
{self._generate_component_styles(component_type)}
</style>"""

        return f"""
## 🎨 生成的Vue2组件代码

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

<script>
import {component_name} from '@/components/{component_name}.vue'

export default {{
  components: {{
    {component_name}
  }}
}}
</script>
```

### 组件特性：
{self._format_features_list(features)}

### 注意事项：
- ✅ 遵循团队编码规范
- ✅ 支持Vue2选项式API
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
    <!-- 自定义组件内容 -->
    <div class="component-header" v-if="title">
      <h3>{{ title }}</h3>
    </div>
    
    <div class="component-body">
      <slot>
        <!-- 默认内容 -->
        <p>这是一个自定义组件</p>
      </slot>
    </div>
  </div>'''

    def _get_third_party_auth_template(self) -> str:
        """获取第三方授权组件模板"""
        return '''  <div class="third-party-auth" :class="['auth-type--' + authType, authStatusClass]">
    <!-- 授权状态展示 -->
    <div class="auth-status">
      <div class="status-icon" :class="authStatusClass">
        <i v-if="isAuthorized" class="icon-success">✓</i>
        <i v-else-if="errorMessage" class="icon-error">✗</i>
        <i v-else class="icon-pending">◎</i>
      </div>
      
      <div class="status-info">
        <h4 class="auth-title">{{ getAuthTitle() }}</h4>
        <p class="auth-desc" v-if="!isAuthorized">{{ getAuthDescription() }}</p>
        <p class="auth-success" v-if="isAuthorized">授权成功，可以正常使用相关功能</p>
        <p class="auth-error" v-if="errorMessage">{{ errorMessage }}</p>
      </div>
    </div>
    
    <!-- 进度指示 -->
    <div v-if="loading" class="auth-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: authProgress + '%' }"></div>
      </div>
      <p class="progress-text">授权进度: {{ authProgress }}%</p>
    </div>
    
    <!-- 授权按钮 -->
    <div class="auth-actions">
      <button 
        class="auth-btn"
        :class="{ 
          'auth-btn--loading': loading,
          'auth-btn--success': isAuthorized,
          'auth-btn--error': errorMessage
        }"
        :disabled="loading"
        @click="handleAuth"
        v-if="!isAuthorized"
      >
        <span v-if="loading" class="loading-spinner"></span>
        {{ authButtonText }}
      </button>
      
      <button 
        v-if="errorMessage && !loading"
        class="retry-btn"
        @click="retry"
      >
        重试
      </button>
      
      <div v-if="isAuthorized" class="auth-success-info">
        <span class="success-text">{{ authButtonText }}</span>
        <button class="reauth-btn" @click="reauthorize">重新授权</button>
      </div>
    </div>
    
    <!-- 帮助信息 -->
    <div class="auth-help" v-if="!isAuthorized && !loading">
      <p class="help-text">
        <i class="help-icon">?</i>
        点击授权按钮将跳转到{{ getAuthProviderName() }}完成授权
      </p>
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
        
        base_styles = """.component {
  padding: 16px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  
  &:hover {
    opacity: 0.8;
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  &.btn--primary {
    background: #1890ff;
    color: white;
  }
  
  &.btn--secondary {
    background: #f5f5f5;
    color: #666;
  }
}"""

        if component_type == "form":
            return '''.custom-form {
  .form-container {
    max-width: 500px;
    margin: 0 auto;
  }

  .form-header {
    margin-bottom: 24px;
    
    .form-title {
      font-size: 18px;
      font-weight: 500;
      color: #333;
      margin: 0;
    }
  }

  .form-item {
    margin-bottom: 16px;
    
    &.form-item--error {
      .form-input,
      .form-select,
      .form-textarea {
        border-color: #ff4d4f;
      }
    }
  }

  .form-label {
    display: block;
    margin-bottom: 8px;
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
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    font-size: 14px;
    transition: border-color 0.3s;
    
    &:focus {
      outline: none;
      border-color: #1890ff;
      box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    }
    
    &:disabled {
      background-color: #f5f5f5;
      cursor: not-allowed;
    }
  }

  .field-error {
    color: #ff4d4f;
    font-size: 12px;
    margin-top: 4px;
  }

  .form-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid #f0f0f0;
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
            return self._format_component_suggestions(filtered_components)
            
        except Exception as e:
            return f"查找组件时出错：{str(e)}"
    
    def _find_component_files(self, project_dir: Path) -> List[Path]:
        """查找项目中的Vue组件文件"""
        component_files = []
        
        # 排除目录列表
        exclude_dirs = {
            'node_modules', '.git', 'dist', 'build', '.vscode', '.idea', 
            'coverage', 'test', 'tests', '__pycache__', '.pytest_cache',
            '.next', '.nuxt', 'out', 'public', 'static'
        }
        
        # 优先搜索的组件目录
        priority_dirs = [
            "src/components",
            "src/views", 
            "src/pages",
            "components",
            "views", 
            "pages"
        ]
        
        # 次级搜索目录
        secondary_dirs = [
            "src",
            "app",
            "lib"
        ]
        
        # 支持的组件文件类型
        component_patterns = ["*.vue", "*.jsx", "*.tsx"]
        
        def should_exclude_path(path: Path) -> bool:
            """检查路径是否应该被排除"""
            path_parts = path.parts
            return any(exclude_dir in path_parts for exclude_dir in exclude_dirs)
        
        # 首先搜索优先目录
        for search_dir in priority_dirs:
            component_dir = project_dir / search_dir
            if component_dir.exists() and not should_exclude_path(component_dir):
                for pattern in component_patterns:
                    files = list(component_dir.rglob(pattern))
                    # 过滤掉被排除的路径
                    files = [f for f in files if not should_exclude_path(f)]
                    component_files.extend(files)
        
        # 如果优先目录没找到足够组件，搜索次级目录
        if len(component_files) < 5:
            for search_dir in secondary_dirs:
                component_dir = project_dir / search_dir
                if component_dir.exists() and not should_exclude_path(component_dir):
                    for pattern in component_patterns:
                        files = list(component_dir.rglob(pattern))
                        files = [f for f in files if not should_exclude_path(f)]
                        component_files.extend(files)
        
        # 去重
        component_files = list(set(component_files))
        
        # 输出调试信息
        print(f"🔍 在 {project_dir} 中找到 {len(component_files)} 个组件文件")
        for file in component_files[:5]:  # 只显示前5个作为示例
            print(f"  - {file}")
        
        return component_files
    
    def _analyze_component_file(self, file_path: Path) -> Optional[Dict]:
        """分析单个组件文件"""
        # 使用新的改进后的分析方法
        return self._analyze_single_component(file_path)
    
    def _is_valid_ui_component(self, content: str, file_path: Path) -> bool:
        """检查文件是否为有效的UI组件"""
        content_lower = content.lower()
        file_name = file_path.name.lower()
        
        # 排除明显的非组件文件
        exclude_patterns = [
            'interop', 'helper', 'util', 'config', 'constant', 'type', 'interface',
            '.d.ts', '.spec.', '.test.', 'babel', 'runtime', 'polyfill',
            'webpack', 'rollup', 'build', 'demo.spec', 'index.spec'
        ]
        
        if any(pattern in file_name for pattern in exclude_patterns):
            return False
        
        # Vue组件必须包含template或render
        if file_path.suffix == '.vue':
            if '<template>' in content_lower or 'render' in content_lower:
                return True
            return False
        
        # React组件检查
        if file_path.suffix in ['.jsx', '.tsx']:
            react_indicators = [
                'react', 'jsx', 'component', 'return (', 'export default',
                'usestate', 'useeffect', 'props', 'render'
            ]
            
            if any(indicator in content_lower for indicator in react_indicators):
                # 确保不是工具函数
                utility_indicators = [
                    'module.exports = ', 'export function', 'export const', 
                    'export { default }', 'interopRequire', 'helpers'
                ]
                
                if any(indicator in content_lower for indicator in utility_indicators):
                    return False
                    
                return True
        
        return False
    
    def _extract_component_name(self, file_path: Path) -> str:
        """提取组件名称 - 智能命名算法"""
        # 如果文件名是 index.vue，使用父目录名
        if file_path.name == 'index.vue' or file_path.name == 'index.js' or file_path.name == 'index.tsx':
            original_name = file_path.parent.name
        else:
            # 使用文件名（去掉扩展名）
            original_name = file_path.stem
            # 处理常见的组件命名模式
            if original_name.lower().endswith('component'):
                original_name = original_name[:-9]  # 移除 'component' 后缀
        
        return self._generate_smart_component_name(original_name, file_path)
    
    def _generate_smart_component_name(self, original_name: str, file_path: Path) -> str:
        """智能组件命名算法 - 解决重名和通用命名问题"""
        name_lower = original_name.lower()
        path_parts = file_path.parts
        
        # 处理重名问题 - List, Index 等通用名称
        if name_lower in ['list', 'index', 'item', 'card', 'box', 'page']:
            return self._generate_contextual_name(file_path, original_name)
        
        # 处理过于通用的名称
        generic_names = ['component', 'item', 'card', 'box', 'wrapper', 'container']
        if any(generic in name_lower for generic in generic_names):
            return self._generate_contextual_name(file_path, original_name)
        
        # 处理单字符或过短的名称
        if len(original_name) <= 2:
            return self._generate_contextual_name(file_path, original_name)
        
        return self._to_pascal_case(original_name)
    
    def _generate_contextual_name(self, file_path: Path, original_name: str) -> str:
        """基于路径上下文生成组件名称"""
        path_parts = [p for p in file_path.parts if p not in ['src', 'components', 'views', 'pages', 'index.vue', 'index.js', 'index.tsx']]
        
        # 获取最有意义的路径段
        meaningful_parts = []
        for part in reversed(path_parts[-4:]):  # 最多取4层路径
            if part != file_path.stem and len(part) > 1:
                meaningful_parts.append(part)
            if len(meaningful_parts) >= 2:
                break
        
        if meaningful_parts:
            # 组合路径段生成名称
            contextual_name = ''.join(self._to_pascal_case(part) for part in reversed(meaningful_parts))
            
            # 添加原始名称后缀（如果有意义）
            if original_name.lower() not in ['index', 'item'] and len(original_name) > 2:
                contextual_name += self._to_pascal_case(original_name)
            elif 'list' in str(file_path).lower():
                contextual_name += 'List'
            elif 'card' in str(file_path).lower():
                contextual_name += 'Card'
            elif 'item' in str(file_path).lower():
                contextual_name += 'Item'
            
            return contextual_name
        
        return self._to_pascal_case(original_name)
    
    def _to_pascal_case(self, text: str) -> str:
        """转换为PascalCase"""
        # 处理kebab-case和snake_case
        words = text.replace('-', '_').replace(' ', '_').split('_')
        return ''.join(word.capitalize() for word in words if word)
    
    def _extract_component_base_name(self, name: str) -> str:
        """提取组件的基础名称，去除通用前缀"""
        name_lower = name.lower()
        
        # 常见的组件前缀
        common_prefixes = ['base', 'common', 'fs', 'fb', 'my', 'custom', 'app', 'ui']
        
        for prefix in common_prefixes:
            if name_lower.startswith(prefix):
                # 移除前缀并返回剩余部分
                remaining = name[len(prefix):]
                if remaining:  # 确保移除前缀后还有内容
                    return remaining
        
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
        wrapper_indicators = ['base', 'common', 'fs', 'fb', 'custom', 'my', 'ui', 'app']
        has_wrapper_prefix = any(indicator in path_str for indicator in wrapper_indicators)
        
        return has_ui_import or has_wrapper_prefix

    def _get_dependency_type(self, file_path: Path) -> str:
        """获取依赖类型"""
        path_str = str(file_path)
        path_parts = file_path.parts
        
        # 第三方库检查
        if 'node_modules' in path_parts:
            return 'third_party'
        
        # 项目组件检查
        project_indicators = ['src/components', 'components', 'src/views', 'views']
        if any(indicator in path_str for indicator in project_indicators):
            return 'project'
        
        # 页面组件
        page_indicators = ['src/pages', 'pages', 'src/views', 'views']
        if any(indicator in path_str for indicator in page_indicators):
            return 'view'
        
        # 默认为项目组件
        return 'project'
    
    def _extract_props_and_events(self, content: str) -> Tuple[List[Dict], List[str]]:
        """增强的props和events解析"""
        props = self._extract_props_enhanced(content)
        events = self._extract_events_enhanced(content)
        return props, events
    
    def _extract_props_enhanced(self, content: str) -> List[Dict]:
        """增强的props提取"""
        try:
            props = []
            
            # Vue 3 Composition API defineProps
            defineprops_pattern = r'defineProps\s*\(\s*\{([^}]+)\}'
            match = re.search(defineprops_pattern, content, re.DOTALL)
            if match:
                props_content = match.group(1)
                parsed_props = self._parse_props_object(props_content)
                if isinstance(parsed_props, list):
                    props.extend(parsed_props)
            
            # Vue 2 Options API props
            options_props_pattern = r'props\s*:\s*\{([^}]+)\}'
            match = re.search(options_props_pattern, content, re.DOTALL)
            if match:
                props_content = match.group(1)
                parsed_props = self._parse_props_object(props_content)
                if isinstance(parsed_props, list):
                    props.extend(parsed_props)
            
            # 数组形式的props声明
            array_props_pattern = r'props\s*:\s*\[([^\]]+)\]'
            match = re.search(array_props_pattern, content)
            if match:
                props_array = match.group(1)
                prop_names = re.findall(r'[\'"`]([^\'"`]+)[\'"`]', props_array)
                for name in prop_names:
                    props.append({
                        'name': name,
                        'type': 'unknown',
                        'required': False,
                        'default': None
                    })
            
            return props
        except Exception as e:
            logger.error(f"提取props时出错: {str(e)}")
            return []
    
    def _parse_props_object(self, props_content: str) -> List[Dict]:
        """解析props对象定义"""
        props = []
        
        # 匹配每个prop定义
        prop_pattern = r'(\w+)\s*:\s*\{([^}]+)\}'
        for match in re.finditer(prop_pattern, props_content, re.DOTALL):
            prop_name = match.group(1)
            prop_def = match.group(2)
            
            # 解析prop属性
            prop_info = {'name': prop_name, 'type': 'unknown', 'required': False, 'default': None}
            
            # 提取type
            type_match = re.search(r'type\s*:\s*(\w+)', prop_def)
            if type_match:
                prop_info['type'] = type_match.group(1)
            
            # 提取required
            if 'required: true' in prop_def:
                prop_info['required'] = True
            
            # 提取default
            default_match = re.search(r'default\s*:\s*([^,\n]+)', prop_def)
            if default_match:
                prop_info['default'] = default_match.group(1).strip()
            
            props.append(prop_info)
        
        # 简单的prop声明（直接类型）
        simple_prop_pattern = r'(\w+)\s*:\s*(\w+)(?:\s*,|\s*$)'
        for match in re.finditer(simple_prop_pattern, props_content):
            prop_name = match.group(1)
            prop_type = match.group(2)
            # 避免重复添加
            if not any(p['name'] == prop_name for p in props):
                props.append({
                    'name': prop_name,
                    'type': prop_type,
                    'required': False,
                    'default': None
                })
        
        return props
    
    def _extract_events_enhanced(self, content: str) -> List[str]:
        """增强的events提取"""
        try:
            events = set()
            
            # Vue 3 defineEmits
            defineemits_pattern = r'defineEmits\s*\(\s*\[([^\]]+)\]'
            match = re.search(defineemits_pattern, content)
            if match:
                emits_content = match.group(1)
                event_names = re.findall(r'[\'"`]([^\'"`]+)[\'"`]', emits_content)
                events.update(event_names)
            
            # Vue 2 emits选项
            emits_pattern = r'emits\s*:\s*\[([^\]]+)\]'
            match = re.search(emits_pattern, content)
            if match:
                emits_content = match.group(1)
                event_names = re.findall(r'[\'"`]([^\'"`]+)[\'"`]', emits_content)
                events.update(event_names)
            
            # $emit调用
            emit_pattern = r'\$emit\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
            emit_matches = re.findall(emit_pattern, content)
            events.update(emit_matches)
            
            # this.$emit调用
            this_emit_pattern = r'this\.\$emit\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
            this_emit_matches = re.findall(this_emit_pattern, content)
            events.update(this_emit_matches)
            
            return list(events)
        except Exception as e:
            logger.error(f"提取events时出错: {str(e)}")
            return []
    
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
        """智能描述生成 - 基于组件内容和结构分析"""
        # 1. 优先查找组件级别的注释（非 @function）
        component_comment = self._extract_component_level_comment(content)
        if component_comment and not component_comment.startswith('@function'):
            return component_comment
        
        # 2. 如果没有有效注释，基于代码结构生成描述
        return self._generate_smart_description(content)
    
    def _extract_component_level_comment(self, content: str) -> str:
        """提取组件级别的注释"""
        # Vue组件的注释模式
        patterns = [
            r'<!--\s*([^@][^->]*?)\s*-->',  # HTML注释，排除@function
            r'/\*\*\s*\n\s*\*\s*([^@][^*]*?)\s*\*/',  # JSDoc注释
            r'//\s*([^@][^\n]*)',  # 单行注释
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                comment = match.group(1).strip()
                # 排除明显的函数注释和无意义注释
                if (not comment.startswith('@') and 
                    len(comment) > 10 and 
                    not comment.startswith('eslint') and
                    not comment.startswith('TODO')):
                    return comment
        
        return ""
    
    def _generate_smart_description(self, content: str) -> str:
        """基于代码结构生成智能描述"""
        template_features = self._analyze_template_features(content)
        interaction_capabilities = self._analyze_interaction_capabilities(content)
        
        # 组合生成描述
        if template_features and interaction_capabilities:
            return f"{template_features}，{interaction_capabilities}"
        elif template_features:
            return template_features
        elif interaction_capabilities:
            return interaction_capabilities
        else:
            return "可复用组件"
    
    def _analyze_template_features(self, content: str) -> str:
        """分析模板功能特性"""
        features = []
        content_lower = content.lower()
        
        if 'v-for' in content_lower or ':key=' in content_lower:
            features.append('支持列表渲染')
        if 'v-model' in content_lower:
            features.append('支持双向绑定')
        if '@click' in content_lower or '@tap' in content_lower:
            features.append('支持点击交互')
        if 'v-if' in content_lower or 'v-show' in content_lower:
            features.append('支持条件显示')
        if 'swiper' in content_lower:
            features.append('支持轮播功能')
        if 'loading' in content_lower:
            features.append('支持加载状态')
        if 'input' in content_lower or 'textarea' in content_lower:
            features.append('支持表单输入')
        if 'button' in content_lower:
            features.append('支持操作按钮')
        if 'draggable' in content_lower:
            features.append('支持拖拽排序')
        if 'dialog' in content_lower or 'modal' in content_lower:
            features.append('支持弹窗显示')
        if 'table' in content_lower or 'tr>' in content_lower:
            features.append('支持表格展示')
        if 'form' in content_lower:
            features.append('支持表单操作')
        
        return '、'.join(features) if features else '基础展示组件'
    
    def _analyze_interaction_capabilities(self, content: str) -> str:
        """分析交互能力"""
        capabilities = []
        content_lower = content.lower()
        
        if 'computed' in content_lower:
            capabilities.append('响应式计算')
        if 'watch' in content_lower:
            capabilities.append('数据监听')
        if 'router' in content_lower or '$router' in content_lower:
            capabilities.append('路由导航')
        if 'axios' in content_lower or 'request' in content_lower or 'api' in content_lower:
            capabilities.append('数据请求')
        if '$emit' in content_lower:
            capabilities.append('事件通信')
        if 'vuex' in content_lower or '$store' in content_lower:
            capabilities.append('状态管理')
        if 'mounted' in content_lower or 'created' in content_lower:
            capabilities.append('生命周期处理')
        
        return '、'.join(capabilities) if capabilities else ''
    
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
        
        # 动态阈值策略
        base_threshold = 0.15
        
        # 如果有高质量匹配，使用标准阈值
        high_quality_matches = [comp for comp, score in scored_components if score >= 0.6]
        if high_quality_matches:
            return high_quality_matches
        
        # 如果有中等质量匹配，使用中等阈值
        medium_quality_matches = [comp for comp, score in scored_components if score >= base_threshold]
        if medium_quality_matches:
            return medium_quality_matches
        
        # 如果没找到任何组件，降低阈值包含潜在匹配
        if scored_components:
            emergency_threshold = 0.05
            return [comp for comp, score in scored_components if score >= emergency_threshold]
        
        return []
    
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
            'button': ['btn', 'link', 'action'],
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
        
        # 通用组件名称匹配
        comp_name = component.get('name', '')
        comp_path = component.get('path', '')
        
        # 获取去除前缀的基础名称
        base_name = self._extract_component_base_name(comp_name).lower()
        
        # 检查基础名称是否包含目标类型
        if target_type.lower() in base_name:
            return 0.6
        
        # 检查完整名称和路径
        all_text = f"{comp_name} {comp_path}".lower()
        if target_type.lower() in all_text:
            return 0.5
        
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
        # 获取去除前缀的基础名称
        base_name_lower = self._extract_component_base_name(component_name).lower()
        max_similarity = 0.0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # 对原名称的匹配
            original_similarity = self._calculate_single_name_similarity(name_lower, keyword_lower)
            
            # 对基础名称的匹配（去除前缀后）
            base_similarity = self._calculate_single_name_similarity(base_name_lower, keyword_lower)
            
            # 取两者中的最高分
            best_similarity = max(original_similarity, base_similarity)
            max_similarity = max(max_similarity, best_similarity)
        
        return max_similarity
    
    def _calculate_single_name_similarity(self, name: str, keyword: str) -> float:
        """计算单个名称与关键词的相似度"""
        # 完全匹配
        if keyword == name:
            return 1.0
        
        # 包含匹配
        if keyword in name or name in keyword:
            return 0.8
        
        # 编辑距离相似度
        return self._string_similarity(keyword, name)
    
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
            return "\n\n💡 **搜索建议**: 项目中没有发现组件文件，请检查项目路径是否正确。"
        
        # 获取所有组件类型和名称作为建议
        component_types = set()
        component_names = []
        
        for comp in all_components:
            if comp.get('features'):
                component_types.update(comp['features'])
            component_names.append(comp['name'].lower())
        
        suggestions = ["\n\n💡 **搜索建议**:"]
        
        if component_types:
            type_list = list(component_types)[:5]  # 只显示前5个
            suggestions.append(f"- 尝试搜索组件类型: {', '.join(type_list)}")
        
        if component_names:
            name_list = list(set(component_names))[:5]  # 只显示前5个唯一名称
            suggestions.append(f"- 尝试搜索组件名称: {', '.join(name_list)}")
        
        suggestions.append("- 使用更通用的关键词，如: button, list, form, card")
        
        return '\n'.join(suggestions)
    

    
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

    def _analyze_single_component(self, file_path: Path) -> Optional[Dict]:
        """分析单个组件文件 - 根据改进规格重构"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 智能组件命名
            name = self._extract_component_name(file_path)
            
            # 增强的代码解析
            props, events = self._extract_props_and_events(content)
            
            # 确保数据类型正确
            if not isinstance(props, list):
                props = []
            if not isinstance(events, list):
                events = []
                
            slots = self._extract_slots(content)
            if not isinstance(slots, list):
                slots = []
            
            # 智能描述生成
            description = self._extract_description(content)
            if not isinstance(description, str):
                description = "可复用组件"
            
            # 功能特性分析
            features = self._extract_features(content)
            if not isinstance(features, list):
                features = []
            
            # 使用场景推断
            usage_scenario = self._infer_usage_scenario(file_path, content)
            if not isinstance(usage_scenario, str):
                usage_scenario = "通用场景"
            
            return {
                "name": name,
                "path": str(file_path),
                "description": description,
                "props": [prop.get('name', '') if isinstance(prop, dict) else str(prop) for prop in props],  # 安全的props处理
                "events": events,
                "features": features,
                "usage_scenario": usage_scenario,
                "props_detail": props,  # 详细的props信息
                "slots": slots
            }
            
        except Exception as e:
            logger.error(f"分析组件时出错 {file_path}: {str(e)}")
            return None
    
    def _extract_features(self, content: str) -> List[str]:
        """提取组件功能特性"""
        features = []
        content_lower = content.lower()
        
        # 基于模板分析
        if 'v-for' in content_lower or ':key=' in content_lower:
            features.append('列表渲染')
        if 'draggable' in content_lower:
            features.append('拖拽排序')
        if 'swiper' in content_lower:
            features.append('轮播展示')
        if 'v-model' in content_lower:
            features.append('双向绑定')
        if 'loading' in content_lower:
            features.append('加载状态')
        if 'dialog' in content_lower or 'modal' in content_lower:
            features.append('弹窗显示')
        if 'table' in content_lower:
            features.append('表格展示')
        
        # 基于脚本分析
        if 'computed' in content_lower:
            features.append('响应式计算')
        if 'watch' in content_lower:
            features.append('数据监听')
        if 'router' in content_lower or '$router' in content_lower:
            features.append('路由导航')
        if 'axios' in content_lower or 'request' in content_lower or 'api' in content_lower:
            features.append('数据请求')
        if '$emit' in content_lower:
            features.append('事件通信')
        if 'vuex' in content_lower or '$store' in content_lower:
            features.append('状态管理')
        
        return features
    
    def _infer_usage_scenario(self, file_path: Path, content: str) -> str:
        """推断使用场景"""
        path_lower = str(file_path).lower()
        
        # 基于路径位置
        if '/views/' in path_lower or '/pages/' in path_lower:
            return '完整页面组件，适用于路由页面'
        elif '/components/' in path_lower:
            return '可复用组件，适用于多个页面'
        
        # 基于功能域
        if 'manage' in path_lower:
            return '管理系统页面或组件'
        elif 'list' in path_lower:
            return '列表展示相关场景'
        elif 'item' in path_lower:
            return '单个数据项展示'
        elif 'modal' in path_lower or 'dialog' in path_lower:
            return '弹窗组件场景'
        elif 'form' in path_lower:
            return '表单相关场景'
        
        return '通用场景'

    def _format_component_info(self, component: Dict) -> str:
        """格式化组件信息输出 - 根据改进规格重构"""
        name = component.get('name', 'Unknown')
        path = component.get('path', '')
        description = component.get('description', '暂无描述')
        props = component.get('props', [])
        events = component.get('events', [])
        features = component.get('features', [])
        usage_scenario = component.get('usage_scenario', '通用场景')
        
        output = [f"### {name}"]
        output.append(f"**路径**: `{path}`")
        output.append(f"**描述**: {description}")
        
        if props:
            output.append(f"**Props**: {', '.join(props)}")
        
        if events:
            output.append(f"**事件**: {', '.join(events)}")
        
        if features:
            output.append(f"**功能特性**: {', '.join(features)}")
        
        output.append(f"**适用场景**: {usage_scenario}")
        
        return '\n'.join(output) + '\n'

    def _format_component_suggestions(self, components: List[Dict]) -> str:
        """格式化组件建议输出"""
        if not components:
            return "未找到匹配的可复用组件。"
        
        output = [f"找到 {len(components)} 个可复用组件:\n"]
        
        for i, component in enumerate(components, 1):
            formatted_info = self._format_component_info(component)
            output.append(formatted_info)
        
        return '\n'.join(output)

    def _generate_vue2_props_code(self, props: List[Dict]) -> str:
        """生成Vue2的props代码"""
        if not props:
            return """props: {
    title: {
      type: String,
      default: ''
    }
  },"""
        
        prop_definitions = []
        for prop in props:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'String')
            is_required = prop.get('required', False)
            default_value = prop.get('default', '')
            
            # Vue2 类型映射
            vue2_type_map = {
                'string': 'String',
                'number': 'Number',
                'boolean': 'Boolean',
                'array': 'Array',
                'object': 'Object',
                'function': 'Function'
            }
            
            vue2_type = vue2_type_map.get(prop_type.lower(), 'String')
            
            prop_def = f"    {prop_name}: {{\n      type: {vue2_type}"
            
            if is_required:
                prop_def += ",\n      required: true"
            
            if not is_required and default_value:
                if vue2_type == 'String':
                    prop_def += f",\n      default: '{default_value}'"
                elif vue2_type in ['Array', 'Object']:
                    prop_def += f",\n      default: () => {default_value}"
                else:
                    prop_def += f",\n      default: {default_value}"
            elif not is_required:
                if vue2_type == 'String':
                    prop_def += ",\n      default: ''"
                elif vue2_type == 'Number':
                    prop_def += ",\n      default: 0"
                elif vue2_type == 'Boolean':
                    prop_def += ",\n      default: false"
                elif vue2_type == 'Array':
                    prop_def += ",\n      default: () => []"
                elif vue2_type == 'Object':
                    prop_def += ",\n      default: () => ({})"
            
            prop_def += "\n    }"
            prop_definitions.append(prop_def)
        
        return f"""props: {{
{',\n'.join(prop_definitions)}
  }},"""

    def _generate_vue2_component_logic(self, component_type: str, features: List[str]) -> str:
        """生成Vue2组件逻辑代码"""
        
        if component_type == "form":
            return """data() {
    return {
      formData: {},
      errors: {},
      loading: false
    }
  },
  
  computed: {
    isFormValid() {
      return Object.keys(this.errors).length === 0
    }
  },
  
  methods: {
    validateField(fieldName) {
      // 字段验证逻辑
      // this.$set(this.errors, fieldName, errorMessage)
    },
    
    handleSubmit() {
      if (this.isFormValid) {
        this.loading = true
        this.$emit('submit', this.formData)
      }
    },
    
    handleCancel() {
      this.$emit('cancel')
    },
    
    getFieldError(fieldName) {
      return this.errors[fieldName]
    }
  },
  
  mounted() {
    // 组件挂载后的逻辑
  }"""

        elif component_type == "table":
            return """data() {
    return {
      loading: false,
      sortConfig: {
        key: '',
        direction: 'asc'
      }
    }
  },
  
  computed: {
    paginatedData() {
      if (!this.data || !this.pagination) return []
      const start = (this.pagination.current - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.data.slice(start, end)
    },
    
    totalPages() {
      if (!this.pagination) return 0
      return Math.ceil(this.pagination.total / this.pagination.pageSize)
    }
  },
  
  methods: {
    handleRefresh() {
      this.$emit('refresh')
    },
    
    handleSort(key) {
      this.sortConfig.key = key
      this.sortConfig.direction = this.sortConfig.direction === 'asc' ? 'desc' : 'asc'
      this.$emit('sort', { key, direction: this.sortConfig.direction })
    },
    
    handleRowClick(row, index) {
      this.$emit('row-click', { row, index })
    },
    
    getRowKey(row, index) {
      return row.id || index
    },
    
    getColumnValue(row, key) {
      return row[key]
    },
    
    getSortClass(key) {
      if (this.sortConfig.key === key) {
        return `sort-${this.sortConfig.direction}`
      }
      return ''
    },
    
    isRowSelected(row) {
      return false
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.$emit('page-change', page)
      }
    }
  }"""

        elif component_type == "modal":
            return """data() {
    return {
      loading: false
    }
  },
  
  computed: {
    sizeClass() {
      return `modal--${this.size || 'medium'}`
    }
  },
  
  methods: {
    handleClose() {
      this.$emit('update:visible', false)
      this.$emit('close')
    },
    
    handleCancel() {
      this.$emit('cancel')
      this.handleClose()
    },
    
    handleConfirm() {
      this.$emit('confirm')
    },
    
    handleOverlayClick() {
      if (this.maskClosable) {
        this.handleClose()
      }
    }
  },
  
  watch: {
    visible(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          // 获取焦点等操作
        })
      }
    }
  }"""

        elif component_type == "custom":
            return """data() {
    return {
      loading: false,
      isAuthorized: false,
      authProgress: 0,
      errorMessage: ''
    }
  },
  
  computed: {
    authButtonText() {
      if (this.loading) return '授权中...'
      if (this.isAuthorized) return '已授权'
      return '立即授权'
    },
    
    authStatusClass() {
      if (this.isAuthorized) return 'status--success'
      if (this.errorMessage) return 'status--error'
      return 'status--pending'
    }
  },
  
  methods: {
    getAuthTitle() {
      const titles = {
        wechat: '微信授权',
        alipay: '支付宝授权', 
        qq: 'QQ授权',
        weibo: '微博授权'
      }
      return titles[this.authType] || '第三方授权'
    },
    
    getAuthDescription() {
      const descriptions = {
        wechat: '需要获取您的微信基本信息以提供个性化服务',
        alipay: '需要获取您的支付宝基本信息以提供相关服务',
        qq: '需要获取您的QQ基本信息以提供个性化服务',
        weibo: '需要获取您的微博基本信息以提供相关功能'
      }
      return descriptions[this.authType] || '需要您的授权以提供更好的服务'
    },
    
    getAuthProviderName() {
      const names = {
        wechat: '微信',
        alipay: '支付宝',
        qq: 'QQ',
        weibo: '微博'
      }
      return names[this.authType] || '第三方平台'
    },
    
    handleAuth() {
      if (this.loading || this.isAuthorized) return
      
      this.loading = true
      this.errorMessage = ''
      this.authProgress = 0
      
      // 模拟授权流程
      this.simulateAuthProgress()
      
      // 实际授权逻辑
      this.performAuth()
    },
    
    simulateAuthProgress() {
      const interval = setInterval(() => {
        this.authProgress += 10
        if (this.authProgress >= 100) {
          clearInterval(interval)
        }
      }, 200)
    },
    
    async performAuth() {
      try {
        // 这里应该调用实际的授权API
        const authUrl = this.buildAuthUrl()
        
        if (this.redirectUrl) {
          window.location.href = authUrl
        } else {
          // 弹窗授权
          this.openAuthWindow(authUrl)
        }
        
      } catch (error) {
        this.handleAuthError(error)
      }
    },
    
    buildAuthUrl() {
      const baseUrl = this.getAuthBaseUrl()
      const params = new URLSearchParams({
        client_id: this.getClientId(),
        redirect_uri: this.redirectUrl || window.location.origin,
        response_type: 'code',
        scope: this.getAuthScope()
      })
      
      return `${baseUrl}?${params.toString()}`
    },
    
    getAuthBaseUrl() {
      const authUrls = {
        wechat: 'https://open.weixin.qq.com/connect/oauth2/authorize',
        alipay: 'https://openauth.alipay.com/oauth2/publicAppAuthorize.htm',
        qq: 'https://graph.qq.com/oauth2.0/authorize'
      }
      return authUrls[this.authType] || authUrls.wechat
    },
    
    getClientId() {
      // 从配置或环境变量获取
      return process.env.VUE_APP_CLIENT_ID || 'your_client_id'
    },
    
    getAuthScope() {
      const scopes = {
        wechat: 'snsapi_userinfo',
        alipay: 'auth_user',
        qq: 'get_user_info'
      }
      return scopes[this.authType] || scopes.wechat
    },
    
    openAuthWindow(authUrl) {
      const authWindow = window.open(
        authUrl, 
        'auth_window',
        'width=500,height=600,scrollbars=yes,resizable=yes'
      )
      
      // 监听授权窗口
      const checkClosed = setInterval(() => {
        if (authWindow.closed) {
          clearInterval(checkClosed)
          this.handleAuthComplete()
        }
      }, 1000)
    },
    
    handleAuthComplete() {
      this.loading = false
      this.authProgress = 100
      this.isAuthorized = true
      this.$emit('auth-success', { authType: this.authType })
    },
    
    handleAuthError(error) {
      this.loading = false
      this.authProgress = 0
      this.errorMessage = error.message || '授权失败，请重试'
      this.$emit('auth-error', { error, authType: this.authType })
    },
    
    retry() {
      this.errorMessage = ''
      this.handleAuth()
    },
    
    reauthorize() {
      // 清除授权状态
      this.isAuthorized = false
      this.authProgress = 0
      localStorage.removeItem(`${this.authType}_token`)
      this.handleAuth()
    },
    
    checkAuthStatus() {
      // 检查本地存储或调用API检查授权状态
      const token = localStorage.getItem(`${this.authType}_token`)
      if (token) {
        this.isAuthorized = true
        this.authProgress = 100
      }
    }
  },
  
  mounted() {
    // 检查是否已经授权
    this.checkAuthStatus()
  }"""

        else:
            return """data() {
    return {
      loading: false
    }
  },
  
  computed: {
    // 计算属性
  },
  
  methods: {
    // 组件方法
  },
  
  mounted() {
    // 组件挂载后的逻辑
  }"""