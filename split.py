import os
import random
import shutil

# ================= 核心修改：路径补全到最后一级子文件夹 =================
RAW_IMAGES_DIR = r"experiment_images/茶多酚 (16 mg)"  # 精确指向图片所在的子文件夹
RAW_LABELS_DIR = r"./labels"  # labels 文件夹
OUTPUT_DATASET = r"./my_yolo_dataset"  # 划分后输出的文件夹
# ====================================================================

# 1. 创建 YOLO 所需的目录结构
for split in ["train", "val"]:
    os.makedirs(os.path.join(OUTPUT_DATASET, "images", split), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DATASET, "labels", split), exist_ok=True)

# 2. 读取所有的 labels 标签文件
label_files = [f for f in os.listdir(RAW_LABELS_DIR) if f.endswith(".txt")]
random.seed(42)
random.shuffle(label_files)

# 8:2 划分验证集
val_ratio = 0.2
val_count = max(1, int(len(label_files) * val_ratio))
val_files = set(label_files[:val_count])

success_count = 0
not_found_images = []

for lbl in label_files:
    base_name = os.path.splitext(lbl)[0]
    split = "val" if lbl in val_files else "train"

    # 寻找匹配的图片（支持 jpg, png, jpeg, JPG, PNG）
    matched_img = None
    for ext in [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]:
        possible_path = os.path.join(RAW_IMAGES_DIR, base_name + ext)
        if os.path.exists(possible_path):
            matched_img = possible_path
            break

    if matched_img:
        # 复制图片到对应 split
        shutil.copy(matched_img, os.path.join(OUTPUT_DATASET, "images", split))
        # 复制对应的 label txt 到对应 split
        shutil.copy(
            os.path.join(RAW_LABELS_DIR, lbl),
            os.path.join(OUTPUT_DATASET, "labels", split, lbl),
        )
        success_count += 1
    else:
        not_found_images.append(base_name)

print("=" * 40)
print(f"处理完成！成功配对并划分了 {success_count} 组图片和标签。")
if not_found_images:
    print(f"以下标签未找到对应图片: {not_found_images}")
else:
    print("所有图片与标签全部完美配对！")
print(f"结果保存在: {os.path.abspath(OUTPUT_DATASET)}")
print("=" * 40)