# Dataset module

- Own import/normalization, manifests, split generation, metadata and ID mapping.
- Preserve original IDs and record model-adapter mapping by dataset version.
- Enforce train/validation/test disjointness and train = retain ∪ forget.
- Never conflate Amazon rating/review observations with real clickstream actions.
- Dataset downloads are opt-in, licensed and excluded from git.
- Update the interface specification and notify downstream consumers before changing split/forget manifests.
