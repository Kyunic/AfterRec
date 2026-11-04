# Dataset module (Student A)

- Own import/normalization, manifests, split generation, metadata and ID mapping.
- Preserve original IDs and record internal RecBole mapping by dataset version.
- Enforce train/validation/test disjointness and train = retain ∪ forget.
- Never conflate Amazon rating/review observations with real clickstream actions.
- Dataset downloads are opt-in, licensed and excluded from git.
- Notify Student B before changing split/forget manifest contracts.
