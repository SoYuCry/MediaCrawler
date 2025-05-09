import json
from pathlib import Path
from datetime import datetime
import html

# ==== 配置路径 ====
json_path = Path(r"D:\Projects\MediaCrawler\data\weibo\json\detail_contents_2025-05-01.json")
image_dir = Path(r"D:\Projects\MediaCrawler\data\weibo\images")
output_dir = Path(r"D:\Projects\MediaCrawler\data\weibo\html")
output_dir.mkdir(parents=True, exist_ok=True)

# ==== 读取 JSON 数据 ====
with open(json_path, "r", encoding="utf-8") as f:
    all_data = json.load(f)

# ==== 遍历每条微博 ====
for i, data in enumerate(all_data):
    # 构造 file:/// 图片 HTML 段
    image_html = ""
    for pid in data.get("pic_list", []):
        img_path = image_dir / f"{pid}.jpg"
        file_url = "file:///" + img_path.as_posix()
        image_html += f'<img src="{file_url}" width="400"><br>\n'

    # 构造文件名（如 20240410_073242.html）
    dt_str = datetime.fromisoformat(data["create_date_time"]).strftime("%Y%m%d_%H%M%S")
    filename = f"{dt_str}.html"
    output_path = output_dir / filename

    # 构造 HTML 内容
    html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{data['nickname']} 的微博</title></head>
<body>
    <h2>{data['nickname']} @ {data.get('ip_location', '未知')}</h2>
    <p><strong>{data['create_date_time']}</strong></p>
    <p>{html.escape(data['content']).replace('\\n', '<br>')}</p>
    {image_html}
    <p>👍 {data.get('liked_count', '0')} 💬 {data.get('comments_count', '0')} 🔁 {data.get('shared_count', '0')}</p>
    <p><a href="{data['note_url']}">原微博链接</a></p>
</body>
</html>
    """.strip()

    # 写入 HTML 文件
    output_path.write_text(html_content, encoding="utf-8")
    print(f"✅ 写入 {output_path.name}")
