# Recommendation core

- Call RecBole through a bounded adapter. Do not vendor or fork its entire source.
- Implement real training, checkpoint loading, Top-K, and item scoring separately.
- Preserve user/item ID mapping; document observed-item filtering and ranking pool.
- Do not use untested mock recommendations as model output.
- Coordinate any `ModelArtifact` or recommendation contract change with downstream modules.
