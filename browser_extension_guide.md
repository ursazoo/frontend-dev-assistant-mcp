# 前端开发提示词浏览器插件

## 🌐 无需本地服务的浏览器方案

### 快速实现方案

1. **使用现有的ChatGPT/Claude插件**
   - 安装ChatGPT for VSCode插件
   - 将提示词保存为代码片段
   - 一键调用常用提示词

2. **创建简单的HTML页面**
   - 本地HTML文件
   - 包含所有提示词模板
   - 快速复制到Cursor

### HTML页面实现

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前端开发提示词库</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 20px; }
        .prompt-card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .copy-btn { background: #007AFF; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .copy-btn:hover { background: #0056CC; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>🚀 前端开发提示词库</h1>
    
    <div class="prompt-card">
        <h3>🔧 Git代码提交助手</h3>
        <button class="copy-btn" onclick="copyPrompt('git-commit')">复制提示词</button>
        <pre id="git-commit">帮我分批次提交代码。请先检查 git status，然后分析所有未暂存的修改，并一次性提供一个完整的、按模块或功能分组的提交计划。

计划应包含：
1. 每个批次要提交的文件列表
2. 为每个批次建议的 commit message (格式为 feat/fix: 中文描述)

请等待我确认或修改计划后再执行任何 git 命令。

注意事项：
- 遵循 Conventional Commits 规范
- commit message 使用中文描述
- 按功能模块合理分组
- 避免混合不相关的改动

附加上下文：[在这里填写你的具体改动描述]</pre>
    </div>

    <script>
        function copyPrompt(id) {
            const text = document.getElementById(id).textContent;
            navigator.clipboard.writeText(text).then(() => {
                alert('提示词已复制到剪贴板！');
            });
        }
    </script>
</body>
</html>
``` 