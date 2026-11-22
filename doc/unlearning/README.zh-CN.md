# AfterRec B 模块软件设计报告 V7

## 1 模块功能与边界

整体流程为 C 的多个 Agent 生成带顺序的模拟点击，A 固定数据版本并训练推荐模型，B 冻结遗忘范围并执行 Retrain 或 SCIF，A 登记新产物供 C 推荐和模拟。B 负责请求、执行协调、方法适配、输入审计、静态评测和结果追溯。推荐器训练与推理由 A 提供，任务持久化、HTTP 和多 Agent 模拟由 C 提供 [1]。

| 功能 | 当前证据 | 本阶段交付 |
| --- | --- | --- |
| 请求和集合校验 | 本地已有交互 ID 选择、比例抽样、清单冻结与哈希校验。 | 增加模拟点击顺序、序列样本来源和跨方法共享划分的审计。 |
| Retrain 与静态评测 | 历史本地 BPR 小样本跑通过重训、重载和 Recall/NDCG 比较。 | 复用已有逻辑，接入 A 的首个模型和固定历史输入。 |
| SCIF 与新推荐模型 | ERASE 有 SCIF 及 SASRec 参数选择代码。AfterRec 适配待验证。 | 交付兼容性验证、独立产物和同划分的三组比较。 |
| 页面与上下游集成 | HTML 为离线流程演示，正式 A/B/C 服务待联调。 | 向 C 提供真实阶段、产物及结果，支持评测单独重试。 |

历史证据来自 300 名用户的 BPR 实验，原 Train 2,128 条，Forget 212 条，Retain 1,916 条 [10]。这项证据支持已有本地流程。序列推荐、双塔和 SCIF 分别验收。

## 2 技术实现方案

### 2.1 推荐模型和关键组件

序列推荐根据有序点击预测下一件商品，优先阅读并验证 RecBole 的 SASRec [2,3]。双塔分别编码用户侧特征和商品特征，按向量匹配分数召回商品 [4]。具体实现由 A 冻结。首个模型通过后再复用流程适配第二个模型，每个“推荐模型、遗忘方法、实现版本”组合分别记录状态。

B 使用 Python 服务。请求服务冻结分区，执行器调度 Retrain 或 SCIF，A 适配器转换数据和产物，审计器检查输入及来源，评测器统一计算指标。复用 AfterRec 公共数据类型、方法协议与 Pydantic 校验 [1]。SCIF 参考 ERASE，评测参考 CURE4Rec [5–7]。

| 组件 | 直接复用 | 需要实现或扩展 |
| --- | --- | --- |
| 请求与分区 | unlearning/requests.py 的 prepare_request、load_prepared，以及 manifests.py 的哈希和文件操作。 | 绑定 A 的原实验与点击版本，审计重建序列，支持同一 selection_id 下的多个方法请求。 |
| Retrain 编排 | unlearning/retrain.py 的 RetrainMethod，含派生 Retain 切分、新初始化和产物检查。 | 接 A 的模型工厂、序列或双塔训练输入与实际回执。现有默认支持名单只有 BPR。 |
| SCIF 适配 | ERASE 的 Trainer.scif、target_params 和相关梯度求解、保存代码 [5]。 | 核对模型和库版本，构造删前/删后样本及 Retain 加载器，统一错误、阶段、产物和审计回执。 |
| 评测与交接 | evaluation/metrics.py 的 Recall、NDCG，以及 runner.py 的候选、屏蔽和确定性排序。 | 扩展为 Original/Retrain/SCIF，加入历史输入、第三组产物校验、结果格式转换。Hit@K 单独补实现与验算。 |

表中文件以 backend/src/recforgetbench 为根。本地增量位于工作区 Code/Backend/B_Baseline，公开仓库主干仍是基础骨架。外部参考快照只用于阅读，正式接入时固定完整源码版本、依赖与许可证。

### 2.2 Retrain 执行方案

B 接收原实验、原检查点和冻结的 Retain 引用，要求 A 从 Retain 重建训练样本、采样器及派生特征，使用新权重和新优化器开始训练。保留原模型结构、ID 映射、配置依据及 Valid/Test 目标记录，另存新运行目录。需要调整的训练参数写入新配置，记录与原实验的差异。

序列模型从保留的原始点击重建所有历史前缀与下一物品标签，检查忘记的点击未出现在任何训练输入或标签。双塔从 Retain 重建训练对、用户历史特征及负采样依赖。商品塔若更新，重新导出商品向量，并在使用索引时登记对应索引版本。

A 返回实际训练清单和派生样本哈希、初始化记录及新检查点。B 校验数据归属、原产物与映射哈希、输入回执、新模型可重载与可打分，再登记产物。Retrain 为同一原模型与同一划分下的近似方法提供对照。

### 2.3 SCIF 执行方案

SCIF 根据被遗忘数据及保留数据的影响估计更新原模型参数，以保留协同推荐信息 [6]。执行从原检查点的独立副本开始。记录目标参数、梯度求解配置、阻尼、迭代预算和随机种子，分别保存更新前后检查点的哈希。

适配重点是对齐 ERASE 中 forget_data、clean_forget_data 与 retain_train_data 的含义。序列模型以原点击 ID 追踪所有受影响的历史前缀和标签，分别提供变更前后的训练样本及 Retain 加载器。仅按标签删除训练行会遗漏历史中的同一次点击。样本权重、归一化、补齐、截断与负采样按所选实现核对。

ERASE 的 target_params 对 SASRec 显式选择 item_embedding.weight，这是可阅读的实现依据。AfterRec 仍需验证模型类识别、参数名、损失及二阶梯度求解能否对上。双塔需要另外确定更新用户塔、商品塔或两塔的方案，并检查目标参数确实参与损失计算。通过这些检查后才开放对应方法组合。

运行中若出现非有限数值、输入不匹配或求解超出预算，记录失败或未完成状态及原因。更新结束后由 A 重载新产物，再以同一分区和评测协议比较 Original、Retrain、SCIF 的指标与分阶段耗时。成员推断诊断在独立样本和攻击协议确定后加入。

### 2.4 后续方法

后续候选调整为 RecEraser 与 SISA。两者均有原始论文和作者实现 [8,9]。OpenAlex 于 2026-11-22 查询的引用数分别为 214 和 2,142 [11]，用于说明选型的研究基础。

| 候选 | 主要实现方式 | 接入依赖 |
| --- | --- | --- |
| RecEraser，WWW 2022 | 按协同信息将训练数据分片，分别训练子模型并学习聚合器。遗忘时重训受影响子模型及相应聚合部分。 | A 预先提供分片、子模型和聚合器。原实现覆盖 BPR、WMF、LightGCN，序列与双塔需单独改造和验证。 |
| SISA，IEEE S&P 2021 | 训练前分片、分段并保存检查点，删除数据后从受影响位置重训，聚合各分片预测。 | A 需从原训练阶段保留分片与分段检查点。推荐分数的聚合方式和模型产物结构另行约定。 |

这两种方案都依赖训练阶段准备。进入开发前，先由 A/B 确认多检查点产物和训练成本，再以各自完整训练方案建立对照并排期。

### 2.5 可行性与验收

已有材料覆盖本地 BPR 数据分区、Retrain、模型重载和两组静态指标。测试文件覆盖固定种子、清单变化、映射错误、训练失败和手算指标等用例 [10]。本阶段验收依次检查 A 的真实数据和训练回执、首个模型的重训重载、SCIF 的参数与加载器兼容、三组固定口径评测、C 的重复提交与评测重试。

静态推荐分数、训练输入审计、攻击诊断和 Agent 交互轨迹分别保存并解释。C 在比较各模型时重置 Agent 与会话初始状态，模型参数在评测期间冻结。新增模拟点击另存数据版本，进入下一次训练前重新固定切分。

## 3 数据结构与模块接口

### 3.1 数据对象和产物关联

沿用公共对象，新增 selection_id、历史引用和方法回执作为待评审的服务扩展。以下字段和 JSON 为设计示例，正式契约由 A/B/C 联调确认。资源引用由服务解析。

| 对象或文件 | 必需内容 | 关联与保存 |
| --- | --- | --- |
| 点击记录 | interaction_id、user_id、item_id、event_time、step、synthetic；会话模型另含 session_id。 | C 产出，A 保存数据版本、排序和同时间记录的稳定顺序，明确 Agent 与用户的映射。 |
| DatasetRef / SplitRef | 数据版本、原 Train/Valid/Test、切分和映射哈希、序列构造规则。 | A 固定。Train/Valid/Test 按原始记录定位，训练样本保存来源点击 ID。 |
| 选择与请求 | selection_id 绑定 Forget/Retain 与哈希；request_id 绑定原产物、方法、指标及选择。 | B 冻结清单，同一选择可产生不同方法请求；单次请求重试沿用原清单。 |
| 运行和模型 | run_id、request_id、原/新 artifact_id、方法与版本、训练回执、检查点和映射。 | C 保存任务状态，A 托管检查点，B 记录来源、审计及派生样本。 |
| 评测结果 | comparison_id、三组模型和运行引用、selection_id、protocol_id、覆盖人数、指标、耗时与缺失原因。 | B 输出 comparison.json 和逐用户明细，C 查询并展示。 |

冻结清单放在 requests/<request_id>/，执行记录放在 runs/<run_id>/，比较结果放在 comparisons/<comparison_id>/。A 的产物目录保存模型、映射、序列配置与需要的特征、向量或索引引用。记录原始清单哈希和派生训练样本哈希，保证结果可追溯。

### 3.2 Forget 与 Retain 规则

首轮按原 Train 的交互比例抽取，5% 转成 0.05 并向下取整。1,000 条分为 50 条 Forget 和 950 条 Retain。两集合互斥且精确覆盖原 Train，记录字段和稳定 ID 保持可追溯。拒绝重复 ID、跨分区选择、空集合及清单或源数据哈希变化。

序列示例中 Train 为 I1:P1 → I2:P2 → I3:P3 → I4:P4。遗忘 I2 后，从 Retain 重建为 [P1]→P3 和 [P1,P3]→P4，审计 I2 在输入历史和标签中的全部来源。其他仍保留的 P2 点击按其独立交互 ID 处理。Valid/Test 的目标固定，评测历史由统一协议单独生成，历史中使用的数据必须早于目标且符合分区规则。

A-014 表示原训练，art-014 表示所选原检查点，sel-014 表示同一分区，req-R 和 req-S 分别选择 Retrain 与 SCIF，run-R 与 run-S 表示两次执行，art-R 与 art-S 表示两个新产物。跨方法比较核对原产物、sel-014 及分区哈希。

### 3.3 上下游提供的主要能力

| 方向 | 主要能力 | 输入与返回要点 |
| --- | --- | --- |
| A → B | 读取原实验、点击、切分与映射，提供重训、模型副本、打分和产物登记。 | 接收原训练/检查点及 Retain 引用，返回训练回执或可加载的新产物。SCIF 另需可计算损失和梯度的模型环境。 |
| B → C | 方法查询、请求预览与确认、提交执行、状态与事件、产物和结果查询、评测重试。 | 接收原产物与选择条件，返回请求、清单、运行、阶段、产物及比较引用。 |
| A → C | 返回指定模型的推荐，C 记录 Agent 曝光和点击。 | 传 artifact_id、用户和历史/会话引用、K，返回物品 ID、分数和名次。 |

序列打分拟扩展为 score_items(artifact_id, user_id, history_ref, item_ids)，返回每个候选的有限分数。recommend 同样绑定历史或会话状态。现有单用户 score_items(user_id, item_ids) 缺少显式历史，需由 A 包装或扩展。双塔除用户 ID 外所需的特征版本也随 history_ref 或上下文引用固定。

### 3.3.1 请求示例

C 提交预览给 B，比例用于生成可复现分区，评测协议固定后续打分输入。

```json
{
  "base_run_id": "A-014", "base_artifact_id": "art-014",
  "ratio_pct": 5, "seed": 2026, "method": "retrain",
  "metric_ids": ["recall@20", "ndcg@20"],
  "protocol_id": "seq-clean-v1"
}
```

B 返回确认用的请求编号、共享分区和实际清单引用。

```json
{
  "request_id": "req-R", "selection_id": "sel-014",
  "split_id": "split-014",
  "forget_count": 50, "retain_count": 950,
  "forget_ref": "requests/req-R/forget.jsonl",
  "retain_ref": "requests/req-R/retain.jsonl"
}
```

确认时冻结原产物、选择、方法、指标和协议。变更配置需新请求，比较 SCIF 时复用 sel-014 并核对清单哈希。同一次提交的幂等键由 C 维护，主动重试创建新 run_id。run_status、artifact_status 与 evaluation_status 分别返回，事件用 seq 增量查询。模型已登记而评测失败时保留产物，可单独创建评测尝试。

### 3.4 静态评测与结果格式

Original、Retrain、SCIF 共享用户、候选、映射、K、历史屏蔽、同分排序和聚合规则。首个序列实验建议使用从 Retain 构造的清洁历史作为三组相同的输入，另固定原 Train＋Valid 的业务屏蔽集合。测试正例与屏蔽冲突时先报错并核对协议。无测试目标者排除并计数，候选不足保留实际长度并计数，缺分或非有限分值返回失败。

| 维度 | 计算和保存规则 |
| --- | --- |
| 推荐效用 | Recall@K = Top-K 中测试正例数 / 该用户测试正例总数。NDCG@K 用 1/log2(rank+1) 折损命中，加总后除以理想排序得分。先逐用户计算再取均值。Hit@K 记录有无命中，补验后加入。 |
| 输入审计 | Retrain 核对 Retain 与派生样本哈希、新权重及优化器回执。SCIF 核对原权重、受影响样本、清理后样本、Retain 和更新参数来源。 |
| 效率 | 记录数据准备、方法执行、产物检查、评测和本次总耗时，注明设备与起止点。排队与单独评测重试另计。 |
| 遗忘诊断 | 保留逐用户分数和同选择 Retrain 对照。成员推断的交互级样本、独立攻击验证和判定口径待确认，再提供诊断结果 [7]。 |

### 3.4.1 比较结果示例

下列分数为虚构示例。正式结果保存所有指标、协议配置、覆盖和排除人数、数据与历史哈希、审计回执、方法版本及逐阶段计时。缺失结果使用 null 并附原因。

```json
{
  "schema_version": "b-comparison-v2",
  "comparison_id": "cmp-014", "selection_id": "sel-014",
  "protocol_id": "seq-clean-v1", "k": 20, "evaluated_users": 10,
  "arms": {
    "original": {"artifact_id": "art-014", "run_id": "A-014"},
    "retrain": {"artifact_id": "art-R", "run_id": "run-R"},
    "scif": {"artifact_id": "art-S", "run_id": "run-S"}
  },
  "metrics": {
    "ndcg@20": {"original": 0.21, "retrain": 0.20, "scif": 0.19}
  },
  "audit": {"retrain": "passed", "scif": "passed"},
  "method_seconds": {"retrain": 8.4, "scif": 2.1},
  "evaluation_seconds": 1.2
}
```

比较记录还关联各运行对应的 request_id 与输入哈希。差值明确写明新模型减原模型或 SCIF 减 Retrain。本地旧 comparison.json 是两组结构，接入时补充版本转换和第三组校验。双塔首轮建议用小商品集全量打分，使用近似检索时另记录索引与候选差异。

## 4 开发计划与验收

按每周 5–7 小时安排首个模型约 5 周、合计 25–35 小时，包含学习、适配与自检。A 的模型环境、接口反馈及算力排队另计。SCIF 先完成最小验证，再按兼容性结果调整后续工时。

| 阶段 | 任务与投入 | 验收产物 |
| --- | --- | --- |
| 11.23–11.29 | 1.5–2 小时读 SASRec 的数据构造与预测入口；2–3 小时整理原始点击、分区和历史字段；1.5–2 小时与 A/C 对齐小例子并整理文档。 | 四次点击删除前后的样本、简要接口清单、模型能力检查表和本设计稿。 |
| 11.30–12.06 | 1–1.5 小时读现有 requests.py；2.5–3.5 小时适配稳定点击 ID、清单及序列来源；1.5–2 小时核对哈希、重复请求和非法输入。 | 同一选择可复现，Forget/Retain 完整，遗忘点击在所有派生训练输入和标签中被清理。 |
| 12.07–12.13 | 1–1.5 小时读 retrain.py；2.5–3.5 小时接 A 的 Retain 训练和产物登记；1.5–2 小时重载、打分并核对实际输入回执。 | 首个推荐模型 Retrain 产物、初始化和数据回执、可重载与可打分记录。 |
| 12.14–12.20 | 1.5–2 小时跟读 ERASE 的 scif 和 target_params；2–3 小时对齐参数与加载器；1.5–2 小时做单次小样本更新并记录失败原因或结果。 | SCIF 最小兼容证据和独立产物；存在阻塞时给出具体缺失能力和修订工时。 |
| 12.21–12.27 | 1–1.5 小时手算指标；2.5–3.5 小时输出三组比较并接 C 查询；1.5–2 小时验证输入变化、求解失败和评测重试。 | 固定协议 JSON、实际阶段事件、失败重试记录及 A/C 交接。 |

首个模型验收后，为第二个模型另安排适配与联调。RecEraser/SISA 的训练准备与工时在 A/B 确认分片方案后估算。等待上游时，用现有本地样例验证分区、手算指标和结果格式。

## 5 评审待确认事项

A/B 需确认首个模型是否采用 SASRec、双塔的具体实现和训练框架，以及序列重建、目标参数和模型保存方式。C/A/B 需确认 Agent 与用户的映射、初始曝光来源、时间顺序、训练与评测历史的生成规则、Forget 再次进入后续训练时的排除机制。

A/B/C 需确认 selection_id 等扩展字段、模型产物和索引的登记方式，以及方法兼容查询。B 与负责人确认 SCIF 的交互级诊断协议，并评估后续分片方法对原训练流程的要求。

## 6 参考资料

[1] AfterRec 公共接口约定

`https://github.com/zhang-haichao/AfterRec/blob/main/docs/contracts/INTERFACES.md`

[2] RecBole SASRec 源码与序列样本构造

`https://recbole.io/docs/_modules/recbole/model/sequential_recommender/sasrec.html`

`https://github.com/RUCAIBox/RecBole/blob/master/recbole/data/dataset/sequential_dataset.py`

[3] Kang 与 McAuley，Self-Attentive Sequential Recommendation，ICDM 2018

`https://arxiv.org/abs/1808.09781`

`https://github.com/kang205/SASRec`

[4] TensorFlow Recommenders 双塔检索示例

`https://www.tensorflow.org/recommenders/examples/basic_retrieval`

[5] ERASE 源码和基准论文

`https://github.com/deem-data/erase-bench`

`https://arxiv.org/abs/2603.08341`

本地阅读快照提交 42ea967ba56f9472cc0ea3b746f32e80153e1170。

[6] Selective and collaborative influence function for efficient recommendation unlearning，Expert Systems with Applications

`https://www.sciencedirect.com/science/article/abs/pii/S0957417423015270`

[7] CURE4Rec，NeurIPS 2024 Datasets and Benchmarks

`https://papers.neurips.cc/paper_files/paper/2024/file/b364953e402d7d92e13830383677efb5-Paper-Datasets_and_Benchmarks_Track.pdf`

[8] Chen 等，Recommendation Unlearning，WWW 2022

`https://doi.org/10.1145/3485447.3511997`

`https://arxiv.org/abs/2201.06820`

`https://github.com/chenchongthu/Recommendation-Unlearning`

[9] Bourtoule 等，Machine Unlearning，IEEE S&P 2021

`https://doi.org/10.1109/SP40001.2021.00019`

`https://arxiv.org/abs/1912.03817`

`https://github.com/cleverhans-lab/machine-unlearning`
