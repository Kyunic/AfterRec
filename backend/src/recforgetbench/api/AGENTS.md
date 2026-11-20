# API and orchestration

- API endpoints validate, dispatch, and return artifacts. Do not implement ML
  training, split generation, or research metrics inside route handlers.
- Never expose filesystem paths, environment secrets, or unapproved input files.
- Report not-implemented capabilities honestly; no simulated training progress.
- Maintain versioned API and tested cross-module schemas.
- Review shared contract changes with affected modules before merging.
