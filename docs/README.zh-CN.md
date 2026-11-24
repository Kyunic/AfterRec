# AfterRec 项目文档

[English](README.md) · [整体架构](architecture/OVERVIEW.zh-CN.md) · [项目首页](../README.zh-CN.md)

建议先阅读[整体架构](architecture/OVERVIEW.zh-CN.md)。以下文档按**功能模块和接口边界**组织，便于分别维护；新建的设计文件目前仅为待完善的模板。

## 开发前先统一设计和接口

各模块开始开发前，请按[模块设计模板](templates/DESIGN_TEMPLATE.zh-CN.md)（[English](templates/DESIGN_TEMPLATE.md)）整理目标、第一版范围、整体流程、模块依赖及可执行的验收条件。

涉及两个模块协作或前后端对接时，按[接口模板](templates/INTERFACE_TEMPLATE.zh-CN.md)（[English](templates/INTERFACE_TEMPLATE.md)）提前确认调用方式、输入输出、异常及联调测试，并填写到对应的 `interfaces/` 文件。现有[公共协议](contracts/INTERFACES.md)已确定的内容不得在新文档中另行定义一套。

模板用于把关键问题提前说清楚，不要求凑字数。未确认的内容要标明，不能直接作为开发依据。

## 模块设计

| 模块 | 文档 | 需要补充的内容 |
| --- | --- | --- |
| 数据管理 | [datasets](modules/datasets/DESIGN.md) | 数据格式、预处理、划分、Forget/Retain 清单与数据版本 |
| 推荐模型 | [recommendation](modules/recommendation/DESIGN.md) | 模型训练、加载、打分、Top-K、Checkpoint 与适配方式 |
| 遗忘算法 | [unlearning](modules/unlearning/DESIGN.md) | 遗忘请求、算法接入、Retrain 基线与模型输出 |
| 静态评测 | [evaluation](modules/evaluation/DESIGN.md) | 指标定义、候选集、过滤规则、对照实验与结果记录 |
| Agent 模拟 | [agent simulation](modules/agent-simulation/DESIGN.md) | Agent 策略、观察/动作、会话状态与轨迹记录 |
| 实验平台 | [platform](modules/platform/DESIGN.md) | 后端任务编排、前端流程、实验状态与产物管理 |

## 接口协议

现有[共享接口协议](contracts/INTERFACES.md)记录当前数据结构与方法签名。模块对接细节在以下文件补充，避免接口定义分散在各模块文档中：

| 接口 | 需要明确的内容 |
| --- | --- |
| [前后端接口](interfaces/FRONTEND_BACKEND.md) | HTTP 路由、请求响应、错误、任务状态、前端调用 |
| [数据与推荐](interfaces/DATA_RECOMMENDATION.md) | 数据引用、ID 映射、商品元数据、模型训练输入 |
| [推荐与遗忘](interfaces/RECOMMENDATION_UNLEARNING.md) | 模型产物、遗忘请求、兼容性和输出格式 |
| [模型与评测](interfaces/MODEL_EVALUATION.md) | 排序候选集、指标输入、评测协议和结果格式 |
| [推荐与 Agent](interfaces/RECOMMENDATION_AGENT.md) | 推荐观察、动作、会话反馈、轨迹事件 |
| [实验产物](interfaces/EXPERIMENT_ARTIFACTS.md) | 任务 ID、文件组织、模型关系、实验溯源 |

## 研究与进度

- [Agent 研究与评测协议](research/SIMULATION_PROTOCOL.md)
- [开发路线图](ROADMAP.md)

此前已形成的[Agent 模拟设计草稿](../doc/agent-simulation/README.zh-CN.md)暂时保留。草稿中的拟议 API 需与共享协议核对后，再作为正式实现接口。
