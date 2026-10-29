from ultralytics import YOLO

# 1. 加载刚才微调出来的最佳模型权重（注意路径中的反斜杠或使用原始字符串 r""）
model_path = r"runs/detect/my_runs/tea_model-3/weights/best.pt"
model = YOLO(model_path)

# 2. 选择一张图片进行预测（换成你想测试的任意图片路径）
# 你也可以把 source 改为一个文件夹路径，比如 source=r"experiment_images/茶多酚 (16 mg)" 批量预测整个文件夹
test_img = r"experiment_images/茶多酚 (80 mg)/0 d.jpg"

# 3. 开始预测并保存带画框的结果
results = model.predict(
    source=test_img,
    conf=0.50,  # 置信度阈值（高于 25% 确定是茶多酚就画框）
    save=True,  # 自动保存标注画框后的图片
    show=False,
)

print("\n预测完成！画好检测框的图片已经保存在 runs/detect/predict 文件夹中，快去打开看看吧！")