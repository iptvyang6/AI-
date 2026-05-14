import os
import json
import re
from datetime import datetime
from openai import OpenAI

# 1. 从环境变量读取 API Key
api_key = os.getenv("DEEPSK")
if not api_key:
    raise RuntimeError("环境变量 DEEPSK 未设置")

# 2. 初始化 DeepSeek 客户端（兼容 OpenAI 接口）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 3. 定义提示词：让 DeepSeek 返回结构化 JSON
prompt = """你是一名全球 AI 行业分析师。请根据今天（2026-05-14）的最新信息，生成一份中文的“全球AI每日情报”。

严格按下面的 JSON 格式输出，不要添加任何额外解释：
{
  "stats": {
    "news_count": 数字,
    "tools_count": 数字,
    "agents_count": 数字,
    "models_count": 数字
  },
  "top_news": [
    {"title": "新闻标题", "summary": "一句话摘要"}
  ],
  "new_tools": [
    {"name": "工具名称", "desc": "一句话介绍"}
  ],
  "trends": [
    {"keyword": "趋势关键词", "change": "增长百分比"}
  ],
  "daily_summary": "一段50字以内的整体摘要"
}"""

# 4. 调用 DeepSeek
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=2000
)

content = response.choices[0].message.content.strip()

# 5. 清理可能的 Markdown 代码块标记
if content.startswith("```"):
    content = re.sub(r"```\w*\n?|```", "", content).strip()

# 6. 解析 JSON
try:
    data = json.loads(content)
except json.JSONDecodeError:
    # 如果解析失败，用备用数据防止生成空白页
    data = {
        "stats": {"news_count": 0, "tools_count": 0, "agents_count": 0, "models_count": 0},
        "top_news": [],
        "new_tools": [],
        "trends": [],
        "daily_summary": "今日数据加载失败，请稍后再试。"
    }

# 7. 用数据构建 HTML（版面和你之前给的静态模板完全一致，但动态填充）
stats = data["stats"]
news_list = data["top_news"]
tools_list = data["new_tools"]
trends_list = data["trends"]
summary = data["daily_summary"]

news_html = ""
for item in news_list:
    news_html += f"""
    <div class="bg-black/20 p-4 rounded-xl">
        <h3 class="text-xl font-bold">{item['title']}</h3>
        <p class="mt-2 text-gray-300">{item['summary']}</p>
    </div>"""

tools_html = ""
for item in tools_list:
    tools_html += f"""
    <div class="bg-black/20 p-4 rounded-xl">
        <h3 class="font-bold">{item['name']}</h3>
        <p class="text-gray-300">{item['desc']}</p>
    </div>"""

trends_html = ""
for item in trends_list:
    trends_html += f"""
    <div class="flex justify-between">
        <span>{item['keyword']}</span>
        <span>↑{item['change']}</span>
    </div>"""

# 如果趋势列表为空，给个默认提示
if not trends_html:
    trends_html = '<div class="flex justify-between"><span>暂无数据</span></div>'

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球AI每日情报站</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body {{ background:#0b1020; color:white; font-family:sans-serif; }}
.card {{ background:rgba(255,255,255,0.06); border-radius:20px; padding:20px; }}
</style>
</head>
<body class="p-6">
<div class="max-w-6xl mx-auto">
<h1 class="text-4xl font-bold mb-6">全球 AI 每日情报站</h1>

<div class="grid md:grid-cols-4 gap-4 mb-6">
  <div class="card"><div>今日 AI 新闻</div><div class="text-3xl font-bold mt-2">{stats['news_count']}</div></div>
  <div class="card"><div>新增 AI 工具</div><div class="text-3xl font-bold mt-2">{stats['tools_count']}</div></div>
  <div class="card"><div>热门 Agent</div><div class="text-3xl font-bold mt-2">{stats['agents_count']}</div></div>
  <div class="card"><div>重点模型更新</div><div class="text-3xl font-bold mt-2">{stats['models_count']}</div></div>
</div>

<div class="grid lg:grid-cols-3 gap-6">
  <div class="lg:col-span-2">
    <div class="card mb-6">
      <h2 class="text-2xl font-bold mb-4">全球 AI 最新动态</h2>
      <div class="space-y-4">
        {news_html}
      </div>
    </div>
    <div class="card">
      <h2 class="text-2xl font-bold mb-4">AI 新工具</h2>
      <div class="space-y-4">
        {tools_html}
      </div>
    </div>
  </div>
  <div>
    <div class="card mb-6">
      <h2 class="text-xl font-bold mb-4">今日趋势</h2>
      <div class="space-y-2">
        {trends_html}
      </div>
    </div>
    <div class="card">
      <h2 class="text-xl font-bold mb-4">每日摘要</h2>
      <p class="text-gray-300 leading-7">{summary}</p>
      <p class="text-gray-500 text-sm mt-4">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
  </div>
</div>
</div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated with AI-generated content")
