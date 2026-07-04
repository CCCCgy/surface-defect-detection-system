# 智能制造场景下基于 YOLO 的陶瓷表面缺陷检测系统

本项目是一个用于求职展示的轻量工程骨架，面向智能制造场景下的陶瓷表面缺陷检测。当前展示版优先完成单图推理、检测结果可视化和 JSON 结果输出，后续计划扩展为 FastAPI + Vue Web Demo。

真实定位：这是一个从科研实验向工程展示迁移的 AI 应用开发原型，不声明已工业部署，也不声明 SOTA。

## 项目背景

陶瓷表面缺陷检测是典型的工业视觉检测任务，目标是在生产质检场景中识别表面异常。项目围绕 CE7-DET 数据集进行实验整理，包含 YOLO full-image detection、ROI refinement、tile inference、错误分析和可视化等环节。

## 数据集

主数据集：`CE7-DET`

类别名称保持原始缩写：

```text
CK, DS, GS, SS, EC, AC, PH
```

类别中文映射待确认，README 中不强行翻译。

## 方法概述

实验主线可以概括为：

```text
YOLO full-image detection + sparse ROI refinement
```

已验证的核心思路：

- 使用 YOLO 进行 full-image defect detection。
- 对高分辨率陶瓷图像中的稀疏疑似区域生成 ROI candidates。
- 对重点类别相关 ROI 进行二次检测和结果合并。
- 使用 class-aware NMS 降低重复框和误检。
- 对比 full image、dense tile、sparse ROI refinement 的精度和推理成本。

## 当前展示版功能

当前已提供：

- 单图推理脚本：`scripts/infer_image.py`
- 检测结果可视化图片输出
- JSON 结构化检测结果输出
- 实验指标摘要：`experiments/metrics_summary.md`
- 后端和前端目录占位，便于后续扩展

## 数据与权重说明

- 本展示仓库不包含完整 CE7-DET 数据集。
- 本展示仓库不包含训练权重。
- `assets/demo_images/` 中的图片仅用于功能展示，公开前应确认脱敏和授权。
- 论文未正式录用前，不公开完整实验仓库、完整运行日志和投稿材料。
- 如需复现实验，应根据论文和公开数据集自行配置环境。
- 权重路径由用户在本地自行配置，可通过 `--weights` 参数或 `CERAMIC_YOLO_WEIGHTS` 环境变量传入。

## 实验结果摘要

| Method | Precision | Recall | F1 | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| Full image HRCROP-WConcat | 0.7243 | 0.6745 | 0.6985 | 0.7058 | 0.3546 |
| DS/GS-only ROI refine + global class-aware NMS | 0.7564 | 0.7523 | 0.7543 | 0.7241 | 0.3523 |

Runtime 记录：

| Method | Latency | FPS |
|---|---:|---:|
| Full image | 28.691 ms/image | 34.854 |
| Dense 9-tile | 113.239 ms/image | 8.831 |
| Proposed ROI refine | 70.381 ms/image | 14.208 |

说明：runtime 是实验记录，不代表生产环境 benchmark。

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

单图推理示例：

```bash
python scripts/infer_image.py \
  --source assets/demo_images/sample_001.jpg \
  --weights path/to/your/local/best.pt \
  --output-dir assets/demo_outputs \
  --conf 0.25 \
  --iou 0.60 \
  --imgsz 800
```

也可以通过环境变量指定本地权重：

```bash
export CERAMIC_YOLO_WEIGHTS=path/to/your/local/best.pt
python scripts/infer_image.py \
  --source assets/demo_images/sample_001.jpg \
  --output-dir assets/demo_outputs
```

如果使用本地 Ultralytics 源码而不是 pip 包，可设置：

```bash
export YOLO_SOURCE_DIR=path/to/your/local/ultralytics_source
```

输出内容：

```text
assets/demo_outputs/
├── sample_001_pred.jpg
└── sample_001_result.json
```

## 项目结构

```text
surface-defect-detection-system/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│   └── infer_image.py
├── backend/
│   ├── main.py
│   └── detector.py
├── frontend/
│   └── README.md
├── experiments/
│   └── metrics_summary.md
├── assets/
│   ├── demo_images/
│   └── demo_outputs/
└── docs/
    ├── DATA_SAFETY.md
    ├── SECURITY_CHECK_REPORT.md
    ├── interview_notes.md
    └── engineering_plan.md
```

## 后续计划

- 完成 FastAPI 后端接口：`POST /api/predict`
- 完成 Vue 前端上传检测页面
- 增加 Web Demo 截图
- 增加少量脱敏 demo images
- 整理简历项目 bullet 和面试讲解稿
- 可选：增加 ROI refinement 高级推理模式

## 真实声明

- 本项目为科研实验到工程展示的原型。
- 当前展示版未工业部署。
- 不声明 SOTA。
- runtime 是实验记录，不代表生产环境 benchmark。
- 完整数据集、训练权重、投稿材料和完整实验仓库不直接公开。
