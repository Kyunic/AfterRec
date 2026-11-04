"""Explicit component registry. Avoid magic imports or dynamic user-supplied code."""

from typing import Any


class ComponentRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def register(self, name: str, component: Any) -> None:
        if not name or name in self._items:
            raise ValueError(f"Invalid or duplicate component name: {name!r}")
        self._items[name] = component

    def get(self, name: str) -> Any:
        if name not in self._items:
            raise KeyError(f"Unknown component: {name}")
        return self._items[name]

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))
