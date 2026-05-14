from datetime import datetime

html = f"""
<html>
<head>
<title>AI Daily News</title>
</head>

<body style="background:#111;color:white;font-family:sans-serif;padding:40px;">

<h1>全球 AI 每日情报站</h1>

<p>GitHub Actions 自动运行成功</p>

<p>当前时间：</p>

<p>{datetime.now()}</p>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated")
