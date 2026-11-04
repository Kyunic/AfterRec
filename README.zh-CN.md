# RecForgetBench：推荐系统遗忘 × LLM Agent 评测平台

[English README](README.md) · [系统架构](docs/architecture/OVERVIEW.md) · [模块分工](docs/team/OWNERSHIP.md) · [第一批开发任务](docs/team/FIRST_ISSUES.md)

> **当前为仓库初始骨架，不是完整平台。** `frontend/index.html` 是离线交互演示，
> 其中的训练结果、商品和 Agent 行为均为**模拟示例**，不可作为真实实验结果。

## 一、项目介绍

本项目计划建设一个**可视化、可复现、可扩展**的推荐系统 Unlearning 评测平台。
通过统一的实验流程整合数据管理、推荐模型训练、Unlearning、静态指标、
多轮 LLM Agent 用户模拟和结果分析。

核心科研问题是：传统推荐系统遗忘指标与用户感知的遗忘体验之间存在怎样的关系？
当用户要求删除特定交互后，推荐系统是否仍会展示用户能够感知到的间接语义关联？

**研究必须区分两类结论：**

1. **技术层面的数据遗忘：** 指定交互对模型的影响是否被移除，应与 Retain Set 上
   从头训练的 Retrain 基准及其他指标比较。
2. **用户感知遗忘：** 在实际推荐曝光和交互过程中，用户是否仍接触到与遗忘目标
   相关的内容，以及 Agent 是否能可靠预测人类判断。

某次推荐仍包含关联商品，不自动意味着模型技术上没有完成 Machine Unlearning。

## 二、六个核心模块与分工

| 模块 | 职责 | 负责人 |
| --- | --- | --- |
| 1. 数据集管理 | 数据导入、预处理、数据版本、训练/验证/测试及遗忘/保留划分 | 学生 A |
| 2. 推荐模型与训练 | RecBole 集成、BPR/LightGCN、训练、加载、Top-K 推荐 | 学生 A |
| 3. Unlearning | 遗忘请求、Retrain 参考模型、后续近似遗忘算法 | 学生 B |
| 4. 静态评测 | Recall/NDCG、遗忘诊断、效率和可复现实验比较 | 学生 B |
| 5. Agent 动态模拟 | 用户画像、遗忘意图、多轮动作、会话状态、轨迹记录 | 学生 C 负责运行框架，项目负责人负责科研算法 |
| 6. Web 与实验管理 | 前后端、任务执行、结果展示、系统集成 | 学生 C |

项目负责人负责总体架构、研究问题、Agent 科研设计、阶段验收；
**不负责日常代码审查和 Git 冲突解决**。学生 C 负责协调集成，A、B 各自
对算法模块和科研正确性负责。

## 三、当前仓库已经包含什么？

**可运行：**

- `frontend/index.html`：可离线打开的交互式产品原型，仅用于团队展示。
- `backend/src/recforgetbench/api/`：FastAPI 启动、健康检查与能力状态查询。
- `core/validation.py`：数据划分与遗忘/保留集合的基本正确性检查。
- `evaluation/metrics.py`：可单独测试的基础 Recall@K/NDCG@K 函数。
- `simulation/`：Agent 动作协议和最小多轮执行器，当前仅以测试夹具运行。
- `AGENTS.md`、`CLAUDE.md`、模块级规则：统一 AI Coding 的行为约束。
- `.github/`：CI、Issue 与 PR 协作模板。

**尚未实现：** 真实的 RecBole 训练、Retrain 遗忘、完整 Web 工作流、
真实数据集评测以及经过人类校准的 LLM Agent。必须由后续开发实现和验证。

## 四、本地运行

推荐使用 Python 3.11 创建虚拟环境，先安装基础包（当前不需要 GPU 或 RecBole）：

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/verify_scaffold.py
python scripts/check_frontend.py
python -m uvicorn recforgetbench.api.main:app --reload --port 8000
```

启动后访问：

- `http://127.0.0.1:8000/docs`：API 文档。
- `http://127.0.0.1:8000/api/v1/health`：服务状态。
- `http://127.0.0.1:8000/api/v1/capabilities`：功能实现状态。

前端原型直接双击 `frontend/index.html` 打开即可。真实模型运行环境
由学生 A 在验证 RecBole 与 PyTorch 兼容性后单独记录。

## 五、三名学生如何协作？

**统一 GitHub 仓库；每人独立电脑、独立分支；每项任务一个 Issue、一个 PR。**

- 学生 A 主要修改 `datasets/`、`recsys/`。
- 学生 B 主要修改 `unlearning/`、`evaluation/`。
- 学生 C 主要修改 `api/`、`frontend/`，并负责跨模块集成。
- `core/`、`simulation/`、公共接口文档和 CI 属于共享部分，先协商再修改。
- Claude Code 使用 `CLAUDE.md`，Codex 使用 `AGENTS.md`。
- 每个 PR 必须包含实际功能、测试结果、演示方式和已知限制。
- 学生之间进行交叉功能验证；项目负责人以 Demo、指标和复现结果验收。

GitHub 创建及上传流程见 [`docs/team/BOOTSTRAP_GITHUB.md`](docs/team/BOOTSTRAP_GITHUB.md)。

详细规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)、
[`AGENTS.md`](AGENTS.md) 和 [`docs/team/OWNERSHIP.md`](docs/team/OWNERSHIP.md)。

## 六、第一阶段开发目标

**先打通真实 Pipeline，再添加复杂功能。**

1. **阶段 1：** RecBole 模型训练与推荐页面，真实 Top-K 展示。
2. **阶段 2：** Forget/Retain 划分、Retrain、静态指标对照。
3. **阶段 3：** 连接真实推荐模型、3–5 轮 Agent 动态模拟、轨迹展示。
4. **研究扩展：** 语义关联评测、Agent 校准、更多模型与遗忘方法。

第一批任务详见 [`docs/team/FIRST_ISSUES.md`](docs/team/FIRST_ISSUES.md)。

## 七、开源与数据说明

仓库建议初期设为 **Private**。目前**尚未选择开放源代码许可证**，
正式公开前由项目负责人决定。RecBole 代码与外部数据集的许可互相独立；
不要提交数据集、模型权重、真实用户信息或 API Key。
