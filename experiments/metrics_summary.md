# Metrics Summary

本文件记录已确认实验结果，用于 README、简历和面试展示。  
注意：这里不声明 SOTA，不声明工业部署。

## Accuracy Results

| Method | Precision | Recall | F1 | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| Full image HRCROP-WConcat | 0.7243 | 0.6745 | 0.6985 | 0.7058 | 0.3546 |
| DS/GS-only ROI refine + global class-aware NMS | 0.7564 | 0.7523 | 0.7543 | 0.7241 | 0.3523 |

## Runtime Records

| Method | Latency | FPS |
|---|---:|---:|
| Full image | 28.691 ms/image | 34.854 |
| Dense 9-tile | 113.239 ms/image | 8.831 |
| Proposed ROI refine | 70.381 ms/image | 14.208 |

## Notes

- Runtime 是实验记录，不应写成工业部署性能。
- ROI refinement 的主要价值体现在召回率和 F1 提升，以及相对 dense tile 的计算成本折中。
- 最终展示版应强调“科研实验到工程展示原型”，不要写“已工业落地”。

