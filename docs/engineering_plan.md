# Engineering Plan

目标：在 7 天内把论文实验项目整理成可用于简历、README 和面试展示的轻量工程项目。

## Day 1-2: infer_image.py + README

- 完成展示目录结构。
- 完成 `scripts/infer_image.py`。
- 输出检测后图片和 JSON 文件。
- 写 README 初版。
- 整理 `experiments/metrics_summary.md`。
- 准备 2-3 张脱敏 demo image。

验收标准：

- 能用一条命令完成单图推理。
- README 能说明项目背景、方法、结果、限制和运行方式。

## Day 3-4: FastAPI Backend

- 新建 `backend/main.py`。
- 新建 `backend/detector.py`。
- 后端启动时加载 YOLO 权重。
- 实现 `GET /health`。
- 实现 `POST /api/predict`。
- 返回 JSON 和可视化图片 URL。

验收标准：

- 使用 Postman 或浏览器能上传单张图片并返回检测结果。
- 后端不会重复加载模型。

## Day 5: Vue Frontend

- 新建 Vue 项目。
- 完成上传图片区域。
- 完成 confidence / IoU 控件。
- 调用 FastAPI `/api/predict`。
- 展示检测后图片和检测框表格。

验收标准：

- 用户能在网页完成一次上传检测流程。

## Day 6: 联调和截图

- 联调前后端。
- 修复路径、跨域、静态文件访问问题。
- 准备 README 截图。
- 准备 2-3 个 demo case。

验收标准：

- README 有可视化效果图。
- 项目能按文档启动。

## Day 7: 简历、面试稿、投递材料

- 整理简历项目描述。
- 整理面试讲解稿。
- 整理 GitHub/Gitee 公开仓库。
- 检查 `.gitignore`。
- 确认不提交数据集、权重、投稿文档和临时实验输出。

验收标准：

- 有一版可投递简历 bullet。
- 有一版可展示 README。
- 有一版可讲清楚的面试提纲。

