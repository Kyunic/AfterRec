"""Simple, auditable ranking metrics for small contract tests.

Production evaluation must additionally define candidate sets and seen-item masking.
Do not compare these metrics against RecBole output without matching protocols.
"""

import math
from collections.abc import Sequence


def _validated_ids(recommended: Sequence[str], relevant: set[str], k: int) -> list[str]:
    if k <= 0:
        raise ValueError("k must be positive")
    if len(set(recommended)) != len(recommended):
        raise ValueError("recommended item IDs must be unique")
    if not relevant:
        raise ValueError("users with no relevant held-out items require an explicit policy")
    return list(recommended[:k])


def recall_at_k(recommended: Sequence[str], relevant: set[str], k: int) -> float:
    top_k = _validated_ids(recommended, relevant, k)
    return sum(item in relevant for item in top_k) / len(relevant)


def ndcg_at_k(recommended: Sequence[str], relevant: set[str], k: int) -> float:
    top_k = _validated_ids(recommended, relevant, k)
    dcg = sum(1 / math.log2(index + 2) for index, item in enumerate(top_k) if item in relevant)
    ideal_hits = min(k, len(relevant))
    idcg = sum(1 / math.log2(index + 2) for index in range(ideal_hits))
    return dcg / idcg
