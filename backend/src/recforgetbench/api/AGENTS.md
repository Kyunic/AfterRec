# API and orchestration (Student C)

- API endpoints validate, dispatch, and return artifacts. Do not implement ML
  training, split generation, or research metrics inside route handlers.
- Never expose filesystem paths, environment secrets, or unapproved input files.
- Report not-implemented capabilities honestly; no simulated training progress.
- Maintain versioned API and tested cross-module schemas.
- Shared contract changes require A/B agreement before merge.
