"""
用户偏好分析器
基于用户反馈数据分析偏好，生成AI行为调整建议
"""

import json
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

class UserPreferenceAnalyzer:
    def __init__(self, data_dir: str = "src/data"):
        self.data_dir = Path(data_dir)
        self.usage_stats_file = self.data_dir / "usage_stats.json"
        
    def load_user_feedback(self, user_id: str = "rabbitsbear") -> List[Dict]:
        """加载指定用户的反馈数据"""
        try:
            with open(self.usage_stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            feedback_data = data.get("user_feedback", [])
            # 过滤指定用户的反馈
            user_feedback = [f for f in feedback_data if f.get("user_id") == user_id]
            
            return user_feedback
        except Exception as e:
            print(f"加载反馈数据失败: {e}")
            return []
    
    def analyze_feedback_patterns(self, user_id: str = "rabbitsbear") -> Dict:
        """分析用户反馈模式，生成偏好配置"""
        feedback_data = self.load_user_feedback(user_id)
        
        if not feedback_data:
            return self._get_default_preferences()
        
        # 按工具类型分组分析
        tool_feedback = {}
        overall_satisfaction = Counter()
        
        for feedback in feedback_data:
            tool_name = feedback.get("tool_name", "")
            rating = feedback.get("feedback", "")
            context = feedback.get("context", "")
            
            if tool_name not in tool_feedback:
                tool_feedback[tool_name] = []
            
            tool_feedback[tool_name].append({
                "rating": rating,
                "context": context,
                "timestamp": feedback.get("timestamp", "")
            })
            
            overall_satisfaction[rating] += 1
        
        # 生成偏好配置
        preferences = self._generate_preferences(tool_feedback, overall_satisfaction)
        
        return preferences
    
    def _generate_preferences(self, tool_feedback: Dict, overall_satisfaction: Counter) -> Dict:
        """根据反馈数据生成偏好配置"""
        preferences = {
            "communication_style": "detailed",  # detailed, concise, balanced
            "git_workflow": "batch_commits",    # batch_commits, single_commit
            "code_style": "with_comments",      # with_comments, minimal, extensive
            "task_completion": "complete",      # complete, quick, interactive
            "feedback_frequency": "end_only",   # end_only, intermediate, frequent
            "explanation_level": "medium",      # minimal, medium, detailed
            "error_handling": "graceful"        # graceful, strict, permissive
        }
        
        # 基于整体满意度调整
        total_feedback = sum(overall_satisfaction.values())
        if total_feedback > 0:
            satisfaction_rate = (overall_satisfaction["excellent"] + overall_satisfaction["good"]) / total_feedback
            
            if satisfaction_rate > 0.8:
                preferences["communication_style"] = "maintain_current"
            elif satisfaction_rate < 0.5:
                preferences["communication_style"] = "adjust_needed"
        
        # 基于具体工具反馈调整
        for tool_name, feedbacks in tool_feedback.items():
            excellent_count = sum(1 for f in feedbacks if f["rating"] == "excellent")
            total_count = len(feedbacks)
            
            if "git" in tool_name.lower() or "提交" in tool_name:
                if excellent_count / total_count > 0.7:
                    preferences["git_workflow"] = "batch_commits"  # 继续分批次
                else:
                    preferences["git_workflow"] = "flexible"
            
            if "生成" in tool_name or "component" in tool_name.lower():
                if excellent_count / total_count > 0.7:
                    preferences["code_style"] = "with_comments"  # 继续详细注释
                else:
                    preferences["code_style"] = "balanced"
        
        return preferences
    
    def _get_default_preferences(self) -> Dict:
        """默认偏好配置"""
        return {
            "communication_style": "balanced",
            "git_workflow": "batch_commits",
            "code_style": "with_comments", 
            "task_completion": "complete",
            "feedback_frequency": "end_only",
            "explanation_level": "medium",
            "error_handling": "graceful"
        }
    
    def get_behavior_adjustments(self, user_id: str = "rabbitsbear") -> Dict:
        """获取基于偏好的行为调整建议"""
        preferences = self.analyze_feedback_patterns(user_id)
        
        adjustments = {
            "communication_rules": [],
            "workflow_rules": [],
            "code_generation_rules": [],
            "feedback_rules": []
        }
        
        # 生成具体的行为调整规则
        if preferences["communication_style"] == "maintain_current":
            adjustments["communication_rules"].append("继续保持当前的沟通风格，用户满意度高")
        elif preferences["communication_style"] == "adjust_needed":
            adjustments["communication_rules"].append("需要调整沟通方式，考虑更简洁或更详细的表达")
        
        if preferences["git_workflow"] == "batch_commits":
            adjustments["workflow_rules"].append("继续使用智能分批次提交，用户反馈良好")
        
        if preferences["code_style"] == "with_comments":
            adjustments["code_generation_rules"].append("继续生成详细注释的代码，用户偏好明确")
        
        if preferences["feedback_frequency"] == "end_only":
            adjustments["feedback_rules"].append("仅在任务完成后收集反馈，避免中途打断")
        
        return adjustments
    
    def generate_session_prompt_additions(self, user_id: str = "rabbitsbear") -> str:
        """生成会话开始时的额外提示词"""
        adjustments = self.get_behavior_adjustments(user_id)
        
        prompt_additions = []
        
        for category, rules in adjustments.items():
            if rules:
                prompt_additions.extend(rules)
        
        if prompt_additions:
            return f"\n## 基于用户反馈的行为调整:\n" + "\n".join(f"- {rule}" for rule in prompt_additions)
        
        return ""
    
    def export_preferences_report(self, user_id: str = "rabbitsbear") -> str:
        """导出用户偏好分析报告"""
        feedback_data = self.load_user_feedback(user_id)
        preferences = self.analyze_feedback_patterns(user_id)
        adjustments = self.get_behavior_adjustments(user_id)
        
        report = f"""
# 用户偏好分析报告

**用户ID**: {user_id}
**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**反馈数据量**: {len(feedback_data)} 条

## 当前偏好配置
"""
        
        for key, value in preferences.items():
            report += f"- **{key}**: {value}\n"
        
        report += "\n## 行为调整建议\n"
        
        for category, rules in adjustments.items():
            if rules:
                report += f"\n### {category}\n"
                for rule in rules:
                    report += f"- {rule}\n"
        
        return report


# 使用示例
if __name__ == "__main__":
    analyzer = UserPreferenceAnalyzer()
    
    # 分析用户偏好
    preferences = analyzer.analyze_feedback_patterns()
    print("用户偏好配置:", json.dumps(preferences, ensure_ascii=False, indent=2))
    
    # 获取行为调整建议
    adjustments = analyzer.get_behavior_adjustments()
    print("行为调整建议:", json.dumps(adjustments, ensure_ascii=False, indent=2))
    
    # 生成会话提示词补充
    session_prompt = analyzer.generate_session_prompt_additions()
    print("会话提示词补充:", session_prompt) 