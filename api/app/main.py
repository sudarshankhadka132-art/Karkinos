"""FastAPI application entrypoint for the API services."""

from __future__ import annotations

from fastapi import FastAPI

from .routers import search


def create_app() -> FastAPI:
    app = FastAPI(title="Karkinos API", version="1.0.0")
    app.include_router(search.router)
    return app


app = create_app()
