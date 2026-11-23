# Shared module interfaces (v0.1)

**Changes:** Propose interface updates in an Issue. Update the schema, affected consumers, tests and migration notes in the same PR.

## Shared identifiers and lineage

Use stable string IDs (`dataset_id`, `split_id`, `model_id`, `run_id`,
`request_id`, `user_id`, `item_id`). Internal integer IDs used by particular model adapters are implementation details. Keep the mapping with each model artifact.

The concrete typed objects are in `recforgetbench.core.contracts` and
`recforgetbench.simulation.contracts`.

## Dataset and split

- `DatasetRef`: dataset ID + version + optional metadata location.
- `SplitRef`: immutable paths to train, validation and test interaction manifests,
  linked to dataset version and seed.
- `ForgetRequest`: interaction-wise forget and retain manifest paths, same split,
  random seed and request ID.
- Invariants: no overlap across train/validation/test; train = retain ∪ forget;
  no validation/test item accidentally enters the forget set.

## Recommendation

`Recommender.train(dataset, split, config) -> ModelArtifact`

`Recommender.load(artifact) -> None`

`Recommender.recommend(user_id, top_k, state) -> RecommendedItem[]`

`Recommender.score_items(user_id, item_ids) -> scores`

`RecommendedItem`: item ID, base score, rank, optional title/category.
When a session adapter is added, distinguish **base** scores from displayed
(re-ranked) scores and preserve both in the run log.

A real implementation must define seen-item masking, candidate catalogue,
unknown-user behavior, model version, and deterministic ranking tie-break rules.

## Unlearning

`UnlearningMethod.is_compatible(model_name) -> bool`

`UnlearningMethod.unlearn(original, forget_request, config) -> ModelArtifact`

Retrain is a *new training run* from fresh initialization using retained
training interactions. Some other algorithms require special preparation at
original training time; the contract may be extended with a prepare phase.

## Evaluation

Each result must specify original model, comparison model, split, forget request,
metric name, K, ranking protocol, filtering and aggregation; include runtime
and provenance metadata. No fabricated placeholder metric may share a namespace
with a measured metric.

## Simulation

`AgentObservation`: user ID, step, persona, forgetting intent, displayed items,
**prior executed actions only**.

`AgentAction`: `click(item_id)`, `dislike(item_id)`, `skip`, or `exit`.

`SimulationTrace`: user ID, model ID, ordered events and synthetic flag.

The simulator can reject invalid actions and terminate early. The base
recommender must not receive a semantic forgetting instruction when measuring
data-unlearning-only outcomes.

## API surface **currently implemented**

- `GET /api/v1/health`: service liveness, package version.
- `GET /api/v1/capabilities`: honest readiness list; no experiment execution.

The following are **planned**, not working endpoints:

- `POST /api/v1/training-runs`
- `POST /api/v1/unlearning-runs`
- `POST /api/v1/evaluation-runs`
- `POST /api/v1/simulation-runs`

Implement route models and validation through Pydantic,
not invent API payloads independently in the front end.
