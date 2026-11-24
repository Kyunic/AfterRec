# AfterRec documentation

[简体中文](README.zh-CN.md) · [Architecture](architecture/OVERVIEW.md) · [Main README](../README.md)

Read the [architecture overview](architecture/OVERVIEW.md) first. The documents below are organized by **system responsibility**, not by contributor. New design pages are placeholders for future implementation details.

## Before implementation: design and interface templates

Start with the [module design template](templates/DESIGN_TEMPLATE.md) ([中文](templates/DESIGN_TEMPLATE.zh-CN.md)). Confirm the goal, first-release scope, simple workflow, dependencies and measurable acceptance checks before writing the implementation.

If two modules exchange data, agree on the [interface template](templates/INTERFACE_TEMPLATE.md) ([中文](templates/INTERFACE_TEMPLATE.zh-CN.md)) before building either side. Record calls, input/output types, failure behavior and integration checks in the relevant `interfaces/` file. The existing [shared contracts](contracts/INTERFACES.md) take precedence over conflicting proposals.

Use the templates as guides, not forms to fill for their own sake. A short design with clear boundaries and testable outcomes is better than a long catalogue of speculative features.

## Module design

| Module | Design document | What to document |
| --- | --- | --- |
| Data | [datasets](modules/datasets/DESIGN.md) | Supported inputs, preprocessing, dataset splits, forget/retain manifests and versioning |
| Recommendation | [recommendation](modules/recommendation/DESIGN.md) | Model lifecycle, training configuration, scoring, Top-K, checkpoints and adapters |
| Unlearning | [unlearning](modules/unlearning/DESIGN.md) | Forget requests, algorithm integration, Retrain baseline and model artifacts |
| Static evaluation | [evaluation](modules/evaluation/DESIGN.md) | Metrics, candidate/masking protocol, baselines, reporting and reproducibility |
| Agent simulation | [agent simulation](modules/agent-simulation/DESIGN.md) | Agent policies, observation/action schema, session state and trajectory recording |
| Experiment platform | [platform](modules/platform/DESIGN.md) | Backend orchestration, Web workflows, experiment status and local artifacts |

## Interfaces

The existing [shared contracts](contracts/INTERFACES.md) remain the reference for current typed objects and module signatures. Fill in the following pages as interfaces are implemented:

| Interface | Define |
| --- | --- |
| [Frontend ↔ backend](interfaces/FRONTEND_BACKEND.md) | HTTP routes, payloads, errors, job status and frontend integration |
| [Data ↔ recommendation](interfaces/DATA_RECOMMENDATION.md) | Dataset refs, ID mapping, metadata and training inputs |
| [Recommendation ↔ unlearning](interfaces/RECOMMENDATION_UNLEARNING.md) | Original checkpoints, forget requests, method compatibility and outputs |
| [Model ↔ evaluation](interfaces/MODEL_EVALUATION.md) | Ranking candidates, metric inputs, protocols and result schemas |
| [Recommendation ↔ agent](interfaces/RECOMMENDATION_AGENT.md) | Recommendation observations, actions, session feedback and trace events |
| [Experiment artifacts](interfaces/EXPERIMENT_ARTIFACTS.md) | Run IDs, file layout, model/run lineage, provenance and serialization |

## Research and progress

- [Simulation research protocol](research/SIMULATION_PROTOCOL.md)
- [Roadmap](ROADMAP.md)

Existing detailed agent notes are available in [the agent simulation working draft](../doc/agent-simulation/README.md). Reconcile the draft with the shared interfaces before treating proposed endpoints as implemented.
