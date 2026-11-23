# Recommendation to unlearning

设计评审稿 V8 · 2026-11-24

本页描述推荐与遗忘模块的交接。现有类型与方法签名来自[共享接口协议](../contracts/INTERFACES.md)。拟议的适配能力和记录字段用于联调讨论。遗忘步骤见[遗忘算法设计](../modules/unlearning/DESIGN.md)。

## 公共调用和数据对象

- 推荐到遗忘的入口为 `UnlearningMethod.unlearn(original, request, config) -> ModelArtifact`。`original` 是原模型产物，`request` 是已确认的遗忘请求，`config` 保存本次方法配置。`UnlearningMethod.is_compatible(model_name) -> bool` 提供模型类型的初步检查。
- Retrain 通过 `Recommender.train(dataset, split, config) -> ModelArtifact` 调用推荐模块，在派生 Retain 划分上创建新模型。通过 `Recommender.load(artifact)` 核对新检查点是否可加载。
- 现有 `Recommender.score_items(user_id, item_ids)` 提供固定候选打分。序列打分如需传固定历史或历史引用，由推荐与评测模块另行确认适配方式。

| 交接对象 | 现有字段与职责 |
| --- | --- |
| `DatasetRef`、`SplitRef` | 数据集 ID、版本、`split_id`、Train/Valid/Test 清单引用和种子。推荐模块提供原模型实际使用的版本和切分。 |
| 原 `ModelArtifact` | `model_id`、`dataset_id`、`split_id`、`model_name`、`checkpoint_uri`、`id_mapping_uri`、`config`。推荐模块提供可加载的检查点和与之配套的映射。 |
| `ForgetRequest` | `request_id`、`split_id`、`strategy`、`forget_manifest_uri`、`retain_manifest_uri`、`seed`。遗忘模块先按交互 ID 准备并确认清单。 |
| 新 `ModelArtifact` | 包含新模型和检查点引用，并通过 `parent_model_id` 关联原模型，通过 `forget_request_id` 关联该次请求。 |

`ForgetRequest.split_id` 指原训练切分。Retrain 的新产物可使用派生 Retain 切分 ID，运行记录保存派生切分与原切分的关联。SCIF 的新产物记录原检查点及实际使用的 Forget、清理后样本和 Retain 来源。

## 准备要求

1. 推荐模块提供原始训练交互及稳定的 `interaction_id`、`user_id`、`item_id`。序列训练还需能定位事件时间、稳定顺序、必要的会话边界和历史构造配置。
2. 遗忘模块核对原产物、数据版本、切分和映射属于同一原实验。Forget 和 Retain 互斥且精确覆盖原 Train。确认后保存清单引用和摘要，运行前复核。
3. 推荐模块从 Retain 重建训练输入，返回实际训练数据和派生样本的回执。序列样本应能追溯历史和目标的交互 ID。双塔应记录训练对、受影响的用户特征及必要的商品向量或索引版本。
4. SCIF 所需适配能力包括原模型副本、与版本匹配的配置、目标参数、损失与梯度接口，以及受影响样本和 Retain 加载器。只有加载、更新和产物回读通过验证的组合才可接受执行。

## 结果、来源与失败信息

执行成功后，推荐模块用返回的 `ModelArtifact` 重载新模型。遗忘模块保存实际输入摘要、方法配置和来源关系。实验平台用运行 ID 获取状态和产物，再把指定模型交给推荐、评测或模拟。产物记录及评测输入分别见[实验产物接口](EXPERIMENT_ARTIFACTS.md)和[模型与评测接口](MODEL_EVALUATION.md)。

| 场景 | 返回信息 |
| --- | --- |
| 模型或方法不兼容 | 说明具体模型、方法及缺少的能力，例如 SCIF 梯度接口尚未验证。 |
| 原产物、映射或清单不匹配 | 标识问题字段、预期版本与实际版本，保留失败运行的引用。 |
| 求解失败或检查点无法加载 | 记录失败阶段和原因，保留已产生的诊断信息。 |
| 产物可用且评测失败 | 返回已登记的模型引用和评测错误，允许沿用该模型单独重跑评测。 |

同一划分可服务于 Retrain 和 SCIF 的对照。跨方法关联划分的 `selection_id`、固定历史引用 `history_ref` 及阶段回执字段均为拟议扩展。当前对照至少记录原模型、原切分和两份清单的哈希。字段进入公共类型前遵循[共享协议的变更流程](../contracts/INTERFACES.md)。

## 示例

以下 ID 和 URI 都是虚构示例。请求中的 `split-014` 是原切分。

```json
{
  "request_id": "req-014-R",
  "split_id": "split-014",
  "strategy": "interaction",
  "forget_manifest_uri": "requests/req-014-R/forget.jsonl",
  "retain_manifest_uri": "requests/req-014-R/retain.jsonl",
  "seed": 2026
}
```

同一次 Retrain 的输出示例如下。`split-014-retain` 是训练使用的派生切分，`model-014` 是原模型。

```json
{
  "model_id": "model-014-R",
  "dataset_id": "agent-clicks",
  "split_id": "split-014-retain",
  "model_name": "SASRec",
  "checkpoint_uri": "models/model-014-R/checkpoint.pt",
  "id_mapping_uri": "datasets/agent-clicks/v1/id_mapping.json",
  "config": {
    "method": "retrain",
    "fresh_initialization": true,
    "source_split_id": "split-014"
  },
  "parent_model_id": "model-014",
  "forget_request_id": "req-014-R"
}
```
