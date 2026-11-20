"""Honest feature catalogue: not-yet-built modules are never marked ready."""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/capabilities")
def capabilities() -> dict[str, object]:
    return {
        "phase": "repository-scaffold",
        "production_experiments_available": False,
        "components": [
            {"name": "datasets", "status": "planned"},
            {"name": "recsys", "status": "interface-defined"},
            {"name": "unlearning", "status": "interface-defined"},
            {"name": "evaluation", "status": "unit-metrics-only"},
            {"name": "simulation", "status": "runtime-scaffold"},
            {"name": "web", "status": "offline-prototype-only"},
        ],
    }
