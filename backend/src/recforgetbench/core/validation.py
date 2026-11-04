"""Pure validation helpers for critical scientific data invariants."""

from collections.abc import Iterable


def _as_unique_set(values: Iterable[str], name: str) -> set[str]:
    items = list(values)
    result = set(items)
    if len(items) != len(result):
        raise ValueError(f"{name} contains duplicate interaction IDs")
    return result


def assert_disjoint_splits(
    train: Iterable[str], validation: Iterable[str], test: Iterable[str]
) -> None:
    """Ensure interaction IDs do not cross train/validation/test boundaries."""
    sets = {
        "train": _as_unique_set(train, "train"),
        "validation": _as_unique_set(validation, "validation"),
        "test": _as_unique_set(test, "test"),
    }
    for left, right in (("train", "validation"), ("train", "test"), ("validation", "test")):
        if sets[left] & sets[right]:
            raise ValueError(f"{left} and {right} overlap")


def assert_forget_partition(
    train: Iterable[str], retain: Iterable[str], forget: Iterable[str]
) -> None:
    """Require an exact disjoint partition of the original training interactions."""
    train_ids = _as_unique_set(train, "train")
    retain_ids = _as_unique_set(retain, "retain")
    forget_ids = _as_unique_set(forget, "forget")
    if retain_ids & forget_ids:
        raise ValueError("retain and forget sets overlap")
    if retain_ids | forget_ids != train_ids:
        raise ValueError("retain and forget must partition the original train set")
