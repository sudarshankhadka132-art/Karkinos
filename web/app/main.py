"""FastAPI application serving the web UI."""

from __future__ import annotations

from fastapi import FastAPI

from .routes import search


def create_app() -> FastAPI:
    app = FastAPI(title="Karkinos Web", version="1.0.0")
    app.include_router(search.router)
    return app


app = create_app()
