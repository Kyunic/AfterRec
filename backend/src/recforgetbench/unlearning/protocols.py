"""Unlearning contracts; strategy-specific preparation is allowed."""

from typing import Protocol

from recforgetbench.core.contracts import ForgetRequest, ModelArtifact


class UnlearningMethod(Protocol):
    name: str

    def is_compatible(self, model_name: str) -> bool: ...

    def unlearn(
        self, original: ModelArtifact, request: ForgetRequest, config: dict
    ) -> ModelArtifact: ...


# Retrain must initialize a new model on the retain split. It is NOT fine-tuning
# the original checkpoint or merely removing edges at inference.
# Shard-based algorithms may require preparation before original model training.
