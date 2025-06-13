#!/usr/bin/env python3
"""
MCP 数据位置检查工具
用于查看 MCP 使用数据的保存位置
"""

import sys
import os
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

def check_data_locations():
    """检查所有可能的数据保存位置"""
    print("🔍 MCP 数据位置检查")
    print("=" * 50)
    
    # 1. 环境变量指定的目录
    env_data_dir = os.environ.get('FRONTEND_DEV_ASSISTANT_DATA_DIR')
    if env_data_dir:
        print(f"🌟 环境变量数据目录: {env_data_dir}")
        check_directory(Path(env_data_dir))
    else:
        print("❌ 未设置环境变量 FRONTEND_DEV_ASSISTANT_DATA_DIR")
    
    print()
    
    # 2. 用户主目录
    home_data_dir = Path.home() / ".frontend-dev-assistant"
    print(f"🏠 用户主目录数据目录: {home_data_dir}")
    check_directory(home_data_dir)
    
    print()
    
    # 3. 项目开发模式目录
    project_data_dir = project_root / "src" / "data"
    print(f"🔧 项目开发模式数据目录: {project_data_dir}")
    check_directory(project_data_dir)
    
    print()
    
    # 4. 检查包安装模式
    try:
        from frontend_dev_assistant.usage_tracker import UsageTracker
        tracker = UsageTracker()
        actual_data_dir = tracker.data_dir
        usage_file = tracker.usage_file
        
        print(f"✅ 当前实际使用的数据目录: {actual_data_dir}")
        print(f"📄 使用统计文件: {usage_file}")
        
        if usage_file.exists():
            file_size = usage_file.stat().st_size
            print(f"📊 文件大小: {file_size} 字节")
            
            # 读取并显示基本统计
            import json
            try:
                with open(usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                total_logs = len(data.get('usage_logs', []))
                total_feedback = len(data.get('user_feedback', []))
                tools_used = len(data.get('tool_usage', {}))
                
                print(f"📈 使用记录条数: {total_logs}")
                print(f"💬 反馈记录条数: {total_feedback}")
                print(f"🔧 使用过的工具数: {tools_used}")
                
            except Exception as e:
                print(f"⚠️  读取使用数据时出错: {e}")
        else:
            print("❌ 使用统计文件不存在")
            
    except ImportError as e:
        print(f"❌ 无法导入 UsageTracker: {e}")
        print("可能需要先安装依赖或检查Python路径")

def check_directory(directory_path: Path):
    """检查单个目录的状态"""
    if directory_path.exists():
        if directory_path.is_dir():
            files = list(directory_path.glob("*"))
            print(f"  ✅ 目录存在，包含 {len(files)} 个文件")
            
            usage_file = directory_path / "usage_stats.json"
            if usage_file.exists():
                file_size = usage_file.stat().st_size
                print(f"  📄 找到使用统计文件 (大小: {file_size} 字节)")
            else:
                print(f"  ❌ 未找到使用统计文件")
        else:
            print(f"  ⚠️  路径存在但不是目录")
    else:
        print(f"  ❌ 目录不存在")

def show_migration_guide():
    """显示数据迁移指南"""
    print("\n" + "=" * 50)
    print("📋 数据位置说明")
    print("=" * 50)
    
    print("""
🎯 **不同安装方式的数据位置**:

1. **开发模式** (git clone + 直接运行):
   - 数据保存在: `项目目录/src/data/`
   - 便于开发和调试

2. **pip 安装模式** (pip install git+...):
   - 数据保存在: `~/.frontend-dev-assistant/`
   - 跨项目共享，数据持久化

3. **自定义位置** (环境变量):
   - 设置: `export FRONTEND_DEV_ASSISTANT_DATA_DIR=/your/path`
   - 完全自定义数据保存位置

🔄 **数据迁移**:
如果需要迁移数据，只需将 `usage_stats.json` 文件复制到新位置即可。

💡 **推荐配置**:
- 开发者: 使用项目目录
- 普通用户: 使用用户主目录 (pip安装自动选择)
- 企业用户: 使用环境变量指定网络共享位置
""")

if __name__ == "__main__":
    check_data_locations()
    show_migration_guide() 