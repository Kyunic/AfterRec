import pytest

from recforgetbench.core.validation import assert_disjoint_splits, assert_forget_partition


def test_disjoint_split_passes():
    assert_disjoint_splits(["i1", "i2"], ["i3"], ["i4"])


def test_split_overlap_fails():
    with pytest.raises(ValueError, match="overlap"):
        assert_disjoint_splits(["i1"], ["i1"], ["i2"])


def test_duplicate_interactions_fail():
    with pytest.raises(ValueError, match="duplicate"):
        assert_disjoint_splits(["i1", "i1"], [], [])


def test_forget_partition_passes():
    assert_forget_partition(["i1", "i2", "i3"], ["i1", "i3"], ["i2"])


def test_forget_partition_missing_interactions_fails():
    with pytest.raises(ValueError, match="partition"):
        assert_forget_partition(["i1", "i2"], ["i1"], [])


def test_forget_partition_overlap_fails():
    with pytest.raises(ValueError, match="overlap"):
        assert_forget_partition(["i1", "i2"], ["i1", "i2"], ["i2"])
