"""Honest feature catalogue: not-yet-built modules are never marked ready."""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/capabilities")
def capabilities() -> dict[str, object]:
    return {
        "phase": "repository-scaffold",
        "production_experiments_available": False,
        "components": [
            {"name": "datasets", "owner": "A", "status": "planned"},
            {"name": "recsys", "owner": "A", "status": "interface-defined"},
            {"name": "unlearning", "owner": "B", "status": "interface-defined"},
            {"name": "evaluation", "owner": "B", "status": "unit-metrics-only"},
            {"name": "simulation", "owner": "C + Research Lead", "status": "runtime-scaffold"},
            {"name": "web", "owner": "C", "status": "offline-prototype-only"},
        ],
    }
