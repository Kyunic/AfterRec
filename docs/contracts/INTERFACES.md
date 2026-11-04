# Shared module interfaces (v0.1 — initial agreement)

**Owners:** Students A/B/C jointly. **Change protocol:** change proposal Issue,
updated schema, consumers notified, updated tests, PR describing migration.

## Shared identifiers and lineage

Use stable string IDs (`dataset_id`, `split_id`, `model_id`, `run_id`,
`request_id`, `user_id`, `item_id`). RecBole's internal integer IDs are adapter
implementation details. Keep the mapping with each model artifact.

The concrete typed objects are in `recforgetbench.core.contracts` and
`recforgetbench.simulation.contracts`.

## Dataset and split (A -> B)

- `DatasetRef`: dataset ID + version + optional metadata location.
- `SplitRef`: immutable paths to train, validation and test interaction manifests,
  linked to dataset version and seed.
- `ForgetRequest`: interaction-wise forget and retain manifest paths, same split,
  random seed and request ID.
- Invariants: no overlap across train/validation/test; train = retain ∪ forget;
  no validation/test item accidentally enters the forget set.

## Recommendation (A -> B, C)

`Recommender.train(dataset, split, config) -> ModelArtifact`

`Recommender.load(artifact) -> None`

`Recommender.recommend(user_id, top_k, state) -> RecommendedItem[]`

`Recommender.score_items(user_id, item_ids) -> scores`

`RecommendedItem`: item ID, base score, rank, optional title/category.
When a session adapter is added, distinguish **base** scores from displayed
(re-ranked) scores and preserve both in the run log.

A real implementation must define seen-item masking, candidate catalogue,
unknown-user behavior, model version, and deterministic ranking tie-break rules.

## Unlearning (A -> B -> C)

`UnlearningMethod.is_compatible(model_name) -> bool`

`UnlearningMethod.unlearn(original, forget_request, config) -> ModelArtifact`

Retrain is a *new training run* from fresh initialization using retained
training interactions. Some other algorithms require special preparation at
original training time; the contract may be extended with a prepare phase.

## Evaluation (B -> C)

Each result must specify original model, comparison model, split, forget request,
metric name, K, ranking protocol, filtering and aggregation; include runtime
and provenance metadata. No fabricated placeholder metric may share a namespace
with a measured metric.

## Simulation (Research Lead -> C; A provides model)

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

The owning teams should implement route models and validation through Pydantic,
not invent API payloads independently in the front end.
