import pytest

from recforgetbench.core.registry import ComponentRegistry


def test_component_registry_is_explicit():
    registry = ComponentRegistry()
    registry.register("toy", object())
    assert registry.names() == ("toy",)
    with pytest.raises(ValueError, match="duplicate"):
        registry.register("toy", object())
    with pytest.raises(KeyError, match="Unknown"):
        registry.get("not_registered")
