import pytest

from recforgetbench.evaluation.metrics import ndcg_at_k, recall_at_k


def test_recall_exact():
    assert recall_at_k(["a", "b", "c"], {"b", "z"}, 2) == 0.5


def test_ndcg_perfect_ranking():
    assert ndcg_at_k(["a", "b", "c"], {"a", "b"}, 2) == pytest.approx(1.0)


def test_ndcg_discount_and_recall_diverge():
    assert 0 < ndcg_at_k(["x", "a", "b"], {"a", "b"}, 2) < 1
    assert recall_at_k(["x", "a", "b"], {"a", "b"}, 2) == 0.5


def test_empty_relevant_is_undefined():
    with pytest.raises(ValueError, match="no relevant"):
        recall_at_k(["a"], set(), 1)


def test_duplicate_items_rejected():
    with pytest.raises(ValueError, match="unique"):
        ndcg_at_k(["a", "a"], {"a"}, 2)
