"""Lightweight liveness endpoint with no model or dataset dependencies."""

from fastapi import APIRouter

from recforgetbench import __version__

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
