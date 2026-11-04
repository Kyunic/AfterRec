# First development Issues to create in GitHub

These are project-management starting points, **not** completed functionality.
Create them as Issues using `.github/ISSUE_TEMPLATE/feature_request.yml`.

| Issue | Owner | Deliverable | Acceptance |
| --- | --- | --- | --- |
| A-01 RecBole environment validation | A | documented reproducible environment | Train one authentic model from a small fixture |
| A-02 Recommender adapter | A | train/load/recommend and ID mapping | Reload a checkpoint; two real users yield real Top-K |
| A-03 Amazon sample ingestion | A | licensed download instructions + versioned manifest | Repeat split with same seed; partition tests pass |
| B-01 Forget/retain generator | B | train-only interaction split | Disjoint + exact partition tests pass |
| B-02 Retrain reference | B | reinitialize model on retain set | Compare actual trained checkpoints, log provenance |
| B-03 Basic evaluation | B | Recall@K/NDCG@K with fixed protocol | Hand-computed fixtures match and metadata recorded |
| C-01 API skeleton integration | C | documented FastAPI endpoints | Health, real model run wiring after A complete |
| C-02 Frontend migration | C | replace static prototype with real Web app | Demo values remain clearly synthetic until connected |
| C-03 Local run orchestration | C | one task at a time with status/logging | Simulated errors do not produce fake success |
| C-04 Agent runtime wiring | C + Lead | structured observation/action + 3–5 turns | Invalid item actions rejected; baseline state reset |

**Priority:** First complete A-01/A-02, B-01, C-01/C-02 concurrently.
Then B-02/B-03, followed by simulation integration.
