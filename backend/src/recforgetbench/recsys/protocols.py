"""Recommender contracts: implement with RecBole, not with a fabricated model."""

from collections.abc import Sequence
from typing import Protocol

from recforgetbench.core.contracts import DatasetRef, ModelArtifact, SplitRef
from recforgetbench.simulation.contracts import RecommendedItem, SessionState


class Recommender(Protocol):
    def train(self, dataset: DatasetRef, split: SplitRef, config: dict) -> ModelArtifact: ...

    def load(self, artifact: ModelArtifact) -> None: ...

    def recommend(
        self, user_id: str, top_k: int, state: SessionState | None = None
    ) -> Sequence[RecommendedItem]: ...

    def score_items(self, user_id: str, item_ids: Sequence[str]) -> dict[str, float]: ...
