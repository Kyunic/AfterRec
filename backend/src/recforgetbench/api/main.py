"""HTTP application factory. Scientific tasks are not implemented in the scaffold."""

from fastapi import FastAPI

from recforgetbench.api.routes.capabilities import router as capabilities_router
from recforgetbench.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="RecForgetBench API",
        description="Experimental infrastructure; not a production recommendation service.",
        version="0.1.0a0",
    )
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(capabilities_router, prefix="/api/v1")
    return app


app = create_app()
