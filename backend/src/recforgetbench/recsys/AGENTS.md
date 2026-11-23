# Recommendation core

- Keep external model-framework integrations behind narrow adapters. Do not vendor entire frameworks.
- Implement real training, checkpoint loading, Top-K, and item scoring separately.
- Preserve user/item ID mapping; document observed-item filtering and ranking pool.
- Do not use untested mock recommendations as model output.
- Coordinate any `ModelArtifact` or recommendation contract change with downstream modules.
