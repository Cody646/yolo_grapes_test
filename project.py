import torch
from ultralytics import YOLO

if __name__ == "__main__":
    # 检查是否有 NVIDIA 显卡可用
    has_gpu = torch.cuda.is_available()
    device = 0 if has_gpu else "cpu"
    print(f"当前使用的训练设备: {'NVIDIA GPU' if has_gpu else 'CPU'}")

    # 1. 加载官方预训练权重（首次会自动下载 yolo11n.pt，体积仅约 6MB）
    model = YOLO("yolo11n.pt")

    # 2. 开始微调训练
    model.train(
        data="data.yaml",  # 数据集配置文件
        epochs=100,  # 训练轮数（样本较少，建议跑 80~100 轮充分收敛）
        imgsz=640,  # 输入图片缩放尺寸
        batch=4,  # 每批处理图片数（小样本设为 4 较为稳定）
        workers=2,  # Windows 下建议设为 0 或 2，防止子进程卡死
        device=device,  # 自动选择 GPU 或 CPU
        project="my_runs",  # 训练结果保存的主文件夹名称
        name="tea_model",  # 本次训练实验的名字
    )