# Unlearning module

- Implement Retrain as fresh initialization on retained interactions only.
- Never describe edge deletion at inference or model fine-tuning as exact retrain.
- Methods must explicitly declare supported recommender models and setup needs.
- Compare against the same split, ID maps, candidate set, and evaluation protocol.
- Model/algorithm implementations require reference to paper/code and tests.
- Any dependency on upstream training artifacts must be documented in the contract.
