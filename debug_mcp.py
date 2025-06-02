#!/usr/bin/env python3
import sys
import os
import traceback

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("调试MCP启动...", file=sys.stderr)
    print(f"Python版本: {sys.version}", file=sys.stderr)
    print(f"工作目录: {os.getcwd()}", file=sys.stderr)
    print(f"Python路径: {sys.executable}", file=sys.stderr)
    
    import start_mcp
    print("start_mcp模块加载成功", file=sys.stderr)
    
except Exception as e:
    print(f"错误: {e}", file=sys.stderr)
    print(f"详细错误:\n{traceback.format_exc()}", file=sys.stderr)
    sys.exit(1) 