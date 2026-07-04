# Interview Notes

## 1. 项目背景

这个项目面向智能制造场景中的陶瓷表面缺陷检测。陶瓷表面缺陷通常比较细小、稀疏，而且不同类别之间外观差异明显，适合作为工业视觉检测和目标检测工程化实践项目。

我把它定位为一个从科研实验到工程展示的原型项目，而不是已经工业部署的生产系统。

## 2. 数据和任务

数据集为 CE7-DET，任务是检测陶瓷表面的 7 类缺陷：

```text
CK, DS, GS, SS, EC, AC, PH
```

类别中文映射还需要最终确认，所以展示版中保留原始类别名。

任务输出是目标检测框，包括：

- class_id
- class_name
- confidence
- bbox_xyxy

## 3. 为什么用 YOLO

YOLO 适合这个项目的原因：

- 工业检测通常需要较快推理速度。
- YOLO 工程生态成熟，训练、验证、推理、可视化工具链完整。
- 便于从实验迁移到 FastAPI / Web Demo。
- 对中小规模检测任务有较好的 baseline 表现。

## 4. 我的工作

可以真实表述为：

- 整理 CE7-DET 数据配置和类别信息。
- 完成 YOLO26n baseline、多分辨率对比和 HRCROP 数据变体实验。
- 对 WeightedConcat、HRCROP + WeightedConcat 等候选方案进行实验对比。
- 编写 tile inference、ROI candidate analysis、ROI coverage analysis、ROI refine、mAP 评估和 error analysis 脚本。
- 整理 PR/F1 曲线、混淆矩阵、定性检测图和实验表格。
- 将论文实验仓库整理为求职展示版工程骨架，准备接入 FastAPI 和 Vue Demo。

不要说“我发明了全新检测算法”。更准确的说法是：我设计并验证了面向高分辨率缺陷检测的稀疏 ROI refinement 实验流程，并完成了应用工程化准备。

## 5. 实验结果

主结果：

| Method | Precision | Recall | F1 | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| Full image HRCROP-WConcat | 0.7243 | 0.6745 | 0.6985 | 0.7058 | 0.3546 |
| ROI refine + global class-aware NMS | 0.7564 | 0.7523 | 0.7543 | 0.7241 | 0.3523 |

可以讲：

- ROI refine 后 Recall 从 0.6745 提升到 0.7523。
- F1 从 0.6985 提升到 0.7543。
- mAP50 有提升，但 mAP50-95 没有明显提升，所以不能夸大成定位质量全面提升。

## 6. ROI refinement 的作用

ROI refinement 的核心作用：

- full-image 检测先给出全局结果。
- 对容易漏检或需要高分辨率复核的区域生成 ROI。
- ROI crop 上再推理，恢复部分漏检目标。
- 最后通过 class-aware NMS 合并结果。

它主要帮助提升召回率和 F1，尤其对 DS/GS 等重点类别更有意义。

需要注意：

- ROI refinement 不是对所有 base detector 都无条件有效。
- Dense tile 虽然提高局部分辨率，但计算量大。
- Sparse ROI 是在效果和计算成本之间做折中。

## 7. 工程化展示版怎么做

展示版分三步：

1. 单图推理脚本：输入图片，输出可视化和 JSON。
2. FastAPI 后端：封装模型加载和 `/api/predict`。
3. Vue 前端：上传图片、展示检测结果和检测框表格。

当前已经创建项目骨架和 `scripts/infer_image.py`。

## 8. 项目不足

需要真实说明：

- 还没有工业现场部署。
- FastAPI 和 Vue 仍处于展示版规划阶段。
- 数据集和权重暂不适合直接公开。
- Runtime 目前是实验记录，不是生产环境 benchmark。
- 类别中文映射需要最终确认。
- ROI refine 的收益依赖 base detector 和类别选择。

## 9. 后续优化方向

- 完成 FastAPI + Vue Web Demo。
- 增加多图批量检测。
- 增加 ROI refine 高级模式。
- 做多次 repeat runtime benchmark。
- 增加 ONNX/TensorRT 推理优化。
- 补充更清晰的错误案例分析和可视化。
- 整理脱敏样例数据。

## 10. 面试官可能追问的问题

- CE7-DET 的数据规模和类别是什么？
- 为什么选择 YOLO，而不是 Faster R-CNN 或 DETR？
- Precision、Recall、F1、mAP50、mAP50-95 分别代表什么？
- 为什么 ROI refine 能提升 Recall？
- 为什么 mAP50-95 没有明显提升？
- Dense tile 和 sparse ROI 的区别是什么？
- class-aware NMS 是什么？
- 你具体写了哪些代码？
- 如果要部署成 Web Demo，你会怎么设计接口？
- 这个项目离真实工业部署还差什么？

