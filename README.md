# 茶多酚图像目标检测

这是一个使用 Ultralytics YOLO 对实验图片进行目标检测微调的示例项目。项目包含标注格式转换、训练集/验证集划分、模型训练和图片预测脚本。

> **配置提醒：** 当前 `exchange.py` 中的类别映射为 `tea_polyphenol`，但 `data.yaml` 将类别 0 命名为 `grapes`。训练前请确认类别名称，并将两处设置统一，否则模型类别名称会与实际目标不符。

## 项目流程

1. 将 Label Studio 导出的 JSON 标注转换为 YOLO 格式标签。
2. 将图片与标签配对，并按约 8:2 划分训练集和验证集。
3. 使用 `yolo11n.pt` 预训练权重训练模型。
4. 加载训练得到的最佳权重，对图片进行预测并保存检测结果。

## 文件说明

| 文件/目录 | 用途 |
|---|---|
| `exchange.py` | 将 Label Studio JSON 标注转换为 YOLO `.txt` 标签 |
| `split.py` | 配对图片与标签，并生成训练集、验证集 |
| `test.py` | 加载 `yolo11n.pt` 微调模型 |
| `project.py` | 加载训练得到的权重并进行图片预测 |
| `data.yaml` | YOLO 数据集路径和类别配置 |
| `project-7-at-2026-10-30-01-45-d583e74b.json` | Label Studio 标注导出文件 |
| `experiment_images/` | 实验图片目录 |
| `labels/` | 转换生成的 YOLO 标签 |
| `my_yolo_dataset/` | 划分生成的数据集 |
| `yolo11n.pt` | YOLO 预训练权重 |
| `runs/`、`weights/` | 训练或模型运行产生的文件 |

## 环境准备

建议使用 Python 虚拟环境。安装 PyTorch 时，请根据电脑上的 CUDA 版本或是否使用 CPU，选择 PyTorch 官方提供的安装命令；然后安装 Ultralytics：

```powershell
pip install ultralytics
```

检查安装：

```powershell
python -c "import torch, ultralytics; print('torch:', torch.__version__); print('ultralytics:', ultralytics.__version__); print('CUDA available:', torch.cuda.is_available())"
```

## 数据准备与训练

在项目根目录运行以下命令：

```powershell
python exchange.py
python split.py
python test.py
```

运行前请检查以下配置：

- `exchange.py` 中的 `JSON_FILE` 应指向实际的标注 JSON 文件；`CLASS_MAPPING` 中的类别名应与标注中的标签名完全一致。
- `split.py` 中的 `RAW_IMAGES_DIR` 应指向包含待训练图片的目录。当前设置为 `experiment_images/茶多酚 (16 mg)`；图片文件名（不含扩展名）需要与标签文件名对应。
- `data.yaml` 中的训练集、验证集路径应指向 `my_yolo_dataset/images/train` 和 `my_yolo_dataset/images/val`。当前路径是本机绝对路径，换电脑后需要修改。
- `data.yaml` 中 `names` 的类别名称应与标注类别一致。当前的 `grapes` 与 `exchange.py` 中的 `tea_polyphenol` 不一致。

训练参数在 `test.py` 中设置：100 个 epoch、640 输入尺寸、batch size 为 4。脚本会在可用时使用 NVIDIA GPU，否则使用 CPU。训练结果通常会包含 `weights/best.pt`；请以训练日志打印的实际保存路径为准。

## 图片预测

训练成功后，修改 `project.py` 中的 `model_path`，使其指向本次训练生成的 `weights/best.pt`。也可以修改 `test_img` 指定要预测的图片，然后运行：

```powershell
python project.py
```

预测结果由 Ultralytics 保存到运行结果目录（通常为 `runs/detect/predict` 或相邻的递增目录）。

## YOLO 标签格式

每个图片对应一个同名 `.txt` 文件，每行表示一个目标：

```text
类别编号 x中心 y中心 宽 高
```

坐标和宽高均为相对于图片尺寸归一化到 `0` 到 `1` 的数值。
