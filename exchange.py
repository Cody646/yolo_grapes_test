import json
import os
from urllib.parse import unquote

# 1. 填入你下载的 JSON 文件名
JSON_FILE = "project-7-at-2026-10-30-01-45-d583e74b.json"  # 改成你的 json 文件名
OUTPUT_DIR = "./labels"  # 生成的 YOLO txt 标签存放目录

# 2. 你的类别标签映射（必须与标注时一致，索引从 0 开始）
# 如果你只有一个类（比如茶多酚），写 { "你的类别名": 0 }
CLASS_MAPPING = {"tea_polyphenol": 0}  # 请把 "tea_polyphenol" 改成你当时设置的具体标签名

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    # 获取图片原始文件名（自动解码中文字符和特殊符号）
    raw_path = item.get("image", "")
    decoded_path = unquote(raw_path)
    filename = os.path.basename(decoded_path)
    name_without_ext = os.path.splitext(filename)[0]

    txt_filename = f"{name_without_ext}.txt"
    txt_path = os.path.join(OUTPUT_DIR, txt_filename)

    # 提取标注框（兼容 JSON 和 JSON-MIN 结构）
    annotations = []
    # 如果是 JSON-MIN 格式
    if "label" in item:
        for box in item["label"]:
            label_name = (
                box.get("rectanglelabels", [""])[0]
                if isinstance(box.get("rectanglelabels"), list)
                else box.get("labels", [""])[0]
            )
            cls_id = CLASS_MAPPING.get(label_name, 0)

            # Label Studio 坐标是 0~100 的百分比，转换成 YOLO 标准的 0~1 归一化中心点与宽高
            x_center = (box["x"] + box["width"] / 2.0) / 100.0
            y_center = (box["y"] + box["height"] / 2.0) / 100.0
            width = box["width"] / 100.0
            height = box["height"] / 100.0

            annotations.append(
                f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            )

    # 写入 YOLO 格式的 txt
    with open(txt_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(annotations))

print(f"转换完成！所有 YOLO 标签已保存到: {os.path.abspath(OUTPUT_DIR)}")