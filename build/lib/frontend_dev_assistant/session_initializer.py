"""
会话初始化器
在新对话开始时自动加载用户偏好，并提供行为调整建议
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_local.user_preference_analyzer import UserPreferenceAnalyzer
import json

class SessionInitializer:
    def __init__(self):
        self.preference_analyzer = UserPreferenceAnalyzer()
    
    def initialize_session(self, user_id: str = "rabbitsbear") -> str:
        """初始化新会话，返回基于用户偏好的系统提示"""
        
        # 分析用户偏好
        preferences = self.preference_analyzer.analyze_feedback_patterns(user_id)
        adjustments = self.preference_analyzer.get_behavior_adjustments(user_id)
        
        # 生成会话初始化提示
        system_prompt = self._generate_system_prompt(preferences, adjustments, user_id)
        
        return system_prompt
    
    def _generate_system_prompt(self, preferences: dict, adjustments: dict, user_id: str) -> str:
        """生成系统提示词"""
        
        prompt = f"""
# 🤖 会话初始化 - 用户偏好加载

## 用户偏好配置 (基于历史反馈)
"""
        
        # 重要偏好提示
        if preferences["communication_style"] == "maintain_current":
            prompt += "- ✅ **沟通风格**: 保持当前方式，用户满意度高\n"
        elif preferences["communication_style"] == "adjust_needed":
            prompt += "- ⚠️ **沟通风格**: 需要调整，考虑更简洁或详细的表达\n"
        
        if preferences["git_workflow"] == "batch_commits":
            prompt += "- 🔄 **Git工作流**: 继续使用智能分批次提交\n"
        
        if preferences["code_style"] == "with_comments":
            prompt += "- 📝 **代码风格**: 继续生成详细注释的代码\n"
        
        if preferences["feedback_frequency"] == "end_only":
            prompt += "- 💬 **反馈收集**: 仅在任务完成后收集，避免中途打断\n"
        
        # 行为调整建议
        prompt += "\n## 🎯 本次会话行为调整\n"
        
        for category, rules in adjustments.items():
            if rules:
                category_name = {
                    "communication_rules": "沟通方式",
                    "workflow_rules": "工作流程", 
                    "code_generation_rules": "代码生成",
                    "feedback_rules": "反馈收集"
                }.get(category, category)
                
                prompt += f"\n### {category_name}\n"
                for rule in rules:
                    prompt += f"- {rule}\n"
        
        prompt += f"""
## 📊 统计信息
- **用户ID**: {user_id}
- **偏好数据状态**: 已加载
- **行为调整**: 已应用

---
*此提示基于你的历史反馈自动生成，用于优化本次对话体验*
"""
        
        return prompt
    
    def get_quick_preferences_summary(self, user_id: str = "rabbitsbear") -> dict:
        """获取快速偏好摘要，用于AI内部参考"""
        preferences = self.preference_analyzer.analyze_feedback_patterns(user_id)
        
        # 简化为AI容易理解的指令
        quick_guide = {
            "communication": "maintain_current" if preferences["communication_style"] == "maintain_current" else "normal",
            "git_workflow": "batch_commits" if preferences["git_workflow"] == "batch_commits" else "flexible",
            "code_comments": "detailed" if preferences["code_style"] == "with_comments" else "normal",
            "feedback_timing": "end_only" if preferences["feedback_frequency"] == "end_only" else "flexible",
            "satisfaction_level": "high" if preferences["communication_style"] == "maintain_current" else "normal"
        }
        
        return quick_guide


# 提供给AI助手的便捷函数
def load_user_preferences_for_session(user_id: str = "rabbitsbear") -> tuple:
    """
    为AI助手提供的便捷函数
    返回: (用户偏好摘要, 详细初始化提示)
    """
    initializer = SessionInitializer()
    
    quick_guide = initializer.get_quick_preferences_summary(user_id)
    detailed_prompt = initializer.initialize_session(user_id)
    
    return quick_guide, detailed_prompt


# 测试函数
if __name__ == "__main__":
    initializer = SessionInitializer()
    
    # 生成会话初始化提示
    session_prompt = initializer.initialize_session()
    print("=== 会话初始化提示 ===")
    print(session_prompt)
    
    print("\n" + "="*50 + "\n")
    
    # 获取快速偏好指南
    quick_guide = initializer.get_quick_preferences_summary()
    print("=== 快速偏好指南 ===")
    print(json.dumps(quick_guide, ensure_ascii=False, indent=2)) 