from datetime import datetime

html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球AI每日情报站</title>

<script src="https://cdn.tailwindcss.com"></script>

<style>
body {{
background:#0b1020;
color:white;
font-family:sans-serif;
padding:40px;
}}

.card {{
background:rgba(255,255,255,0.06);
border-radius:20px;
padding:20px;
margin-bottom:20px;
}}
</style>

</head>

<body>

<h1 style="font-size:42px;font-weight:bold;">
全球 AI 每日情报站
</h1>

<div class="card">
<h2>今日 AI 动态</h2>

<p>DeepSeek 自动 AI 新闻系统运行成功。</p>

<p>GitHub Actions 自动更新成功。</p>

<p>当前更新时间：</p>

<p>{datetime.now()}</p>
</div>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html generated successfully")
